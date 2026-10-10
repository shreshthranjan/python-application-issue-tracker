import sqlite3
import logging
from pathlib import Path

def get_connection(database_name):
    return sqlite3.connect(database_name)

def initialize_database(database_name):
    connection=get_connection(database_name)
    cursor=connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        issue TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    connection.commit()

    return connection,cursor


DATABASE_PATH = Path(__file__).resolve().parent / "incidents.db"
connection, cursor = initialize_database(str(DATABASE_PATH))

def add_incident(title,issue,priority,status):
    try:
        cursor.execute('''
        INSERT INTO incidents(title,issue,priority,status)
        VALUES(?,?,?,?)
        ''',(title,issue,priority,status))
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        logging.exception("Failed to add incident")
        print(f"Database Error: {e}.")

def get_all_incidents():
    try:
        cursor.execute("SELECT * FROM incidents")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database Error: {e}.")
        logging.exception("Failed to get incidents")
        return []

def search_incident(title, db_cursor=cursor):
    try:
        db_cursor.execute('''
        SELECT * FROM incidents
        WHERE LOWER(title)=LOWER(?)
        ''',(title,))
        return db_cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database Error: {e}.")
        logging.exception("Failed to search incident")
        return None

def update_status(title,status):
    try:
        cursor.execute('''
        UPDATE incidents
        SET status=?
        WHERE LOWER(title)=LOWER(?)
        ''',(status,title,))
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Database Error: {e}.")
        logging.exception("Failed to update incident status")
        return 0
    
def delete_incident(title):
    try:
        cursor.execute('''
        DELETE FROM incidents
        WHERE LOWER(title)=LOWER(?)
        ''',(title,))
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Database Error: {e}.")
        logging.exception("Failed to delete incident")
        return 0

def get_incident_report():
    try:
        cursor.execute('''
        SELECT COUNT(*) FROM incidents
        ''')
        total = cursor.fetchone()[0]
        cursor.execute('''
        SELECT status, COUNT(*)
        FROM incidents
        GROUP BY status
        ''')
        status_counts=cursor.fetchall()
        cursor.execute('''
        SELECT priority, COUNT(*)
        FROM incidents
        GROUP BY priority
        ''')
        priority_counts=cursor.fetchall()
        logging.info("Incident Report generated successfully.")
        return total,status_counts,priority_counts

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        logging.exception("Failed to generate incident report.")
        return None

def update_status_by_id(incident_id, status):
    try:
        cursor.execute("""
            UPDATE incidents
            SET status = ?
            WHERE id = ?
        """, (status, incident_id))

        connection.commit()
        return cursor.rowcount

    except sqlite3.Error as e:
        connection.rollback()
        logging.exception("Failed to update incident status")
        print(f"Database Error: {e}.")
        return 0

def delete_incident_by_id(incident_id):
    try:
        cursor.execute(
            "DELETE FROM incidents WHERE id = ?",
            (incident_id,)
        )
        connection.commit()
        return cursor.rowcount

    except sqlite3.Error as e:
        connection.rollback()
        logging.exception("Failed to delete incident")
        print(f"Database Error: {e}.")
        return 0