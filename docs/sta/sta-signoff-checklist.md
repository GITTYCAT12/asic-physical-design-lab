# Static Timing Analysis Signoff Checklist

Use this checklist when reviewing timing results. A clean summary is useful only when constraints, corners, and reports are trustworthy.

## Validate inputs
- [ ] Confirm the intended netlist and matching Liberty and technology files.
- [ ] Check clock period, waveform, uncertainty, latency, and transition assumptions in the SDC.
- [ ] Check input/output delays, input transitions, and output loads.
- [ ] Confirm generated clocks and clock relationships.
- [ ] Review false paths and multicycle paths; each exception needs a design-based reason.
- [ ] Confirm the intended PVT and RC corners.

## Setup timing
- [ ] Record worst negative slack (WNS) and total negative slack (TNS).
- [ ] Inspect the worst paths, including startpoint, endpoint, launch/capture clocks, data delay, and required time.
- [ ] Identify whether cell delay, net delay, fanout, slew, or capacitance dominates.
- [ ] Check unconstrained endpoints and unexpected path groups.

Setup slack is commonly reported as required time minus arrival time. Negative slack indicates a setup violation under the active constraints.

## Hold timing
- [ ] Record worst hold slack and violating endpoint count.
- [ ] Inspect minimum-delay paths and clock skew.
- [ ] Check whether setup repair introduced a hold regression.
- [ ] Re-run both setup and hold analysis after every ECO.

Do not assume improving setup automatically improves hold. The two checks use different timing relationships.

## After an ECO
- [ ] Save baseline metrics before changing the netlist.
- [ ] Make controlled changes and record the rationale.
- [ ] Re-run timing with the same constraints and corners.
- [ ] Compare WNS, TNS, hold slack, transition, capacitance, and fanout.
- [ ] Check for new violations elsewhere.
- [ ] Archive ECO commands, reports, tool versions, and a before/after table.

## Signoff evidence
Record netlist and SDC revisions, libraries and corners, tool version, and report commands. A result is reproducible only when its inputs and procedure are identifiable.

This checklist is a learning aid, not a substitute for a project-specific signoff methodology.
