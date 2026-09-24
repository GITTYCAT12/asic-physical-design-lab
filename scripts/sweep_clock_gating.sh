#!/bin/bash
set -e
RESULTS_FILE="designs/riscv32/runs/clock_gating_results.csv"
echo "Run,ClockGating,TotalPower_mW,SeqPower_mW,TotalCells,WNS,DRC" > "$RESULTS_FILE"
for GATING in 0 1; do
  if [ "$GATING" = "0" ]; then TAG="day13_ungated"; else TAG="day13_gated"; fi
  cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 8.0,
  "FP_CORE_UTIL": 55,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": 0.60,
  "SYNTH_CLOCK_GATING": $GATING,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
  ./flow.tcl -design riscv32 -tag "$TAG" -overwrite
done
cat "$RESULTS_FILE"
