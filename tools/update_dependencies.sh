#!/bin/bash

# This script checks if all dependencies in the lock files are up to date and increments the version numbers if necessary.

# Import utility functions
# shellcheck source=./tools/utils/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/utils/_functions.sh"

# Format a line according to pyproject.toml including indentation, quotes and comma
# E.g. "Django==4.1.7" is converted to "    "\Django==4.1.7\","
function format_pyproject_toml {
    while IFS= read -r line; do
        echo "${line}" | sed --regexp-extended 's/^(.*)$/    "\1",\\n/g' | tr -d '\n'
    done
}

function update_npm_dependencies {
    # Check if npm dependencies are up to date
    echo "Updating JavaScript dependencies..." | print_info
    npm update --save

    # Fix npm security issues (skip all breaking changes)
    echo "Running security audit of JavaScript dependencies..." | print_info
    npm audit fix || true
}

function update_pip_dependencies {
    # Update pip dependencies
    echo "Updating Python dependencies..." | print_info
    # Create temporary venv to make sure dev dependencies are not included initially
    python3 -m venv .venv.tmp
    source .venv.tmp/bin/activate
    # Install package locally (without the pinned extra, so the newest available versions are installed)
    pip install -e .
    # Parse the newly installed versions
    PINNED_VERSIONS=$(pip freeze --exclude-editable --local | sort)
    PINNED_VERSIONS_TOML=$(echo "${PINNED_VERSIONS}" | format_pyproject_toml)
    # Now also install dev dependencies
    pip install -e .[dev]
    # Parse the newly installed versions
    PINNED_VERSIONS_ALL=$(pip freeze --exclude-editable --local | sort)
    # Only consider packages that were not already pinned in the normal dependencies
    PINNED_DEV_VERSIONS=$(comm -3 <(echo "${PINNED_VERSIONS_ALL}") <(echo "${PINNED_VERSIONS}"))
    PINNED_DEV_VERSIONS_TOML=$(echo "${PINNED_DEV_VERSIONS}" | format_pyproject_toml)
    # Write the new versions to pyproject.toml
    sed --in-place --regexp-extended \
        --expression "/^pinned = \[$/,/^\]$/c\pinned = [\n${PINNED_VERSIONS_TOML}]" \
        --expression "/^dev-pinned = \[$/,/^\]$/c\dev-pinned = [\n${PINNED_DEV_VERSIONS_TOML}]" \
        pyproject.toml
    # Remove the temporary venv
    deactivate
    rm -rf .venv.tmp

    # Install updated versions in the real venv
    if [[ -d ".venv" ]]; then
        # shellcheck disable=SC2102
        pip install -e .[dev-pinned,pinned]
    else
        bash "${DEV_TOOL_DIR}/install.sh"
    fi
    echo "✔ Updated pyproject.toml and installed the new versions" | print_success
}

function update_pre_commit_hooks {
    echo "Updating pre-commit hooks..." | print_info
    echo "Note: Please downgrade any alpha versions manually" | print_warning
    pre-commit autoupdate
}

function only_once_warning {
    echo "The --only flag can only be passed once" | print_error
    exit 1
}

require_installed
ensure_not_root

# Parse given command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --only) [ -n "${ONLY}" ] && only_once_warning || ONLY="$2"; shift 2;;
        --only=*) [ -n "${ONLY}" ] && only_once_warning || ONLY="${1#*=}"; shift 1;;
        *) echo "Unknown option: $1" | print_error; exit 1;;
    esac
done

if [[ -n "${ONLY}" ]] && [[ "${ONLY}" != @(npm|pip|pre-commit) ]]; then
    echo "The value ${ONLY} is not supported for the --only flag." | print_error
    exit 1
fi

if [[ -z "${ONLY}" ]] || [[ "${ONLY}" == "npm" ]]; then
    update_npm_dependencies
fi

if [[ -z "${ONLY}" ]] || [[ "${ONLY}" == "pip" ]]; then
    update_pip_dependencies
fi

if [[ -z "${ONLY}" ]] || [[ "${ONLY}" == "pre-commit" ]]; then
    update_pre_commit_hooks
fi
