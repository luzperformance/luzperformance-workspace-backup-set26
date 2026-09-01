# FAQ — Starter Kit Hermes

## O Hermes não inicia ou o gateway parou

```bash
hermes status --all
hermes doctor
hermes gateway status
hermes logs errors
hermes gateway restart
```

Use `hermes doctor --fix` somente depois de revisar o diagnóstico. Não apague `$HERMES_HOME` como tentativa de correção.

## Onde ficam as configurações?

Use `hermes config path`, `hermes config show` e `hermes config set CHAVE VALOR`. Não edite YAML manualmente.

## Onde coloco API keys?

Veja `hermes config env-path`. Em hPanel, altere em **Hermes Agent → Dashboard → Environment**. OAuth deve ser configurado por `hermes auth`.

## Como troco de modelo?

Use `hermes model`, `/model` ou aliases em `model.aliases`. Verifique com `hermes doctor`.

## Skills instaladas não aparecem

Rode `hermes skills list`, `hermes skills check` e `hermes skills config`; depois inicie nova sessão ou use `/reset`.

## Como faço backup?

Versione apenas arquivos de projeto e skills próprias. Não versione `.env`, `auth.json`, logs, sessões ou bancos de memória. Use `hermes backup` para recursos suportados e Git privado para o workspace.

## Como agendo tarefas?

Use `cronjob` em conversa ou `hermes cron create`. Jobs rodam em sessão fresca; o prompt precisa ser autocontido.

## Como conecto Telegram/WhatsApp?

Use `hermes gateway setup` e siga o assistente da plataforma. Tokens ficam no ambiente, nunca em markdown ou Git.

## Como separo agentes?

Use perfis (`hermes profile create`) para identidades/configurações isoladas, `delegate_task` para subtarefas e Kanban para trabalho durável entre workers.

## Privacidade

Bots do Telegram não são E2E. Mantenha `security.redact_secrets` ativo e habilite `privacy.redact_pii` quando necessário.
