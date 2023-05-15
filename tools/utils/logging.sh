# shellcheck shell=bash
# Do not execute this file directly, but include it with `source`.

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
# This function prints the given prefix in the given color in front of the stdin lines. If no color is given, white (37) is used.
# This is useful for commands which run in the background to separate its output from other commands.
function print_prefix {
    while IFS= read -r line; do
        echo -e "\x1b[1;${2:-37};40m[$1]\x1b[0m $line"
    done
}

# This function prints the given input lines with a nice little border to separate it from the rest of the content.
# Pipe your content to this function.
function print_with_borders {
    echo "┌──────────────────────────────────────"
    while IFS= read -r line; do
        echo "│ $line"
    done
    echo -e "└──────────────────────────────────────\n"
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
