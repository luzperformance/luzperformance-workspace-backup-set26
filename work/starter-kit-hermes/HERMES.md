# Starter Kit Hermes — contexto do projeto

## Objetivo

Este repositório é um harness inicial em português para configurar o Hermes Agent com skills, identidade, contexto de projeto, memória, gateway, cron e práticas de segurança.

## Regras para trabalhar neste kit

1. Leia `README.md` e `MIGRACAO-OPENCLAW-HERMES.md` antes de instalar.
2. Resolva o home ativo por `$HERMES_HOME`; use `~/.hermes` apenas como fallback.
3. Não sobrescreva skills, `SOUL.md`, arquivos de contexto, configuração ou credenciais sem consentimento explícito.
4. Configuração deve ser alterada com `hermes config set`; não edite `config.yaml` manualmente.
5. Segredos ficam no caminho retornado por `hermes config env-path`. Em ambientes hPanel, use **Hermes Agent → Dashboard → Environment**.
6. Skills são instaladas em `$HERMES_HOME/skills/<nome>/`, não na pasta do projeto.
7. Use `memory` para fatos duráveis, `session_search` para histórico e `todo` para progresso temporário.
8. Use `cronjob` ou `hermes cron` para agendamentos. Cada prompt de cron deve ser autocontido.
9. Mudanças em skills e toolsets exigem nova sessão ou `/reset`.
10. Nunca declare sucesso sem saída real de validação.

## Instalação

```bash
bash scripts/install.sh
hermes skills list
hermes skills check
hermes doctor
```

Depois, abra uma nova sessão com a skill de onboarding:

```bash
hermes -s onboarding-checklist
```

## Validação do pacote

```bash
python scripts/validate.py
bash -n scripts/install.sh
```

## Documentação oficial

A documentação oficial prevalece sobre este material:
https://hermes-agent.nousresearch.com/docs/
