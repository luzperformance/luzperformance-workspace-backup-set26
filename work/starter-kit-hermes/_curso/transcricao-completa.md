# Transcrição resumida — Curso Hermes Agent

## A0 · Visão da stack

Hermes separa modelo, agente, ferramentas, memória, skills, projeto, gateway e scheduler. Essa separação evita colocar tudo em um único arquivo de configuração.

Prática: `hermes status --all`.

## A1 · Três padrões de agente

Use uma sessão principal para trabalho geral, perfis para identidades isoladas e `delegate_task` para subtarefas. Para filas duráveis entre workers, use Kanban.

Prática: `hermes profile list`.

## A1 · Instalação

Instale pelo script oficial, rode o wizard e diagnostique antes de personalizar. Em hospedagem hPanel, variáveis são geridas no Dashboard → Environment.

Prática: `hermes setup` e `hermes doctor`.

## A2 · Interfaces e cockpit

CLI/TUI, Desktop e Dashboard usam o mesmo núcleo. O Dashboard administra canais, memória, webhooks e perfis; `hermes sessions` inspeciona conversas.

Prática: `hermes dashboard`.

## A3 · Starter kit

O instalador copia skills para o home do perfil sem tocar em credenciais ou identidade. Skills só entram no prompt na sessão seguinte.

Prática: `bash scripts/install.sh` e `hermes skills check`.

## A4 · Telegram

Crie o bot no BotFather, guarde o token no ambiente e configure pelo gateway. Valide status, logs e uma mensagem real; bots Telegram não são E2E.

Prática: `hermes gateway setup` e `hermes gateway status`.

## A5 · Identidade

`SOUL.md` define identidade global. `HERMES.md`/`.hermes.md` define regras do projeto. `AGENTS.md` serve para portabilidade e só é descoberto no cwd.

Prática: `hermes config path`.

## A6 · Workspace

O projeto contém entregáveis, documentação e regras. Skills e memória do agente vivem no home do perfil, não dentro do projeto por obrigação.

Prática: `pwd`.

## A7 · Memória

Use `memory` para fatos estáveis e `session_search` para histórico. TODOs e progresso temporário não são memória durável.

Prática: `hermes memory status`.

## A8 · Skills

Cada skill é uma pasta com `SKILL.md` e frontmatter válido. Instale, cheque, configure por plataforma e reinicie a sessão.

Prática: `hermes skills list` e `hermes skills check`.

## A9 · Crons

Jobs rodam em sessões frescas: prompts precisam ser autocontidos. Use entrega silenciosa quando não houver novidade e teste o job manualmente.

Prática: `hermes cron list` e `hermes cron status`.

## A10 · Segurança

Mantenha redaction de segredos ativa, aprovações em `smart`, toolsets mínimos e credenciais fora do Git. `--yolo` é exceção, não onboarding.

Prática: `hermes config get approvals.mode`.

## A11 · Outros canais

O gateway suporta Discord, Slack, WhatsApp, Signal, Matrix, Email e outros por plugins. Cada canal tem permissões e riscos próprios.

Prática: `hermes gateway setup`.

## A12 · Integrações

Prefira toolsets nativos, skills e MCP. Configure credenciais no ambiente e valide cada integração com a menor operação possível.

Prática: `hermes tools list` e `hermes mcp list`.

## A13 · Multiagente

`delegate_task` é rápido e não durável. Perfis isolam contexto. Kanban coordena trabalho durável. Worktrees evitam conflito em código.

Prática: `hermes profile list` e `hermes kanban --help`.

## A14 · Dashboard e Kanban

Use Dashboard para visão operacional, sessions para histórico, cron para automações e Kanban para fila multiagente.

Prática: `hermes sessions list` e `hermes cron list`.

## A15 · Fechamento

Um harness saudável é pequeno, verificável e evolui por skills. Revise memória, jobs e toolsets periodicamente.

Prática: `hermes doctor` e `hermes curator status`.
