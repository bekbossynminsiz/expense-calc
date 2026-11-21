# Simple expense calculator logic

expenses = []


def add_expense(amount, category, description):
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


def apply_rule(amount, category):
    # discount or tax depends on category
    if category == "food":
        return amount * 0.95      # 5% discount
    elif category == "health":
        return amount * 0.90      # 10% discount
    elif category == "entertainment":
        return amount * 1.20      # 20% tax
    elif category == "transport":
        return amount * 1.10      # 10% tax
    else:
        return amount


def get_total_with_rules():
    total = 0
    for e in expenses:
        total = total + apply_rule(e["amount"], e["category"])
    return total


def clear_expenses():
    expenses.clear()
