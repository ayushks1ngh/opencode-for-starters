#!/usr/bin/env bash
set -euo pipefail

OPCODE_DIR="$(cd "$(dirname "$0")" && pwd)/.opencode"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"

usage() {
  echo "Usage: $0 [--global | --local]"
  echo "  --global   Symlink .opencode/ to ~/.config/opencode/ (default)"
  echo "  --local    Keep it per-project (already set up, nothing to do)"
  exit 0
}

MODE="${1:---global}"

case "$MODE" in
  --global)
    mkdir -p "$CONFIG_DIR"
    for f in "$OPCODE_DIR"/*; do
      name="$(basename "$f")"
      target="$CONFIG_DIR/$name"
      if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "WARNING: $target exists and is not a symlink, skipping"
      else
        ln -sfn "$f" "$target"
        echo "Linked $name"
      fi
    done
    echo "Done. opencode will use this config globally."
    ;;
  --local)
    echo "Already set up for local use. opencode will pick up .opencode/ in this project."
    ;;
  *)
    usage
    ;;
esac
