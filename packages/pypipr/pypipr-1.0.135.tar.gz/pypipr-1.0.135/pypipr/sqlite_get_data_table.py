import sqlite3


def sqlite_get_data_table(filename, tablename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tablename}")
    rows = cursor.fetchall()
    conn.close()
    return rows
