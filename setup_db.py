import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def setup_database():
    try:
        # Connect to MySQL without specifying a database
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Read and execute schema.sql
        with open("sql/schema.sql", "r") as f:
            schema_content = f.read()
        
        # Split by semicolon and execute each statement
        statements = schema_content.split(";")
        for statement in statements:
            statement = statement.strip()
            if statement:
                print(f"Executing: {statement[:50]}...")
                cursor.execute(statement)
        
        conn.commit()
        print(" Database setup completed successfully!")
        
    except Error as e:
        print(f"✗ Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
