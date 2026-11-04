#!/usr/bin/env bash
# Run a blender-build spec headless.
#   blender.sh <spec.json> [--preview|--draft] [--only stills,turntable,glb]
# Finds Blender in the usual places, or use BLENDER=/path/to/Blender.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
B="${BLENDER:-}"
for c in "$B" /Applications/Blender.app/Contents/MacOS/Blender "$HOME/Applications/Blender.app/Contents/MacOS/Blender" "$(command -v blender || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then B="$c"; break; fi
done
if [ -z "$B" ] || [ ! -x "$B" ]; then
  echo "Blender not found. Install it (brew install --cask blender, or blender.org) or set BLENDER=/path/to/Blender." >&2; exit 2
fi
exec "$B" -b --factory-startup -noaudio -P "$HERE/run.py" -- "$@"
