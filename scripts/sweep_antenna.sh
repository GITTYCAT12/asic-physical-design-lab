#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/antenna_experiment_results.csv"
echo "Run,Strategy,Diodes,PinViolations,NetViolations,DRC,Area_mm2" > "$RESULTS_FILE"
./flow.tcl -design riscv32 -tag ant_diodes_only -overwrite
./flow.tcl -design riscv32 -tag ant_layer_hopping -overwrite
cat "$RESULTS_FILE"
