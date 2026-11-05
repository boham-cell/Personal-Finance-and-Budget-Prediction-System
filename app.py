from flask import Flask, render_template, request, redirect, url_for, flash
import models
import analysis, prediction, charts, recommendations

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
    table = analysis.monthly_by_category(df)
    shares = analysis.category_share(df)
    preds = prediction.run_predictions(USER_ID, table)

    charts.category_pie(shares, "static/charts/pie.png")
    charts.spending_trend(table, "Food", "static/charts/food.png")

    budgets = {"Food": 500, "Transport": 200}  # later: load from budgets table
    tips = recommendations.generate_recommendations(preds, budgets, shares)

    return render_template("dashboard.html", preds=preds, tips=tips)

if __name__ == "__main__":
    app.run(debug=True)
