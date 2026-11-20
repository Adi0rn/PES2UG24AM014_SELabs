# Lab 7: Fuzz Testing for Input Validation

**Adithya Ajith Pillai | PES2UG24AM014**

Assigned project: Cloud Storage Tier, from [https://github.com/SETAPESU26/L6_L7_12_cloud_storage_tier](https://github.com/SETAPESU26/L6_L7_12_cloud_storage_tier),
tree `3d3a798a451777c4300706166f7be1c8b3e13859`, folder `Lab 7`.

## Results

The three completed initial fuzz properties failed against the original
processor: **3 failed, 55 deselected**. The hardened implementation passes
the complete suite: **58 passed**, including six Hypothesis properties with
300 passing examples each (**1,800 passing generated examples**), plus 52
explicit regression/example cases. Strategy-generation rejects reported as
`invalid examples` are discarded draws, not invalid application outcomes.

## Deliverables

- `processor.py`: fixed application.
- `test_processor.py`: completed Hypothesis tests and regression cases.
- `Lab7_Fuzz_Testing_Report_PES2UG24AM014.pdf`: before/after CLI and test evidence,
  minimized failures, fixes and validation contract.
- `processor_before.txt`: original application snapshot for replay.
- `evidence/`: raw transcripts and terminal-output evidence images.

Evidence images render genuine captured command output; they are not native
desktop screenshots. Long output is paginated or explicitly excerpted, and
the complete transcripts remain available. Native terminal screenshots can
be taken on rerun if required by the evaluator.

## Run

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
./.venv/Scripts/python.exe processor.py
./.venv/Scripts/python.exe -m pytest test_processor.py -q --hypothesis-show-statistics
```

Normal demo input: `500MB`, `1024:256`, `HOT_TIER` on separate lines.
Invalid demo input: `bad`, `1:0`, `UNKNOWN` on separate lines. The CLI now
reports each invalid input and continues. EOF is handled explicitly.

To replay original failures without overwriting the fixed application:

```powershell
python replay_before.py
```

The replay script copies the snapshot and unchanged test suite into a
temporary directory, then runs only the three original no-crash properties.
The expected subprocess exit code is 1. Ordinary pytest on the fixed version
has no expected failures, skipped tests or swallowed failures.

## Defined validation contract

Invalid input returns `None`; the CLI prints `Invalid input.`. Functions do
not guess a value or conceal unexpected exceptions with broad catches.
The explicit 256-character limit bounds work before parsing/conversion.

| Function | Accepted input | Result | Rejected cases |
|---|---|---|---|
| `parse_storage_quota` | Non-negative ASCII integer with MB, GB or TB; case-insensitive; outer whitespace allowed | Formatted decimal GB, 1 TB = 1000 GB | Wrong type, empty text, negatives, fractional quotas, unsupported units, non-ASCII digits, oversized text |
| `compute_compression_ratio` | Exactly one colon; two finite float values; raw >= 0 and compressed > 0 | Finite ratio rounded to 2 decimals | Wrong type, malformed fields, NaN, infinity, overflow/underflow to invalid denominator, negative sizes, zero denominator |
| `lookup_bandwidth_tier_rate` | Exact normalized names/aliases listed in `TIER_RATES` | Hot .08, cool/cold .05, archive .02 | Unknown names, misleading prefixes, wrong types, oversized text |

Explicit examples and generated valid-input tests prevent an implementation
that merely returns `None` for everything from passing. Mixed Unicode, None,
integers, floats, bytes, lists and dictionaries probe invalid input types.
Deterministic generation and no on-disk Hypothesis database make local
reproduction straightforward. Fuzzing is bounded testing, not proof of no bugs.
