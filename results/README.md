# Results Guide

The `results/` directory contains curated measurements and signoff evidence from the physical-design experiments.

## Status meanings

| Status | Meaning |
|---|---|
| `captured` | The repository contains numeric output or a report produced by a real run. |
| `placeholder` | The file documents the intended measurement schema but does not contain captured numeric run data. |

Do not use a placeholder CSV as evidence of a completed experiment.

## Evidence groups

### Baseline
`reports_day1_baseline/` contains the baseline OpenLane metrics.

### ECO
`reports_day6_eco/` contains a deliberately retained failed timing/ECO run. Failed runs are useful because they preserve the conditions that produced the violation.

### Multi-corner / signoff
`reports_day7_multicorner/` contains the captured STA summary plus DRC, LVS and XOR reports.

### Parameter sweeps
The top-level CSV files capture selected utilization, aspect-ratio, placement and congestion experiments.

The experiment scripts include additional studies whose output tables are currently empty placeholders. Those experiments remain visible in the repository so their intended measurement interface is clear, but they are not represented as completed results.
