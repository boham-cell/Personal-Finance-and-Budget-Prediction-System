import random
from datetime import date
import models

# Monthly food spending with a gentle upward trend + noise
base = 400
for i in range(12):                       # 12 months
    month = i + 1
    for _ in range(random.randint(8, 15)):  # many small transactions
        day = random.randint(1, 28)
        amount = round((base + i * 15) / 12 + random.uniform(-8, 8), 2)
        models.add_transaction(1, 3, amount, "Food", date(2025, month, day))
