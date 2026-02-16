#!/bin/bash
#
# USA Business Journey - Game Launcher Script
# Usage: ./run_game.sh [options]
#
# Options:
#   --player NAME     Player name
#   --scenario ID     Scenario ID (e.g., SCN002)
#   --difficulty LVL  Difficulty: easy, normal, hard, expert
#   --no-tutorial     Disable tutorial
#   --no-analytics    Disable analytics
#   --help            Show this help
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
PLAYER=""
SCENARIO=""
DIFFICULTY="normal"
NO_TUTORIAL=""
NO_ANALYTICS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --player)
            PLAYER="$2"
            shift 2
            ;;
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --difficulty)
            DIFFICULTY="$2"
            shift 2
            ;;
        --no-tutorial)
            NO_TUTORIAL="--no-tutorial"
            shift
            ;;
        --no-analytics)
            NO_ANALYTICS="--no-analytics"
            shift
            ;;
        --help|-h)
            echo -e "${CYAN}USA Business Journey - Game Launcher${NC}"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --player NAME     Player name"
            echo "  --scenario ID     Scenario ID (e.g., SCN002)"
            echo "  --difficulty LVL  Difficulty: easy, normal, hard, expert"
            echo "  --no-tutorial     Disable tutorial hints"
            echo "  --no-analytics    Disable analytics tracking"
            echo "  --help, -h        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Launch with main menu"
            echo "  $0 --player John --scenario SCN002"
            echo "  $0 --player Jane --scenario SCN001 --difficulty hard"
            echo "  $0 --no-tutorial             # Launch without tutorial"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}Python version: ${PYTHON_VERSION}${NC}"

# Navigate to project directory
cd "$PROJECT_DIR" || exit 1

# Check if processed directory exists with required files
if [ ! -d "processed" ]; then
    echo -e "${YELLOW}Warning: processed directory not found${NC}"
fi

# Check for required data files
REQUIRED_FILES=(
    "processed/action_planner.json"
    "processed/game_mechanics_spec.json"
    "processed/sample_scenarios.json"
    "processed/assessment_system.json"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}Warning: Some data files may be missing:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
fi

# Build command
CMD="python3 src/main.py"

if [ -n "$PLAYER" ]; then
    CMD="$CMD --player \"$PLAYER\""
fi

if [ -n "$SCENARIO" ]; then
    CMD="$CMD --scenario \"$SCENARIO\""
fi

if [ -n "$DIFFICULTY" ]; then
    CMD="$CMD --difficulty $DIFFICULTY"
fi

if [ -n "$NO_TUTORIAL" ]; then
    CMD="$CMD $NO_TUTORIAL"
fi

if [ -n "$NO_ANALYTICS" ]; then
    CMD="$CMD $NO_ANALYTICS"
fi

# Display launch info
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}        ${CYAN}USA BUSINESS JOURNEY${NC} - Launching...            ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ -n "$PLAYER" ]; then
    echo -e "  Player:   ${GREEN}$PLAYER${NC}"
fi

if [ -n "$SCENARIO" ]; then
    echo -e "  Scenario: ${GREEN}$SCENARIO${NC}"
fi

echo -e "  Difficulty: ${GREEN}${DIFFICULTY^}${NC}"

if [ -n "$NO_TUTORIAL" ]; then
    echo -e "  Tutorial: ${YELLOW}Disabled${NC}"
else
    echo -e "  Tutorial: ${GREEN}Enabled${NC}"
fi

echo ""

# Run the game
eval $CMD

# Check exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Game exited successfully${NC}"
else
    echo -e "${RED}Game exited with code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
