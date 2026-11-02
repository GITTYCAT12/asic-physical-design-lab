# Comparing STA Metrics

Use `scripts/compare_timing_metrics.py` to compare a small, manually curated set
of baseline and candidate timing metrics. This is useful for recording the
effect of a timing ECO without needing to re-open an EDA GUI.

## Input format

Each JSON file may contain any of these numeric fields:

| Key | Meaning | Unit / interpretation |
|---|---|---|
| `wns_ns` | Setup worst negative slack | ns; higher is generally better |
| `tns_ns` | Setup total negative slack | ns; closer to zero is generally better |
| `hold_wns_ns` | Hold worst slack | ns; interpret using the STA tool's sign convention |
| `violating_endpoints` | Number of violating endpoints | Non-negative integer; lower is generally better |

Unknown fields are ignored, and omitted metrics are displayed as unavailable.
Boolean values, strings, NaN/infinity, and invalid endpoint counts are rejected
rather than silently included in the comparison.

## Example

Create `baseline.json`:

```json
{
  "wns_ns": -0.18,
  "tns_ns": -3.40,
  "hold_wns_ns": 0.02,
  "violating_endpoints": 14
}
```

Create `candidate.json` with metrics from the same design and comparable run
conditions, then execute:

```bash
python scripts/compare_timing_metrics.py baseline.json candidate.json
```

The report prints baseline, candidate and candidate-minus-baseline deltas.
Preserve the source reports and run configuration alongside the JSON files so
the numbers can be traced back to their origin.

## Important limitations

- This utility compares values supplied by the user; it does not parse STA
  reports, validate SDC constraints, or prove that the metrics are correct.
- Compare like-for-like runs: same design, libraries, corners, modes and
  relevant tool settings. Do not combine metrics from different corners without
  labelling them clearly.
- A better setup WNS alone does not prove timing closure. Review TNS, hold,
  transition/capacitance/fanout violations, all required corners and physical
  verification before considering signoff.
- Treat this report as a lightweight comparison aid, not a signoff certificate.
