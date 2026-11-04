#!/usr/bin/env bash
# Installs Fastidious as plain skills in ~/.claude/skills (or $CLAUDE_SKILLS_DIR), for anyone not using the
# plugin marketplace. Copies the Fastidious skills, then installs the third-party crew at its pinned commits.
#
#   ./install.sh               add what is missing; never touch a skill you already have
#   ./install.sh --force       replace existing copies, moving yours to a timestamped backup first
#   ./install.sh --with-film   also install the pinned promotional-film stack (see PROMO-STACK.md)
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src="$here/plugins/fastidious/skills"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
force=0; film=0
for a in "$@"; do
  case "$a" in
    --force) force=1 ;;
    --with-film) film=1 ;;
    *) echo "Unknown option: $a" >&2; exit 2 ;;
  esac
done
command -v python3 >/dev/null || { echo "Python 3 is required." >&2; exit 1; }
command -v git >/dev/null || { echo "git is required." >&2; exit 1; }
backup="$dest/../skills-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$dest"; added=0; kept=(); moved=0

move_aside() { mkdir -p "$backup"; mv "$dest/$1" "$backup/$1"; moved=$((moved+1)); }

for dir in "$src"/*/; do
  name="$(basename "$dir")"
  if [ -e "$dest/$name" ]; then
    if [ "$force" = 1 ]; then move_aside "$name"; else kept+=("$name"); continue; fi
  fi
  cp -R "$dir" "$dest/$name"; added=$((added+1))
done
echo "Installed $added Fastidious skills to $dest"

# The crew: with --force, any copy not installed by Fastidious (an older bundled one, say) is backed up first.
crew="$dest/fastidious/scripts/crew_stack.py"
[ -f "$crew" ] || crew="$src/fastidious/scripts/crew_stack.py"
if [ "$force" = 1 ]; then
  while read -r name; do
    if [ -e "$dest/$name" ] && [ ! -e "$dest/$name/.fastidious-pin.json" ]; then move_aside "$name"; fi
  done < <(python3 "$crew" names)
fi
python3 "$crew" install --dir "$dest"
if [ "$film" = 1 ]; then python3 "$(dirname "$crew")/promo_stack.py" install --dir "$dest"; fi

[ "$moved" -gt 0 ] && echo "Moved $moved existing skills to $backup"
if [ "${#kept[@]}" -gt 0 ]; then
  echo "Kept ${#kept[@]} existing skills, so these were not updated: ${kept[*]}"
  echo "Run ./install.sh --force to replace them. Your versions are backed up first."
fi
python3 "$crew" check --dir "$dest" || true
echo 'Restart Claude Code, then start a project with: /fastidious'
