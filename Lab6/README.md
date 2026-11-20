# Lab 6: Code and Branch Coverage

**Adithya Ajith Pillai | PES2UG24AM014**

Assigned application: Cloud Storage Tier. Source: [https://github.com/SETAPESU26/L6_L7_12_cloud_storage_tier](https://github.com/SETAPESU26/L6_L7_12_cloud_storage_tier),
tree `3d3a798a451777c4300706166f7be1c8b3e13859`, folder `Lab 6`. Application logic is unchanged.

## Measured results

| Stage | Tests | Statements | Branches | Coverage.py combined percentage |
|---|---:|---:|---:|---:|
| Original test, branch run | 1 passed | 26/57 (45.61%) | 14/40 (35%) | 41.24% |
| Code coverage suite | 12 passed | 57/57 (100%) | Not instrumented | 100% |
| Branch coverage suite | 29 passed | 57/57 (100%) | 40/40 (100%) | 100% |

Both final results exceed the required 90%. The branch percentage above is
calculated from covered branch exits, not mistaken for the combined percentage.
JSON reports retain the raw counts and missing arcs. Nothing is excluded or
suppressed; the measured source is only `cloud_storage_tier.py`.

## Run the two submissions

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
./.venv/Scripts/python.exe -m coverage run --source=cloud_storage_tier -m pytest -q CodeCoverageTest_PES2UG24AM014_application.py
./.venv/Scripts/python.exe -m coverage report -m --fail-under=90
./.venv/Scripts/python.exe -m coverage run --branch --source=cloud_storage_tier -m pytest -q BranchCoverageTest_PES2UG24AM014_application.py
./.venv/Scripts/python.exe -m coverage report -m --fail-under=90
```

Explicit filenames are required because the handout's naming convention does
not match pytest's default `test_*.py` discovery. The branch suite collects the
line-stage cases by importing them, then adds boundary tests. It runs independently.

## Evidence and analysis

- `evidence/line_coverage.txt` and `line_coverage.png`: actual final line run.
- `evidence/branch_coverage.txt` and `branch_coverage.png`: actual final branch run.
- `evidence/*_coverage.json`: machine-readable measurements.
- `evidence/baseline.txt`: original test's line and branch results (text only).
- `Lab6_Coverage_Report_PES2UG24AM014.pdf`: results, evidence images and interpretation.

Evidence images render captured command output for readability. They are not
native desktop screenshots. All counts and output come from real local runs;
full unabridged transcripts are retained. Only final >=90% results are imaged,
as the handout requests. Native terminal screenshots can be taken on rerun if
required by the evaluator.

## Test rationale

The tests cover each storage tier, inactive tenants, invalid container/fee,
zero and negative sizes, unknown tiers, volume discounts, free versus paid
egress, backup support, and audit thresholds. Archive corruption resets the
accumulated tenant charge and breaks the bucket loop, while support fees
still apply; tests document that existing policy rather than changing it.

Boundary cases distinguish size 500/501, egress 100/101, four/five flags, and
latency 200/201. Replication tests verify reset after a healthy sample, reset
between nodes, empty node logs and early alert after two consecutive spikes.

Line coverage measures executed statements. Branch coverage measures decision
exits. Path coverage concerns combinations of decisions and loop iterations;
function coverage asks which functions ran. Both application functions run
here. 100% line/branch coverage does not establish all paths, all input types,
correctness of the business policy, or security.

The delivery history separates the code-coverage test/evidence commit from
the branch-coverage test/evidence commit, satisfying the two-commit structure.
