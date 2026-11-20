"""Run the three analyzers and regression tests from the Lab5 directory."""

import subprocess
import sys
from pathlib import Path


def main():
    """Record current results and fail when any validation fails."""
    root = Path(__file__).resolve().parent
    checks = (
        ("pylint", ["-m", "pylint", "--persistent=n", "scheduler_system.py"]),
        ("bandit", ["-m", "bandit", "-r", "scheduler_system.py"]),
        ("flake8", ["-m", "flake8", "scheduler_system.py"]),
        ("tests", ["-m", "unittest", "-v", "test_scheduler_system.py"]),
    )
    failed = False
    for name, arguments in checks:
        result = subprocess.run(
            [sys.executable, *arguments], cwd=root, capture_output=True,
            text=True, encoding="utf-8", errors="replace", check=False,
        )
        report = (
            f"Command: python {' '.join(arguments)}\n"
            f"Exit code: {result.returncode}\n\n"
            f"{result.stdout}{result.stderr}"
        )
        (root / f"{name}_report_current.txt").write_text(
            report, encoding="utf-8"
        )
        print(f"{name}: exit {result.returncode}")
        failed = failed or result.returncode != 0
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
