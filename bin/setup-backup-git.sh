#!/bin/bash
# Setup git + primeiro push do workspace pro repo de backup
set -e
TOKEN=$(grep ^GITHUB_TOKEN= /data/.env | cut -d= -f2)
REPO="luzperformance/luzperformance-workspace-backup-set26"
cd /data

# .gitignore defensivo
cat > .gitignore <<'EOF'
.env
.env.local
.env.*.local
*.key
*.pem
*-credentials.json
auth.json
auth.lock
tokens.json
credentials.json
.tmp-*
cache/
audio_cache/
image_cache/
logs/
pending_messages/
gateway.sock
gateway.pid
gateway.lock
gateway_state.json
kanban.db*
*.session
starter-kit-hermes-v2.5.7/
EOF

git init -b main 2>/dev/null || git init
git remote remove backup 2>/dev/null || true
git remote add backup "https://x-access-token:${TOKEN}@github.com/${REPO}.git"
git add -A
git commit -m "backup: initial setup $(date +%Y-%m-%d-%H%M)" || echo "nada pra commitar"
git push -u backup main
