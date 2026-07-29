#!/bin/bash

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="${SCRIPT_DIR}/src"
QUESTIONS_FILE="${SRC_DIR}/questions.txt"
WORK_DIR="${SCRIPT_DIR}/work"
RUNNER="${SCRIPT_DIR}/.exam/test_runner.py"

# Ensure the work directory is emptied when this script exits
cleanup_workdir() {
    if [[ -d "${WORK_DIR}" ]]; then
        rm -rf "${WORK_DIR:?}"/* || true
    fi
}

# Run cleanup on normal exit and on common terminating signals
trap 'cleanup_workdir' EXIT INT TERM HUP

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
BOLD='\033[1m'
NC='\033[0m'

banner() {
    local msg="$1"
    local color="${2:-$CYAN}"
    echo -e "${color}${BOLD}"
    printf '%*s\n' "$(( (${#msg} + 80) / 2 ))" "$msg"
    echo -e "${NC}"
}

get_question_text() {
    local num="$1"
    awk -v n="$num" '
        /^====/ {
            if (found && started_content) exit
            if (found) { started_content=1; next }
            next
        }
        $0 ~ "^" n "\\. .*\\.py" { found=1; print; next }
        found { print }
    ' "$QUESTIONS_FILE"
}

file_to_qnum() {
    local fname="$1"
    local num
    num="${fname%%_*}"
    num=$((10#$num))
    echo "$num"
}

main() {
    mkdir -p "$WORK_DIR"

    clear
    banner "🐍 PYTHON EXAM SIMULATOR 🐍" "$MAGENTA"
    echo
    echo -e "You will be given ${BOLD}5 levels${NC} of Python problems."
    echo -e "Write your solution in the file that opens, then press ${BOLD}Enter${NC} to test."
    echo -e "Get it right → advance.  Get it wrong → try again."
    echo
    echo -e "Press ${BOLD}Enter${NC} to begin..."
    read -r

    local total_attempts=0

    for level in 1 2 3 4 5; do
        clear
        banner "LEVEL ${level} / 5" "$YELLOW"

        local level_dir="${SRC_DIR}/${level}"
        if [[ ! -d "$level_dir" ]]; then
            echo -e "${RED}Missing directory: ${level_dir}${NC}"
            exit 1
        fi

        local files=()
        while IFS= read -r -d '' f; do
            files+=("$(basename "$f")")
        done < <(find "$level_dir" -maxdepth 1 -name '*.py' -print0 | sort -zR)

        if [[ ${#files[@]} -eq 0 ]]; then
            echo -e "${RED}No .py files found in ${level_dir}${NC}"
            exit 1
        fi

        local picked="${files[0]}"
        local solution_path="${level_dir}/${picked}"
        local qnum
        qnum=$(file_to_qnum "$picked")

        echo
        echo -e "${CYAN}${BOLD}Question ${qnum}:${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        get_question_text "$qnum"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo

        local work_file="${WORK_DIR}/${picked}"
        local func_name="${picked#*_py_}"
        func_name="${func_name%.py}"

        cat > "$work_file" <<STUBEOF
"""${picked} — your solution.

Implement: ${func_name}
"""

def ${func_name}():
    # TODO: implement this function
    pass
STUBEOF

        echo -e "📝 Write your code in: ${BOLD}${work_file}${NC}"
        echo

        local attempts=0
        while true; do
            attempts=$((attempts + 1))
            total_attempts=$((total_attempts + 1))

            echo -ne "Press ${BOLD}Enter${NC} when ready to test "
            echo -ne "(attempt ${attempts})... "
            read -r

            echo
            echo -e "${YELLOW}Testing...${NC}"
            echo

            if python3 "$RUNNER" "$solution_path" "$work_file" "$WORK_DIR"; then
                echo
                echo -e "${GREEN}${BOLD}✅ Correct!  Moving to next level.${NC}"
                echo
                sleep 2
                break
            else
                echo
                echo -e "${RED}${BOLD}❌ Not quite right.  Fix your code and try again.${NC}"
                echo
                echo -e "Edit ${BOLD}${work_file}${NC} and press Enter to retest."
                echo
            fi
        done
    done

    clear
    banner "🎉 EXAM COMPLETE! 🎉" "$GREEN"
    echo
    echo -e "You completed all 5 levels in ${BOLD}${total_attempts} total attempt(s)${NC}."
    echo
    echo -e "${GREEN}Congratulations — great work!${NC}"
    echo
}

main "$@"
