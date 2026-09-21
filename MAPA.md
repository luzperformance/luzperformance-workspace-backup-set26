# MAPA.md — Workspace do Hermes

> Mapa raiz. Hermes lê este arquivo antes de navegar o workspace.
> Atualizado em 2026-09-01.

## Arquivos raiz — operação

| Arquivo | Conteúdo |
|---|---|
| `SOUL.md` | Personalidade, tom e princípios do Hermes |
| `IDENTITY.md` | Identidade, versão e domínios do agente |
| `USER.md` | Quem sirvo: Dr. Vinícius Luzardi / Luz Performance |
| `AGENTS.md` | Regras operacionais e boot sequence |
| `TOOLS.md` | Ferramentas e permissões |
| `MAPA.md` | Este arquivo |

## Áreas ativas do negócio

| Pasta | Finalidade | Mapa local |
|---|---|---|
| `content/` | Roteiros, posts, drafts e análises editoriais | `content/MAPA.md` |
| `decisions/` | Decisões duráveis, organizadas por mês | `decisions/MAPA.md` |
| `projects/` | Projetos ativos; cada novo projeto começa com `PRD.md` | `projects/MAPA.md` |
| `Luzperformance/` | Frentes operacionais da Luz Performance | `Luzperformance/MAPA.md` |
| `Luzperformance/AvatarHype/` | Conhecimentos e aplicações do curso AvatarGen | `Luzperformance/AvatarHype/MAPA.md` |
| `archive/` | Histórico recuperável de arquivos substituídos | `archive/MAPA.md` |

## Inteligência operacional

| Pasta | Finalidade | Mapa local |
|---|---|---|
| `skills/` | Procedimentos reutilizáveis do Hermes | `skills/MAPA.md` |
| `backups/` | Backups manuais e de segurança | — |
| `scripts/` | Scripts operacionais | — |
| `work/` | Instalação, testes e artefatos de construção; não é área de negócio | — |
| `workspace/` | Materiais transitórios de trabalho; não é destino de entregáveis | — |

## Infraestrutura do Hermes — não usar para entregáveis

`audio_cache/`, `cache/`, `cron/`, `gateway/`, `image_cache/`, `kanban/`, `logs/`, `memories/`, `sessions/`, `state/`, `webui/` e arquivos de configuração na raiz são dados internos do Hermes. Não mover, renomear ou salvar entregáveis nesses locais.

## Convenções

- Conteúdo novo: `content/drafts/{canal}/{tema-curto}-{YYYY-MM-DD}.{md|txt}`.
- Decisões: `decisions/{YYYY-MM}.md`, append-only.
- Projetos: `projects/{nome-curto}/PRD.md`.
- Material substituído: preservar em `archive/`; lixo vai para a lixeira, nunca para `archive/`.
- Skills: `skills/{categoria}/{nome}/SKILL.md`, com registro em `skills/_registry.md`.
- Nenhuma saída fica solta na raiz ou apenas no chat.

## Navegação

Antes de salvar, ler o `MAPA.md` da pasta de destino. Ao criar uma nova frente ou subpasta que passe a receber trabalho recorrente, criar seu mapa local e atualizar este arquivo.

## Referência

O Starter Kit Hermes v2.5.7 está em `starter-kit-hermes-v2.5.7/`: é material de referência, não fluxo operacional ativo.
