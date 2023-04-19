#!/bin/bash

# This script can be used to lint the static files with eslint

# Import utility functions
# shellcheck source=./tools/utils/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/utils/_functions.sh"

# Run prettier
echo "Starting code linting with eslint..." | print_info
npx eslint .
echo "✔ Linting finished" | print_success
