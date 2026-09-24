#!/bin/bash
set -e
AR_VALUES="0.5 1.0 1.5 2.0"
RESULTS_FILE="designs/riscv32/runs/ar_sweep_results.csv"
echo "Run,AspectRatio,WNS,TNS,DRC,DieWidth_um,DieHeight_um,Area_mm2" > "$RESULTS_FILE"
for AR in $AR_VALUES; do
  TAG="ar_$AR"
  cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 20.0,
  "FP_CORE_UTIL": 55,
  "FP_ASPECT_RATIO": $AR,
  "PL_TARGET_DENSITY": 0.60,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
  ./flow.tcl -design riscv32 -tag "$TAG" -overwrite
done
cat "$RESULTS_FILE"
