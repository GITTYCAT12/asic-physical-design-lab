# Timing ECO Review Record

Use one copy of this record for each setup- or hold-timing ECO. Keep the pre-change report so the result can be reproduced and reviewed.

## Change identification

- **Experiment ID:**
- **Date / tool version:**
- **Design and implementation stage:**
- **Baseline report path or commit:**
- **Candidate report path:**

## Violation diagnosis

- **Violation type:** setup / hold / other
- **Startpoint:**
- **Endpoint:**
- **Slack before change (ns):**
- **Dominant contributor:** cell delay / net delay / fanout / transition / capacitance / congestion / clock path
- **Evidence from report:**

## ECO proposal

- **Proposed action:** buffer / resize / placement change / route change / other
- **Target instance or net:**
- **Expected benefit:**
- **Expected side effects:**
- **Why this is the smallest reasonable change:**

## Before-and-after comparison

| Metric | Before | After | Pass condition |
|---|---:|---:|---|
| Setup WNS (ns) | | | Meets project constraint |
| Setup TNS (ns) | | | No unresolved setup debt |
| Hold WHS (ns) | | | Meets project constraint |
| Hold THS (ns) | | | No unresolved hold debt |
| Cell area | | | Within area budget |
| Signal-metal / wire metric | | | No unacceptable routing cost |
| DRC violations | | | 0 required for signoff |
| Antenna violations | | | 0 required for signoff |
| LVS errors | | | 0 required for signoff |

## Decision

- [ ] Accept — timing improves and no signoff gate regresses.
- [ ] Reject — the change introduces a regression or fails constraints.
- [ ] Investigate — evidence is incomplete or the cause is unclear.

**Decision rationale:**

**Follow-up action:**

> Do not claim an ECO is successful from setup WNS alone. Re-check hold timing, physical verification, and relevant area/routing constraints after the change.
