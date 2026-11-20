# Identified issues and fixes

Adithya Ajith Pillai | PES2UG24AM014 | Lab 5

Line numbers below refer to the unchanged upstream source retained as `scheduler_system_before.txt`. Tool codes come from the actual before reports. Bandit found one High and one Low issue, with no Medium findings. Manual logic findings are identified separately and are not attributed to the tools.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Bandit B605 | Security, High | 43 | `os.system("cat " + file)` interprets a filename as shell syntax and also depends on a Unix command. | Remove shell execution; read the UTF-8 log with `Path.read_text` and print it. A regression test uses shell metacharacters in the filename. |
| Bandit B110; Pylint W0702; Flake8 E722 | Error handling, Low security severity | 27-28 | Bare `except: pass` silently hides programming and data errors during cancellation. | Stage 1 catches only KeyError. The final implementation uses `dict.pop` and returns a boolean for an unknown booking; unexpected errors remain visible. |
| Pylint W0102 | Bug | 11 | The equipment default list is shared across calls, and caller-owned lists are stored directly. | Use `None`, create a fresh list and copy supplied equipment. Test default isolation and caller-list mutation. |
| Pylint W0603; C0103 | Maintainability | 6-9, 12 | Global mutable state and a globally incremented ID couple independent uses of the scheduler. | Encapsulate state in `RoomScheduler` with one ID sequence per instance; test instance isolation and ID stability after rejected bookings. |
| Pylint W1514; R1732 | Resource management and portability | 35-37, 40-43 | Files use implicit encoding and manual lifetime management; the log handle is never explicitly closed. | Use context managers with UTF-8 for export and logging. Let I/O errors propagate to the CLI, which reports them. |
| Pylint C0114; C0116 | Documentation | 1, 11, 22, 30, 34, 39, 45 | Module and public functions have no docstrings explaining their contracts. | Add module, class and method docstrings, including return values and validation behaviour. |
| Pylint C0103 | Naming | 39 | `logConflicts` does not follow snake_case. | Rename the method to `log_conflicts` and update its caller. |
| Pylint W0612; Flake8 F841 | Unused variables | 46, 47, 49 | Demo variables are assigned and never used. | Call the methods directly and replace invalid example bookings with explicit rejection demonstrations. |
| Pylint C0206; C0209 | Readability | 13, 15 | Dictionary keys are used solely to retrieve values, and old-style formatting obscures a simple message. | Iterate over `.values()` when keys are unnecessary and use f-strings. |
| Pylint C0301; Flake8 E501, E302, E305 | Formatting | 11, 14, 18, 22, 30, 34, 39, 45, 59 | Long lines and missing blank lines make the original harder to read. | Use PEP 8 spacing and a 79-character limit. The third commit resolves the remaining E501 findings after the Pylint refactor. |
| Double bookings are accepted | Logic, manual review | 13-15 | A conflict is logged but booking continues; partially overlapping intervals are not checked. | Reject intersections using half-open intervals `[start, end)` before storing the booking. Adjacent intervals remain valid. |
| Equipment over-allocation | Logic, manual review | 16-18 | Stock can go negative, unknown items crash, and permanent decrements prevent time-based reuse. | Keep equipment capacity fixed. Count quantities used in each overlapping hour, validate names and quantities before mutation, and free availability by cancelling bookings. |
| Invalid slot type or duration | Input validation, manual review | 18, 30-32, 48-50 | Reversed slots produce a negative duration; numeric slots are stored. | Validate ASCII `HH-HH` format and `0 <= start < end <= 24` before booking or calculating duration. |
| Import executes interactive code | Design, manual review | 59 | Importing the original runs the demo and waits for input. | Guard the CLI with `if __name__ == "__main__"` so tests can safely import the module. |

The class-based API is an intentional refactor: callers create `RoomScheduler()` and invoke its booking, cancellation, export and logging methods. The terminal entry point remains `python scheduler_system.py`.
