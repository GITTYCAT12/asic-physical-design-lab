# Physical Design Experiment Log

Copy this template for each floorplan, placement, CTS, routing, or timing-ECO experiment. Keep one file per experiment so results can be compared without losing run context.

## Run identity
- **Experiment ID:**
- **Date:**
- **Design / source revision:**
- **Branch or commit:**
- **Tool and version:**
- **PDK / standard-cell library:**
- **Operating corner(s):**

## Hypothesis
What issue are you investigating? What change do you expect to help, and why?

## Controlled variables
Record clock target, SDC revision, utilization, aspect ratio, placement density, routing settings, and other relevant configuration. Mark settings that differ from baseline.

## Results

| Metric | Baseline | Candidate | Difference | Report / evidence |
|---|---:|---:|---:|---|
| Cell area | | | | |
| Setup WNS (ns) | | | | |
| Setup TNS (ns) | | | | |
| Hold WNS (ns) | | | | |
| Max transition violations | | | | |
| Max capacitance violations | | | | |
| DRC count / status | | | | |
| Runtime | | | | |

Use consistent units and identical constraints when comparing runs. If a metric is unavailable, write N/A and explain why.

## Analysis
1. What changed in the reports?
2. Which paths or physical effects explain the change?
3. Did any metric regress, especially hold, congestion, or DRC?
4. Is the result repeatable?
5. What is the next experiment?

## Decision
- [ ] Keep the change
- [ ] Revert the change
- [ ] Run additional validation

**Conclusion:** State only what the reports demonstrate. Do not claim signoff based on a single metric or partial run.
