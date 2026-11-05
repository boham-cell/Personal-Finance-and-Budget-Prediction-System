import numpy as np
from sklearn.linear_model import LinearRegression

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
