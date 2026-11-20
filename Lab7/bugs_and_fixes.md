# Bugs and fixes

| Evidence source | Input / issue | Original behaviour | Fix |
|---|---|---|---|
| Hypothesis, minimized | Quota `None` and empty string | AttributeError or ValueError | Type check; full ASCII quota grammar |
| Hypothesis, minimized | Ratio `None`, empty string, `:`, `b''` | AttributeError, unpacking/float ValueError, TypeError | Type check; exactly one delimiter; numeric parsing |
| Hypothesis, minimized | Tier `None` and empty string | AttributeError or KeyError | Type check; bounded normalization; dictionary `.get` |
| Targeted regression and generated zero-denominator property | `1:0`, `0:0` | ZeroDivisionError | Require positive compressed size before division |
| Targeted regression | `nan:1`, `1:inf`, overflowing ratio | Non-finite or misleading numeric result | Require finite operands and finite result |
| Targeted regression | Negative sizes, negative/fractional quota | Invalid domain value accepted or conversion error | Explicit domain/format checks |
| Targeted regression | `HOTDOG`, `COLLISION`, `ARCHAIC` | Accepted due to three-character prefix | Exact normalized alias lookup |
| Robustness review and long-input regression | Excessively long text | Unbounded parsing work / integer conversion failure | 256-character limit before parsing |

Only the first three rows are attributed to minimized failures in the actual
initial Hypothesis run. The other cases were added deliberately as stronger
properties or regressions; they are not claimed as random discoveries.
