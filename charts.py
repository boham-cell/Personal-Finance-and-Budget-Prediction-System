import os
import matplotlib
matplotlib.use("Agg")   # draw to files, no pop-up window (required for Flask)
import matplotlib.pyplot as plt

# Absolute path, so it works no matter where you run the script from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE_DIR, "static", "charts")
os.makedirs(CHART_DIR, exist_ok=True)


def _save(filename):
    path = os.path.join(CHART_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()          # free memory, important in a web app
    return path


def _slug(text):
    return text.lower().replace(" & ", "_").replace(" ", "_")


def spending_trend(table, category, prediction=None):
    """Line chart of monthly spending, plus the forecast if given."""
    data = table[table["category"] == category].sort_values("month")
    if data.empty:
        return None

    months = [str(m) for m in data["month"]]
    amounts = data["amount"].tolist()

    plt.figure(figsize=(8, 4))
    plt.plot(months, amounts, marker="o", label="Actual")

    if prediction:
        next_month = str(data["month"].iloc[-1] + 1)   # e.g. 2025-12 -> 2026-01
        est, low, high = prediction["estimate"], prediction["low"], prediction["high"]

        # Dashed line from the last real point to the estimate
        plt.plot([months[-1], next_month], [amounts[-1], est],
                 linestyle="--", color="orange")
        # The estimate, with its likely range as an error bar
        plt.errorbar([next_month], [est],
                     yerr=[[est - low], [high - est]],
                     fmt="s", color="orange", capsize=6,
                     label="Estimate (likely range)")

    plt.title(f"{category}: monthly spending and next-month estimate")
    plt.ylabel("GH₵")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(alpha=0.3)
    return _save(f"{_slug(category)}_trend.png")


def category_pie(shares):
    """Pie chart. shares = output of analysis.category_share()."""
    plt.figure(figsize=(6, 6))
    plt.pie(shares.values, labels=shares.index, autopct="%1.0f%%", startangle=90)
    plt.title("Where your money goes")
    return _save("category_pie.png")


def income_vs_expense(summary):
    """Bar chart. summary = output of analysis.monthly_summary()."""
    data = summary.reindex(columns=["income", "expense"], fill_value=0)
    labels = [str(m) for m in data.index]

    x = range(len(labels))
    width = 0.4
    plt.figure(figsize=(9, 4))
    plt.bar([i - width / 2 for i in x], data["income"], width, label="Income")
    plt.bar([i + width / 2 for i in x], data["expense"], width, label="Expenses")
    plt.xticks(list(x), labels, rotation=45)
    plt.ylabel("GH₵")
    plt.title("Income vs expenses per month")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    return _save("income_vs_expense.png")
