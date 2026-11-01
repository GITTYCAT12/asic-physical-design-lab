# RTL-to-GDSII Stage Review Gates

A stage-by-stage review for digital implementation. Exact commands and report names vary by tool and platform.

## 1. RTL and constraints
Review top module, parameters, clock/reset intent, synthesis constraints, and lint or simulation results.
**Gate:** the intended design elaborates and constraints represent the intended interface and clocking.

## 2. Synthesis
Review inferred memories and latches, cell statistics, warnings, unmapped logic, and timing estimates.
**Gate:** no unexplained latch inference or unresolved synthesis warning; confirm the mapped netlist matches design intent.

## 3. Floorplan and power planning
Review die/core dimensions, utilization, aspect ratio, pin placement, macro placement, and power-grid connectivity.
**Gate:** floorplan is feasible and power structures are connected according to the platform methodology.

## 4. Placement
Review placement legality, congestion estimates, high-fanout nets, density, and timing changes.
**Gate:** no unexpected placement violations; investigate congestion and critical paths before proceeding.

## 5. Clock-tree synthesis
Review clock-tree topology, insertion delay, skew, transition, and clock-cell count.
**Gate:** clock network meets the design's checks and new setup/hold violations are understood.

## 6. Routing
Review global-route congestion, detailed-route completion, DRC markers, antenna checks, and parasitic extraction status.
**Gate:** routing completes and remaining violations are classified; a successful tool exit alone is not signoff.

## 7. Extraction and timing
Review extracted parasitics, setup/hold reports, unconstrained paths, slew/capacitance violations, and required corners.
**Gate:** timing uses the intended extracted parasitics and signoff constraints.

## 8. Physical verification and handoff
Review DRC/LVS results where supported, final database consistency, GDS/OASIS generation, and handoff artifacts.
**Gate:** archive the final database, reports, constraints, tool configuration, and verification status.

## Experiment log template

| Field | Value |
|---|---|
| Design / revision | |
| PDK / standard-cell library | |
| Tool versions | |
| Clock target and constraints | |
| Floorplan utilization / aspect ratio | |
| Setup WNS / TNS | |
| Hold WNS / violating endpoints | |
| DRC / LVS status | |
| Key issue and next action | |

Never report a stage as passed solely because a command completed. Attach the relevant report and state the scope of checks performed.
