#################################################################################
# GLOBALS
#################################################################################

VENV_NAME="venv"
VENV_DIR="./${VENV_NAME}"
VENV_BIN="${VENV_DIR}/bin/activate" # ./ is optional at front

REQUIREMENTS_DEV_TXT="requirements/requirements_dev.txt"
REQUIREMENTS_PROD_TXT="requirements/requirements.txt"
REQUIREMENTS_PROD_HASH="requirements/requirements.hash"
REQUIREMENTS_DEV_HASH="requirements/requirements_dev.hash"

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
		--pip-args "--require-hashes" \
		${REQUIREMENTS_DEV_HASH} ${REQUIREMENTS_PROD_HASH} && \
	echo "Done!"

day1:
	@python -um day-1.tasks;

day1-test:
	@python -um day-1.tasks test;

day1-sample:
	@python -um day-1.tasks;
