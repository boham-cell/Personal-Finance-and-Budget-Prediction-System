import analysis
import prediction
import charts

df = analysis.clean(analysis.load_transactions(1))
table = analysis.monthly_by_category(df)
shares = analysis.category_share(df)
summary = analysis.monthly_summary(df)
preds = prediction.run_predictions(table)

# One trend chart per category that has a prediction
for category, p in preds.items():
    print("Saved:", charts.spending_trend(table, category, p))

print("Saved:", charts.category_pie(shares))
print("Saved:", charts.income_vs_expense(summary))
