def generate_recommendations(preds, budgets, shares):
    tips = []

    for category, p in preds.items():
        limit = budgets.get(category)

        # 1. Estimated to go over budget
        if limit and p["estimate"] > limit:
            over = p["estimate"] - limit
            tips.append(
                f"{category}: the estimate of GH₵{p['estimate']:.0f} could exceed "
                f"your GH₵{limit:.0f} budget by about GH₵{over:.0f}."
            )
        elif limit and p["high"] > limit:
            tips.append(
                f"{category}: the estimate is within budget, but the upper end of "
                f"the likely range (GH₵{p['high']:.0f}) is above your GH₵{limit:.0f} limit."
            )

        # 2. Rising quickly (more than 5% of the estimate per month)
        if p["estimate"] > 0 and p["trend_per_month"] > 0.05 * p["estimate"]:
            tips.append(
                f"{category} has been rising by about GH₵{p['trend_per_month']:.0f} "
                f"a month. Worth keeping an eye on."
            )

        # 3. Good news: falling
        if p["trend_per_month"] < -0.05 * max(p["estimate"], 1):
            tips.append(
                f"{category} spending has been falling by about "
                f"GH₵{abs(p['trend_per_month']):.0f} a month. Nice work."
            )

    # 4. One category dominates spending
    if len(shares) > 0 and shares.iloc[0] > 40:
        tips.append(
            f"{shares.index[0]} makes up {shares.iloc[0]:.0f}% of your spending, "
            f"so small cuts there would make the biggest difference."
        )

    if not tips:
        tips.append("Your spending looks steady. No concerns at the moment.")
    return tips
