import mariadb
from config import MARIADB_HOST, MARIADB_PORT, MARIADB_DATABASE, MARIADB_USER, MARIADB_ROOT_PASSWORD
from fastapi import HTTPException
import json

print(MARIADB_HOST, MARIADB_PORT, MARIADB_DATABASE, MARIADB_USER, MARIADB_ROOT_PASSWORD)

def get_db_connection():
    try:
        connection = mariadb.connect(
            host=MARIADB_HOST,
            port=int(MARIADB_PORT),
            database=MARIADB_DATABASE,
            user=MARIADB_USER,
            password=MARIADB_ROOT_PASSWORD
        )
        return connection
    except mariadb.Error as error:
        raise HTTPException(status_code=500, detail=f"Database connection error: {error}")

def execute_query(query: str, params=None):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Build a list of dictionaries (JSON objects) from the rows
        result = []
        for row in rows:
            row_dict = {}
            for idx, col in enumerate(cursor.description):
                row_dict[col[0]] = row[idx]
            result.append(row_dict)

        connection.commit()
        cursor.close()
        connection.close()

        return result  # Return the list of JSON objects

    except mariadb.Error as error:
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
