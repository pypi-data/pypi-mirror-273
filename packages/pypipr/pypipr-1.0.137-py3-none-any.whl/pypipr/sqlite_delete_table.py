import sqlite3


def sqlite_delete_table(filename, tablename):
    conn = sqlite3.connect(filename)
    conn.execute(f"DROP TABLE IF EXISTS {tablename}")
    conn.commit()
    conn.close()
