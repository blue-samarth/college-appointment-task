#!/usr/bin/env bash

set -eo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BASE_DIR="."
LINT_FILE="lint_check.txt"

# Create array of paths to lint
FILES_TO_LINT=(
    "$BASE_DIR/app.py"
    "$BASE_DIR/src/api"
    "$BASE_DIR/src/models"
    "$BASE_DIR/src/utils"
    "$BASE_DIR/src/config.py"
    "$BASE_DIR/src/__init__.py"
    "$BASE_DIR/tests"
)

# Function to log messages with timestamp and color
log() {
    local msg=$1
    local color=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${color}[${timestamp}] ${msg}${NC}"
    echo "[${timestamp}] ${msg}" >> "$LINT_FILE"
}

# Check for pylint installation
verify_pylint() {
    if ! command -v pylint &> /dev/null; then
        log "Error: pylint is not installed. Please install it first." "$RED"
        exit 1
    fi
}

# Initialize lint report
setup_report() {
    echo "Lint Check Report - $(date '+%Y-%m-%d %H:%M:%S')" > "$LINT_FILE"
    echo "=============================" >> "$LINT_FILE"
}

# Main linting function
run_lint() {
    local path=$1
    if [ -e "$path" ]; then
        log "Linting: ${path}" "$CYAN"
        if [ -d "$path" ]; then
            pylint -r y "$path" >> "$LINT_FILE" 2>&1 || true
        else
            pylint "$path" >> "$LINT_FILE" 2>&1 || true
        fi
    else
        log "Path not found: ${path}" "$YELLOW"
    fi
}

# Main execution
main() {
    verify_pylint
    setup_report
    
    log "Starting linting process..." "$GREEN"
    log "Saving report to: ${LINT_FILE}" "$CYAN"
    
    for path in "${FILES_TO_LINT[@]}"; do
        run_lint "$path"
    done
    
    log "Linting process completed successfully!" "$GREEN"
    log "Total report size: $(wc -l < "$LINT_FILE") lines" "$CYAN"
}

# Run main function
main
