#!/bin/bash
set -e
cat > designs/riscv32/config.json << EOF
{
  "DESIGN_NAME": "picorv32",
  "VERILOG_FILES": "dir::src/*.v",
  "CLOCK_PORT": "clk",
  "CLOCK_PERIOD": 8.0,
  "FP_CORE_UTIL": 55,
  "FP_ASPECT_RATIO": 1.0,
  "PL_TARGET_DENSITY": 0.60,
  "RUN_LINTER": 0,
  "QUIT_ON_LINTER_ERRORS": 0,
  "SYNTH_STRATEGY": "AREA 0"
}
EOF
./flow.tcl -design riscv32 -tag sta_deep_dive -overwrite
