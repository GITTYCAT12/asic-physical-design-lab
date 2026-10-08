# Controlled Physical-Design Experiments

The laboratory is intended to show engineering trade-offs, not only final tool output. Each experiment should isolate one implementation variable and preserve enough evidence to explain the result.

## Experiment record

| Field | Purpose |
|---|---|
| Baseline | Fixed reference implementation |
| Variable | Parameter being changed |
| Values | Values or modes tested |
| Metrics | Timing, area, routing, power and verification data |
| Best candidate | Selection criterion |
| Regression | Any metric that became worse |
| Evidence | Report or CSV containing the measurement |

## Isolation rule

Change one major implementation variable at a time whenever practical.

Examples:

- utilization sweep → keep aspect ratio and timing constraints fixed
- aspect-ratio sweep → keep utilization target fixed
- placement experiment → keep floorplan and constraints fixed
- CTS experiment → compare clock-tree settings against the same placed design
- ECO experiment → preserve the pre-ECO metrics as the baseline

If multiple variables must change together, document the reason.

## Metric interpretation

### Timing

Use WNS and TNS together. WNS identifies the worst setup path, while TNS captures the aggregate amount of negative slack.

For hold closure, inspect WHS and THS. A setup improvement that creates a hold regression is not automatically an improvement.

### Physical cost

Review area/utilization, wire length, vias and congestion alongside timing. A faster implementation can still be a poor candidate if it causes excessive physical cost.

### Verification

Treat DRC, LVS, XOR and antenna results as release gates rather than optional metrics.

## Candidate selection

Prefer a candidate that satisfies all required constraints with the smallest unnecessary physical cost.

A simple decision order is:

1. Reject candidates with unresolved verification failures.
2. Reject candidates with required timing violations.
3. Compare area, congestion and power among the remaining candidates.
4. Keep the smallest controlled change that provides the desired improvement.

## Reproducibility

An experiment should be reproducible from:

- the source-controlled configuration,
- the exact script or command,
- the baseline reference,
- the captured result artifact.

Do not replace measured results with manually edited values. If an experiment has not been run, mark its status as "placeholder" in the result manifest.
