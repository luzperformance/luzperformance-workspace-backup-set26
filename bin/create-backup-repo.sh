#!/bin/bash
# Criar repo privado no GitHub
TOKEN=$(grep ^GITHUB_TOKEN= /data/.env | cut -d= -f2)
curl -s -X POST -H "Authorization: token $TOKEN" \
     https://api.github.com/user/repos \
     -d '{"name":"luzperformance-workspace-backup-set26","private":true,"auto_init":false}' \
     | grep -E '"full_name"|"message"'
