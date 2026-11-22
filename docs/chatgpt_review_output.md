# **READ-ONLY Risk Review — Expense Calculator**

**Review scope:** Static review of the supplied `AGENTS.md`, `README.md`, `requirements.txt`, `main.py`, `expense_calc/calculator.py`, and `tests/test_calculator.py`.

**Review approach:** No files were modified. No commands or tests were executed. All verification commands below are proposed commands for the project owner to run.

**Overall assessment:** The project is small and understandable, but it has several correctness, input-validation, maintainability, and dependency risks. The most important concerns are accepting invalid expense amounts, using floating-point arithmetic for money, handling invalid console input, and relying on shared mutable global state.

## **1. Candidate risk register**

### **RISK-01 — Non-numeric input crashes the application**



High priority

High confidence



- **ID:** RISK-01
- **Category:** Correctness
- **Cause:** The application converts console input directly using `float(input(...))` without exception handling.
- **Event:** A user enters text such as `abc` instead of a numeric amount.
- **Consequence:** Python raises `ValueError`, terminating the application instead of allowing the user to try again.
- **Affected file and function:** `main.py` — `main()`, option `"1"`.
- **Evidence:** `amount = float(input("Amount: "))`.
- **Verification command:**

```
python main.py
```

Select option `1` and enter `abc` for the amount.

- **Expected verification:** Check whether the application terminates with `ValueError`.
- **Confidence:** High.
- **Status:** Known issue explicitly documented in `AGENTS.md`.

### **RISK-02 — Negative and zero expenses are accepted**



High priority

High confidence



- **ID:** RISK-02
- **Category:** Correctness
- **Cause:** `add_expense()` does not validate the amount.
- **Event:** A user enters `-100` or `0`.
- **Consequence:** Invalid or meaningless expense records can be stored and can reduce or distort calculated totals.
- **Affected file and function:** `expense_calc/calculator.py` — `add_expense()`.
- **Evidence:** The function directly inserts `amount` into the expense dictionary and appends it to `expenses`.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense(-100, 'food', 'test'); c.add_expense(0, 'food', 'test'); print(c.expenses); print(c.get_total())"
```

- **Expected verification:** Check whether both records are accepted and whether the total becomes `-100`.
- **Confidence:** High.
- **Status:** Known issue explicitly documented in `AGENTS.md`.

### **RISK-03 — Floating-point precision errors in financial calculations**



High priority

High confidence



- **ID:** RISK-03
- **Category:** Correctness
- **Cause:** Monetary amounts and calculations use Python `float`.
- **Event:** A user adds decimal amounts that cannot be represented exactly in binary floating-point.
- **Consequence:** The displayed total may contain unexpected decimal digits, potentially producing inaccurate financial results.
- **Affected file and function:**
  - `expense_calc/calculator.py` — `add_expense()`
  - `expense_calc/calculator.py` — `get_total()`
  - `expense_calc/calculator.py` — `apply_rule()`
  - `expense_calc/calculator.py` — `get_total_with_rules()`
- **Evidence:** `get_total()` initializes `total = 0` and adds floating-point expense amounts. `apply_rule()` multiplies the amount by a floating-point multiplier.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense(0.1, 'other', 'a'); c.add_expense(0.2, 'other', 'b'); print(c.get_total())"
```

- **Expected verification:** Check whether the result is `0.30000000000000004` rather than exactly `0.3`.
- **Confidence:** High.
- **Status:** Known issue explicitly documented in `AGENTS.md`.

### **RISK-04 — Category matching is case-sensitive**



Medium priority

High confidence



- **ID:** RISK-04
- **Category:** Correctness
- **Cause:** Category comparisons and dictionary lookups use exact string matching without normalization.
- **Event:** A user enters `Food` instead of `food`.
- **Consequence:** The expense is not included in the lowercase `food` category total, and the food discount is not applied. The default multiplier of `1.0` is used instead.
- **Affected file and function:**
  - `expense_calc/calculator.py` — `get_total_by_category()`
  - `expense_calc/calculator.py` — `apply_rule()`
  - `main.py` — `main()`
- **Evidence:** `if e["category"] == category` and `CATEGORY_RULES.get(category, 1.0)`.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense(100, 'Food', 'lunch'); print(c.get_total_by_category('food')); print(c.apply_rule(100, 'Food'))"
```

- **Expected verification:** Check whether the category total is `0` and the rule result is `100.0`.
- **Confidence:** High.
- **Status:** Known issue explicitly documented in `AGENTS.md`.

### **RISK-05 — Unknown categories silently receive no discount or tax**



Medium priority

High confidence



- **ID:** RISK-05
- **Category:** Correctness
- **Cause:** `apply_rule()` uses `CATEGORY_RULES.get(category, 1.0)`, which assigns a default multiplier to every unrecognized category.
- **Event:** A user enters a category such as `shopping`, `travel`, or a misspelled category.
- **Consequence:** The application accepts the expense and calculates its adjusted amount without notifying the user that the category is unsupported.
- **Affected file and function:**
  - `expense_calc/calculator.py` — `add_expense()`
  - `expense_calc/calculator.py` — `apply_rule()`
  - `main.py` — `main()`
- **Evidence:** The default multiplier is `1.0`. The parameterized test also explicitly expects `unknown` to receive `100.0`.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense(100, 'shopping', 'test'); print(c.get_total_with_rules())"
```

- **Expected verification:** Check whether an unsupported category is accepted and included without any rule.
- **Confidence:** High.
- **Status:** Behavior is verified from the source text. Whether this is a defect depends on whether unsupported categories are intended to be permitted.

### **RISK-06 — Global mutable state creates test and maintenance risks**



Medium priority

High confidence



- **ID:** RISK-06
- **Category:** Maintainability
- **Cause:** All expenses are stored in a module-level mutable list named `expenses`.
- **Event:** Multiple functions, tests, or future modules access or modify the same list.
- **Consequence:** Unexpected state changes can affect calculations and make behavior dependent on the order of operations. The application also has no separation between individual user sessions.
- **Affected file and function:**
  - `expense_calc/calculator.py` — `add_expense()`
  - `expense_calc/calculator.py` — `get_total()`
  - `expense_calc/calculator.py` — `get_total_by_category()`
  - `expense_calc/calculator.py` — `get_total_with_rules()`
  - `expense_calc/calculator.py` — `clear_expenses()`
  - `main.py` — `main()`
- **Evidence:** All calculation functions read the shared `expenses` list, and `main.py` accesses it directly when listing expenses.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense(100, 'food', 'test'); print(c.expenses); c.clear_expenses(); print(c.expenses)"
```

- **Expected verification:** Observe that clearing the list changes the same shared state used by all functions.
- **Confidence:** High.
- **Status:** The shared state is directly confirmed by the source. The likelihood of actual cross-component interference is a design risk, not an observed failure.

### **RISK-07 — Business logic is not protected against invalid direct function calls**



Medium priority

High confidence



- **ID:** RISK-07
- **Category:** Correctness
- **Cause:** `add_expense()` has no validation of argument types or values.
- **Event:** Another Python module calls `add_expense()` with a string, `None`, or another unexpected value.
- **Consequence:** Invalid records may be stored successfully, but subsequent calculations can fail with `TypeError` or produce unintended results.
- **Affected file and function:** `expense_calc/calculator.py` — `add_expense()`, `get_total()`, `apply_rule()`.
- **Evidence:** The function directly stores the provided arguments without checking their types.
- **Verification command:**

```
python -c "from expense_calc import calculator as c; c.clear_expenses(); c.add_expense('100', 'food', 'test'); print(c.get_total())"
```

- **Expected verification:** Check whether the invalid record is accepted and whether `get_total()` raises `TypeError`.
- **Confidence:** High.
- **Status:** Inferred directly from the implementation; no runtime result has been observed.

### **RISK-08 — Dependency and development-tool configuration is incomplete**



Medium priority

High confidence



- **ID:** RISK-08
- **Category:** Dependency
- **Cause:** `ruff` and `mypy` are mentioned as local development tools in `AGENTS.md`, but they are absent from `requirements.txt`.
- **Event:** A developer creates a fresh virtual environment and installs only the declared requirements.
- **Consequence:** The developer may be unable to run the documented static-analysis checks because the required executables are not installed.
- **Affected file:** `requirements.txt`; development checks are associated with the entire project.
- **Affected functions:** Not applicable — development tooling configuration.
- **Evidence:** The dependency file lists `pytest` and its dependencies, while `AGENTS.md` explicitly states that `ruff` and `mypy` are not included.
- **Verification command:**

```
pip list
```

After installing the requirements in a clean environment, additionally run:

```
ruff check .
mypy .
```

- **Expected verification:** Check whether `ruff` and `mypy` are available in the environment.
- **Confidence:** High.
- **Status:** Missing development dependencies are explicitly documented. Their availability in an existing local environment is unverified.

### **RISK-09 — Missing type annotation for the global expenses list**



Low priority

High confidence



- **ID:** RISK-09
- **Category:** Maintainability
- **Cause:** The global `expenses` variable has no explicit type annotation.
- **Event:** A developer runs static type checking or extends the application with more complex expense structures.
- **Consequence:** Type checking may report an annotation issue, and the intended structure of expense records is less explicit.
- **Affected file and function:** `expense_calc/calculator.py` — module-level `expenses`; affects functions accessing the list.
- **Evidence:** `expenses = []` has no declared type.
- **Verification command:**

```
mypy .
```

- **Expected verification:** Check whether the tool reports the missing annotation.
- **Confidence:** High.
- **Status:** Explicitly identified as a known issue in `AGENTS.md`. Actual current output is unverified.

### **RISK-10 — Direct access to internal data reduces maintainability**



Low priority

High confidence



- **ID:** RISK-10
- **Category:** Maintainability
- **Cause:** The console interface directly accesses `calculator.expenses` and the internal dictionary structure of each record.
- **Event:** The expense data structure changes, for example from dictionaries to another representation.
- **Consequence:** The console interface may break even if the business calculation functions continue to work correctly.
- **Affected file and function:**
  - `main.py` — `main()`, option `"5"`.
  - `expense_calc/calculator.py` — `add_expense()`.
- **Evidence:**

```
for e in calculator.expenses:    print(e["category"], "-", e["description"], "-", e["amount"])
```

\- **Verification command:**

```
git grep -n "calculator.expenses"
```

- **Expected verification:** Check whether the console interface depends directly on the calculator's internal data representation.
- **Confidence:** High.
- **Status:** Direct coupling is confirmed from the supplied source.

### **RISK-11 — Incomplete test coverage of category rules and edge cases**



Medium priority

High confidence



- **ID:** RISK-11
- **Category:** Correctness
- **Cause:** Existing tests cover the food discount individually and all category multipliers through a parameterized test, but they do not comprehensively test validation, invalid amounts, category case handling, or floating-point accumulation.
- **Event:** A defect is introduced in an untested behavior or an existing edge case is overlooked.
- **Consequence:** The test suite may pass despite incorrect or undesirable application behavior.
- **Affected file and functions:**
  - `tests/test_calculator.py` — all existing tests.
  - `expense_calc/calculator.py` — `add_expense()`, `get_total()`, `get_total_by_category()`, `apply_rule()`.
- **Evidence:** The test file has no tests for negative amounts, zero amounts, invalid types, or category normalization. The current tests also do not verify the console input behavior.
- **Verification command:**

```
pytest -v
```

- **Expected verification:** Review the collected test names and compare their coverage with the listed acceptance criteria and edge cases.
- **Confidence:** High.
- **Status:** Test gaps are visible in the supplied test file. Actual test execution and coverage percentages are unverified.

### **RISK-12 — Agent setup instructions can lead to inconsistent environments**



Medium priority

High confidence



- **ID:** RISK-12
- **Category:** Agent operations
- **Cause:** `AGENTS.md` recommends creating a Windows virtual environment using `py -3`, while the README provides generic `python -m venv .venv` instructions.
- **Event:** A developer follows the README in an environment where `python` resolves to the MSYS2 interpreter instead of the intended Windows Python interpreter.
- **Consequence:** An incompatible virtual environment may be created, causing activation or execution problems.
- **Affected files:**
  - `AGENTS.md` — Setup instructions.
  - `README.md` — Setup instructions.
- **Affected functions:** Not applicable.
- **Evidence:** `AGENTS.md` explicitly warns about the MSYS2 Python executable and documents a different Windows setup command from the README.
- **Verification commands:**

```
where.exe python
where.exe py
python --version
py -3 --version
```

- **Expected verification:** Compare the interpreter paths and versions to determine which Python executable is selected.
- **Confidence:** High.
- **Status:** The instruction discrepancy and documented environment risk are confirmed. Whether the current machine has this issue is unverified.

## **2. Risk summary**

Counts represent candidate risks identified through static inspection, not confirmed runtime failures.

| Category         | Number of risks |
| ---------------- | --------------- |
| Correctness      | 6               |
| Maintainability  | 3               |
| Dependency       | 1               |
| Agent operations | 1               |
| **Total**        | **12**          |

## **3. Recommended verification order**

I recommend checking the following risks first because they directly affect the correctness of expense calculations or application stability.

| Priority | Risk ID | Reason                                                            |
| -------- | ------- | ----------------------------------------------------------------- |
| 1        | RISK-01 | Invalid input can terminate the application.                      |
| 2        | RISK-02 | Invalid financial values are accepted.                            |
| 3        | RISK-03 | Floating-point arithmetic can produce inaccurate monetary totals. |
| 4        | RISK-07 | Invalid direct function arguments can break calculations.         |
| 5        | RISK-04 | Category capitalization can change calculation results.           |
| 6        | RISK-05 | Unsupported categories are silently accepted.                     |
| 7        | RISK-11 | Existing tests do not cover several important edge cases.         |
| 8        | RISK-08 | Fresh development environments may lack static-analysis tools.    |

## **4. Verification checklist**

These commands are compatible with the read-only review requirements in `AGENTS.md`, except that interactive testing requires manual input. No command below has been executed as part of this review.

**Verification progress**

0/12

pytest -v

ruff check .

mypy .

git status

git diff

python main.py — test invalid amount and exit with 0

Verify negative and zero amounts

Verify floating-point precision

Verify category capitalization

Verify unsupported categories

Verify invalid direct function arguments

Check Python interpreter paths

## **5. Final assessment**

The highest-priority risks concern input validation and financial calculation correctness. The project also has maintainability concerns due to global mutable state and direct access to internal data.

The following distinctions are important:

- **Confirmed from source:** The code contains the identified implementation patterns.
- **Known issues:** Some risks are explicitly documented in `AGENTS.md`.
- **Unverified:** No tests, static-analysis tools, or interactive commands were executed. Therefore, no runtime failures or successful test results are claimed.
- **Assumptions:** Whether certain behaviors, such as accepting unknown categories or allowing zero-value expenses, violate the intended requirements depends on the project's business rules.

**Conclusion:** The project has 12 candidate risks across 4 categories, satisfying the requirement of at least 8 risks across at least 4 categories. The review is read-only, and no changes to the source code, tests, or dependencies are proposed or claimed.