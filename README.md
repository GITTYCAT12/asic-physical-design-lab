# ASIC Physical Design Lab

A hands-on **ASIC physical design and RTL-to-GDSII laboratory** built around a PicoRV32 RISC-V processor and the open-source SKY130 digital ASIC ecosystem.

The objective is to study the backend implementation process through **measured experiments, timing analysis, ECO work and physical signoff**, rather than treating RTL-to-GDSII as a single push-button flow.

## Project Overview

| Item | Details |
|---|---|
| Design | PicoRV32 RISC-V CPU |
| Target | SkyWater SKY130 |
| Flow | RTL → Synthesis → Floorplan → Placement → CTS → Routing → STA → Physical Verification |
| Main flow | OpenLane / OpenROAD ecosystem |
| Analysis | OpenSTA |
| Synthesis | Yosys |
| Verification | Magic, Netgen, KLayout |
| Automation | Bash, Tcl, Python |

## RTL-to-GDSII Flow

```text
RTL / PicoRV32
      │
      ▼
  Synthesis
    Yosys
      │
      ▼
  Floorplan
      │
      ▼
  Placement
      │
      ▼
     CTS
      │
      ▼
   Routing
      │
      ▼
    STA
 setup / hold
      │
      ├──────────────► Timing ECO / Optimization
      │                         │
      └─────────────────────────┘
      │
      ▼
 DRC / LVS / XOR / Antenna
      │
      ▼
    GDSII
```

## What This Lab Covers

### Synthesis
- Verilog RTL synthesis
- Technology mapping
- Cell-count and area analysis
- Area-versus-timing synthesis exploration

### Floorplanning
- Core utilization sweeps
- Aspect-ratio sweeps
- Die/core area exploration
- Placement density
- Macro-placement configuration
- PDN configuration

### Placement
- Timing-driven placement experiments
- Utilization exploration
- Congestion-oriented experiments
- Cell-padding experiments
- HPWL and routing-resource analysis

### Clock Tree Synthesis
- CTS configuration
- Clock-buffer experiments
- Clock latency
- Clock skew
- Setup/hold impact of clock-tree implementation

### Static Timing Analysis
The project records:
- Setup WNS/TNS
- Hold WHS/THS
- Critical-path delay
- Clock period/frequency
- Timing-path information
- Post-ECO timing

### Timing Closure / ECO
The repository contains scripts for:
- Parsing timing reports
- Detecting negative-slack paths
- Generating hold-ECO commands
- Buffer insertion experiments
- Post-ECO timing validation

Typical reasoning:

```text
Timing violation
      ↓
Find critical path
      ↓
Analyze cell/net delay
      ↓
Choose ECO strategy
      ↓
Apply optimization
      ↓
Re-run STA
      ↓
Compare before / after
```

### Physical Verification
Collected evidence includes:
- DRC
- LVS
- XOR comparison
- Antenna checks
- Routing violations
- Signoff metrics

## Experiments

| Script | Experiment |
|---|---|
| `sweep_util.sh` | Core-utilization sweep |
| `sweep_ar.sh` | Floorplan aspect-ratio sweep |
| `sweep_placement.sh` | Placement-mode comparison |
| `sweep_congestion.sh` | Cell-padding / congestion experiment |
| `sweep_cts.sh` | CTS experiment |
| `run_sta_experiments.sh` | STA deep-dive run |
| `run_timing_marathon.sh` | Timing/frequency exploration |
| `sweep_clock_gating.sh` | Clock-gating experiment |
| `sweep_antenna.sh` | Antenna-repair experiment |
| `generate_hold_eco.py` | Generate hold-ECO commands |
| `parse_timing_paths.py` | Parse STA timing paths |
| `verify_tapeout_signoff.py` | Summarize signoff metrics |

## Repository Structure

```text
asic-physical-design-lab/
│
├── rtl/
│   └── picorv32.v
│
├── configs/
│   └── config.json
│
├── designs/
│   └── riscv32/
│       └── config.json
│
├── constraints/
│   └── clocks.sdc
│
├── scripts/
│   ├── fix_hold_eco.tcl
│   ├── generate_hold_eco.py
│   ├── macro_placement.cfg
│   ├── parse_timing_paths.py
│   ├── run_sta_experiments.sh
│   ├── run_timing_marathon.sh
│   ├── sweep_antenna.sh
│   ├── sweep_ar.sh
│   ├── sweep_clock_gating.sh
│   ├── sweep_congestion.sh
│   ├── sweep_cts.sh
│   ├── sweep_placement.sh
│   ├── sweep_util.sh
│   └── verify_tapeout_signoff.py
│
├── results/
│   ├── *_results.csv
│   ├── reports_day1_baseline/
│   ├── reports_day6_eco/
│   └── reports_day7_multicorner/
│
├── .gitignore
└── README.md
```

Large generated run directories and complete PDK/tool installations are intentionally excluded. Curated reports and measured results are retained.

# Open-Source Tools & References

## OpenLane — RTL-to-GDSII Flow

[OpenLane — GitHub](https://github.com/The-OpenROAD-Project/OpenLane)

Used as the flow infrastructure for automating the RTL-to-GDSII implementation process and coordinating the underlying synthesis, physical-design and verification tools.

**Note:** The OpenLane repository currently recommends LibreLane for new projects. This laboratory remains based on the OpenLane flow because these experiments were developed around that environment.

## OpenROAD — Physical Design

[OpenROAD — GitHub](https://github.com/The-OpenROAD-Project/OpenROAD)

Used for the main backend implementation stages:
- Floorplanning
- Placement
- Clock-tree synthesis
- Routing
- Physical optimization
- Database manipulation

## OpenSTA — Static Timing Analysis

[OpenSTA — GitHub](https://github.com/The-OpenROAD-Project/OpenSTA)

Used for:
- Setup analysis
- Hold analysis
- WNS/TNS
- Timing-path analysis
- Clock constraints
- Post-ECO timing validation

## Yosys — RTL Synthesis

[Yosys — GitHub](https://github.com/YosysHQ/yosys)

Used for RTL synthesis and technology mapping before physical implementation.

## Magic — Layout / DRC

[Magic VLSI — GitHub](https://github.com/RTimothyEdwards/magic)

Used in the physical-verification flow for layout processing, extraction and DRC.

## Netgen — LVS

[Netgen — GitHub](https://github.com/RTimothyEdwards/netgen)

Used for Layout Versus Netlist comparison during signoff.

## KLayout — Layout Verification

[KLayout — GitHub](https://github.com/KLayout/klayout)

Used within the verification ecosystem for layout inspection and rule-based checks.

## SkyWater SKY130 PDK

[SkyWater SKY130 PDK — GitHub](https://github.com/google/skywater-pdk)

The target open-source process design kit for the laboratory, providing SKY130 technology data and standard-cell resources.

## PicoRV32 — RTL Design

[PicoRV32 — GitHub](https://github.com/YosysHQ/picorv32)

The open-source RISC-V processor core used as the RTL design under test.

## Metrics Tracked

| Category | Metrics |
|---|---|
| Timing | WNS, TNS, WHS, THS, critical-path delay |
| Clock | Skew, latency, CTS buffer count |
| Area | Die area, core area, cell count, utilization |
| Routing | Wire length, vias, congestion, routing violations |
| Power | Internal, switching, leakage power |
| Verification | DRC, LVS, XOR, antenna |
| ECO | Before/after timing and signoff metrics |

## Signoff Evidence

The `results/` directory contains curated artifacts from multiple implementation stages, including:
- Baseline implementation metrics
- ECO metrics
- Multi-corner STA summaries
- Power reports
- DRC results
- LVS results
- XOR results
- Timing/frequency experiments
- Floorplan and utilization sweeps

The repository deliberately stores **selected evidence instead of entire generated EDA run directories**.

## Reproducibility

A properly configured Linux/Ubuntu environment with the required open-source tools and SKY130 PDK is required.

Typical workflow:

```text
1. Prepare RTL
2. Define clocks and I/O constraints
3. Configure SKY130 / OpenLane
4. Synthesize
5. Floorplan
6. Place
7. CTS
8. Route
9. Run STA
10. Identify violations
11. Apply ECO / optimization
12. Re-run STA
13. Run DRC / LVS / XOR
14. Record final metrics
```

For the repository's reproducibility rules, experiment hygiene, and guidance on the current captured evidence, see [`docs/reproducibility.md`](docs/reproducibility.md).

## Engineering Questions Explored

This lab is organized around practical backend questions:

- How does utilization affect congestion?
- How does aspect ratio affect routing and timing?
- What changes after CTS?
- How do skew and clock latency affect setup and hold?
- Which timing paths should receive an ECO?
- What are the timing/area/routing trade-offs of an optimization?
- How are DRC, LVS and XOR results interpreted?
- What evidence is required before considering an implementation signoff-ready?

## Attribution

This repository contains original experiment configurations, automation scripts, analysis and curated results alongside third-party open-source components.

Third-party components remain subject to their respective licenses. Refer to the upstream repositories above for their authoritative source code, licenses and documentation.
