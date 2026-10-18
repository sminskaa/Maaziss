#!/usr/bin/env bash
set -euo pipefail
project_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
export XDG_DATA_HOME="$project_dir/.local/share"
export XDG_CACHE_HOME="$project_dir/.local/cache"
export XDG_CONFIG_HOME="$project_dir/.local/config"
mkdir -p "$XDG_DATA_HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME"
godot_binary="$project_dir/.local/bin/godot"
if [[ ! -x "$godot_binary" ]]; then
  godot_binary="$(command -v godot || command -v godot4 || true)"
fi
if [[ -z "$godot_binary" ]]; then
  echo 'Run python3 tools/setup.py first to install the pinned Godot runtime.' >&2
  exit 1
fi
exec "$godot_binary" "$@"
