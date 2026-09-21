# PRD — Migração Hermes → OpenClaw

## Objetivo

Migrar a instalação pessoal do Hermes (perfil `default`, `HERMES_HOME=/data`) para o OpenClaw, preservando identidade, skills, crons, memória, canais e integrações.

## Estado de partida (verificado 2026-09-21)

- Workspace versionado, push em dia: commit `144240d2` → `luzperformance/luzperformance-workspace-backup-set26` (privado)
- 118 skills em `skills/`
- 11 jobs em `cron/jobs.json`
- Config em `/data/config.yaml`; segredos em `/data/.env`
- Mem0 + Qdrant local travado por lock de processo — backend de memória instável
- MCP `luz_crm` configurado no `config.yaml`, OAuth nunca concluído
- OpenClaw não está instalado nesta máquina (sem binário, sem `~/.openclaw`)

## Mapa de equivalências

| Hermes | OpenClaw | Observação |
|---|---|---|
| `$HERMES_HOME` (tudo em `/data`) | `~/.openclaw/workspace` + `~/.openclaw/` | OpenClaw separa workspace de config/credenciais/sessões |
| `SOUL.md` | `SOUL.md` | carregado toda sessão |
| `AGENTS.md` | `AGENTS.md` | carregado toda sessão |
| `USER.md` | `USER.md` | orçamento próprio; importador nativo disponível |
| `MEMORY.md` | `MEMORY.md` | importador nativo disponível |
| `memory/YYYY-MM-DD.md` | `memory/YYYY-MM-DD.md` | mesma convenção |
| `TOOLS.md` | `TOOLS.md` | equivalente existe |
| `MAPA.md` | — | sem equivalente nativo; vira doc on-demand |
| — | `IDENTITY.md`, `HEARTBEAT.md`, `BOOT.md`, `BOOTSTRAP.md` | não existem hoje; precisam ser criados |
| `skills/*/SKILL.md` | `skills/` do workspace | precedência máxima no destino |
| `cron/jobs.json` | `openclaw cron` | recriação, não cópia |
| `config.yaml` | `~/.openclaw/openclaw.json` (JSON5) | schema diferente |
| `.env` | `~/.openclaw/credentials/` | não versionar |
| Mem0 + Qdrant | SQLite interno + `memory_search` | embeddings OpenAI suportados |
| `gateway.platforms.telegram.*` | `channels.telegram.*` | |

## Migra direto

- `SOUL.md`, `AGENTS.md` — markdown carregado por sessão nos dois
- `USER.md` e `MEMORY.md` — o OpenClaw tem importador nativo de memória do Hermes (Control UI → Settings → Import Memory). Copia **apenas Markdown**: config, credenciais e skills **não** entram por esse caminho.
- `memory/` (notas diárias) — mesma convenção de nome
- Conteúdo do workspace: `decisions/`, `projects/`, `content/`, `Luzperformance/`, `memories/`

## Precisa ser recriado

### 1. Estrutura
Hoje tudo vive em `/data`. No destino, workspace e runtime são separados. Criar `IDENTITY.md`, `HEARTBEAT.md` e `BOOT.md` — não existem no Hermes.

### 2. Skills (118)
Vão para `skills/` do workspace. Cada arquivo precisa de revisão:
- frontmatter válido no destino
- as seções "Contrato Hermes desta skill" citam ferramentas Hermes (`read_file`, `write_file`, `search_files`, `cronjob`, `memory`, `skill_manage`) e `hermes config set` — reescrever para os equivalentes do OpenClaw

Não é substituição de nome de produto.

### 3. Crons (11)
Recriar com `openclaw cron add`:

| Job atual | Destino |
|---|---|
| `monitor-leads-novos` (every 15m, no_agent) | `--every 15m` com payload de script |
| `watchdog-leads` (every 30m, no_agent) | `--every 30m` com payload de script |
| 8 × `reavaliar-plano-raphael-silva-2027-09-12-*` | `--at 2027-09-12T..Z --delete-after-run` |
| `reflexao-diaria-07h-14h` | `--cron "0 10,17 * * *" --tz UTC`, modelo `gpt-5.6-luna` |

OpenClaw aplica stagger determinístico de até 5 min em expressões no topo da hora; `--exact` força o horário preciso. Sem `--tz`, usa o fuso do host.

### 4. Memória
- `MEMORY.md` e `USER.md` entram pelo importador nativo.
- O índice vetorial do OpenClaw é SQLite próprio com embeddings OpenAI (`text-embedding-3-small` é suportado explicitamente). Substitui Mem0 + Qdrant e elimina o lock atual.
- `mem0_qdrant` não migra.

### 5. Telegram
- O mesmo bot token não pode rodar em dois gateways ao mesmo tempo — parar o Hermes antes de subir o OpenClaw.
- `channels.telegram.allowFrom` (IDs numéricos) + `dmPolicy: "allowlist"` + `commands.ownerAllowFrom`.
- IDs atuais: Dr. Vinícius `8634563463`; secretária `7831560002`.
- Grupos e tópicos: `channels.telegram.groups` + `groups.*.topics.*`.

### 6. MCP `luz_crm`
O schema `mcp_servers` do Hermes não é o do OpenClaw, e o OAuth nunca completou. Reconfigurar do zero no destino.

### 7. Config e segredos
- `config.yaml` → `openclaw.json` (JSON5), campo por campo.
- `.env` → `credentials/` do OpenClaw, fora de qualquer versionamento.

## Riscos

1. **Lembretes clínicos one-shot.** Os 8 jobs de reavaliação de plano em 12/09/2027 são follow-up clínico de um ano. Se a recriação falhar em silêncio, some.
2. **Bot do Telegram.** Dois gateways ativos ao mesmo tempo geram conflito de polling.
3. **Hospedagem.** OpenClaw precisa de host próprio. O OneClick da Hostinger é do Hermes — confirmar se suporta OpenClaw antes de assumir.
4. **Skills.** 118 arquivos com contratos específicos do Hermes.
5. **Segredos.** `credentials/` nunca entra no repositório.

## Ordem de execução

1. Backup do workspace — feito
2. Subir OpenClaw em host separado e rodar `openclaw onboard`
3. Importar `MEMORY.md` e `USER.md`
4. Levar o conteúdo do workspace
5. Criar `IDENTITY.md`, `HEARTBEAT.md`, `BOOT.md`
6. Migrar skills com revisão arquivo por arquivo
7. Recriar os 11 crons
8. Configurar Telegram (Hermes parado)
9. Reconfigurar MCP `luz_crm`
10. Rodar os dois em paralelo por alguns dias; só então desligar o Hermes

## Verificação

- `openclaw doctor`
- `openclaw cron list` mostrando os 11 jobs
- DM de teste no Telegram com os dois IDs autorizados
- `openclaw memory status --index`
