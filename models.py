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

def get_budgets(user_id):
    """Returns {"Food": 550.0, "Transport": 200.0, ...}"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT c.name, b.monthly_limit
           FROM budgets b
           JOIN categories c ON b.category_id = c.category_id
           WHERE b.user_id = %s""",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return {name: float(limit) for name, limit in rows}


def save_predictions(user_id, month, preds):
    """Store this month's estimates. month is a date like 2026-01-01."""
    cats = {c["category_id"]: c["name"] for c in get_categories()}
    ids = {name: cid for cid, name in cats.items()}

    conn = get_connection()
    cur = conn.cursor()
    # Remove older estimates for the same month, so refreshing the page doesn't pile up duplicates
    cur.execute("DELETE FROM predictions WHERE user_id = %s AND predicted_month = %s",
                (user_id, month))
    for category, p in preds.items():
        cur.execute(
            """INSERT INTO predictions
               (user_id, category_id, predicted_month, predicted_amount)
               VALUES (%s, %s, %s, %s)""",
            (user_id, ids[category], month, p["estimate"]),
        )
    conn.commit()
    conn.close()
