#!/bin/bash
# Backup diário do workspace pro GitHub (cron Hermes roda isto)
set -e
cd /data
git add -A
if git diff --cached --quiet; then
  echo "backup: sem mudanças $(date +%Y-%m-%d-%H%M)"
  exit 0
fi
git commit -q -m "backup: $(date +%Y-%m-%d-%H%M)"
git push backup main -q
echo "backup: push ok $(date +%Y-%m-%d-%H%M)"
