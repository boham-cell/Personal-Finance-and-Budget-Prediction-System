import random
from datetime import date
import models

YEAR = 2025

# (category_id, name, starting monthly total, change per month, transactions per month)
EXPENSES = [
    (3, "Food",           400, 15, (8, 15)),
    (4, "Transport",      150,  5, (6, 12)),
    (5, "Airtime & Data",  60,  2, (2, 5)),
    (7, "Entertainment",   80, -3, (2, 6)),
]

for i in range(12):
    month = i + 1
    for cat_id, name, base, growth, (low, high) in EXPENSES:
        n = random.randint(low, high)
        # Monthly total follows a trend, with about +/-10% noise
        total = base + i * growth + random.uniform(-0.1, 0.1) * base
        for _ in range(n):
            amount = round(total / n * random.uniform(0.95, 1.05), 2)
            models.add_transaction(1, cat_id, amount, name,
                                   date(YEAR, month, random.randint(1, 28)))

    # One salary per month
    models.add_transaction(1, 1, 2500, "Monthly salary", date(YEAR, month, 1))

print("Seeding done.")
