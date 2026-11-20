# Static analysis reflection

Adithya Ajith Pillai | PES2UG24AM014 | Lab 5

The supplied handout requests reflection answers, and the upstream README refers to four questions, but the supplied three-page PDF does not contain the actual question text. The four topics below address the stated learning outcomes; they are not presented as verbatim handout questions.

## 1. What did each tool contribute?

Pylint identified the mutable default argument, global state, missing documentation, naming problems, unused variables and unsafe file handling. Flake8 highlighted spacing, line length, unused local variables and the bare exception. Bandit identified shell execution as a High-severity issue and exception swallowing as Low severity. Their overlap helped confirm priorities, while their different scopes explained why all three were useful.

## 2. Which issues were prioritized and how were they fixed?

The first priority was Bandit B605: a filename was concatenated into a shell command. Replacing the command with direct file reading removed command interpretation and the dependency on `cat`. The silent exception was also removed. Next, the refactor introduced isolated scheduler instances, explicit validation and managed UTF-8 file operations. The final formatting pass corrected the remaining Flake8 warnings without disabling checks or raising the line-length limit.

## 3. What did static analysis miss, and how were the changes checked?

The original program accepted a second reservation after logging a room conflict, returned a negative duration for `14-12` and stored the integer `1530` as a time slot. The tools did not establish whether those outcomes matched scheduler requirements. Fourteen regression tests therefore check exact and partial overlaps, adjacent slots, invalid inputs, duplicate equipment quantities, exhaustion, reuse at other times, cancellation, independent instances, copied lists, export, log filenames and visible I/O errors. The CLI was also run before and after using Enter for the default slot.

## 4. What was learned about code quality and the limits of the results?

The actual Pylint score improved from 5.60/10 to 10.00/10. Bandit went from two findings to none, and Flake8 went from thirteen findings to none. These results support code quality and remove known flagged patterns; they do not prove the program has no bugs or vulnerabilities. The scheduler remains an in-memory, single-process, single-day CLI: it does not implement calendar dates, user authentication, concurrent writers or persistent reload. Tests and review must accompany static analysis when those requirements are added.
