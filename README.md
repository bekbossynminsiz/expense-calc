# Expense Calculator

Small console app in Python 3 for tracking expenses.

## Features
- Add an expense (amount, category, description)
- Total of all expenses
- Total by category
- Total with category rules (discount/tax)

## Category rules
| Category      | Rule        |
|---------------|-------------|
| food          | 5% discount |
| health        | 10% discount |
| entertainment | 20% tax     |
| transport     | 10% tax     |
| other         | no change   |

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Run tests
```bash
pytest -v
```

## Project structure
```
expense_calc/calculator.py   # business logic
main.py                      # console menu
tests/test_calculator.py     # pytest tests
```
