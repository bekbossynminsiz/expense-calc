import pytest

import main
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

@pytest.mark.parametrize("category, expected", [
    ("food", 95.0),
    ("health", 90.0),
    ("entertainment", 120.0),
    ("transport", 110.0),
    ("other", 100.0),
    ("unknown", 100.0),
])
def test_apply_rule_all_categories(category, expected):
    assert calculator.apply_rule(100, category) == pytest.approx(expected)

def run_menu(monkeypatch, inputs):
    answers = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main.main()


def test_non_numeric_amount_does_not_crash(monkeypatch, capsys):
    run_menu(monkeypatch, ["1", "abc", "0"])
    output = capsys.readouterr().out
    assert "Invalid amount" in output
    assert calculator.get_total() == 0