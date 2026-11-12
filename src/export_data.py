import csv
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

import database.database as db


def _dict_to_xml(parent: ET.Element, data: dict) -> None:
    for key, value in data.items():
        child = ET.SubElement(parent, str(key))
        if isinstance(value, dict):
            _dict_to_xml(child, value)
        else:
            child.text = "" if value is None else str(value)


def find_table_with_relations(cursor) -> str:
    """
    Автоматически находит в базе данных первую таблицу со связями (FOREIGN KEY).
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row for (row,) in cursor.fetchall()]

    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        if cursor.fetchall():
            return table

    if tables:
        return tables[0]
    raise RuntimeError("В базе данных не найдено ни одной таблицы.")


def fetch_any_table_data(table_name: str | None = None) -> tuple[str, list[dict], list[dict]]:
    """
    Читает структуру любой таблицы через PRAGMA, находит внешние ключи,
    подтягивает связанные записи и возвращает вложенные и плоские данные.
    """
    conn = db.get_connection()
    try:
        cursor = conn.cursor()

        if not table_name:
            table_name = find_table_with_relations(cursor)

        cursor.execute(f"PRAGMA table_info({table_name})")
        main_cols = [col_name for (_, col_name, _, _, _, _) in cursor.fetchall()]

        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fk_list = cursor.fetchall()

        select_parts = [f"main.{col} AS main__{col}" for col in main_cols]
        join_parts = []
        fk_map = {}

        for idx, (_, _, ref_table, from_col, to_col, _, _, _) in enumerate(fk_list):
            group_name = from_col[:-3] if from_col.endswith("_id") else ref_table
            alias = f"rel_{idx}"
            fk_map[from_col] = group_name

            cursor.execute(f"PRAGMA table_info({ref_table})")
            ref_cols = [r_name for (_, r_name, _, _, _, _) in cursor.fetchall()]
            for r_col in ref_cols:
                select_parts.append(f"{alias}.{r_col} AS {group_name}__{r_col}")

            join_parts.append(f"LEFT JOIN {ref_table} {alias} ON main.{from_col} = {alias}.{to_col}")

        sql = f"SELECT {', '.join(select_parts)} FROM {table_name} main {' '.join(join_parts)}"
        cursor.execute(sql)
        col_names = [desc[0] for desc in cursor.description]
        raw_rows = cursor.fetchall()
    finally:
        conn.close()

    nested_rows = []
    flat_rows = []

    for row in raw_rows:
        nested_item = {}
        flat_item = {}

        for col_name, value in zip(col_names, row):
            group, field = col_name.split("__", 1)

            if group == "main":
                flat_item[field] = "" if value is None else value
                if field not in fk_map:
                    nested_item[field] = value
            else:
                flat_item[f"{group}_{field}"] = "" if value is None else value
                if group not in nested_item:
                    nested_item[group] = {}
                nested_item[group][field] = value

        for key, val in list(nested_item.items()):
            if isinstance(val, dict) and all(v is None for v in val.values()):
                nested_item[key] = None

        nested_rows.append(nested_item)
        flat_rows.append(flat_item)

    return table_name, nested_rows, flat_rows


def auto_export(table_name: str | None = None) -> None:
    """
    Экспортирует любую таблицу базы данных в JSON, YAML, XML и CSV в папку out.
    """
    out_dir = Path(__file__).resolve().parent.parent / "out"
    os.makedirs(out_dir, exist_ok=True)

    chosen_table, nested_rows, flat_rows = fetch_any_table_data(table_name)

    with open(out_dir / "data.json", "w", encoding="utf-8") as f:
        json.dump(nested_rows, f, ensure_ascii=False, indent=4)

    with open(out_dir / "data.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(nested_rows, f, allow_unicode=True, sort_keys=False)

    root = ET.Element(f"{chosen_table}_list")
    for item in nested_rows:
        record_el = ET.SubElement(root, chosen_table)
        _dict_to_xml(record_el, item)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(out_dir / "data.xml", encoding="utf-8", xml_declaration=True)

    if flat_rows:
        headers = list(next(iter(flat_rows)).keys())
        with open(out_dir / "data.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(flat_rows)