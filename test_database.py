import unittest
import sqlite3

from database import search_incident

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.connection=sqlite3.connect("test_database.db")
        self.cursor=self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL
         )
        """)

        self.connection.commit()

        self.cursor.execute("""
            INSERT INTO incidents(title, issue, priority, status)
            VALUES(?,?,?,?)
            """, ("Login Failure", "Unable to login", "High", "Open"))

        self.connection.commit()

    def test_search_non_existing_incident(self):
        result=search_incident("This incident does not exist")
        self.assertIsNone(result)

    def test_search_existing_incident(self):
        result=search_incident("Login Failure",self.cursor)
        self.assertIsNone(result)

    def tearDown(self):
        self.cursor.execute("DELETE FROM incidents")
        self.connection.commit()
        self.connection.close()