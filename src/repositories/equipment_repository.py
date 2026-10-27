from database.database import get_connection

def get_by_serial(serial: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.equipment_id, e.model, e.serial_number, e.status_id, e.employee_id, s.name 
        FROM equipment e
        JOIN statuses s ON e.status_id = s.status_id
        WHERE e.serial_number = ?
    """, (serial,))
    row = cur.fetchone()
    conn.close()
    return row

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.equipment_id, e.model, e.serial_number, e.status_id, e.employee_id, s.name 
        FROM equipment e
        JOIN statuses s ON e.status_id = s.status_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def update_status(equipment_id: int, status_id: int, employee_id: int | None = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE equipment 
        SET status_id = ?, employee_id = ? 
        WHERE equipment_id = ?
    """, (status_id, employee_id, equipment_id))
    conn.commit()
    conn.close()

def create_equipment(model: str, serial_number: str, status_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO equipment (model, serial_number, status_id, employee_id)
        VALUES (?, ?, ?, NULL)
    """, (model, serial_number, status_id))
    conn.commit()
    conn.close()

def delete_equipment(equipment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM equipment
        WHERE equipment_id = ?
    """, (equipment_id,))
    conn.commit()
    conn.close()