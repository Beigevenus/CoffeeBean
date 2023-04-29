import os
import sqlite3


def query_db(query: str, vars: tuple) -> list:
    conn = sqlite3.connect(os.getenv("DB_PATH"))

    with conn:
        cursor = conn.execute(query, vars)
        result = cursor.fetchall()

    return result
