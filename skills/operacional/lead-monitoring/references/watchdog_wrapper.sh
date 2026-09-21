#!/usr/bin/env bash
# Wrapper para o watchdog rodar via cron `no_agent`.
# O cron busca scripts em ~/.hermes/scripts/ ou /data/scripts/.
# O workdir do cron aponta para o diretório do projeto (ex: /data/Luzperformance/new-leads).
exec python3 /caminho/para/projeto/watchdog_leads.py
