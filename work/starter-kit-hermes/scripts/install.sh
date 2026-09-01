#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1
mkdir -p "$HERMES_HOME/skills"
installed=0; skipped=0
while IFS= read -r -d '' skillfile; do
  src="$(dirname "$skillfile")"; name="$(basename "$src")"; dst="$HERMES_HOME/skills/$name"
  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then printf 'SKIP %s (já existe)\n' "$name"; skipped=$((skipped+1)); continue; fi
  if [[ -e "$dst" ]]; then backup="$dst.backup.$(date +%Y%m%d%H%M%S)"; cp -a "$dst" "$backup"; fi
  rm -rf "$dst"; cp -a "$src" "$dst"; printf 'OK   %s\n' "$name"; installed=$((installed+1))
done < <(find "$ROOT/skills" -mindepth 2 -name SKILL.md -print0)
printf '\nInstaladas: %d · puladas: %d · home: %s\n' "$installed" "$skipped" "$HERMES_HOME"
printf 'Agora rode: hermes skills list && hermes skills check\nAbra uma nova sessão para carregar mudanças.\n'
