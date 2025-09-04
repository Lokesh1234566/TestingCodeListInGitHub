from typing import Any, Dict, List, Optional

from eventure import EventLog
from eventure.event import Event
import mysql.connector

# MySQL Database connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "microservicedatabase",
}


class EventLog1:

    def __init__(self):
        self.events: List[Event] = []
        self._current_tick: int = 0

    @property
    def save_to_file(self, filename: str) -> None:
        """Save event log to file.

        The entire game state can be reconstructed from this file.
        Each event is stored as a separate line of JSON for easy
        parsing and appending.
        """
        with open(filename, "w") as f:
            for event in self.events:
                f.write(event.to_json() + "\n")

    def save_to_db(self, _filename: str = "") -> str:
        """Save  id and name to database (test connection)."""
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Create a simple table if not exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sample_data (
                    id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(100)
                )
            """
            )

            # Hardcoded values
            record_id = "U002"
            record_name = "testing"

            # Insert query
            cursor.execute(
                """
                INSERT INTO sample_data (id, name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE name = VALUES(name)
                """,
                (record_id, record_name),
            )

            conn.commit()
            return "Hardcoded data inserted successfully."

        except mysql.connector.Error as err:
            return f"Error: {err}"

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def show_db_data(self, _filename: str = "") -> str:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sample_data")
            data = cursor.fetchall()

            conn.commit()
            return data

        except mysql.connector.Error as err:
            return f"Error: {err}"

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
