import csv
import json
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

import auth
import menu
import database.database as db

EXPORT_SQL = """
    SELECT
        eq.equipment_id,
        eq.model,
        eq.serial_number,
        st.status_id AS status__id,
        st.name AS status__name,
        emp.employee_id AS employee__id,
        emp.full_name AS employee__full_name,
        emp.login AS employee__login
    FROM equipment eq
    LEFT JOIN statuses st ON eq.status_id = st.status_id
    LEFT JOIN employees emp ON eq.employee_id = emp.employee_id
"""


def _dict_to_xml(parent: ET.Element, data: dict) -> None:
    for key, value in data.items():
        child = ET.SubElement(parent, str(key))
        if isinstance(value, dict):
            _dict_to_xml(child, value)
        else:
            child.text = "" if value is None else str(value)


def export_data(sql_query: str, root_tag: str = "equipments", item_tag: str = "equipment") -> None:
    out_dir = Path(__file__).resolve().parent.parent / "out"
    os.makedirs(out_dir, exist_ok=True)

    conn = db.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        raw_rows = cursor.fetchall()
    finally:
        conn.close()

    nested_rows = []
    flat_rows = []

    for row in raw_rows:
        nested_item = {}
        flat_item = {}

        for col_name, value in zip(columns, row):
            flat_item[col_name.replace("__", "_")] = "" if value is None else value

            if "__" in col_name:
                group, sub_key = col_name.split("__", 1)
                if group not in nested_item:
                    nested_item[group] = {}
                nested_item[group][sub_key] = value
            else:
                nested_item[col_name] = value

        for key, val in list(nested_item.items()):
            if isinstance(val, dict) and all(v is None for v in val.values()):
                nested_item[key] = None

        nested_rows.append(nested_item)
        flat_rows.append(flat_item)

    with open(out_dir / "data.json", "w", encoding="utf-8") as f:
        json.dump(nested_rows, f, ensure_ascii=False, indent=4)

    with open(out_dir / "data.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(nested_rows, f, allow_unicode=True, sort_keys=False)

    root = ET.Element(root_tag)
    for item in nested_rows:
        record_el = ET.SubElement(root, item_tag)
        _dict_to_xml(record_el, item)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(out_dir / "data.xml", encoding="utf-8", xml_declaration=True)

    if flat_rows:
        with open(out_dir / "data.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat_rows[0].keys()))
            writer.writeheader()
            writer.writerows(flat_rows)

def main():
    db.init_db()
    export_data(EXPORT_SQL)
    while True:
        print("\n======================================")
        print("      СИСТЕМА УЧЕТА ОБОРУДОВАНИЯ   ")
        print("======================================")
        print("1. Войти в аккаунт")
        print("0. Закрыть программу")

        choice = input("Выберите действие: ")
        if choice == "1":
            login = input("Логин: ")
            password = input("Пароль: ")
            user = auth.authenticate(login, password)

            if user:
                print(f" Вход выполнен успешно!")
                if user[4] == 1:
                    menu.admin_menu(user)
                elif user[4] == 2:
                    menu.employee_menu(user)
            else:
                print(" Неверный логин или пароль!")
        elif choice == "0":
            print("Программа закрыта.")
            break


if __name__ == "__main__":
    main()

