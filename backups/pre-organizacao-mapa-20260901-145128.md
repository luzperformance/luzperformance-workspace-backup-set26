# MAPA.md — Workspace do Hermes

> Mapa raiz. Hermes lê isto antes de navegar o workspace.
> Atualizado em 2026-08-31.

## Arquivos raiz (quem eu sou)

| Arquivo | Conteúdo |
|---|---|
| `SOUL.md` | Personalidade, tom, princípios — quem sou |
| `IDENTITY.md` | Identidade: nome, versão, agent ID, domínios |
| `USER.md` | Quem sirvo: Dr Vinícius Luzardi / Luz Performance |
| `AGENTS.md` | Regras de comportamento: boot sequence + red lines |
| `TOOLS.md` | Ferramentas e permissões |
| `MAPA.md` | Este arquivo |

## Pastas

| Pasta | Conteúdo |
|---|---|
| `content/` | Tudo que eu crio (drafts, posts, roteiros) |
| `content/drafts/` | Rascunhos em produção |
| `content/archive/` | Peças publicadas/versionadas |
| `decisoes/` | Decisões importantes (append-only, 1 arquivo por mês) |
| `projects/` | Projetos ativos (1 arquivo por projeto) |
| `skills/` | Skills instaladas (cada uma em `{categoria}/{nome}/SKILL.md`) |
| `archive/` | Arquivos substituídos — história, não lixo |
| `backups/` | Backups timestamped (fora do fluxo ativo) |
| `memory/` | Memória persistente do Hermes (gerenciada pela tool `memory`) |

## Convenções

- Posts/drafts: `content/drafts/{tipo}-{tema}-{YYYY-MM-DD}.md`
- Decisões: `decisoes/{YYYY-MM}.md` (append-only)
- Projetos: `projects/{nome-curto}.md`
- Saída nunca fica solta no chat nem na raiz do workspace.
- Skills: `skills/{categoria}/{nome}/SKILL.md` + registro em `skills/_registry.md`

## Kit original

O Starter Kit Hermes v2.5.7 extraído está em `/data/starter-kit-hermes-v2.5.7/` — material de referência, não fluxo ativo.
