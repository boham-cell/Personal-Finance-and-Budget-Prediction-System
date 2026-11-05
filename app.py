import time
import os
from flask import Flask, render_template, request, redirect, url_for, flash

import models
import analysis
import prediction
import charts
import recommendations

app = Flask(__name__)
app.secret_key = "change-this-later"
USER_ID = 1  # temporary until you add login


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a valid positive amount.")
            return redirect(url_for("add"))

        models.add_transaction(
            USER_ID,
            int(request.form["category_id"]),
            amount,
            request.form.get("description", ""),
            request.form["date"],
        )
        flash("Transaction saved.")
        return redirect(url_for("add"))

    return render_template("add_transaction.html",
                           categories=models.get_categories())


@app.route("/")
def dashboard():
    df = analysis.clean(analysis.load_transactions(USER_ID))
    if df.empty:
        return render_template("dashboard.html", empty=True)

    table = analysis.monthly_by_category(df)
    shares = analysis.category_share(df)
    summary = analysis.monthly_summary(df)
    preds = prediction.run_predictions(table)
    budgets = models.get_budgets(USER_ID)

    # The month being predicted = the month after the last one in the data
    next_period = table["month"].max() + 1
    next_month_label = next_period.strftime("%B %Y")
    models.save_predictions(USER_ID, next_period.to_timestamp().date(), preds)

    # Backtest error per category (how far off the model has been)
    errors = {}
    for category, group in table.groupby("category"):
        err = prediction.backtest(group.sort_values("month")["amount"].tolist())
        if err is not None:
            errors[category] = round(err, 2)

    # Charts
    trend_charts = []
    for category, p in preds.items():
        path = charts.spending_trend(table, category, p)
        if path:
            trend_charts.append({"category": category,
                                 "file": os.path.basename(path)})
    charts.category_pie(shares)
    charts.income_vs_expense(summary)

    tips = recommendations.generate_recommendations(preds, budgets, shares)

    return render_template(
        "dashboard.html",
        empty=False,
        preds=preds,
        budgets=budgets,
        errors=errors,
        tips=tips,
        trend_charts=trend_charts,
        next_month=next_month_label,
        ts=int(time.time()),     # stops the browser showing old cached images
    )


if __name__ == "__main__":
    app.run(debug=True)
