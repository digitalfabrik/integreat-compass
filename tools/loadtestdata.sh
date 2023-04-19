#!/bin/bash

# This script imports test data into the database.

# Import utility functions
# shellcheck source=./tools/utils/_functions.sh
source "$(dirname "${BASH_SOURCE[0]}")/utils/_functions.sh"

require_installed
require_database

deescalate_privileges integreat-compass-cli loaddata "${PACKAGE_DIR}/cms/fixtures/test_data.json" --verbosity "${SCRIPT_VERBOSITY}"
echo "✔ Imported test data" | print_success