import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_categories():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM categories")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_transaction(user_id, category_id, amount, description, date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO transactions
           (user_id, category_id, amount, description, transaction_date)
           VALUES (%s, %s, %s, %s, %s)""",
        (user_id, category_id, amount, description, date),
    )
    conn.commit()
    conn.close()
