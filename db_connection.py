import mysql.connector


def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",        # Your database host, usually "localhost"
        user="root",    # Your MySQL username
        password="Dheepika@123",# Your MySQL password
        database="cricbuzz_db"   # Your MySQL database name
    )
    return conn

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dheepika@123",
        database="cricbuzz_db",
        port=3306
    )
