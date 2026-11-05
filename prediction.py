import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import models
from sklearn.metrics import mean_absolute_error

MIN_MONTHS = 3

def predict_next_month(monthly_amounts):
    """
    monthly_amounts: list of totals, oldest first, e.g. [400, 450, 480, 500, 520]
    Returns dict with the estimate and a rough uncertainty range.
    """
    y = np.array(monthly_amounts, dtype=float)
    if len(y) < MIN_MONTHS:
        return None  # not enough history

    X = np.arange(1, len(y) + 1).reshape(-1, 1)
    model = LinearRegression().fit(X, y)

    next_x = np.array([[len(y) + 1]])
    pred = float(model.predict(next_x)[0])
    pred = max(pred, 0)  # spending can't be negative

    # Rough error range from past residuals
    residuals = y - model.predict(X)
    margin = float(np.std(residuals)) * 1.5

    return {
        "estimate": round(pred, 2),
        "low": round(max(pred - margin, 0), 2),
        "high": round(pred + margin, 2),
        "trend_per_month": round(float(model.coef_[0]), 2),
    } 

print(predict_next_month([400, 450, 480, 500, 520]))
# ≈ {'estimate': 553.33, ..., 'trend_per_month': 30.0}

def backtest(monthly_amounts, test_size=2):
    train, test = monthly_amounts[:-test_size], monthly_amounts[-test_size:]
    X = np.arange(1, len(train) + 1).reshape(-1, 1)
    model = LinearRegression().fit(X, train)
    X_test = np.arange(len(train) + 1, len(monthly_amounts) + 1).reshape(-1, 1)
    return mean_absolute_error(test, model.predict(X_test))

def run_predictions(table):
    """table = output of analysis.monthly_by_category()"""
    results = {}
    for category, group in table.groupby("category"):
        group = group.sort_values("month")

        # Fill months with zero spending so there are no gaps
        full = pd.period_range(group["month"].min(), group["month"].max(), freq="M")
        group = (group.set_index("month")
                      .reindex(full, fill_value=0)
                      .rename_axis("month")
                      .reset_index())

        result = predict_next_month(group["amount"].tolist())
        if result:
            results[category] = result
    return results

def save_prediction(user_id, category_id, month, amount):
    conn = models.get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO predictions
           (user_id, category_id, predicted_month, predicted_amount)
           VALUES (%s,%s,%s,%s)""",
        (user_id, category_id, month, amount),
    )
    conn.commit()
    conn.close()
