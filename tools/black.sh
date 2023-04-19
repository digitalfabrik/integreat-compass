#!/bin/bash

# This script can be used to format the python code according to the black code style.

# Import utility functions
# shellcheck source=./tools/utils/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/utils/_functions.sh"

require_installed

# Run black
echo "Starting code formatting with black..." | print_info
black .
echo "✔ Code formatting finished" | print_success
