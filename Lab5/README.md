# Lab 5 Static Code Analysis

**Adithya Ajith Pillai | PES2UG24AM014**

Assigned project: **Conference Room and Equipment Scheduler**, from [SETAPESU26/L5_12_room_scheduler](https://github.com/SETAPESU26/L5_12_room_scheduler), source commit `6bce27513c75c5750f1f907e90a97c9ed7907418`.

The program books rooms, allocates equipment by time slot, rejects overlapping bookings, logs room conflicts and exports the schedule as JSON. The cleaned implementation removes shell execution, validates requests before changing reservations and isolates schedule state in a `RoomScheduler` instance.

## Verified results

Actual runs using Python 3.12.10, Pylint 4.1.4, Bandit 1.9.4 and Flake8 7.5.0:

| Check | Before | After |
|---|---|---|
| Pylint | 5.60/10, 22 findings | **10.00/10**, exit 0 |
| Bandit | 1 High and 1 Low finding; no Medium findings | **0 findings**, exit 0 |
| Flake8 | 13 findings | **0 findings**, exit 0 |
| Regression tests | Not present upstream | **14 tests passed** |

No analyzer warnings are suppressed, no Bandit tests are skipped, and the default Flake8 79-character limit is retained. Analysis targets `scheduler_system.py`; the original is kept as a `.txt` snapshot so a recursive Python scan does not mistake it for production code. Tests are run separately.

## Run on Windows

From this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scheduler_system.py
.\.venv\Scripts\python.exe run_checks.py
```

The application itself uses only the Python standard library. The pinned requirements are for the analyzers. On Linux or macOS use `.venv/bin/python` in place of the Windows executable path.

Enter a two-digit hour interval such as `10-12`, or press Enter for that default. This is a single-day model with half-open intervals `[start, end)`: `09-11` and `11-12` may share a room or equipment. Overnight slots and minutes are outside the model. Equipment capacity is fixed; availability is calculated from reservations in each requested hour. Cancelling a booking frees its reserved availability without altering total capacity.

## Deliverables

| File | Content |
|---|---|
| scheduler_system.py | Cleaned executable scheduler |
| scheduler_system_before.txt | Exact upstream source snapshot |
| issues.md | Fourteen issue groups with original line numbers, tool codes and fixes |
| reflection.md | Four reflection topics and answers; missing question wording in the supplied PDF is disclosed |
| pylint_report_before.txt / pylint_report_after.txt | Actual Pylint reports |
| bandit_report_before.txt / bandit_report_after.txt | Actual Bandit reports |
| flake8_report_before.txt / flake8_report_after.txt | Actual Flake8 reports |
| bandit_report_stage1.txt | Bandit verification of the first security fix |
| pylint_report_stage2.txt / flake8_report_stage2.txt | Quality refactor verification before final formatting |
| program_output_before.txt / program_output_after.txt | Real default-input CLI runs |
| test_scheduler_system.py / test_report.txt | Fourteen regression tests and actual result |
| requirements-dev.txt / run_checks.py | Pinned analyzer environment and repeatable validation |
| provenance.json | Source identity and SHA-256 hashes for original and staged code |

Each report records its command, exit code and captured tool output. Reports were generated locally; no screenshots or tool runs are simulated. `run_checks.py` writes separate `*_report_current.txt` files so the submitted before/after evidence is retained.

## Three fix commits

1. **Bandit security fixes:** remove shell execution and silent exception swallowing; retain the upstream snapshot and before reports.
2. **Pylint and logic fixes:** refactor state, add documentation and input validation, correct room/equipment behaviour and verify the Pylint score.
3. **Flake8 formatting and final verification:** fix the remaining line-length findings, add final reports, issue documentation, reflection answers and regression tests.

The retained staged reports and `provenance.json` tie the submitted source versions to these three changes. Runtime output uses synthetic room bookings only. This is a lab CLI, not a multiuser production booking service.
