# Migração conceitual — OpenClaw para Hermes Agent

| Conceito antigo | Equivalente Hermes |
|---|---|
| diretório `.openclaw` | `$HERMES_HOME` (normalmente `~/.hermes`) |
| `openclaw.json` | `config.yaml`, gerenciado por `hermes config set` |
| workspace com skills embutidas | skills em `$HERMES_HOME/skills/`; projeto separado |
| `MEMORY.md` como memória nativa | ferramentas `memory` e `session_search`; backend configurável |
| `IDENTITY.md` | `SOUL.md` em `$HERMES_HOME` |
| regras de boot em `AGENTS.md` global | `SOUL.md` global e `.hermes.md`/`HERMES.md` por projeto |
| heartbeat | jobs duráveis via `cronjob`/`hermes cron` |
| canais OpenClaw | `hermes gateway setup` e plugins de plataforma |
| política de execução própria | `approvals.mode` (`smart`, `manual`, `off`) |
| subagentes ad hoc | `delegate_task`; processos Hermes; Kanban para filas duráveis |
| mission control | Dashboard, sessions, cron, profiles e Kanban |

## Caminhos

Nunca fixe `~/.hermes` em automações de perfil. Resolva primeiro:

```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
```

## Credenciais

- Instalação comum: veja `hermes config env-path`.
- Ambiente hospedado pelo hPanel: **hPanel → Hermes Agent → Dashboard → Environment**.
- OAuth e pools: `hermes auth` / `hermes auth add <provider>`.

## Mudanças deliberadas neste kit

O histórico específico de Hostinger Managed, comandos OpenClaw, pairing e `HEARTBEAT.md` foi removido. Screenshots do GitHub foram preservados porque continuam úteis no fluxo opcional de backup.
