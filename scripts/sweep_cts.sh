#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/cts_experiment_results.csv"
echo "Run,CTS_Buffers,WNS,TNS,WHS,THS,Skew_ps,Latency_ns,BufCount,Area_mm2" > "$RESULTS_FILE"
./flow.tcl -design riscv32 -tag cts_standard -overwrite
./flow.tcl -design riscv32 -tag cts_high_drive -overwrite
cat "$RESULTS_FILE"
