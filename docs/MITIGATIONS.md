# Task #07 - Mitigation Records and Verification

Date: 22 November 2026. Owner: student (bekbossynminsiz).
All results below are copied from the student's own terminal output (`task07_evidence.txt`). Nothing here was run by an AI assistant.

Versions:
- Baseline: `42333a0` (tag `baseline`)
- Before mitigations: `eeb9ae0` (after the `CATEGORY_RULES` refactoring)
- After M1: `0d0dc54`
- After M2: `e4ffc9f` (tag `mitigations`) - the reviewed version

Process: for each mitigation the new tests were written first and run against the unfixed code (they failed), then the fix was applied, the diff was reviewed with `git diff`, tests were re-run, and the change was committed. The code was proposed by an AI assistant (Claude); each diff was reviewed by the student before commit.

## 1. Check summary

| Check | Baseline `42333a0` | Before mitigations `eeb9ae0` | After `e4ffc9f` |
|---|---|---|---|
| `pytest -v` | 4 passed | 10 passed | **15 passed** |
| `ruff check .` | 1 error (I001, `tests/test_calculator.py:1`) | 1 error (same) | **All checks passed!** (side effect: blank line added in the test import block) |
| `mypy .` | 1 error (`calculator.py:3`, missing annotation) | 1 error (same) | 1 error (same, not addressed) |
| Build | not applicable (no build script) | not applicable | not applicable |

Diff `baseline..HEAD --stat`: 5 files changed, 221 insertions(+), 14 deletions(-)
(`AGENTS.md` 83, `docs/RISK_REGISTER.md` 78, `expense_calc/calculator.py` 23, `main.py` 13, `tests/test_calculator.py` 38 changed lines).

## 2. Mitigation record M1 - risk R-01 (non-numeric amount crashes the app)

- **Change:** in `main.py`, `float(input("Amount: "))` is wrapped in `try/except ValueError`; on error the menu prints "Invalid amount. Please enter a number." and returns to the menu (`continue`).
- **Commit:** `0d0dc54` (2 files, 20 insertions, 2 deletions, including the new test and `run_menu` helper).
- **Test added:** `test_non_numeric_amount_does_not_crash` (feeds `1`, `abc`, `0` through a monkeypatched `input`).
- **Before the fix:** `pytest -v -k non_numeric` -> `1 failed, 10 deselected`; error `ValueError: could not convert string to float: 'abc'` at `main.py:21`.
- **After the fix:** `11 passed`.
- **Manual check:** input `abc` printed "Invalid amount. Please enter a number." and the menu was shown again.
- **Trade-offs and limits:** only the amount prompt is guarded. The message does not explain decimal format. Other input exceptions (end of input, Ctrl+C) were not evaluated.

## 3. Mitigation record M2 - risk R-02 (zero and negative amounts accepted)

- **Change:** `add_expense` in `expense_calc/calculator.py` raises `ValueError("Amount must be greater than zero")` when `amount <= 0`; `main.py` catches `ValueError` around `add_expense` and prints "Error: ...".
- **Commit:** `e4ffc9f` (3 files, 20 insertions, 2 deletions).
- **Tests added:** `test_add_expense_rejects_non_positive_amount` (cases `0`, `-1`, `-100.5`) and `test_main_negative_amount_is_not_saved`.
- **Before the fix:** `pytest -v -k "non_positive or negative_amount"` -> `4 failed, 11 deselected` (three `DID NOT RAISE ValueError`, one `AssertionError`: "Expense added." was printed).
- **After the fix:** `15 passed`.
- **Manual check:** input `-5` printed "Error: Amount must be greater than zero"; input `100`/`food` printed "Expense added." and "Total with rules: 95.0".
- **Trade-offs and limits:**
  - The category and description are asked before the invalid amount is rejected (minor usability cost).
  - `add_expense` now raises, so any other caller must handle `ValueError` (behavior change of the function).
  - **Residual risk confirmed:** `add_expense(float('nan'), 'food', 'x')` is accepted and `get_total()` prints `nan`. `inf` was not evaluated.

## 4. Acceptance criteria after changes

| Criterion | Evidence |
|---|---|
| AC1 - valid expense increases total by that amount | `test_add_expense_increases_total` PASSED; manual add of 100 |
| AC2 - category total counts only that category | `test_total_by_category` PASSED |
| AC3 - `apply_rule` follows README table | `test_apply_rule_all_categories` (6 cases) PASSED |
| AC4 - `get_total_with_rules()` equals sum of rules | `test_total_with_rules` PASSED; manual run printed `Total with rules: 95.0` |
| AC5 - `pytest` passes, app exits cleanly on `0` | `15 passed`; manual run ended with "Bye!" |

## 5. Updated risk scores

Scores after mitigation are the student's proposed re-scores based on the evidence above.

| ID | Before (L x I) | After (L x I) | Basis |
|---|---|---|---|
| R-01 | 3 x 2 = 6 | 1 x 2 = **2** | crash path handled; failing test now passes; manual run confirms. Other input exceptions not evaluated |
| R-02 | 2 x 3 = 6 | 1 x 2 = **2** | zero and negatives rejected (4 tests, manual run). `nan` remains, tracked as R-13 |
| R-13 (new) | - | 1 x 2 = **2** | `nan` accepted, `get_total()` prints `nan` (confirmed by command) |
| R-11 | 2 x 2 = 4 | 2 x 2 = 4 | partly reduced (new tests for R-01/R-02), not re-scored: case sensitivity, `nan` and menu options 3-5 still untested |
| R-07 | 1 x 2 = 2 | unchanged | with the new `amount <= 0` check a string amount would likely fail inside `add_expense`; this was **not executed**, so the score is not changed |
| R-03, R-04, R-05, R-06, R-08, R-09, R-10, R-12 | unchanged | unchanged | not mitigated in this assignment (see `RISK_REGISTER.md`, section 2.2) |

Highest remaining confirmed scores: R-04 (4) and R-11 (4).

## 6. Not executed / limitations

- Interactive keyboard run of `python main.py` (the manual checks used piped input).
- End-of-input and Ctrl+C handling; `inf` as an amount.
- Test coverage percentage; CI run; runs on Linux or macOS.
- `ruff check --fix` (forbidden without approval by `AGENTS.md`).
- A mistake during the task: test code was first pasted into the terminal instead of the editor (PowerShell `ParserError`). It had no effect on the repository; the correct files were edited afterwards (see the diffs above).
