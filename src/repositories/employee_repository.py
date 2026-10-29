from database.database import get_connection
import hashlib

def get_by_login(login: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT employee_id, full_name, login, password_hash, userrole 
        FROM employees 
        WHERE login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row


def create_employee(full_name: str, login: str, password_raw: str, userrole: int):
    password_hash = hashlib.sha256(password_raw.encode('utf-8')).hexdigest()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employees (full_name, login, password_hash, userrole)
        VALUES (?, ?, ?, ?)
    """, (full_name, login, password_hash, userrole))
    conn.commit()
    conn.close()

def delete_employee(employee_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM employees
        WHERE employee_id = ?
    """, (employee_id,))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, full_name, login, userrole FROM employees")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_employee_by_login(login: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE login = ?", (login,))
    conn.commit()
    conn.close()