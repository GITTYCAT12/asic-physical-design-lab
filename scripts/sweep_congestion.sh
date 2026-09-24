#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/congestion_pad_results.csv"
echo "Run,CellPad,WNS,TNS,DRC,Area_mm2" > "$RESULTS_FILE"
cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 20.0,
  "FP_CORE_UTIL": 55,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": 0.60,
  "CELL_PAD": 4,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
./flow.tcl -design riscv32 -tag pad_4sites -overwrite
cat "$RESULTS_FILE"
