# ASIC Physical Design Lab

Hands-on ASIC physical-design experiments using PicoRV32, SkyWater SKY130 and open-source RTL-to-GDSII tooling.

## Scope
- RTL-to-GDSII implementation
- Floorplanning, placement and utilization experiments
- Clock-tree synthesis and timing analysis
- Timing-closure and hold-ECO experiments
- Congestion, clock-gating and antenna experiments
- DRC/LVS/XOR signoff evidence

## Structure
`rtl/` RTL source · `configs/` flow configuration · `designs/riscv32/` design configuration · `constraints/` timing constraints · `scripts/` automation · `results/` measured results · `docs/` notes.

## Design
PicoRV32 / RV32I targeted to SkyWater SKY130.

The supplied experiment scripts are preserved as project artifacts. Some reference the original local OpenLane/OpenROAD layout such as `designs/riscv32/runs` and `flow.tcl`. Generated run directories, PDKs and complete EDA installations are intentionally excluded.
