from database.database import get_connection

def create(equipment_id: int, employee_id: int, defect_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO repair_requests (equipment_id, employee_id, defect_name)
        VALUES (?, ?, ?)
    """, (equipment_id, employee_id, defect_name))
    conn.commit()
    conn.close()

def get_requests_by_employee(employee_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT rr.request_id, e.model, e.serial_number, rr.defect_name
        FROM repair_requests rr
        JOIN equipment e ON rr.equipment_id = e.equipment_id
        WHERE rr.employee_id = ?
    """, (employee_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_requests_by_equipment(equipment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT rr.request_id, emp.full_name, rr.defect_name
        FROM repair_requests rr
        JOIN employees emp ON rr.employee_id = emp.employee_id
        WHERE rr.equipment_id = ?
    """, (equipment_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_by_equipment(equipment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM repair_requests
        WHERE equipment_id = ?
    """, (equipment_id,))
    conn.commit()
    conn.close()