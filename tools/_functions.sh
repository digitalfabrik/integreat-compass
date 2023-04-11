#!/bin/bash

# This file contains utility functions which can be used in the tools.

# Do not continue execution if one of the commands fail
set -eo pipefail -o functrace

# Check if the --verbose option is given
if [[ "$*" == *"--verbose"* ]]; then
    # The shell writes a trace for each command to standard error after it expands the command and before it executes it.
    set -vx
fi

# Change to dev tools directory
cd "$(dirname "${BASH_SOURCE[0]}")"
# The absolute path to the dev tools directory
DEV_TOOL_DIR=$(pwd)
# Change to base directory
cd ..
# The absolute path to the base directory of the repository
BASE_DIR=$(pwd)
# The path to the package
PACKAGE_DIR_REL="INTEGREAT_COMPASS"
PACKAGE_DIR="${BASE_DIR}/${PACKAGE_DIR_REL}"
# The filename of the currently running script
SCRIPT_NAME=$(basename "$0")
# The absolute path to the currently running script (required to allow restarting with different permissions
SCRIPT_PATH="${DEV_TOOL_DIR}/${SCRIPT_NAME}"
# The arguments which were passed to the currently running script
SCRIPT_ARGS=("$@")

# This function prints the given input in bold/normal and the given color code
function format_line {
    local BOLD=$1
    local COLOR=$2
    while IFS= read -r line; do
        echo -e "\x1b[${BOLD};${COLOR}m$line\x1b[0;39m"
    done
}
function print_bold {
    local WHITE="39"
    format_line "1" "${WHITE}"
}
function print_error {
    local RED="31"
    format_line "1" "${RED}" >&2
}
function print_success {
    local GREEN="32"
    format_line "1" "${GREEN}"
}
function print_warning {
    local ORANGE="33"
    format_line "1" "${ORANGE}"
}
function print_info {
    local BLUE="34"
    format_line "1" "${BLUE}"
}

# This function prints the major version of a string in the format XX.YY.ZZ
function major {
    # Split by "." and take the first element for the major version
    echo "$1" | cut -d. -f1
}

# This function prints the minor version of a string in the format XX.YY.ZZ
function minor {
    # Split by "." and take the second element for the minor version
    echo "$1" | cut -d. -f2
}
