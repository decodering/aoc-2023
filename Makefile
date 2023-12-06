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

day5:
	@source ${VENV_BIN} && \
		python -um src.main 5 --debug;

day6:
	@source ${VENV_BIN} && \
		python -um src.main 6;
