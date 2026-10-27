from database.database import get_connection

def get_all_roles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT userrole, name FROM roles")
    rows = cur.fetchall()
    conn.close()
    return rows