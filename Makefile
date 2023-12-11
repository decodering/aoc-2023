.PHONY: *

#################################################################################
# GLOBALS
#################################################################################

VENV_NAME="venv"
VENV_DIR="./${VENV_NAME}"
VENV_BIN="${VENV_DIR}/bin/activate" # ./ is optional at front

REQUIREMENTS_DEV_TXT="requirements/requirements_dev.txt"
REQUIREMENTS_PROD_TXT="requirements/requirements.txt"

#################################################################################
# MAKE TARGETS (Building, deps mgmt)
#################################################################################

py-setup:
	@python3 -m venv $(VENV_NAME) && \
		source $(VENV_BIN) && \
		pip install --upgrade pip && \
		pip install --upgrade pip-compile-multi

## Compile requirements.txt and requirements_dev.txt
compile_requirements:
	@bash scripts/compile_requirements_multi.sh

## Sync requirements from requirements_dev.txt in local venv
# Ensures the local venv has all its requirements synced (needed ones installed + unneeded ones uninstalled)
sync_requirements:
	@source ${VENV_BIN} && \
	echo "Syncing requirement files (prod and dev)... " && \
	pip-sync --verbose \
		${REQUIREMENTS_DEV_TXT} ${REQUIREMENTS_PROD_TXT} && \
	echo "Done!"

newday:
	@bash scripts/make_new_day_folder.sh $(ARGS)

day1:
	@source ${VENV_BIN} && \
		python -um src.main 1;

day2:
	@source ${VENV_BIN} && \
		python -um src.main 2;

day3:
	@source ${VENV_BIN} && \
		python -um src.main 3 --debug;

day4:
	@source ${VENV_BIN} && \
		python -um src.main 4;

# Note day5.2 may take a while to run / error out. Will need to run directly, e.g. python -um src.main
day5:
	@source ${VENV_BIN} && \
		python -um src.main 5;

day6:
	@source ${VENV_BIN} && \
		python -um src.main 6;

day7:
	@source ${VENV_BIN} && \
		python -um src.main 7;

day8:
	@source ${VENV_BIN} && \
		python -um src.main 8;

day9:
	@source ${VENV_BIN} && \
		python -um src.main 9;

day10:
	@source ${VENV_BIN} && \
		python -um src.main 10 --debug;

day11:
	@source ${VENV_BIN} && \
		python -um src.main 11;

day12:
	@source ${VENV_BIN} && \
		python -um src.main 12 --debug;

day13:
	@source ${VENV_BIN} && \
		python -um src.main 13 --debug;

day14:
	@source ${VENV_BIN} && \
		python -um src.main 14 --debug;

day15:
	@source ${VENV_BIN} && \
		python -um src.main 15 --debug;

day16:
	@source ${VENV_BIN} && \
		python -um src.main 16 --debug;

day17:
	@source ${VENV_BIN} && \
		python -um src.main 17 --debug;

day18:
	@source ${VENV_BIN} && \
		python -um src.main 18 --debug;

day19:
	@source ${VENV_BIN} && \
		python -um src.main 19 --debug;

day20:
	@source ${VENV_BIN} && \
		python -um src.main 20 --debug;

day21:
	@source ${VENV_BIN} && \
		python -um src.main 21 --debug;

day22:
	@source ${VENV_BIN} && \
		python -um src.main 22 --debug;

day23:
	@source ${VENV_BIN} && \
		python -um src.main 23 --debug;

day24:
	@source ${VENV_BIN} && \
		python -um src.main 24 --debug;

day25:
	@source ${VENV_BIN} && \
		python -um src.main 25 --debug;
