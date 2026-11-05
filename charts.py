import matplotlib
matplotlib.use("Agg")   # needed for Flask (no GUI)
import matplotlib.pyplot as plt

def spending_trend(table, category, path):
    data = table[table["category"] == category]
    plt.figure(figsize=(7, 4))
    plt.plot(data["month"].astype(str), data["amount"], marker="o")
    plt.title(f"{category} spending per month")
    plt.ylabel("GH₵")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def category_pie(shares, path):
    plt.figure(figsize=(5, 5))
    plt.pie(shares.values, labels=shares.index, autopct="%1.0f%%")
    plt.title("Where your money goes")
    plt.savefig(path)
    plt.close()
