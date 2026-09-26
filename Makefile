PYTHON ?= python3
SHELL := /bin/bash

.PHONY: help validate python-check shell-check check parse-timing util-sweep ar-sweep placement-sweep

help:
	@printf '%s\n' \
		'make validate        - validate repository structure and result manifest' \
		'make python-check    - compile Python scripts' \
		'make shell-check     - syntax-check shell experiment scripts' \
		'make check           - run all lightweight repository checks' \
		'make parse-timing REPORT=<path> [LIMIT=10] - parse an OpenSTA report' \
		'make util-sweep      - run the utilization experiment' \
		'make ar-sweep        - run the aspect-ratio experiment' \
		'make placement-sweep - run the placement-mode experiment'

validate:
	$(PYTHON) scripts/validate_repo.py

python-check:
	$(PYTHON) -m compileall -q scripts

shell-check:
	@find scripts -type f -name '*.sh' -print0 | xargs -0 -n1 bash -n

check: validate python-check shell-check

parse-timing:
	@test -n "$(REPORT)" || (echo "Usage: make parse-timing REPORT=<path> [LIMIT=10]" && exit 2)
	$(PYTHON) scripts/parse_timing_paths.py "$(REPORT)" --limit "$(if $(LIMIT),$(LIMIT),10)"

util-sweep:
	bash scripts/sweep_util.sh

ar-sweep:
	bash scripts/sweep_ar.sh

placement-sweep:
	bash scripts/sweep_placement.sh
