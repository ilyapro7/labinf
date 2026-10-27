from database.database import get_connection

def get_all_statuses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT status_id, name FROM statuses")
    rows = cur.fetchall()
    conn.close()
    return rows