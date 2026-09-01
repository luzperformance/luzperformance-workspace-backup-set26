#!/bin/bash
# Histórico limpo de verdade: um único commit, sem nada de whisper/cache no objeto histórico
set -e
cd /data
TOKEN=$(grep ^GITHUB_TOKEN= /data/.env | cut -d= -f2)
REPO="luzperformance/luzperformance-workspace-backup-set26"

rm -rf .git
git init -b main -q
git config user.email "vinicius@luzperformance.com.br"
git config user.name "Vinícius Luzardi"
git remote add backup "https://x-access-token:${TOKEN}@github.com/${REPO}.git"
git add -A
git commit -q -m "backup: initial clean setup $(date +%Y-%m-%d-%H%M)"
echo "maior arquivo no commit:"
git ls-files | xargs -I{} du -b "{}" 2>/dev/null | sort -rn | head -3
git push -u backup main 2>&1 | tail -3
