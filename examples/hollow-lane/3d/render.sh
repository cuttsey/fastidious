#!/bin/bash
# Renders the Hollow Lane world and builds the scroll-film sequences.
# Needs Blender as a Python module (pip install bpy) and ffmpeg with libwebp.
set -e
cd "$(dirname "$0")"
KIT=../../../plugins/fastidious/skills/render-engineer/scripts/make_sequence.py
for s in S01 S02 S03 S04 S05 S06; do
  n=16; [ "$s" = S01 ] && n=24
  python3 build_world.py --scene $s --frames 1-$n --count $n --out ../world/$s --samples 8
  poster=middle; [ "$s" = S04 ] && poster=last
  python3 $KIT ../world/$s ../site/frames/$s --sizes 960,480 --quality 76 --poster $poster
done
