from database.database import get_connection

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

def create_employee(full_name: str, login: str, password_hash: str, userrole: int):
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