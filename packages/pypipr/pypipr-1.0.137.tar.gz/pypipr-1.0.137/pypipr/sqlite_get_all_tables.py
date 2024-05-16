import sqlite3


def sqlite_get_all_tables(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' order by name;")
    tables = cursor.fetchall()
    conn.close()
    return tables
