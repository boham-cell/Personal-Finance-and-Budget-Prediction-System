import pandas as pd
import models

def load_transactions(user_id):
    conn = models.get_connection()
    query = """
        SELECT t.transaction_date, t.amount, c.name AS category, c.type
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
    """
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    return df

def clean(df):
    df = df.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    df = df[df["amount"] > 0]
    df = df.drop_duplicates()
    df["month"] = df["transaction_date"].dt.to_period("M")
    return df

def monthly_by_category(df):
    expenses = df[df["type"] == "expense"]
    table = (expenses.groupby(["month", "category"])["amount"]
             .sum().reset_index())
    return table

def monthly_summary(df):
    pivot = (df.pivot_table(index="month", columns="type",
                            values="amount", aggfunc="sum", fill_value=0))
    pivot["savings"] = pivot.get("income", 0) - pivot.get("expense", 0)
    return pivot

df = clean(load_transactions(1))
print(monthly_by_category(df))
print(category_share(df))
def category_share(df):
    expenses = df[df["type"] == "expense"]
    totals = expenses.groupby("category")["amount"].sum()
    return (totals / totals.sum() * 100).round(1).sort_values(ascending=False)
