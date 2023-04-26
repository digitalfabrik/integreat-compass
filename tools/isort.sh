#!/bin/bash

# This script can be used to sort the python import statements with isort.

# Import utility functions
# shellcheck source=./tools/utils/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/utils/_functions.sh"

require_installed

# Run isort
echo "Sorting import statements with isort..." | print_info
isort .
echo "✔ Sorting finished" | print_success
