#!/bin/bash

# This script installs Integreat Compass in a local virtual environment

# Import utility functions
# shellcheck source=./tools/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/_functions.sh"

# Parse command line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --clean) CLEAN=1; shift 1;;
    --python) PYTHON="$2"; shift 2;;
    --python=*) PYTHON="${1#*=}"; shift 1;;
    *) echo "Unknown option: $1" | print_error; exit 1;;
  esac
done

if [[ -n "${PYTHON}" ]]; then
    PYTHON=$(command -v "${PYTHON}")
    if [[ ! -x "${PYTHON}" ]]; then
        echo "The given python command '${PYTHON}' is not executable." | print_error
        exit 1
    fi
else
    # Default python binary
    PYTHON="python3"
fi

echo "Checking system requirements..." | print_info

# Check if requirements are satisfied
# Define the required python version
required_python_version="3.9"
if [[ ! -x "$(command -v python3)" ]]; then
    echo "Python3 is not installed. Please install Python ${required_python_version} or higher manually and run this script again."  | print_error
    exit 1
fi
# Get the python version (the format is "Python 3.X.Z")
python_version=$(${PYTHON} --version | cut -d" " -f2)
if [[ $(major "$python_version") -lt $(major "$required_python_version") ]] || \
   [[ $(major "$python_version") -eq $(major "$required_python_version") ]] && [[ $(minor "$python_version") -lt $(minor "$required_python_version") ]]; then
    echo "python version ${required_python_version} is required, but version ${python_version} is installed. Please install a recent version manually and run this script again."  | print_error
    echo -e "If you installed higher python version manually which is not your default python3, please pass the alternative python interpreter (e.g. python3.11) to the script:\n" | print_info
    echo -e "\t$(dirname "${BASH_SOURCE[0]}")/install.sh --python python3.11\n" | print_bold
    exit 1
fi
# Check if pip is installed
if [[ ! -x "$(command -v pip3)" ]]; then
    echo "Pip for Python3 is not installed. Please install python3-pip manually and run this script again."  | print_error
    exit 1
fi
echo "✔ All system requirements are satisfied" | print_success

# Check if the --clean option is given
if [[ -n "${CLEAN}" ]]; then
    echo "Removing installed dependencies and compiled static files..." | print_info
    # Report deleted files but only the explicitly deleted directories
    rm -rf .venv
fi

# Check if virtual environment exists
if [[ -d ".venv" ]] && [[ "$(.venv/bin/python3 --version)" != "$(${PYTHON} --version)" ]]; then
    echo "The given $(${PYTHON} --version) version differs from $(.venv/bin/python3 --version) of virtual environment." | print_warning
    echo "Deleting the outdated virtual environment..." | print_info
    rm -rf .venv
fi

# Check if virtual environment exists
if [[ ! -f ".venv/bin/activate" ]]; then
    echo "Creating virtual environment for $(${PYTHON} --version)..." | print_info
    # Check whether venv creation succeeded
    if ! ${PYTHON} -m venv .venv; then
        # Check whether it would succeed without pip
        if ${PYTHON} -m venv --without-pip .venv &> /dev/null; then
            # Remove "broken" venv without pip
            rm -rf .venv
            # Determine which package needs to be installed
            if [[ "$(${PYTHON} --version)" == "$(python3 --version)" ]]; then
                VENV_PACKAGE="python3-venv"
            else
                MINOR_PYTHON=$(minor "${python_version}")
                VENV_PACKAGE="python3.${MINOR_PYTHON}-venv"
            fi
            echo "Pip is not available inside the virtual environment. Please install ${VENV_PACKAGE} manually and run this script again."  | print_error
            exit 1
        fi
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Install pip dependencies
# shellcheck disable=SC2102
pip install -e .[dev-pinned,pinned]
echo "✔ Installed Python dependencies" | print_success

echo -e "\n✔ The Integreat Compass was successfully installed 😻" | print_success
