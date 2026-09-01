# Leia primeiro — instalação do Starter Kit Hermes

Este pacote é um **harness inicial para Hermes Agent**. Ele não substitui regras já existentes e não pede que o agente ignore sua hierarquia de instruções.

## Objetivo

Instalar skills reutilizáveis no diretório correto do perfil Hermes, criar contexto de projeto e conduzir um onboarding seguro.

## Procedimento para o agente

1. Leia `README.md` e `MIGRACAO-OPENCLAW-HERMES.md`.
2. Descubra o home real com `HERMES_HOME`; se vazio, use `~/.hermes`.
3. Antes de sobrescrever qualquer skill existente, compare e peça autorização.
4. Instale as pastas que contêm `SKILL.md` em `$HERMES_HOME/skills/` preservando seus nomes.
5. Não copie `AGENTS.md`, `HERMES.md` ou `SOUL.md` sobre arquivos existentes sem consentimento.
6. Valide com `hermes skills list`, `hermes skills check` e `hermes doctor`.
7. Inicie a skill `onboarding-checklist` ou diga ao usuário para iniciar uma nova sessão com `hermes -s onboarding-checklist`.

## Regras de segurança

- Configuração: use `hermes config set ...`; não edite `config.yaml` manualmente.
- Segredos: use o caminho mostrado por `hermes config env-path`; em instalações hPanel, use **hPanel → Hermes Agent → Dashboard → Environment**.
- Projeto: prefira `.hermes.md`/`HERMES.md`; use `AGENTS.md` apenas para regras portáveis no diretório de trabalho.
- Identidade global: `SOUL.md` fica em `$HERMES_HOME`.
- Memória durável: use as ferramentas `memory`/`session_search`; não invente `MEMORY.md` como mecanismo nativo.
- Agendamentos: use `cronjob` ou `hermes cron`; não crie heartbeat improvisado.
- Sempre mostre a saída real das validações antes de declarar sucesso.
