# AGENTS.md - Expense Calculator

## Purpose
Small console app in Python 3 for tracking personal expenses (amount, category,
description) and calculating totals with category-based discounts/taxes.
Student project for Software Engineering Assignment #05.
No network access, no secrets, no real financial or personal data.

## Architecture
- `main.py` - console menu (input/output). Currently also converts user input.
- `expense_calc/calculator.py` - business logic. Uses a module-level list
  `expenses` (global state). Functions: `add_expense`, `get_total`,
  `get_total_by_category`, `apply_rule`, `get_total_with_rules`, `clear_expenses`.
- `tests/test_calculator.py` - pytest unit tests; an autouse fixture clears state.
- `requirements.txt` - pinned dependencies (pytest and its dependencies).
- `ruff` and `mypy` are used locally for checks but are not yet in `requirements.txt`.

## Setup (Windows PowerShell)
```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Use `py -3` to create the venv: the MSYS2 `python` earlier in PATH creates a
Linux-style venv that does not work on Windows.

## Safe commands (agent may run without asking)
- `pytest -v`
- `ruff check .` (read-only; do NOT use `--fix` without approval)
- `mypy .`
- `python main.py` (interactive menu, enter `0` to exit)
- `git status`, `git diff`, `git log --oneline`, `git show`
- Reading any file in the repository

## Needs human approval first
- `git commit`, creating or switching branches
- `pip install ...` or any change to `requirements.txt`
- `ruff check --fix`, auto-formatters, any command that rewrites many files
- Creating, renaming or deleting files

## Forbidden
- Reading, writing or committing secrets, tokens, `.env` files or real personal data
- Deployments or any production/network operation
- Destructive commands: `git reset --hard`, `git push --force`, `git clean -fdx`,
  `Remove-Item -Recurse` / `rm -rf` outside a temporary folder, deleting `.git`
- Moving, deleting or re-creating the `baseline` tag
- Adding or upgrading dependencies without review
- Weakening, deleting or skipping existing tests to make a run pass

## Coding conventions
- Python 3, PEP 8, 4-space indentation, `snake_case` names
- Keep functions small and simple; no new abstractions unless a concrete
  maintainability problem justifies it (at most ONE design pattern in this project)
- `print`/`input` belong in `main.py`, business logic in `calculator.py`
- Category rules are documented in `README.md`; do not change them silently

## Test expectations
- Run `pytest -v` before and after every change and report the exact command
  and pass/fail totals
- Add or update a test for every behavior you change
- Tests must reset shared state (`clear_expenses`)
- Never claim a check passed if it was not actually run; say "not executed"

## Acceptance criteria (must stay true after any change)
1. AC1 - Adding a valid expense increases `get_total()` by exactly that amount.
2. AC2 - `get_total_by_category(c)` sums only expenses of category `c`.
3. AC3 - `apply_rule` follows the README table: food x0.95, health x0.90,
   entertainment x1.20, transport x1.10, other x1.00.
4. AC4 - `get_total_with_rules()` equals the sum of `apply_rule` over all expenses.
5. AC5 - `pytest -v` passes with 0 failures and `python main.py` exits cleanly on `0`.

## Review gates
- One logical change per commit; show the full diff to a human before commit
- Human approval is required before merge or any release decision
- Final report for each task: change summary, diff, test output, remaining risks
- Anything not verified by a command is labeled "assumption"

## Known issues (do not fix unless a task explicitly asks)
- Non-numeric amount crashes `main.py` with `ValueError`
- Negative and zero amounts are accepted
- Category matching is case-sensitive (`Food` != `food`)
- Money uses `float` (rounding errors such as 0.30000000000000004)
- `mypy` reports a missing annotation for `expenses`; `ruff` reports import order in tests
