import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        # Update these with your actual database credentials
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="enes",
            password="postgres",
            port="5432"
        )
        
        # Check if connection is successful
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("Connected to PostgreSQL successfully!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        cursor.close()
        connection.close()
        print("Connection closed.")
        
        return True
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    test_connection()