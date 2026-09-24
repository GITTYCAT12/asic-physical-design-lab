#!/bin/bash
set -e
UTIL_VALUES="50 55 60 65 70 75"
RESULTS_FILE="designs/riscv32/runs/utilization_sweep_results.csv"
echo "Run,Util,WNS,TNS,WHS,THS,DRC,Area_mm2,CellCount" > "$RESULTS_FILE"
for UTIL in $UTIL_VALUES; do
  TAG="util_$UTIL"
  DENSITY=$(python3 -c "print(f'{($UTIL + 5)/100:.2f}')")
  cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 20.0,
  "FP_CORE_UTIL": $UTIL,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": $DENSITY,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
  ./flow.tcl -design riscv32 -tag "$TAG" -overwrite
done
cat "$RESULTS_FILE"
