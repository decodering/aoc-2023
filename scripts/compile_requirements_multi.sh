#!/usr/bin/env bash

#TODO: ADD a flag to run with hashes or not!

# TODO: WIP
get_requirements_filename() {
    REQUIREMENTS_DEV=(${REQUIREMENTS_DEV_TXT//// })
}

# Options: [ pip-compile-multi, pip-compile ]
PIP_COMPILE_TOOL="pip-compile-multi"

VENV_DIR="venv/bin/activate"

REQUIREMENTS_IN_DIR="requirements"

REQUIREMENTS_PROD_IN="${REQUIREMENTS_IN_DIR}/requirements.in"
REQUIREMENTS_PROD_TXT="${REQUIREMENTS_IN_DIR}/requirements.txt"
REQUIREMENTS_DEV_IN="${REQUIREMENTS_IN_DIR}/requirements_dev.in"
REQUIREMENTS_DEV_TXT="${REQUIREMENTS_IN_DIR}/requirements_dev.txt"
REQUIREMENTS_PROD_HASH="${REQUIREMENTS_IN_DIR}/requirements.hash"
REQUIREMENTS_DEV_HASH="${REQUIREMENTS_IN_DIR}/requirements_dev.hash"

# TODO: WIP
REQUIREMENTS_TXT_HOST_REGEX="s/.*--trusted-host p-nexus/# &/"
REQUIREMENTS_PROD_TXT_REGEX="s/.*-r requirements/# &/"
REQUIREMENTS_PROD_TXT_REGEX_2="^/\-r requirements\.txt$/s/^/#"

REQUIREMENTS_PROD_HASH_REGEX="^\-r requirements\.hash$"

# Dependencies prone to nexus IQ security errors to always keep latest (within bounds of pinned requirements.in!)
PKGS_TO_UPDATE_LATEST=(
    mlflow
    certifi
    urllib3
    cryptography
)

#TODO: upgrade packages to specific contraints based on pip-audit vuln results (e.g. 'urllib3>=1.3')
PIP_COMPILE_UPGRADE_STRING=""
for PKG in "${PKGS_TO_UPDATE_LATEST[@]}"; do
    SEP=$([[ "$PKG" == "${PKGS_TO_UPDATE_LATEST[0]}" ]] && echo "" || echo " ")
    PIP_COMPILE_UPGRADE_STRING="${PIP_COMPILE_UPGRADE_STRING}${SEP}--upgrade-package ${PKG}"
done

PIP_COMPILE_UPGRADE_STRING_TXT=""
PIP_COMPILE_UPGRADE_STRING_HASH=""
TXT_EXISTS=$(ls -1 ${REQUIREMENTS_IN_DIR}/*.txt 2>/dev/null | wc -l)
HASH_EXISTS=$(ls -1 ${REQUIREMENTS_IN_DIR}/*.hash 2>/dev/null | wc -l)

# Only run --upgrade-package <pkg> if requirements.txt/hash is already compiled
if [[ $TXT_EXISTS -eq 2 ]]; then
    PIP_COMPILE_UPGRADE_STRING_TXT=$PIP_COMPILE_UPGRADE_STRING
fi
if [[ $HASH_EXISTS -eq 2 ]]; then
    PIP_COMPILE_UPGRADE_STRING_HASH=$PIP_COMPILE_UPGRADE_STRING
fi

source $VENV_DIR &&
    pip-compile-multi --live \
        --allow-unsafe \
        --use-cache \
        --backtracking \
        --autoresolve \
        --directory ${REQUIREMENTS_IN_DIR} \
        ${PIP_COMPILE_UPGRADE_STRING_TXT} &&
    pip-compile-multi --live \
        --allow-unsafe \
        --use-cache \
        --backtracking \
        --autoresolve \
        --generate-hashes ${REQUIREMENTS_DEV_IN} \
        --generate-hashes ${REQUIREMENTS_PROD_IN} \
        --out-ext hash \
        --directory ${REQUIREMENTS_IN_DIR} \
        ${PIP_COMPILE_UPGRADE_STRING_HASH} &&
    deactivate

# Remove the -r requirements.txt line from requirements_dev.txt
# Causes error otherwise when running pip install -e .[dev] (pip bug not able to parse '-r requirements' line as literal)
# sed in OSX requires an empty string after -i!! (See: https://unix.stackexchange.com/a/128595)
# https://stackoverflow.com/a/4247319
if [[ "$(uname -s)" == "Darwin" ]]; then
    sed -i \
        '' \
        -e "${REQUIREMENTS_PROD_TXT_REGEX}" \
        -e "${REQUIREMENTS_TXT_HOST_REGEX}" \
        ${REQUIREMENTS_DEV_TXT} && \
    sed -i \
        '' \
        -e "${REQUIREMENTS_PROD_TXT_REGEX}" \
        -e "${REQUIREMENTS_TXT_HOST_REGEX}" \
        ${REQUIREMENTS_PROD_TXT}
elif [[ "$(uname -s)" == "Linux" ]]; then
    sed -i'' \
        -e "${REQUIREMENTS_PROD_TXT_REGEX}" \
        -e "${REQUIREMENTS_TXT_HOST_REGEX}" \
        ${REQUIREMENTS_DEV_TXT} && \
    sed -i'' \
        -e "${REQUIREMENTS_PROD_TXT_REGEX}" \
        -e "${REQUIREMENTS_TXT_HOST_REGEX}" \
        ${REQUIREMENTS_PROD_TXT}
else
    echo -e "Not recognised platform! - $(uname -s)"
    exit 0
fi
