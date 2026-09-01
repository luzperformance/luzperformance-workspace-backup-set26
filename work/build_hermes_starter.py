from pathlib import Path
import json, shutil, os, re

SRC = Path('/data/work/starter-kit-openclaw/starter-kit')
DST = Path('/data/work/starter-kit-hermes')
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(SRC, DST)

# Remove assets and historical docs tied exclusively to the old platform.
for p in [
    DST/'skills/starter/wizard-autonomia/screenshots/painel-hostinger-cli.jpg',
]:
    if p.exists(): p.unlink()
for d in [DST/'skills/starter/wizard-autonomia/screenshots']:
    if d.exists() and not any(d.iterdir()): d.rmdir()
for p in [DST/'MENSAGENS-TESTERS-v2.2.md', DST/'MENSAGENS-TESTERS-v2.5.3.md']:
    if p.exists(): p.unlink()

# Rename platform-specific lesson.
old = DST/'_curso/aulas/aula-01-setup-managed.html'
new = DST/'_curso/aulas/aula-01-setup-hermes.html'
if old.exists(): old.rename(new)

root_files = {
'0-LEIA-PRIMEIRO-AGENTE.md': '''# Leia primeiro — instalação do Starter Kit Hermes

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
''',
'README.md': '''# Starter Kit Hermes Agent — PT-BR

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
''',
'MIGRACAO-OPENCLAW-HERMES.md': '''# Migração conceitual — OpenClaw para Hermes Agent

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
''',
'BUILD.md': '''# Build e validação

O artefato oficial é `starter-kit-hermes.zip`.

## Checklist

```bash
python scripts/validate.py
bash -n scripts/install.sh
python -m json.tool skills/starter/onboarding-checklist/evals/evals.json >/dev/null
```

A validação falha se encontrar comandos/caminhos da plataforma anterior, JSON inválido, SKILL sem frontmatter ou links locais ausentes.
''',
'FAQ.md': '''# FAQ — Starter Kit Hermes

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
''',
'CHANGELOG.md': '''# Changelog — Starter Kit Hermes

## 3.0.0 — conversão integral

- Conversão integral do kit para Hermes Agent.
- Skills movidas para o contrato `$HERMES_HOME/skills/<nome>/SKILL.md`.
- `IDENTITY.md`, `USER.md`, `MEMORY.md` e heartbeat deixaram de ser tratados como recursos nativos.
- Contexto convertido para `SOUL.md`, `HERMES.md`/`.hermes.md` e ferramentas de memória.
- Crons convertidos para `cronjob`/`hermes cron`.
- Canais convertidos para o gateway Hermes.
- Curso, exemplos, templates, FAQ e cheatsheets revisados.
- Adicionados instalador idempotente e validador estático.
''',
'manifesto.md': '''# Manifesto do agente útil

Um agente pessoal só é valioso quando entrega resultados verificáveis sem tomar controle indevido.

Este kit defende cinco compromissos:

1. **Você mantém o controle.** Mudanças de escopo, credenciais e ações destrutivas são explícitas.
2. **O agente verifica.** “Pronto” significa saída real, arquivo existente ou serviço saudável.
3. **Contexto tem lugar certo.** Identidade em `SOUL.md`, regras no projeto, fatos duráveis na memória, procedimentos em skills.
4. **Automação respeita atenção.** Cron só envia algo quando há informação útil.
5. **Portabilidade.** O projeto não depende de um provedor ou modelo específico.

Hermes é a infraestrutura; este starter kit é um ponto de partida editável. A documentação oficial sempre prevalece: https://hermes-agent.nousresearch.com/docs/
'''
}
for name, content in root_files.items(): (DST/name).write_text(content, encoding='utf-8')

# Templates: remove old pseudo-native files and create Hermes equivalents.
for p in (DST/'templates').glob('*'):
    if p.is_file() and p.suffix in {'.md'}: p.unlink()
templates = {
'HERMES.template.md': '''# {NOME_PROJETO}\n\n## Objetivo\n{OBJETIVO}\n\n## Comandos de validação\n- `{COMANDO_TESTE}`\n\n## Regras\n- Leia antes de editar.\n- Preserve compatibilidade.\n- Não declare sucesso sem executar a validação.\n- Não exponha segredos.\n\n## Estrutura\nConsulte `MAPA.md`.\n''',
'SOUL.template.md': '''# Identidade\n\nNome: {NOME_AGENTE}\nPapel: {PAPEL}\nTom: {TOM}\n\n## Princípios\n- Ser direto, honesto e útil.\n- Admitir incerteza.\n- Verificar antes de concluir.\n- Pedir decisão quando houver trade-off relevante.\n- Respeitar privacidade e escopo.\n''',
'PERFIL-USUARIO.template.md': '''# Perfil de trabalho de {NOME_USUARIO}\n\n- Como chamar: {COMO_CHAMAR}\n- Idioma: {IDIOMA}\n- Fuso horário: {FUSO}\n- Contexto profissional: {CONTEXTO}\n- Preferências de comunicação: {PREFERENCIAS}\n\n> Para lembrança entre sessões, grave apenas fatos estáveis com a ferramenta `memory`.\n''',
'MAPA.template.md': '''# Mapa — {NOME_PROJETO}\n\n| Caminho | Função |\n|---|---|\n| `HERMES.md` | regras Hermes do projeto |\n| `content/` | entregáveis |\n| `docs/` | documentação |\n| `scripts/` | automações locais |\n| `archive/` | material substituído |\n\nAtualizado em {DATA}.\n''',
'CRONS.template.md': '''# Catálogo de automações\n\nDocumente intenção; gerencie jobs reais com `cronjob` ou `hermes cron`.\n\n| Nome | Schedule | Entrega | Condição de silêncio |\n|---|---|---|---|\n| {NOME} | {SCHEDULE} | origin | sem novidade útil |\n\nTodo prompt deve ser autocontido porque cada execução começa em sessão fresca.\n''',
'AGENTS.template.md': '''# Regras portáveis do projeto\n\nEste arquivo é opcional e lido no diretório de trabalho por Hermes, Codex, Claude Code e outros agentes. Para herança por subdiretórios exclusiva do Hermes, prefira `.hermes.md`/`HERMES.md`.\n\n- Rode `{COMANDO_TESTE}` antes de concluir.\n- Não altere credenciais.\n- Preserve o estilo existente.\n''',
'README.md': '''# Templates Hermes\n\n- `SOUL.template.md` → `$HERMES_HOME/SOUL.md` (identidade global)\n- `HERMES.template.md` → `HERMES.md` na raiz do projeto\n- `AGENTS.template.md` → `AGENTS.md` portátil e opcional\n- `PERFIL-USUARIO.template.md` → documento de projeto opcional; memória nativa usa a ferramenta `memory`\n- `MAPA.template.md` → `MAPA.md`\n- `CRONS.template.md` → catálogo humano; jobs reais ficam no scheduler Hermes\n\nNunca sobrescreva um arquivo preenchido sem backup e consentimento.\n'''
}
for name, content in templates.items(): (DST/'templates'/name).write_text(content, encoding='utf-8')
for name, title in {
    'template-material-didatico.html':'Material didático',
    'template-report-executivo.html':'Relatório executivo',
    'template-report.html':'Relatório técnico'
}.items():
    (DST/'templates'/name).write_text(f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title><style>body{{font:16px/1.6 system-ui;max-width:900px;margin:auto;padding:40px}}h1{{color:#7a5b10}}code{{background:#eee;padding:.15em .35em}}</style></head><body><h1>{title}</h1><p><strong>Projeto:</strong> {{{{PROJETO}}}}</p><p><strong>Data:</strong> {{{{DATA}}}}</p><h2>Objetivo</h2><p>{{{{OBJETIVO}}}}</p><h2>Evidências</h2><p>{{{{EVIDENCIAS}}}}</p><h2>Próximos passos</h2><p>{{{{PROXIMOS_PASSOS}}}}</p></body></html>''', encoding='utf-8')

# Examples.
for p in (DST/'exemplos').glob('*.md'): p.unlink()
examples = {
'README.md':'# Exemplos\n\nExemplos ilustrativos para Hermes. Não copie dados pessoais literalmente.\n',
'SOUL-amora.md':'# Identidade\n\nNome: Amora\nPapel: Chief of Staff digital\nTom: caloroso, direto e sem teatralidade\n\n## Princípios\n- Antecipar riscos sem tomar decisões irreversíveis.\n- Mostrar evidência antes de afirmar conclusão.\n- Separar fatos persistentes de progresso temporário.\n',
'HERMES-amora.md':'# Projeto Amora\n\n## Objetivo\nApoiar planejamento, criação de conteúdo e rotinas operacionais.\n\n## Regras\n- Entregáveis vão para `content/`.\n- Decisões importantes vão para `docs/decisoes/`.\n- Antes de concluir, valide links, datas e formato.\n',
'PERFIL-USUARIO-amora.md':'# Perfil de trabalho\n\n- Como chamar: Bruno\n- Idioma: português do Brasil\n- Preferência: respostas diretas, com próximos passos claros\n- Fuso: America/Sao_Paulo\n',
'MAPA-amora.md':'# Mapa\n\n- `HERMES.md`: regras do projeto\n- `content/`: entregáveis\n- `docs/`: decisões e referências\n- `scripts/`: automações\n- `archive/`: versões substituídas\n',
'CRONS-amora.md':'# Automações\n\n| Nome | Schedule | Regra |\n|---|---|---|\n| briefing diário | `0 9 * * *` | enviar só se houver compromissos ou mudanças relevantes |\n'
}
for name, content in examples.items(): (DST/'exemplos'/name).write_text(content, encoding='utf-8')

# Skill generator.
def skill(name, description, body, version='3.0.0'):
    return f'''---\nname: {name}\ndescription: "{description}"\nversion: {version}\nauthor: Starter Kit Hermes PT-BR\nlicense: MIT\nmetadata:\n  hermes:\n    tags: [starter-kit, pt-br]\n---\n\n# {name}\n\n{body.strip()}\n'''

skills = {
'onboarding-checklist': ('Use quando iniciar ou revisar a configuração do Hermes.', '''## Objetivo
Conduzir o onboarding sem sobrescrever configuração existente.

## Fluxo
1. Rode `hermes doctor` e `hermes status --all`; mostre o resultado.
2. Confirme o perfil/home ativo por `$HERMES_HOME` e `hermes config path`.
3. Verifique modelo com `hermes model`/`hermes auth` sem pedir segredo no chat.
4. Ofereça, um passo por vez: `wizard-agente`, `wizard-aluno`, `wizard-autonomia`, `wizard-workspace`, `wizard-conectar`, `wizard-whisper-quick` e `primeira-vitoria`.
5. Use a ferramenta `todo` para progresso da sessão, não um `MEMORY.md` improvisado.
6. Grave em memória apenas preferências e fatos estáveis, com consentimento quando aplicável.

## Critério de conclusão
`hermes doctor` sem bloqueios, skill carregável e uma tarefa real executada/verificada. Inicie nova sessão após instalar ou habilitar skills.'''),
'wizard-agente': ('Use quando definir identidade e regras do agente Hermes.', '''## Saídas
- `$HERMES_HOME/SOUL.md`: identidade global, somente com consentimento.
- `HERMES.md` ou `.hermes.md`: regras específicas do projeto.

## Entrevista mínima
Pergunte nome/papel, tom, limites e comportamento diante de incerteza. Mostre o rascunho antes de escrever. Preserve arquivos existentes; prefira patch. Valide tamanho (máximo prático de 20 mil caracteres para contexto de projeto) e explique que `SOUL.md` não substitui regras do projeto.'''),
'wizard-aluno': ('Use quando registrar preferências estáveis do usuário.', '''Colete como chamar, idioma, fuso, função, objetivos recorrentes e preferências de resposta. Separe:
- fatos duráveis → ferramenta `memory` no alvo `user`;
- contexto só deste projeto → documento local opcional;
- estado temporário/TODO → `todo` ou sessão, nunca memória persistente.
Leia de volta um resumo e permita correções.'''),
'wizard-autonomia': ('Use quando configurar aprovações e limites de autonomia.', '''Explique os modos `smart`, `manual` e `off`. Recomende `smart`. Só altere após escolha explícita:
```bash
hermes config set approvals.mode smart
```
Mantenha `security.redact_secrets` ativo. Não apresente `--yolo` como padrão. Depois verifique com `hermes config get approvals.mode` e informe que algumas mudanças exigem nova sessão.'''),
'wizard-workspace': ('Use quando criar contexto e estrutura de projeto Hermes.', '''1. Inspecione o diretório antes de criar algo.
2. Faça backup de arquivos que seriam substituídos.
3. Crie apenas o necessário: `HERMES.md`, `MAPA.md`, `content/`, `docs/`, `scripts/`, `archive/`.
4. Não crie `skills/` no projeto como local de instalação; use `$HERMES_HOME/skills/`.
5. Não use `MEMORY.md` como memória nativa.
6. Valide os arquivos e, se possível, inicie Hermes com `workdir` nessa raiz para confirmar carregamento.'''),
'wizard-conectar': ('Use quando conectar modelo, ferramentas, busca e gateway.', '''## Ordem segura
1. `hermes setup` e `hermes model`.
2. Credenciais por `hermes auth` ou caminho de ambiente oficial. Em hPanel, use Dashboard → Environment.
3. `hermes tools list` e habilite somente toolsets necessários.
4. `hermes gateway setup` para Telegram, WhatsApp ou outro canal.
5. `hermes gateway status` e `hermes logs errors` para validar.

Nunca peça ao usuário para colar tokens no chat. Mudanças de ferramentas exigem `/reset`/nova sessão.'''),
'wizard-whisper-quick': ('Use quando configurar transcrição de voz no Hermes.', '''Prefira configuração nativa de STT:
```bash
hermes config set stt.enabled true
hermes config set stt.provider local
```
Para local, instale `faster-whisper` apenas se ausente e com autorização. Alternativas: Groq, OpenAI, Mistral, ElevenLabs e DeepInfra. Segredos vão ao ambiente oficial. Valide com uma mensagem de voz real; não declare sucesso apenas porque a configuração foi salva.'''),
'primeira-vitoria': ('Use após o setup para entregar uma primeira vitória real.', '''Peça uma tarefa pequena e útil que possa ser verificada em até 15 minutos: criar um arquivo, resumir documento, pesquisar com fontes ou organizar um checklist. Confirme o formato, execute com ferramentas, valide o artefato e só então relate o resultado. Termine registrando apenas uma preferência estável que o usuário explicitou.'''),
'continuar-jornada': ('Use quando o usuário pedir para retomar o onboarding.', '''Use `session_search` para localizar a sessão anterior e `todo` para reconstruir o progresso. Não dependa de flags em arquivos locais. Mostre em uma frase onde parou, qual evidência existe e o próximo passo. Se não houver evidência, diga que não foi possível confirmar e ofereça a menor verificação.'''),
'gera-log-jornada': ('Use quando gerar relatório verificável do onboarding.', '''Reúna saídas reais de `hermes doctor`, status, skills e itens concluídos. Não inclua tokens, IDs privados ou conteúdo de memória. Marque cada item como confirmado, pendente ou não verificado. Salve em `content/relatorio-onboarding-YYYY-MM-DD.md` quando houver workspace e entregue o caminho.'''),
'backup-workspace-github': ('Use quando configurar backup Git privado do projeto.', '''Verifique `.gitignore` antes do primeiro commit. Exclua `.env`, chaves, `auth.json`, bancos, logs e sessões. Inicialize Git só com consentimento, use repositório privado e confirme remoto antes do push. Mostre `git status --short`, commit e resultado real do push. Não versionar todo `$HERMES_HOME`.'''),
'commit-diario-workspace': ('Use quando criar rotina diária de commit do projeto.', '''Pré-requisito: repositório privado já validado. Crie um job com `cronjob` ou `hermes cron` cujo prompt seja autocontido e cujo `workdir` seja a raiz do projeto. O job deve sair silenciosamente se não houver mudanças, bloquear arquivos sensíveis e nunca fazer force-push. Teste manualmente uma execução antes de ativar recorrência.'''),
'cron-resume-wizards': ('Use quando agendar lembrete respeitoso de retomada.', '''Crie job durável com `cronjob`; não use heartbeat. Prompt deve citar a finalidade, ler somente contexto permitido e enviar mensagem apenas quando houver etapa realmente pendente. Limite tentativas, ofereça opt-out e use `attach_to_session` quando o lembrete deve aceitar resposta. Liste e teste o job após criar.'''),
'seguranca-checklist': ('Use para auditar segurança e privacidade do Hermes.', '''Verifique: `security.redact_secrets`, `approvals.mode`, `privacy.redact_pii`, toolsets ativos, arquivos versionados, permissões do ambiente, gateway e destinos de cron. Não imprima valores secretos. Recomende `smart`, redaction ativa e menor privilégio. Produza achados com severidade, evidência e correção; não aplique mudanças de alto impacto sem autorização.'''),
'wizard-whatsapp': ('Use quando conectar WhatsApp ao gateway Hermes.', '''Use `hermes gateway setup` e escolha o adaptador WhatsApp disponível (Baileys ou Business Cloud API). Siga o assistente e a documentação oficial; não invente endpoints. Armazene credenciais no ambiente oficial. Valide com `hermes gateway status`, logs e uma mensagem de teste. Explique privacidade, allowlist e risco de grupos antes de habilitar.'''),
'brainstorming': ('Use antes de criar solução quando requisitos estão abertos.', '''Explore objetivo, usuário, restrições e critério de sucesso. Apresente 2–4 opções com trade-offs e peça uma decisão quando ela mudar o projeto. Não implemente durante brainstorming. Registre a decisão no documento do projeto, não em memória global salvo se for preferência estável.'''),
'writing-plans': ('Use quando transformar uma decisão em plano executável.', '''Crie plano com escopo, arquivos, passos pequenos, testes, riscos e rollback. Use caminhos reais depois de inspecionar o projeto. Não invente comandos. Para um plano persistente, salve em `.hermes/plans/` se o projeto adotar essa convenção.'''),
'executing-plans': ('Use quando executar um plano já aprovado.', '''Leia plano e contexto do projeto. Use `todo`, execute em lotes pequenos e valide após cada marco. Pare diante de divergência estrutural ou risco não previsto. Atualize o plano com evidências; não marque como concluído só porque o código foi escrito.'''),
'verification-before-completion': ('Use antes de afirmar que uma tarefa terminou.', '''Identifique a evidência necessária, rode a validação agora e leia a saída completa. Verifique requisitos, regressões, formato e segurança. Se não puder executar, declare explicitamente “não verificado” e explique o bloqueio. Nunca substitua saída real por resultado plausível.''')
}

for p in DST.glob('skills/**/SKILL.md'):
    name = p.parent.name
    if name not in skills:
        raise RuntimeError(f'Skill sem conteúdo: {name}')
    desc, body = skills[name]
    p.write_text(skill(name, desc, body), encoding='utf-8')

registry = '''# Registry de skills Hermes\n\nTodas as skills abaixo são instaladas em `$HERMES_HOME/skills/<nome>/`. Use `hermes skills list`, `hermes skills check` e uma nova sessão após instalação.\n\n'''
for name in sorted(skills): registry += f'- `{name}` — {skills[name][0]}\n'
(DST/'skills/_registry.md').write_text(registry, encoding='utf-8')
for sub in ['starter','operacional','planejamento','canais']:
    names = sorted(p.parent.name for p in (DST/'skills'/sub).glob('*/SKILL.md'))
    (DST/'skills'/sub/'_registry.md').write_text(f'# Skills: {sub}\n\n' + ''.join(f'- `{n}`\n' for n in names), encoding='utf-8')

# Rewrite evals to valid, current expectations.
for p in DST.glob('skills/**/evals/evals.json'):
    name = p.parent.parent.name
    data = {"skill": name, "version": "3.0.0", "evals": [{
        "name": "fluxo-hermes-seguro",
        "prompt": f"Execute a skill {name} em um ambiente Hermes já parcialmente configurado.",
        "success_criteria": ["preserva configuração existente", "usa comandos Hermes válidos", "não expõe segredos", "valida antes de concluir"]
    }]}
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# Onboarding references, each intentionally short and Hermes-native.
refs = {
'arquivamento-pos-jornada.md':'# Arquivamento\n\nMova somente materiais do kit que o usuário autorizar para `archive/starter-kit-hermes/`. Skills instaladas permanecem em `$HERMES_HOME/skills`. Verifique links antes e depois.\n',
'arquivos-raiz.md':'# Arquivos de contexto\n\n- `$HERMES_HOME/SOUL.md`: identidade global.\n- `.hermes.md`/`HERMES.md`: regras hierárquicas do projeto.\n- `AGENTS.md`: regras portáveis, somente no cwd.\n- `MAPA.md`: navegação opcional.\n- Memória: ferramenta `memory`, não `MEMORY.md`.\n',
'aula-menus.md':'# Menu de aulas\n\nA0 visão da stack · A1 instalação · A2 interfaces · A3 kit · A4 Telegram · A5 identidade · A6 workspace · A7 memória · A8 skills · A9 cron · A10 segurança · A11 canais · A12 integrações · A13 multiagente · A14 dashboard/Kanban · A15 fechamento.\n',
'checklist-template.md':'# Checklist\n\n- [ ] `hermes doctor` executado\n- [ ] modelo/autenticação validados\n- [ ] identidade e contexto revisados\n- [ ] aprovações configuradas\n- [ ] skills instaladas e checadas\n- [ ] gateway opcional testado\n- [ ] primeira vitória entregue\n',
'comandos-canonicos.md':'# Comandos canônicos\n\n`hermes setup` · `hermes model` · `hermes doctor` · `hermes status --all` · `hermes config set` · `hermes tools` · `hermes skills list` · `hermes gateway setup` · `hermes cron list` · `hermes logs errors`.\n',
'dependencias.md':'# Dependências\n\nHermes instalado, Python e Git opcionais conforme tarefa. Gateways e provedores têm dependências próprias; confirme em `hermes doctor` e na documentação oficial antes de instalar.\n',
'manifesto-abertura.md':'# Abertura\n\nEste onboarding preserva o que já existe, explica cada mudança e exige evidência antes de concluir. Você pode pausar ou recusar qualquer etapa opcional.\n',
'mapa-aulas.md':'# Mapa de aulas\n\nConsulte `_curso/INDICE.md`. Cada aula separa conceito, prática, validação e próximo passo.\n',
'padrao-exemplos-opt-in.md':'# Exemplos opt-in\n\nExemplos são referência, nunca dados para copiar automaticamente. Antes de aplicar um exemplo, mostre o diff e peça consentimento se ele alterar identidade, memória, gateway ou cron.\n',
'principios-defensivos.md':'# Princípios defensivos\n\n1. Ler antes de escrever. 2. Backup antes de sobrescrever. 3. Menor privilégio. 4. Segredos fora do chat/Git. 5. Evidência real. 6. Sem comandos inventados. 7. Sessão nova após mudar toolsets/skills. 8. Documentação oficial prevalece.\n',
'prompt-upgrade-para-aluno-antigo.md':'# Upgrade de instalação existente\n\nInspecione `$HERMES_HOME`, liste conflitos de skills e proponha migração por diff. Não copie templates sobre `SOUL.md`, arquivos de contexto ou config. Use `hermes config check`, `hermes skills check` e `hermes doctor`.\n',
'sistema-de-mapas.md':'# Sistema de mapas\n\n`MAPA.md` é convenção humana opcional. Não é carregado automaticamente pelo Hermes; referencie-o em `HERMES.md` quando quiser que o agente o consulte.\n',
'sobre-o-kit.md':'# Sobre o kit\n\nStarter educacional independente, compatível com Hermes Agent. Não substitui a documentação oficial nem pressupõe provedor, modelo ou hospedagem específicos.\n',
'wizard-header-template.md':'# Cabeçalho de wizard\n\nDeclare gatilho, pré-requisitos, ações, consentimentos, validação, rollback e critério de conclusão. Nunca dependa de estado oculto em `MEMORY.md`.\n'
}
refdir = DST/'skills/starter/onboarding-checklist/references'
for name, content in refs.items(): (refdir/name).write_text(content, encoding='utf-8')

# Course assets and lessons.
shared = DST/'_curso/aulas/_shared'
(shared/'tokens.css').write_text(''':root{--bg:#0b1020;--card:#151d33;--text:#eef2ff;--muted:#aab5d1;--accent:#d4a94e}body{margin:0;background:var(--bg);color:var(--text);font:18px/1.6 system-ui,sans-serif}.wrap{max-width:920px;margin:auto;padding:48px 24px}article{background:var(--card);padding:32px;border-radius:18px}h1,h2{color:#fff}code,pre{background:#080c17;border-radius:8px;padding:.15em .4em}pre{padding:16px;overflow:auto}a{color:#f2c866}.muted{color:var(--muted)}''', encoding='utf-8')
(shared/'footer.html').write_text('<footer><p>Starter Kit Hermes · documentação oficial: <a href="https://hermes-agent.nousresearch.com/docs/">hermes-agent.nousresearch.com/docs</a></p></footer>', encoding='utf-8')
(shared/'template.html').write_text('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><link rel="stylesheet" href="_shared/tokens.css"><title>{{TITLE}}</title></head><body><main class="wrap"><article>{{CONTENT}}</article></main></body></html>', encoding='utf-8')
lessons = {
'aula-00-visao-stack.html':('A0 · Visão da stack','Hermes separa modelo, agente, ferramentas, memória, skills, projeto, gateway e scheduler. Essa separação evita colocar tudo em um único arquivo de configuração.','hermes status --all'),
'aula-01-cases-3-agentes.html':('A1 · Três padrões de agente','Use uma sessão principal para trabalho geral, perfis para identidades isoladas e `delegate_task` para subtarefas. Para filas duráveis entre workers, use Kanban.','hermes profile list'),
'aula-01-setup-hermes.html':('A1 · Instalação','Instale pelo script oficial, rode o wizard e diagnostique antes de personalizar. Em hospedagem hPanel, variáveis são geridas no Dashboard → Environment.','hermes setup\nhermes doctor'),
'aula-02-cockpit.html':('A2 · Interfaces e cockpit','CLI/TUI, Desktop e Dashboard usam o mesmo núcleo. O Dashboard administra canais, memória, webhooks e perfis; `hermes sessions` inspeciona conversas.','hermes dashboard'),
'aula-03-starter-kit.html':('A3 · Starter kit','O instalador copia skills para o home do perfil sem tocar em credenciais ou identidade. Skills só entram no prompt na sessão seguinte.','bash scripts/install.sh\nhermes skills check'),
'aula-04-telegram.html':('A4 · Telegram','Crie o bot no BotFather, guarde o token no ambiente e configure pelo gateway. Valide status, logs e uma mensagem real; bots Telegram não são E2E.','hermes gateway setup\nhermes gateway status'),
'aula-05-identidade.html':('A5 · Identidade','`SOUL.md` define identidade global. `HERMES.md`/`.hermes.md` define regras do projeto. `AGENTS.md` serve para portabilidade e só é descoberto no cwd.','hermes config path'),
'aula-06-workspace.html':('A6 · Workspace','O projeto contém entregáveis, documentação e regras. Skills e memória do agente vivem no home do perfil, não dentro do projeto por obrigação.','pwd'),
'aula-07-memoria.html':('A7 · Memória','Use `memory` para fatos estáveis e `session_search` para histórico. TODOs e progresso temporário não são memória durável.','hermes memory status'),
'aula-08-skills.html':('A8 · Skills','Cada skill é uma pasta com `SKILL.md` e frontmatter válido. Instale, cheque, configure por plataforma e reinicie a sessão.','hermes skills list\nhermes skills check'),
'aula-09-crons.html':('A9 · Crons','Jobs rodam em sessões frescas: prompts precisam ser autocontidos. Use entrega silenciosa quando não houver novidade e teste o job manualmente.','hermes cron list\nhermes cron status'),
'aula-10-seguranca.html':('A10 · Segurança','Mantenha redaction de segredos ativa, aprovações em `smart`, toolsets mínimos e credenciais fora do Git. `--yolo` é exceção, não onboarding.','hermes config get approvals.mode'),
'aula-11-outros-canais.html':('A11 · Outros canais','O gateway suporta Discord, Slack, WhatsApp, Signal, Matrix, Email e outros por plugins. Cada canal tem permissões e riscos próprios.','hermes gateway setup'),
'aula-12-integracoes.html':('A12 · Integrações','Prefira toolsets nativos, skills e MCP. Configure credenciais no ambiente e valide cada integração com a menor operação possível.','hermes tools list\nhermes mcp list'),
'aula-13-multi-agente.html':('A13 · Multiagente','`delegate_task` é rápido e não durável. Perfis isolam contexto. Kanban coordena trabalho durável. Worktrees evitam conflito em código.','hermes profile list\nhermes kanban --help'),
'aula-14-mission-control.html':('A14 · Dashboard e Kanban','Use Dashboard para visão operacional, sessions para histórico, cron para automações e Kanban para fila multiagente.','hermes sessions list\nhermes cron list'),
'aula-15-fechamento.html':('A15 · Fechamento','Um harness saudável é pequeno, verificável e evolui por skills. Revise memória, jobs e toolsets periodicamente.','hermes doctor\nhermes curator status')
}
for fname,(title,concept,cmd) in lessons.items():
    body=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><link rel="stylesheet" href="_shared/tokens.css"><title>{title}</title></head><body><main class="wrap"><article><p class="muted">Curso Hermes Agent</p><h1>{title}</h1><h2>Conceito</h2><p>{concept}</p><h2>Prática</h2><pre><code>{cmd}</code></pre><h2>Validação</h2><p>Leia a saída real, corrija bloqueios e só então avance.</p><p><a href="../INDICE.md">Voltar ao índice</a></p></article></main></body></html>'''
    (DST/'_curso/aulas'/fname).write_text(body, encoding='utf-8')
(DST/'_curso/README.md').write_text('# Curso Hermes Agent\n\nAulas HTML autocontidas sobre instalação, contexto, memória, skills, gateway, cron, segurança e multiagente. A documentação oficial prevalece.\n', encoding='utf-8')
index = '# Índice do curso Hermes\n\n'
for fname,(title,_,_) in lessons.items(): index += f'- [{title}](aulas/{fname})\n'
(DST/'_curso/INDICE.md').write_text(index, encoding='utf-8')
trans = '# Transcrição resumida — Curso Hermes Agent\n\n' + '\n\n'.join(f'## {t}\n\n{c}\n\nPrática: `{cmd.replace(chr(10), "` e `")}`.' for t,c,cmd in lessons.values()) + '\n'
(DST/'_curso/transcricao-completa.md').write_text(trans, encoding='utf-8')

# Rewrite legacy cheatsheets as Hermes-native compact references.
cheatdir = DST/'archive/cheatsheets-legacy-v1.0'
cheats = {
'crons-do-seu-agente.md':'# Crons no Hermes\n\nUse `cronjob` ou `hermes cron`. Prompt autocontido, workdir explícito, teste manual e silêncio quando não houver novidade.\n',
'identidade-do-seu-agente.md':'# Identidade\n\n`SOUL.md` no home do perfil define identidade; `HERMES.md` define o projeto. Não misture preferências do usuário com regras operacionais.\n',
'integracoes-de-produtividade.md':'# Integrações\n\nAtive toolsets, skills ou MCP pelo Hermes. Guarde credenciais no ambiente oficial e faça smoke test sem expor segredo.\n',
'memoria-do-seu-agente.md':'# Memória\n\nFatos estáveis usam `memory`; histórico usa `session_search`; procedimentos usam skills; tarefas temporárias usam `todo`.\n',
'mission-control.md':'# Controle operacional\n\nDashboard + sessions + cron + logs + Kanban formam o cockpit operacional do Hermes.\n',
'multi-agente.md':'# Multiagente\n\nUse `delegate_task` para subtarefas, perfis para isolamento e Kanban para coordenação durável.\n',
'onboarding-do-seu-agente.md':'# Onboarding\n\nOrdem: doctor, modelo/auth, identidade, projeto, aprovações, skills, gateway opcional e primeira vitória verificada.\n',
'outros-canais.md':'# Canais\n\nConfigure com `hermes gateway setup`; aplique menor privilégio, allowlist e validação por canal.\n',
'skills-do-seu-agente.md':'# Skills\n\nInstale em `$HERMES_HOME/skills`, rode `hermes skills check` e abra sessão nova.\n',
'workspace-do-seu-agente.md':'# Workspace\n\nMantenha projeto separado do home do perfil. Regras em `HERMES.md`, entregáveis em `content/` e documentação em `docs/`.\n'
}
for name, content in cheats.items(): (cheatdir/name).write_text(content, encoding='utf-8')

# Installer and validator.
(DST/'scripts').mkdir(exist_ok=True)
install = r'''#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1
mkdir -p "$HERMES_HOME/skills"
installed=0; skipped=0
while IFS= read -r -d '' skillfile; do
  src="$(dirname "$skillfile")"; name="$(basename "$src")"; dst="$HERMES_HOME/skills/$name"
  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then printf 'SKIP %s (já existe)\n' "$name"; skipped=$((skipped+1)); continue; fi
  if [[ -e "$dst" ]]; then backup="$dst.backup.$(date +%Y%m%d%H%M%S)"; cp -a "$dst" "$backup"; fi
  rm -rf "$dst"; cp -a "$src" "$dst"; printf 'OK   %s\n' "$name"; installed=$((installed+1))
done < <(find "$ROOT/skills" -mindepth 2 -name SKILL.md -print0)
printf '\nInstaladas: %d · puladas: %d · home: %s\n' "$installed" "$skipped" "$HERMES_HOME"
printf 'Agora rode: hermes skills list && hermes skills check\nAbra uma nova sessão para carregar mudanças.\n'
'''
(DST/'scripts/install.sh').write_text(install, encoding='utf-8')
os.chmod(DST/'scripts/install.sh', 0o755)
validate = r'''from pathlib import Path
import json, re, sys
root=Path(__file__).resolve().parents[1]
errors=[]
for p in root.rglob('*'):
    if not p.is_file(): continue
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.webp','.7z','.zip'}: continue
    try: text=p.read_text(encoding='utf-8')
    except UnicodeDecodeError: continue
    low=text.lower()
    # O guia de migração cita nomes antigos deliberadamente; o validador contém os padrões de bloqueio.
    if p.name not in {'MIGRACAO-OPENCLAW-HERMES.md', 'validate.py'}:
        for banned in ('openclaw ', 'openclaw\n', '.openclaw', 'openclaw.json', 'docs.openclaw'):
            if banned in low: errors.append(f'{p.relative_to(root)}: referência residual {banned!r}')
    if p.name=='SKILL.md':
        if not text.startswith('---\n') or '\nname:' not in text or '\ndescription:' not in text:
            errors.append(f'{p.relative_to(root)}: frontmatter inválido')
    if p.suffix=='.json':
        try: json.loads(text)
        except Exception as e: errors.append(f'{p.relative_to(root)}: JSON inválido: {e}')
for p in root.rglob('*.md'):
    text=p.read_text(encoding='utf-8')
    for link in re.findall(r'\[[^]]+\]\(([^)]+)\)', text):
        if '://' in link or link.startswith('#') or link.startswith('mailto:'): continue
        target=(p.parent/link.split('#')[0]).resolve()
        if not target.exists(): errors.append(f'{p.relative_to(root)}: link ausente {link}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'OK: {sum(1 for p in root.rglob("*") if p.is_file())} arquivos validados')
'''
(DST/'scripts/validate.py').write_text(validate, encoding='utf-8')

print(DST)
