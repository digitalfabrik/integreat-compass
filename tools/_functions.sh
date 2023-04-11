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

# This function sets the correct environment variables for the local Redis cache
function configure_redis_cache {
    # Check if local Redis server is running
    echo "Checking if local Redis server is running..." | print_info
    if nc -z localhost 6379; then
        # Enable redis cache if redis server is running
        export INTEGREAT_COMPASS_REDIS_CACHE=1
        # Check if enhanced connection via unix socket is available (write the location into $REDIS_SOCKET_LOCATION)
        if [[ -f "$REDIS_SOCKET_LOCATION" ]]; then
            # Set location of redis unix socket
            INTEGREAT_COMPASS_REDIS_UNIX_SOCKET=$(cat "$REDIS_SOCKET_LOCATION")
            export INTEGREAT_COMPASS_REDIS_UNIX_SOCKET
            echo "✔ Running Redis server on socket $INTEGREAT_COMPASS_REDIS_UNIX_SOCKET detected. Caching enabled." | print_success
        else
            echo "✔ Running Redis server on port 6379 detected. Caching enabled." | print_success
        fi
    else
        echo "❌No Redis server detected. Falling back to local-memory cache." | print_warning
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
        deescalate_privileges pipenv run integreat-compass-cli makemigrations --verbosity "${SCRIPT_VERBOSITY}"
        # Execute migrations
        deescalate_privileges pipenv run integreat-compass-cli migrate --verbosity "${SCRIPT_VERBOSITY}"
        echo "✔ Finished database migrations" | print_success
        DATABASE_MIGRATED=1
    fi
}


# This function checks if the integreat compass is installed
function require_installed {
    if [[ -z "$INTEGREAT_COMPASS_INSTALLED" ]]; then
        echo "Checking if integreat compass is installed..." | print_info
        # Check if script was invoked with sudo
        if [[ $(id -u) == 0 ]] && [[ -n "$SUDO_USER" ]]; then
            # overwrite $HOME directory in case script was called with sudo but without the -E flag
            HOME="$(bash -c "cd ~${SUDO_USER} && pwd")"
        fi
        # Check if pipenv is installed
        if [[ ! -x "$(command -v pipenv)" ]]; then
            # Check if pipenv is installed in the pip user directory
            if [[ -x $HOME/.local/bin/pipenv ]]; then
                # Enable the execution of a user-installed pipenv by adding the user's pip directory to the $PATH variable
                PATH="${PATH}:${HOME}/.local/bin"
            else
                echo "Pipenv for Python3 is not installed. Please install it manually (e.g. with 'pip3 install pipenv --user') and run this script again."  | print_error
                exit 1
            fi
        fi
        # Check if integreat-compass-cli is available in virtual environment
        if [[ ! -x "$(env pipenv run bash -c "command -v integreat-compass-cli")" ]]; then
            echo -e "The integreat compass is not installed. Please install it with:\n"  | print_error
            echo -e "\t$(dirname "${BASH_SOURCE[0]}")/install.sh\n" | print_bold
            exit 1
        fi
        echo "✔ integreat compass is installed" | print_success
        INTEGREAT_COMPASS_INSTALLED=1
        export INTEGREAT_COMPASS_INSTALLED
        # Check if script is running in CircleCI context and set DEBUG=True if not
        if [[ -z "$CIRCLECI" ]]; then
            # Set debug mode for
            INTEGREAT_COMPASS_DEBUG=1
            export INTEGREAT_COMPASS_DEBUG
            # Set dummy FCM key to test functionality
            if [[ -z "${INTEGREAT_COMPASS_FCM_KEY}" ]]; then
                INTEGREAT_COMPASS_FCM_KEY="dummy"
                export INTEGREAT_COMPASS_FCM_KEY
            fi
        fi
    fi
}

# This function makes sure the script has the permission to interact with the docker daemon
function ensure_docker_permission {
    ERROR_MSG="Please start either a local PostgreSQL database server or start the docker daemon so a database docker container can be created."
    # Check if script runs as root
    if [[ $(id -u) == 0 ]]; then
        # Make sure it was invoked with sudo
        if [[ -z "$SUDO_USER" ]]; then
            echo "Please do not run ${SCRIPT_NAME} as root user, use sudo instead." | print_error
            exit 1
        fi
        # Check if docker socket is also available with lower permissions
        if sudo -u "$SUDO_USER" docker ps &> /dev/null; then
            # If command is available to the unprivileged user, ensure we don't run with higher privileges than necessary
            ensure_not_root
        elif ! docker ps &> /dev/null; then
            # If the command fails for root, we assume the docker daemon isn't running
            echo "${ERROR_MSG}" | print_error
            exit 1
        fi
    else
        # Check if docker socket is not available
        if ! docker ps &> /dev/null; then
            # Check if it's available with sudo
            if sudo docker ps &> /dev/null; then
                # If the command fails normally, but succeeds with sudo, require the permissions from now on
                ensure_root
            else
                # If the command still fails with sudo, we assume the docker daemon isn't running
                echo "${ERROR_MSG}" | print_error
                exit 1
            fi
        fi
    fi
}

# This function makes sure the current script is executed with sudo
function ensure_root {
    # Check if script is not running as root
    if ! [[ $(id -u) == 0 ]]; then
        echo "The script ${SCRIPT_NAME} needs root privileges to connect to the docker daemon. It will automatically be restarted with sudo." | print_warning
        # Call this script again as root (pass -E because we want the user's environment, not root's)
        sudo --preserve-env=HOME,PATH env "${SCRIPT_PATH}" "${SCRIPT_ARGS[@]}"
        # Exit with code of subprocess
        exit $?
    elif [[ -z "$SUDO_USER" ]]; then
        echo "Please do not run ${SCRIPT_NAME} as root user, use sudo instead." | print_error
        exit 1
    fi
}

# This function makes sure the current script is not executed as root
function ensure_not_root {
    # Check if script is running as root
    if [[ $(id -u) == 0 ]]; then
        # Check if script was invoked by the root user or with sudo
        if [[ -z "$SUDO_USER" ]]; then
            echo "Please do not execute ${SCRIPT_NAME} as root user." | print_error
            exit 1
        else
            echo "No need to execute ${SCRIPT_NAME} with sudo. It is automatically restarted with lower privileges." | print_info
            # Call this script again as the user who executed sudo
            deescalate_privileges "${SCRIPT_PATH}" "${SCRIPT_ARGS[@]}"
            # Exit with code of subprocess
            exit $?
        fi
    fi
}

# This function executes the given command with the user who invoked sudo
function deescalate_privileges {
    # Check if command is running as root
    if [[ $(id -u) == 0 ]]; then
        # Check if script was invoked by the root user or with sudo
        if [[ -z "$SUDO_USER" ]]; then
            echo "Please do not execute ${SCRIPT_NAME} as root user." | print_error
            exit 1
        else
            # Call this command again as the user who executed sudo
            sudo -u "$SUDO_USER" -E --preserve-env=PATH env "$@"
        fi
    else
        # If user already has low privileges, just call the given command(s)
        env "$@"
    fi
}

# This function makes sure a postgres database docker container is running
function ensure_docker_container_running {
    # Make sure script has the permission to run docker
    ensure_docker_permission
    # Check if postgres database container is already running
    if [[ $(docker ps -q -f name="${DOCKER_CONTAINER_NAME}") ]]; then
        echo "Database container is already running" | print_info
    else
        # Check if stopped container is available
        if [[ $(docker ps -aq -f status=exited -f name="${DOCKER_CONTAINER_NAME}") ]]; then
            # Start the existing container
            start_docker_container
        else
            # Run new container
            create_docker_container
            # Migrate database
            migrate_database
            # Import test data
            bash "${DEV_TOOL_DIR}/loadtestdata.sh"
        fi
    fi
}
