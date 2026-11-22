# Risk Review and Risk Register - Expense Calculator

Baseline: commit `42333a0` (tag `baseline`). Reviewed version: commit `eeb9ae0`.
Date: 22 November 2026. Owner: student (bekbossynminsiz).
AI reviewer: ChatGPT (free version), read-only review, no files modified, no commands run by the AI.
All evidence below comes from commands run by the student (see `task01_evidence.txt`, `task04_evidence.txt`).

Scoring: likelihood (L) 1-3, impact (I) 1-3, score = L x I (1-9).
Status values: **confirmed** (reproduced by command or visible in file), **plausible/unverified**, **unsupported**.

## 1. Task #04 - Classification of AI findings

| AI ID | AI claim (short) | Category | Status | Evidence |
|---|---|---|---|---|
| R-01 | Non-numeric amount crashes the app | Correctness | Confirmed | `main.py:21` `float(input(...))`; entering `abc` gives `ValueError` traceback |
| R-02 | Zero and negative amounts accepted | Correctness | Confirmed | `add_expense(-100)` and `add_expense(0)` both stored; `get_total()` returned `-100` |
| R-03 | Float rounding errors | Correctness | Confirmed | three additions of 0.1 gave `0.30000000000000004` |
| R-04 | Category matching is case-sensitive | Correctness | Confirmed | `'Food'` gave total `100` (no 5% discount); `'food'` gives 95 per test |
| R-05 | Unknown category silently gets no rule | Correctness | Confirmed (behavior); whether it is a defect is an assumption | `'shopping'` gave `100.0`; test `unknown-100.0` passes |
| R-06 | Global mutable state | Maintainability | Cause confirmed; consequences plausible/unverified | `git grep expenses`: `calculator.py` lines 3, 12, 18, 25, 46, 52; no failure observed |
| R-06 (part) | "No separation between user sessions" | - | Unsupported | single-user console app; no session logic exists |
| R-07 | No type validation in `add_expense` | Correctness | Confirmed | `add_expense('100', ...)` accepted; `get_total()` raised `TypeError` at `calculator.py:19` |
| R-08 | `ruff`/`mypy` not declared in requirements | Dependency | Confirmed | `git grep -i -E "ruff\|mypy" requirements.txt` returned nothing; `pip list` before install had neither |
| R-09 | Missing annotation on `expenses` | Maintainability | Confirmed | `mypy .`: `calculator.py:3: Need type annotation for "expenses"` |
| R-10 | `main.py` reads `calculator.expenses` directly | Maintainability | Confirmed | `git grep "calculator.expenses"`: `main.py:34` |
| R-11 | Test gaps | Maintainability | Confirmed | 5 test functions / 10 cases; none for negative/zero amounts, case, `main.py` |
| R-12 | README and AGENTS.md give different venv commands | Agent operations | Confirmed | `README.md:22` `python -m venv`; `AGENTS.md:20` `py -3 -m venv`; `python -m venv` created a Linux-style venv on this machine (MSYS2 Python first in PATH) |

Reviewer notes (human judgment):
- The AI rated R-03 "high priority". Impact is scored 1 here: the error is about 1e-17 in a personal tracker.
- R-01 to R-04 and R-09 largely restate the "Known issues" section of `AGENTS.md` that was pasted into the prompt, so they are not fully independent discoveries.
- R-12 is real but partly self-inflicted: both documents were written with AI help.
- Categories covered: correctness, maintainability, dependency, agent operations. No security finding was confirmed.

## 2. Task #05 - Risk register

### 2.1 Identification and scoring

| ID | Category | Cause -> Event -> Consequence | Affected component | Evidence | L | I | Score |
|---|---|---|---|---|---|---|---|
| R-01 | Correctness | Unchecked `float(input())` -> user types text (or "10,5" with decimal comma, an assumption) -> app terminates, in-memory expenses lost | `main.py` option 1 | `ValueError` traceback, `main.py:21` | 3 | 2 | **6** |
| R-02 | Correctness | No amount validation -> user enters 0 or negative -> invalid records stored, totals silently wrong | `calculator.add_expense` | stored `-100` and `0`, total `-100` | 2 | 3 | **6** |
| R-03 | Correctness | Money stored as `float` -> decimal amounts added -> totals show rounding noise | `calculator.get_total` and others | `0.30000000000000004` | 3 | 1 | 3 |
| R-04 | Correctness | Exact string match on category -> user types `Food` -> no discount, category total 0 | `get_total_by_category`, `apply_rule` | `'Food'` total `100` | 2 | 2 | 4 |
| R-05 | Correctness | Default multiplier 1.0 -> unknown/misspelled category -> accepted with no rule or warning | `apply_rule` | `'shopping'` gave `100.0` | 2 | 1 | 2 |
| R-06 | Maintainability | Module-level list -> code grows or tests share state -> order-dependent behavior (plausible, not observed) | `calculator.expenses` | `git grep expenses` | 1 | 2 | 2 |
| R-07 | Correctness | No type checks -> other code passes a string -> bad record stored, failure deferred to `get_total` | `calculator.add_expense` | `TypeError` at `calculator.py:19` | 1 | 2 | 2 |
| R-08 | Dependency | `ruff`/`mypy` not declared -> fresh venv from `requirements.txt` -> documented checks cannot run | `requirements.txt` | empty `git grep` result | 2 | 1 | 2 |
| R-09 | Maintainability | No annotation -> type check run -> `mypy` fails, record structure implicit | `calculator.py:3` | `mypy .` error | 3 | 1 | 3 |
| R-10 | Maintainability | UI reads internal dict structure -> data representation changes -> menu breaks | `main.py:34` | `git grep` | 2 | 1 | 2 |
| R-11 | Maintainability | Thin tests -> regression in untested behavior -> suite still passes | `tests/test_calculator.py` | test list | 2 | 2 | 4 |
| R-12 | Agent operations | README/AGENTS.md mismatch -> agent follows README -> wrong venv, checks fail | `README.md`, `AGENTS.md` | line references above | 3 | 1 | 3 |

### 2.2 Treatment

| ID | Mitigation | Owner | Verification plan | Residual risk |
|---|---|---|---|---|
| R-01 | **Selected (M1).** Catch `ValueError` around input conversion in `main.py`; print a message and return to the menu | Student | New test with monkeypatched `input` feeding `1`, `abc`, `0`; manual run with `abc`; `pytest -v` before and after | To be re-scored after Task #07 with real output |
| R-02 | **Selected (M2).** Reject `amount <= 0` in `add_expense` with `ValueError`; `main.py` shows the message | Student | New tests for `-1` and `0`; re-run the Task #04 command; `pytest -v` before and after | To be re-scored. `nan`/`inf` input may still pass (plausible, not yet verified) |
| R-03 | Not mitigated now. Accepted: impact is low | Student | Re-evaluate if totals are shown to users as money | Unchanged (3) |
| R-04 | Deferred. Candidate: normalize with `.strip().lower()` | Student | Test `Food` equals `food` | Unchanged (4) |
| R-05 | Deferred; needs a requirement decision | Student | Decide if unknown categories are allowed | Unchanged (2) |
| R-06 | Deferred; wrap state in a class if the project grows | Student | Test order independence | Unchanged (2) |
| R-07 | Partly reduced by M1/M2 for the console path; direct API misuse remains | Student | Add type check test if the API is reused | Low |
| R-08 | Deferred; add `requirements-dev.txt` | Student | Fresh venv, install, run `ruff` and `mypy` | Unchanged (2) |
| R-09 | Deferred; add `expenses: list[dict] = []` | Student | `mypy .` clean | Unchanged (3) |
| R-10 | Deferred; add `list_expenses()` accessor | Student | `git grep` shows no direct access | Unchanged (2) |
| R-11 | Partly addressed by new tests in M1/M2 | Student | Compare test list before and after | Reduced; re-score in Task #07 |
| R-12 | Deferred; align README with `py -3` | Student | Follow README in a clean clone | Unchanged (3) |

### 2.3 Top two confirmed risks for corrective action

1. **R-02** (score 6, impact 3): silent wrong financial data is worse than a visible failure.
2. **R-01** (score 6): any typo terminates the app and loses the session's data.

Selection rationale: both reach the maximum score of 6 (all others are 4 or lower), both are confirmed with command evidence, both can be fixed with minimal diffs, and both are independent of the `CATEGORY_RULES` refactoring. Next in line: R-04 and R-11 (score 4).

Scores after mitigation will be updated in Task #07 using real before/after test output only.
