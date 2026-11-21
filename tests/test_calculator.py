import pytest
from expense_calc import calculator


@pytest.fixture(autouse=True)
def clean():
    calculator.clear_expenses()
    yield
    calculator.clear_expenses()


def test_add_expense_increases_total():
    calculator.add_expense(100, "food", "lunch")
    calculator.add_expense(50, "transport", "bus")
    assert calculator.get_total() == 150


def test_total_by_category():
    calculator.add_expense(100, "food", "lunch")
    calculator.add_expense(40, "food", "dinner")
    calculator.add_expense(50, "transport", "bus")
    assert calculator.get_total_by_category("food") == 140


def test_food_discount_applied():
    assert calculator.apply_rule(100, "food") == pytest.approx(95)


def test_total_with_rules():
    calculator.add_expense(100, "entertainment", "cinema")  # +20% = 120
    calculator.add_expense(100, "other", "misc")            # no change = 100
    assert calculator.get_total_with_rules() == pytest.approx(220)
