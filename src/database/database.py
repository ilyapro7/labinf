import sqlite3
from pathlib import Path

DB_NAME = "equipment.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
        if cursor.fetchone():
            conn.close()
            return
    except sqlite3.Error:
        pass

    sql_path = (
        Path(__file__).parent
        / "schema.sql"
    )

    with open(
        sql_path,
        "r",
        encoding="utf-8"
    ) as file:
        sql_script = file.read()

    conn.executescript(sql_script)
    conn.commit()
    conn.close()

    print("База данных создана.")