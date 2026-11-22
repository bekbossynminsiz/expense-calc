# Readiness Audit, Background Agent Safeguards and Release Decision

Project: Expense Calculator. Date: 22 November 2026. Owner: student (bekbossynminsiz).
Reviewed code version: commit `e4ffc9f` (tag `mitigations`). Documents committed afterwards (`a2a0af6` and later) do not change code.
Evidence comes from the student's own terminal output (`task01_evidence.txt`, `task04_evidence.txt`, `task07_evidence.txt`, and the `git ls-files` / `git grep` / `pip check` output of the audit step).

---

## 1. Task #06 - Agent-readiness audit

### 1.1 Repository audit

| Area | Observation and evidence | Rating |
|---|---|---|
| Readable structure | `git ls-files`: 11 tracked files; entry point `main.py`, logic in `expense_calc/`, tests in `tests/`, documents in `docs/` | Pass |
| README accuracy | README lists features, the category rules table (matches the 6-case test `test_apply_rule_all_categories`), setup, run and test commands. Gaps: `python -m venv .venv` produced a non-Windows venv on this machine (MSYS2 Python first in PATH) while `AGENTS.md` uses `py -3`; README does not mention `ruff`/`mypy` or input validation. README unchanged since baseline | Partial |
| Reproducible setup | `requirements.txt` pinned with `==` (6 packages) in both `baseline` and `HEAD`; `pip check`: "No broken requirements found." Gaps: Python version not declared in any tracked file (3.14.4 used); `ruff` and `mypy` not declared or pinned. Fresh-clone check executed (`git clone .`, `py -3 -m venv .venv`, `pip install -r requirements.txt`, `pytest -v`): 15 passed on Python 3.14.4. Limits: pip used cached wheels (`Using cached`), and the README's own `python -m venv` command was not used | Partial |
| Tests | `pytest -v`: 15 passed; cover acceptance criteria AC1-AC5 and both mitigations. Gaps: no coverage measurement; category case, `nan` and menu options 3-5 untested (R-11) | Partial |
| Lint / type checks | `ruff check .`: All checks passed (default rules, no config file tracked). `mypy .`: 1 error (`calculator.py:3`, missing annotation), not fixed | Partial |
| Build | No build script; not applicable for a pure-Python console app | N/A |
| Logging | `git grep -i logging`: no matches. Errors are only printed to the console | Gap (low impact) |
| Security safeguards | No secrets: `git grep` for password/secret/token/api key matches only two prohibition lines in `AGENTS.md`. No network code: search for requests/socket/urllib/http returned nothing. `.gitignore` excludes `.venv/` and caches. Input validation for numeric and positive amounts. Gaps: no secret scanner, no dependency vulnerability scan (not executed), `nan` accepted (R-13) | Partial |
| Automation / CI | No CI configuration in `git ls-files`; all checks are run manually | Gap |

### 1.2 AGENTS.md inspection

| Item | Observation | Rating |
|---|---|---|
| Permissions and safe commands | Sections "Safe commands" and "Needs human approval first" list exact commands | Pass |
| Prohibited actions | Section "Forbidden": secrets, deployment, destructive git/file commands, baseline tag, dependency changes, weakening tests | Pass |
| Review gates and acceptance criteria | Present (one change per commit, human approval, AC1-AC5) | Pass |
| Accuracy | "Known issues" was stale: it still listed the non-numeric crash and negative amounts (fixed in `0d0dc54`, `e4ffc9f`) and omitted `nan`. Update committed after this audit | Gap (fixed) |
| Enforcement | Rules are advisory text; no tool-level permissions, hooks or CI that would block a violation | Gap |
| Evidence that an agent followed it | The file was pasted manually into the ChatGPT prompt (the tool does not load it automatically); the review stayed read-only and referenced the file. No session log shows an agent obeying it during edits | Partial |

### 1.3 Readiness level: **2 - Documented**

Justification: the repository has accurate documentation (README, AGENTS.md with safe/forbidden actions and review gates), pinned dependencies, 15 passing tests, acceptance criteria and a risk register. It is not Level 3 (agent-ready) because nothing enforces the rules automatically and several checks are not yet clean or automated.

Missing evidence for Level 3:
1. CI (or equivalent) running `pytest`, `ruff`, `mypy` on every change.
2. A clean `mypy` result and `ruff`/`mypy` declared and pinned in a dev requirements file.
3. Python version declared (for example in README or a `.python-version` file).
4. A setup run on a clean machine that follows only the README with a cold pip cache. A fresh-clone run exists (15 passed) but used cached wheels and the `py -3` command from `AGENTS.md`.
5. A recorded agent session showing the agent followed `AGENTS.md` (read-only commands, allowlist, approval gates).
6. Test coverage report and tests for known gaps (case sensitivity, `nan`).

---

## 2. Task #03 summary (for completeness)

See the pattern decision in the main report: Strategy was rejected as unnecessary; a rules table (`CATEGORY_RULES`) replaced the `if/elif` chain in commit `eeb9ae0` with 10 tests passing before and after.

---

## 3. Task #08 - Background agent safeguards (hypothetical)

No paid background-agent access was used. This is a design for an asynchronous agent task.

**Task statement:** "Mitigate R-04: make category matching case-insensitive (`Food` and `food` are the same category) and add tests."

| Safeguard | Definition |
|---|---|
| Isolation | New branch `agent/r04-category-case` created from tag `mitigations`, in a separate `git worktree` (`..\expense-calc-agent`) with its own virtual environment installed from the pinned `requirements.txt`. The main working tree is never touched |
| Allowed files (edit) | `expense_calc/calculator.py`, `tests/test_calculator.py` |
| Read-only files | `README.md`, `AGENTS.md`, `main.py`, `docs/` |
| Never edit | `requirements.txt`, `AGENTS.md`, `.git` configuration, tags |
| Allowed commands | `pytest -v`, `ruff check .`, `mypy .`, `git status`, `git diff`, `git log`, `git show`, `git add`, `git commit` (commits on the agent branch only) |
| Prohibited operations | merge, push, tag changes, branch deletion, `git reset --hard`, `git clean`, `--force`, `pip install` or any dependency change, network access, reading files outside the worktree, secrets, deployment, `ruff --fix` over the whole repo, deleting or weakening existing tests |
| Time and size limits | 20 minutes wall-clock; at most 3 test-fix iterations; at most 150 changed lines; at most 2 files edited |
| Required artifacts | (1) change summary; (2) patch from `git diff mitigations..HEAD`; (3) `pytest -v` log before and after; (4) `ruff` and `mypy` output; (5) build result ("not applicable"); (6) risk notes listing what was not verified; (7) log of commands run |
| Human review gate | Reviewer (student) checks: `git diff --name-only mitigations..agent/r04-category-case` lists only the two allowed files; reads the full diff; re-runs `pytest -v` in a clean checkout; confirms AC1-AC5 and that no test was removed or weakened. Only then merges manually (fast-forward). No automatic merge and no deployment without approval |
| Failure handling | Tests still failing after 3 iterations, time limit exceeded, or any file outside the allowlist changed -> the agent stops, writes a failure report, and the branch stays unmerged |
| Rollback | Unmerged: remove the worktree and delete the branch. Merged and problem found later: the human runs `git revert <commit>` or returns to tag `mitigations` (known-good version). The agent never performs destructive git operations |

---

## 4. Task #09 - Release decision

**Decision: CONDITIONAL** for the reviewed version `e4ffc9f`.

Scope of the release: local, single-user, non-accounting use of the console app. Not approved for cases where totals must be exact money values, and not approved for unattended agent merges.

### 4.1 Evidence

| Source | Result |
|---|---|
| Tests | `pytest -v`: 15 passed (baseline 4, before mitigations 10) |
| Static checks | `ruff`: All checks passed. `mypy`: 1 typing error, not a runtime failure |
| Acceptance criteria | AC1-AC5 hold (see `docs/MITIGATIONS.md`, section 4) |
| Risk register | Top two risks mitigated (6 -> 2 each). Highest remaining confirmed scores: R-04 (4) and R-11 (4); all others 3 or lower |
| Security | No secrets, no network code, no persistence of data |
| Readiness | Level 2 (Documented) |

### 4.2 Why not GO or NO-GO

- Not GO: R-04 (case-sensitive categories) and R-13 (`nan` accepted) have no control yet, `mypy` is not clean, there is no CI, and the readiness level is 2.
- Not NO-GO: all critical checks pass, no data-loss or security problem was observed, and remaining risks score 4 or lower.

### 4.3 Conditions

| ID | Condition | Owner | Verification |
|---|---|---|---|
| C1 | Fix R-04 (normalize category) or document the limitation in README before wider use | Student | Test that `Food` and `food` give the same total and rule |
| C2 | Reject `nan`/`inf` amounts (R-13) or document the limitation | Student | Test that `add_expense(float('nan'), ...)` raises `ValueError` |
| C3 | Keep `AGENTS.md` known issues in sync with the register (updated after this audit) | Student | `git grep -n "Known issues" AGENTS.md` and compare with the register |
| C4 | No background-agent merges until Level 3 evidence exists (CI, clean `mypy`, pinned dev tools, recorded agent session) | Student | Re-run this audit |

### 4.4 Remaining risks and limits

R-03 (float rounding), R-04, R-05 (unknown categories), R-06 (global state), R-07, R-08, R-09, R-10, R-11, R-12, R-13 remain open as listed in `docs/RISK_REGISTER.md` and `docs/MITIGATIONS.md`. Not executed: setup from a clean machine with a cold pip cache following only the README, dependency vulnerability scan, coverage measurement, CI, interactive keyboard testing.

Decision made by the student (bekbossynminsiz); an AI assistant helped draft the document.
