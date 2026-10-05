# Timing Closure Methodology

This lab treats timing closure as a measured optimization loop rather than a single tool invocation.

## 1. Establish the baseline

Before changing the implementation, capture:

- Clock period and generated clocks
- Setup WNS/TNS
- Hold WHS/THS
- Critical path startpoint and endpoint
- Logic depth and major delay contributors
- Utilization and routing congestion
- Cell count and area
- DRC/LVS/antenna status

The baseline should remain immutable so every optimization can be compared against the same reference.

## 2. Classify the violation

### Setup violation

A negative setup slack means the data path is arriving too late.

Typical investigation order:

1. Identify the worst endpoint.
2. Inspect the launch-to-capture path.
3. Separate cell delay from net delay.
4. Check fanout, transition and capacitance.
5. Check whether congestion is forcing long routes.
6. Choose the smallest ECO or implementation change that addresses the dominant cause.

Common levers include cell upsizing, buffering, placement refinement and route optimization.

### Hold violation

A negative hold slack means the data path is arriving too early.

The fix must not simply improve setup while creating a new hold failure. Typical levers include delay insertion, buffering and local route/placement changes.

The repository's `generate_hold_eco.py` and `fix_hold_eco.tcl` provide a starting point for an explicit hold-ECO loop.

## 3. Re-run STA and compare

Every ECO should produce a before/after record containing at least:

| Metric | Why it matters |
|---|---|
| WNS | Worst setup path |
| TNS | Aggregate setup debt |
| WHS / THS | Hold closure |
| Critical-path delay | Direct path-level impact |
| Area / cell count | Physical cost |
| Wire length / vias | Routing cost |
| DRC / antenna | Physical legality |
| LVS / XOR | Connectivity/layout consistency |

An optimization is useful only when the timing improvement is not hiding a serious physical or power regression.

## 4. Check signoff interactions

Timing closure is coupled to physical verification.

A change that improves WNS can still be rejected if it introduces:

- DRC violations
- Antenna violations
- LVS mismatches
- Excessive congestion
- Unacceptable area or power growth
- New hold violations

Therefore the final decision should be based on the complete metric set, not WNS alone.

## 5. Recommended experiment loop

```text
Baseline
   |
   v
Extract critical paths
   |
   v
Classify setup / hold / physical cause
   |
   v
Choose one controlled change
   |
   v
Run implementation + STA
   |
   v
Compare metrics
   |
   +---- regression ----> revert / investigate
   |
   +---- improvement ---> retain and continue
   |
   v
Run physical verification
   |
   v
Signoff candidate
```

## Repository tooling

- `scripts/parse_timing_paths.py` — extracts startpoint, endpoint and slack from OpenSTA-style reports.
- `scripts/generate_hold_eco.py` — generates hold-ECO commands from timing information.
- `scripts/fix_hold_eco.tcl` — applies the hold-ECO operations in the physical-design environment.
- `scripts/verify_tapeout_signoff.py` — checks curated signoff evidence.
- `results/` — stores selected experiment outputs and metric tables.

The methodology intentionally favors small, explainable changes so that timing, physical cost and verification impact can be attributed to each experiment.