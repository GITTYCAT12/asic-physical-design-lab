# ASIC Signoff Readiness Checklist

Use this checklist before describing an implementation as signoff-ready. A passing timing result alone is not sufficient.

## 1. RTL and constraints

- [ ] RTL source is the intended revision.
- [ ] Top module and clock definitions are correct.
- [ ] Input/output delays and clock uncertainty are reviewed.
- [ ] No unintended unconstrained paths remain.
- [ ] Synthesis completes without unexpected warnings that affect functionality.

## 2. Physical implementation

- [ ] Floorplan and utilization are within the intended limits.
- [ ] Placement completes without illegal cells or severe congestion.
- [ ] CTS completes and clock skew/latency are reviewed.
- [ ] Routing completes with no unresolved routing violations.
- [ ] Antenna checks are reviewed.

## 3. Timing

- [ ] Setup WNS >= 0.
- [ ] Setup TNS >= 0.
- [ ] Hold WHS >= 0.
- [ ] Hold THS >= 0.
- [ ] Critical paths have been reviewed rather than relying only on aggregate metrics.
- [ ] Multi-corner analysis is checked where the available flow supports it.
- [ ] ECO changes are compared against a preserved baseline.

## 4. Physical verification

- [ ] DRC reports zero violations.
- [ ] LVS reports zero mismatches/errors.
- [ ] XOR/layout comparison is clean where applicable.
- [ ] Final reports correspond to the same implementation candidate.

## 5. Cost and quality review

- [ ] Area/utilization regression is understood.
- [ ] Routing/congestion regression is understood.
- [ ] Power impact is reviewed when power data is available.
- [ ] No new timing or physical-verification regression was introduced by the final ECO.
- [ ] Report filenames and experiment status are recorded in `results/`.

## Evidence rule

A checklist item should be marked complete only when there is a corresponding report, metric, or reproducible command. If evidence is unavailable, record the item as **not verified** rather than assuming it passed.

## Recommended final sequence

```text
Constraints → Synthesis → Floorplan → Placement → CTS → Routing
      ↓
  STA / ECO → Re-run STA → DRC / LVS / XOR / Antenna
      ↓
  Compare final candidate against baseline
      ↓
  Record evidence and signoff decision
```
