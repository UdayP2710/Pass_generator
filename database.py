import mysql.connector
from config import DB_CONFIG


def save_record(label, length, password):
    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        connection_timeout=5
    )

    cursor = connection.cursor()

    query = """
    INSERT INTO generation_history (label, password_length, Actual_password)
    VALUES (%s, %s, %s)
    """

    values = (label, length, password)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def get_history():
    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        connection_timeout=5
    )

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT record_id, label, password_length, Actual_password
            FROM generation_history
            ORDER BY record_id DESC
        """)

        rows = cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

    return rows