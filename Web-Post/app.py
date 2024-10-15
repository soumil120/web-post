from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

# Get database connection details from environment variables
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_SERVER,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def index():
    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cursor = conn.cursor()
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({"message": f"Connected to PostgreSQL: {db_version}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
