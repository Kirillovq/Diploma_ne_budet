import sqlite3

def execute_query(query, params=()):
    try:
        connection = sqlite3.connect('warehouse.db')
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise

def fetch_all(query, params=()):
    try:
        connection = sqlite3.connect('warehouse.db')
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        connection.close()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise

def fetch_one(query, params=()):
    try:
        connection = sqlite3.connect('warehouse.db')
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        connection.close()
        return result
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise


def execute_query(query, params=()):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_table_info(table_name):
    query = f"PRAGMA table_info({table_name})"
    return fetch_all(query)

