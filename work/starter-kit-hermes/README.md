# Starter Kit Hermes Agent — PT-BR

Harness inicial para configurar um agente Hermes com identidade, contexto de projeto, memória, skills, gateway, cron e práticas de segurança.

## Compatibilidade

- Hermes Agent atual em Linux, macOS, Windows ou WSL
- CLI, Desktop, Dashboard e gateways de mensagens
- Perfis isolados via `HERMES_HOME`

## Início rápido

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes doctor
```

Depois, extraia este pacote e rode:

```bash
bash scripts/install.sh
hermes skills list
hermes skills check
```

Abra uma nova sessão para carregar skills recém-instaladas:

```bash
hermes -s onboarding-checklist
```

## O que o instalador faz

- copia somente diretórios com `SKILL.md` para `$HERMES_HOME/skills/`;
- não sobrescreve skills existentes sem `--force`;
- não toca em `config.yaml`, credenciais, memória ou identidade;
- gera um relatório de instalação.

## Estrutura

- `HERMES.md`: contexto carregado automaticamente ao trabalhar neste kit
- `skills/`: skills compatíveis com Hermes
- `templates/`: modelos de `HERMES.md`, `SOUL.md`, perfil, mapa e crons
- `exemplos/`: exemplos preenchidos
- `_curso/`: aulas revisadas para Hermes
- `archive/`: cheatsheets legados, já convertidos para Hermes
- `scripts/install.sh`: instalador idempotente
- `MIGRACAO-OPENCLAW-HERMES.md`: mapa de conceitos

## Princípios

1. Backup antes de sobrescrever.
2. Ações destrutivas exigem escopo explícito.
3. Segredos nunca entram no repositório.
4. Validação usa saída real de ferramentas.
5. Skills novas só aparecem em uma sessão nova (`/reset` ou reinício).
6. Arquivos de contexto têm papéis distintos: `SOUL.md` para identidade; `HERMES.md` para projeto; memória para fatos duráveis.

Documentação oficial: https://hermes-agent.nousresearch.com/docs/
