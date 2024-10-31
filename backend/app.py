from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "db"),
            database=os.environ.get("DB_NAME", "mydatabase"),
            user=os.environ.get("DB_USER", "myuser"),
            password=os.environ.get("DB_PASSWORD", "mypassword")
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return None

@app.route('/')
def hello():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        return jsonify({"message": "Hello, Docker!", "db_version": db_version})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
