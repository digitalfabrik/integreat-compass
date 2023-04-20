# shellcheck shell=bash
# Do not execute this file directly, but include it with `source`.

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
