def generate_recommendations(predictions, budgets, shares):
    tips = []

    for category, p in predictions.items():
        # 1. Predicted to exceed budget
        limit = budgets.get(category)
        if limit and p["estimate"] > limit:
            over = p["estimate"] - limit
            tips.append(f"{category}: estimated spend of GH₵{p['estimate']} may "
                        f"exceed your GH₵{limit} budget by about GH₵{over:.0f}.")

        # 2. Rising fast
        if p["trend_per_month"] > 0.05 * p["estimate"]:
            tips.append(f"{category} has been rising by about "
                        f"GH₵{p['trend_per_month']} each month. Worth watching.")

    # 3. Dominant category
    top = shares.index[0]
    if shares.iloc[0] > 40:
        tips.append(f"{top} takes up {shares.iloc[0]}% of your spending. "
                    f"Small cuts here have the biggest impact.")

    return tips
