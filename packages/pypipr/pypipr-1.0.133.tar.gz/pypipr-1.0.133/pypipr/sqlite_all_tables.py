import sqlite3


def sqlite_all_tables(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # for table in tables:
    #     print(table[0])
    conn.close()
    return tables
