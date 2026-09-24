#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/placement_modes_results.csv"
echo "Run,TimingDriven,WNS,TNS,DRC,Area_mm2" > "$RESULTS_FILE"
for MODE in 0 1; do
  if [ "$MODE" = "0" ]; then TAG="place_wl_only"; else TAG="place_timing_driven"; fi
  cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 20.0,
  "FP_CORE_UTIL": 55,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": 0.60,
  "PL_TIME_DRIVEN": $MODE,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
  ./flow.tcl -design riscv32 -tag "$TAG" -overwrite
done
cat "$RESULTS_FILE"
