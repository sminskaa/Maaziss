#!/usr/bin/env bash
set -euo pipefail
project_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
mkdir -p "$project_dir/.local/cache/checks"
run_checked() {
  local check_name="$1"
  shift
  local check_log="$project_dir/.local/cache/checks/$check_name.log"
  bash "$project_dir/tools/godot.sh" "$@" 2>&1 | tee "$check_log"
  if rg -q '^ERROR:|SCRIPT ERROR:' "$check_log"; then
    echo "Godot reported an error during $check_name." >&2
    return 1
  fi
}
run_checked import --headless --path "$project_dir" --editor --import
run_checked model --headless --path "$project_dir" --script res://tests/test_opening.gd
run_checked startup --headless --path "$project_dir" --quit-after 3
