import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",  # replace with your MySQL password
    "database": "vehicle_repair",
}


def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Services table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                service_id VARCHAR(50) UNIQUE,
                vehicle_no VARCHAR(50),
                description VARCHAR(255),
                status VARCHAR(50),
                amount FLOAT,
                payment_mode VARCHAR(50)
            )
        """
        )
        # Invoices table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS invoices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_id VARCHAR(50) UNIQUE,
                service_id VARCHAR(50),
                customer VARCHAR(100),
                amount FLOAT,
                payment_mode VARCHAR(50)
            )
        """
        )
        conn.commit()
        return conn
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return None


conn = init_db()
cursor = conn.cursor()
