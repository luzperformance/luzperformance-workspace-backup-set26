---
name: writing-plans
status: ATIVO
category: planejamento
owner: aluno
version: 1.0
mode: guided
estimated_time: 10-30min (varia por complexidade)
model_compatible: [gpt-5, gpt-5.5, claude-sonnet-4, claude-opus-4]
description: Use AFTER brainstorming, BEFORE coding/building. Transforms a brainstorm output into an executable plan with concrete tasks, dependencies, and verification criteria. Adapted from obra/superpowers (writing-plans skill). Plans are documents, not chat — they survive sessions and let agent loop independently.
source: https://github.com/obra/superpowers (skill: writing-plans)
---

## Contrato Hermes desta skill

- Use as ferramentas nativas do Hermes (`read_file`, `write_file`, `search_files`, `web_search`, `cronjob`, `memory` e `skill_manage`) em vez de comandos ou serviços de outra plataforma.
- Trate `$HERMES_HOME` como a raiz do perfil. Skills ficam em `$HERMES_HOME/skills/`; credenciais ficam em `$HERMES_HOME/.env`; configurações são alteradas com `hermes config set`, nunca por edição manual do YAML.
- Para reter estado entre sessões, registre apenas fatos duráveis com a ferramenta `memory`; para estado de projeto, use arquivos no diretório de trabalho definido pelo aluno.
- Qualquer comando que tenha efeito externo, altere integrações, crie cron ou reduza aprovações exige confirmação explícita do aluno e verificação após a ação.
- Não alegue que uma integração, pesquisa, backup ou tarefa agendada funcionou sem apresentar a saída real da ferramenta ou comando que a verificou.


# Writing Plans — Plano Executável Antes de Começar

## Promessa

Pega a saída do brainstorming (problema + solução proposta) e transforma em PLANO EXECUTÁVEL: tarefas concretas, dependências mapeadas, critérios de sucesso por etapa.

Plano vira ARQUIVO no workspace (`notas do projeto em projects/{nome}/PLAN.md`). Sobrevive sessões. Agente lê e executa sem precisar de hand-holding.

Adaptado de [obra/superpowers](https://github.com/obra/superpowers) — originalmente pra software, aplicável a qualquer projeto multi-etapa.

## Quando usar

**Use APÓS brainstorming, ANTES de:**
- Construir feature nova de skill
- Implementar workflow complexo (3+ etapas)
- Migração de algo existente
- Lançamento (produto, conteúdo, evento)

**NÃO use pra:**
- Tarefa one-shot sem etapas
- Decisão pontual (vai pra `notas do projeto em decisoes/`, não plan)

## Estrutura do plano

```markdown
# Plano: {Nome do projeto}

> Criado em {data}. Status: {planejamento|execução|completo|pausado}.

## Objetivo

(1 parágrafo. Resultado concreto que você quer alcançar.
 Não "usar tecnologia X" — RESULTADO.)

## Sucesso = (critérios verificáveis)

- [ ] {critério 1 — concreto, mensurável}
- [ ] {critério 2}
- [ ] {critério 3}

## Tarefas

### Fase 1: {nome}

- [ ] **T1.1** — {descrição}
  - Verificação: {como vai saber que terminou}
  - Estimativa: {Xmin/h}
  - Depende de: nenhuma

- [ ] **T1.2** — {descrição}
  - Verificação: ...
  - Estimativa: ...
  - Depende de: T1.1

### Fase 2: {nome}

- [ ] **T2.1** — ...

## Dependências externas

- {API, serviço, pessoa que precisa fazer algo antes}

## Riscos

- {risco 1} — mitigação: {como evitar/reagir}

## Estado atual

(Atualizado conforme execução. Lista o que tá feito, em progresso, bloqueado.)

---

*Atualizar este arquivo conforme execução. Não criar arquivo novo — versionar este.*
```

## Como invocar

Manda no chat:

```
"Roda writing-plans pra: {projeto}.

Brainstorming já feito (em notas do projeto em decisoes/{data}.md).

Quero plano executável."
```

Agente vai:

1. Ler o brainstorming
2. Te perguntar 3-5 coisas pra refinar (escopo, prazo, recursos)
3. Gerar plano seguindo template acima
4. Salvar em `notas do projeto em projects/{nome}/PLAN.md`

## Princípios do plano

### 1. Tarefas atômicas

Cada T deve ser executável em <2h. Se não cabe em 2h, quebra em sub-tarefas.

❌ "Configurar integração Notion completa"  (muito amplo)
✅ "Configurar Notion API token + validar com call de teste"
✅ "Criar mapeamento de campos USER.md → propriedades do database Notion"
✅ "Implementar sync bidirecional (Notion → workspace + workspace → Notion)"

### 2. Verificação por tarefa

Cada T tem critério de "como sei que terminou". Sem isso, agente não sabe quando parar/seguir.

❌ "Implementar X"  (quando termina?)
✅ "Implementar X até que `curl /api/x` retorne 200 com JSON esperado"

### 3. Dependências mapeadas

Mostrar T1.2 depende de T1.1 evita execução paralela quebrada.

### 4. Estimativa honesta

Se você acha que vai dar 2h, escreve 4h. Sempre escala 2x. Se errar pouco, melhor que estourar.

### 5. Estado vivo

Plano não é doc estático. É arquivo VIVO. Conforme executa, atualiza:

- `[ ]` → `[x]` quando termina
- `[ ]` → `[~]` quando começou mas não terminou
- `[ ]` → `[!]` quando bloqueado (com nota explicando)
- Adicionar T descobertas mid-execução (não esconder escopo)

## Adaptação pro Starter Kit

A versão original do superpower é mais detalhada (especificação de testes, refactors, etc). Esta versão simplifica pra projetos que aluno típico de starter-kit faz: launches, integrações, configs complexas.

Se quer versão completa: https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md

## Princípios herdados

- **Princípio 5 (atualizar estado):** PLAN.md é arquivo vivo, atualiza durante execução.
- **Princípio 8 (logging):** decisões importantes do plano vão em `notas do projeto em decisoes/`.

## Critérios de sucesso

- [ ] Plano salvo em `notas do projeto em projects/{nome}/PLAN.md`
- [ ] Tarefas são atômicas (cada uma <2h)
- [ ] Cada tarefa tem critério de verificação
- [ ] Dependências entre tarefas estão mapeadas
- [ ] Aluno sabe a próxima ação concreta

## Referências

- Skill original: https://github.com/obra/superpowers
- Skill complementar: `executing-plans` (executa o plano)
- Skill complementar: `verification-before-completion` (valida que terminou)

## Status

✅ ATIVO desde v1 do Starter Kit (02/05/2026) — versão curada/simplificada do superpower original.
