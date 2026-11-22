# Simple expense calculator logic

expenses = []


def add_expense(amount, category, description):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
    }
    expenses.append(expense)
    return expense


def get_total():
    total = 0
    for e in expenses:
        total = total + e["amount"]
    return total


def get_total_by_category(category):
    total = 0
    for e in expenses:
        if e["category"] == category:
            total = total + e["amount"]
    return total


# category -> multiplier (below 1 = discount, above 1 = tax)
CATEGORY_RULES = {
    "food": 0.95,           # 5% discount
    "health": 0.90,         # 10% discount
    "entertainment": 1.20,  # 20% tax
    "transport": 1.10,      # 10% tax
}


def apply_rule(amount, category):
    return amount * CATEGORY_RULES.get(category, 1.0)


def get_total_with_rules():
    total = 0
    for e in expenses:
        total = total + apply_rule(e["amount"], e["category"])
    return total


def clear_expenses():
    expenses.clear()
