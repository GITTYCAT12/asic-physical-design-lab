#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/timing_marathon_results.csv"
echo "Run,TargetFreq_MHz,Period_ns,Setup_WNS_ns,Setup_TNS_ns,Hold_WHS_ns,DRC,Area_mm2,Cells" > "$RESULTS_FILE"
for SPEC in "day18_140mhz 7.14 52 0.58" "day18_150mhz 6.66 50 0.55"; do
  set -- $SPEC
  TAG=$1; PERIOD=$2; UTIL=$3; DENSITY=$4
  cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": $PERIOD,
  "FP_CORE_UTIL": $UTIL,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": $DENSITY,
  "SYNTH_STRATEGY": "DELAY 0",
  "GRT_REPAIR_ANTENNAS": 1,
  "DIODE_ON_PORTS": "in",
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0
}
EOF
  ./flow.tcl -design riscv32 -tag "$TAG" -overwrite
done
cat "$RESULTS_FILE"
