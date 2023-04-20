# shellcheck shell=bash
# Do not execute this file directly, but include it with `source`.

# This function waits for the docker database container
function wait_for_docker_container {
    # Wait until container is ready and accepts database connections
    until docker exec -it "${DOCKER_CONTAINER_NAME}" psql -U integreat -d "${PROJECT_NAME}" -c "select 1" > /dev/null 2>&1; do
        sleep 0.1
    done
}

# This function creates a new postgres database docker container
function create_docker_container {
    echo "Creating new PostgreSQL database docker container..." | print_info
    mkdir -p "${BASE_DIR}/.postgres"
    # Run new container
    docker run -d --name "${DOCKER_CONTAINER_NAME}" -e "POSTGRES_USER=integreat" -e "POSTGRES_PASSWORD=password" -e "POSTGRES_DB=${PROJECT_NAME}" -v "${BASE_DIR}/.postgres:/var/lib/postgresql" -p 5434:5432 postgres > /dev/null
    wait_for_docker_container
    echo "✔ Created database container" | print_success
    # Set up exit trap to stop docker container when script ends
    cleanup_docker_container
}

# This function starts an existing postgres database docker container
function start_docker_container {
    echo "Starting existing PostgreSQL database Docker container..." | print_info
    # Start the existing container
    docker start "${DOCKER_CONTAINER_NAME}" > /dev/null
    wait_for_docker_container
    echo "✔ Started database container" | print_success
    # Set up exit trap to stop docker container when script ends
    cleanup_docker_container
}

# This function stops an existing postgres database docker container
function stop_docker_container {
    # Stop the postgres database docker container if it was not running before
    docker stop "${DOCKER_CONTAINER_NAME}" > /dev/null
    echo -e "\nStopped database container" | print_info
}

# This function initializes a trap to stop the docker container when the script ends
function cleanup_docker_container {
    # The trap command overrides existing traps, so we have to check whether this function as invoked from the run.sh script
    if [[ -n "$KILL_TRAP" ]]; then
        trap "stop_docker_container; kill 0" EXIT
    else
        trap stop_docker_container EXIT
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
