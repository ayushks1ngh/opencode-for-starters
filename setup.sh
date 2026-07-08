#!/usr/bin/env bash
set -euo pipefail

REPO="ayushks1ngh/opencode-for-starters"
BRANCH="main"
URL="https://github.com/$REPO.git"
RAW="https://raw.githubusercontent.com/$REPO/$BRANCH"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

usage() {
  echo "Usage:"
  echo "  curl -fsSL $RAW/setup.sh | bash"
  echo "  bash setup.sh [--global | --local]"
  exit 0
}

install_opencode() {
  if command -v opencode &>/dev/null; then
    echo -e "${GREEN}opencode already installed${NC}"
    return
  fi
  echo "Installing opencode..."
  curl -fsSL https://opencode.ai/install | bash
  if ! command -v opencode &>/dev/null; then
    echo "Restart your shell or add opencode to PATH, then re-run this script."
    exit 1
  fi
}

setup_global() {
  local config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
  if [ -d "$config_dir/.git" ]; then
    echo -e "${CYAN}Updating existing global config...${NC}"
    git -C "$config_dir" pull
  else
    echo -e "${CYAN}Installing globally...${NC}"
    mkdir -p "$(dirname "$config_dir")"
    if [ -d "$config_dir" ]; then
      echo "Backing up existing config to ${config_dir}.bak"
      mv "$config_dir" "${config_dir}.bak"
    fi
    git clone "$URL" "$config_dir"
  fi
  echo -e "${GREEN}Global config ready at $config_dir${NC}"
}

setup_local() {
  local target="${1:-.opencode}"
  if [ -d "$target/.git" ]; then
    echo -e "${CYAN}Updating existing .opencode...${NC}"
    git -C "$target" pull
  else
    if [ -d "$target" ]; then
      echo "Backing up existing $target to ${target}.bak"
      mv "$target" "${target}.bak"
    fi
    echo -e "${CYAN}Installing locally...${NC}"
    git clone "$URL" "$target"
  fi
  echo -e "${GREEN}Local config ready at $target${NC}"
}

show_next_steps() {
  echo ""
  echo -e "${GREEN}=== opencode-for-starters ready ===${NC}"
  echo ""
  echo -e "${CYAN}Paste-link usage (add to opencode.json):${NC}"
  echo ""
  echo '  {'
  echo "    \"instructions\": [\"$RAW/AGENTS.md\"]"
  echo '  }'
  echo ""
  echo -e "${CYAN}Or start a session:${NC}"
  echo "  opencode ."
}

MODE="${1:-auto}"

case "$MODE" in
  --global|global)
    install_opencode
    setup_global
    show_next_steps
    ;;
  --local|local)
    install_opencode
    setup_local
    show_next_steps
    ;;
  auto)
    install_opencode
    if [ -f ".opencode/opencode.json" ] || [ -f "opencode.json" ]; then
      setup_local
    else
      setup_global
    fi
    show_next_steps
    ;;
  *)
    usage
    ;;
esac
