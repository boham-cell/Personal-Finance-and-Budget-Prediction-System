#starter version
from flask import Flask, render_template, request, redirect, url_for, flash
import models

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

if __name__ == "__main__":
    app.run(debug=True)
