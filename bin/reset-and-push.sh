#!/bin/bash
# Reescrever histórico removendo blobs grandes (.cache) e fazer push
set -e
cd /data
TOKEN=$(grep ^GITHUB_TOKEN= /data/.env | cut -d= -f2)
REPO="luzperformance/luzperformance-workspace-backup-set26"

# Resetar histórico: commit único limpo
rm -rf .git
git init -b main
git config user.email "vinicius@luzperformance.com.br"
git config user.name "Vinícius Luzardi"
git remote add backup "https://x-access-token:${TOKEN}@github.com/${REPO}.git"
git add -A
git commit -m "backup: initial setup $(date +%Y-%m-%d-%H%M)"
git push -u backup main
