#!/bin/bash

# This file contains utility functions which can be used in the tools.

# shellcheck source=./tools/utils/docker.sh
source "$(dirname "${BASH_SOURCE[0]}")/docker.sh"
# shellcheck source=./tools/utils/logging.sh
source "$(dirname "${BASH_SOURCE[0]}")/logging.sh"
# shellcheck source=./tools/utils/permissions.sh
source "$(dirname "${BASH_SOURCE[0]}")/permissions.sh"

# Do not continue execution if one of the commands fail
set -eo pipefail -o functrace

# Check if the --verbose option is given
if [[ "$*" == *"--verbose"* ]]; then
    # The shell writes a trace for each command to standard error after it expands the command and before it executes it.
    set -vx
fi
# The Port on which the Integreat compass development server should be started (do not use 9000 since this is used for webpack)
INTEGREAT_COMPASS_PORT=8082
# The name of the used database docker container
DOCKER_CONTAINER_NAME="integreat_compass_django_postgres"
PROJECT_NAME="integreat-compass"

# Change to dev tools directory
cd "$(dirname "${BASH_SOURCE[0]}")"
# The absolute path to the dev tools directory
cd ..
DEV_TOOL_DIR=$(pwd)
# Change to base directory
cd ..
# The absolute path to the base directory of the repository
BASE_DIR=$(pwd)
# The path to the package
PACKAGE_DIR_REL="integreat_compass"
PACKAGE_DIR="${BASE_DIR}/${PACKAGE_DIR_REL}"
# The filename of the currently running script
SCRIPT_NAME=$(basename "$0")
# The absolute path to the currently running script (required to allow restarting with different permissions
SCRIPT_PATH="${DEV_TOOL_DIR}/${SCRIPT_NAME}"
# The arguments which were passed to the currently running script
SCRIPT_ARGS=("$@")
# The verbosity of the output (can be one of {0,1,2,3})
SCRIPT_VERBOSITY="1"

# This function shows a success message once the Integreat development server is running
function listen_for_devserver {
    until nc -z localhost "$INTEGREAT_COMPASS_PORT"; do sleep 0.1; done
    echo "✔ Started Integreat Compass at http://localhost:${INTEGREAT_COMPASS_PORT}" | print_success
}

# This function makes sure a database is available
function require_database {
    # Check if local postgres server is running
    if nc -z localhost 5432; then
        ensure_not_root
        echo "✔ Running PostgreSQL database detected" | print_success
        # Migrate database
        migrate_database

        # Set default settings for other dev tools, e.g. testing
        export DJANGO_SETTINGS_MODULE="integreat_compass.core.settings"
    else
        # Set docker settings
        export DJANGO_SETTINGS_MODULE="integreat_compass.core.docker_settings"
        # Make sure a docker container is up and running
        ensure_docker_container_running
    fi
}

# This function migrates the database
function migrate_database {
    # Check for the variable DATABASE_MIGRATED to prevent multiple subsequent migration commands
    if [[ -z "$DATABASE_MIGRATED" ]]; then
        echo "Migrating database..." | print_info
        # Make sure the migrations directory exists
        deescalate_privileges mkdir -pv "${PACKAGE_DIR}/cms/migrations"
        deescalate_privileges touch "${PACKAGE_DIR}/cms/migrations/__init__.py"
        # Generate migration files
        deescalate_privileges integreat-compass-cli makemigrations --verbosity "${SCRIPT_VERBOSITY}"
        # Execute migrations
        deescalate_privileges integreat-compass-cli migrate --verbosity "${SCRIPT_VERBOSITY}"
        echo "✔ Finished database migrations" | print_success
        DATABASE_MIGRATED=1
    fi
}


# This function checks if the integreat compass is installed
function require_installed {
    if [[ -z "$INTEGREAT_COMPASS_INSTALLED" ]]; then
        echo "Checking if Integreat Compass is installed..." | print_info
        # Check if script was invoked with sudo
        if [[ $(id -u) == 0 ]] && [[ -n "$SUDO_USER" ]]; then
            # overwrite $HOME directory in case script was called with sudo but without the -E flag
            HOME="$(bash -c "cd ~${SUDO_USER} && pwd")"
        fi
        # Check if virtual environment exists
        if [[ -f ".venv/bin/activate" ]]; then
            # Activate virtual environment
            # shellcheck disable=SC1091
            source .venv/bin/activate
        else
            echo -e "The virtual environment for this project is missing. Please install it with:\n"  | print_error
            echo -e "\t$(dirname "${BASH_SOURCE[0]}")/install.sh\n" | print_bold
            exit 1
        fi
        # Check if integreat-compass-cli is available in virtual environment
        if [[ ! -x "$(env bash -c "command -v integreat-compass-cli")" ]]; then
            echo -e "The Integreat Compass is not installed. Please install it with:\n"  | print_error
            echo -e "\t$(dirname "${BASH_SOURCE[0]}")/install.sh\n" | print_bold
            exit 1
        fi
        echo "✔ Integreat Compass is installed" | print_success
        INTEGREAT_COMPASS_INSTALLED=1
        export INTEGREAT_COMPASS_INSTALLED
        # Check if script is running in CircleCI context and set DEBUG=True if not
        if [[ -z "$CIRCLECI" ]]; then
            # Set debug mode for
            INTEGREAT_COMPASS_DEBUG=1
            export INTEGREAT_COMPASS_DEBUG
        fi
    fi
}
