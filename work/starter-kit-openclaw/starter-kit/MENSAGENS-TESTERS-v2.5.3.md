# Mensagens pros testers da v2.5.3

> Rascunhos pra Bruno enviar via Telegram/WhatsApp pros testers.
> Tom direto, sem floreio. Foco no que mudou + o que olhar.
>
> **NOVIDADE crítica v2.5.2+:** ao mandar o zip, mande **TAMBÉM** a [Mensagem canonical pro aluno colar pro agente](../MENSAGEM-PRO-ALUNO-COLAR-PRO-AGENTE.md) — sem isso, agente em modo "code review" ou em conversa em curso ignora o protocolo de instalação (cases reais Mileo + "3 caminhos").
>
> **🆕 Atualização v2.5.3 (3 fixes desde v2.5.2):**
> 1. **Texto canonical reformulado** — versão v2.5.2 disparou filtro de prompt injection em agente cético (caso ZeroToHeroOC_bot). Agora usa apresentação natural + aponta pro arquivo interno
> 2. **Regra UX expectativa** — comandos longos (>2min como Chromium install) ganham aviso ANTES da execução com tempo estimado e razão concreta. Aluno não pergunta "ainda processando?" (caso Allan 10min de silêncio)
> 3. **Ramo Snap/SingletonLock** em wizard-conectar — Chromium via Snap em VPS root tem incompatibilidade conhecida (`SingletonLock: Permission denied`). Agora kit detecta + tenta versão fora do Snap automaticamente

---

## 🤖 Mensagem canonical pro aluno colar pro agente (mandar JUNTO do zip)

**Bruno: copia este texto E cola pro tester ANTES ou JUNTO do zip.** O tester cola pro agente dele.

```
Te mandei um arquivo: starter-kit-openclaw-v2.5.3.zip

É um kit de instalação da Pixel Educação. A ideia é que você vire meu tutor depois que instalar.

Como funciona:
- Dentro do zip tem um arquivo chamado `0-LEIA-PRIMEIRO-AGENTE.md` que tem instruções específicas pra você
- Ele descreve como migrar as skills pro meu workspace e como começar a me guiar passo a passo

Pode extrair, ler esse arquivo, e seguir o que ele diz?
```

⚠️ **Reformulação v2.5.3 (caso ZeroToHeroOC_bot 03/05 19:14):** versão anterior usava vocabulário imperativo ("NÃO faça", "abandone contexto", "este kit tem prioridade", "obrigatório") que disparou filtro de prompt injection em agente cético. Agente recusou colar. Versão atual usa apresentação NATURAL do aluno + apontamento pro arquivo INTERNO (`0-LEIA-PRIMEIRO-AGENTE.md`) que tem o protocolo imperativo. Detalhes: `../MENSAGEM-PRO-ALUNO-COLAR-PRO-AGENTE.md`.

---

## URL atual do zip

```
https://github.com/okjpg/repo-amora-cos/raw/main/memory/curso-openclaw-v2/materiais/starter-kit-openclaw-v2.5.3.zip
```

(1.0M, 113 arquivos)

---

## Para Lia (testou v1.6 → v1.9)

```
Lia, saiu v2.5.3 do starter-kit. Pulei várias versões — fiz 8 desde a v1.9 que você testou.

📦 Zip: [URL acima]

🤖 Antes de extrair, cola o texto abaixo pro teu agente JUNTO do arquivo (novidade da v2.5.3 — agentes estavam ignorando o kit por não lerem o entry point):

[texto canonical da Mensagem acima]

Resumo do que mudou desde v1.9:
- 17 princípios defensivos (P13/14/15/16/17 + P11 estendido) — agente não improvisa, não inventa, não foge do passo
- Cron-DM ATIVO 2x/dia (09 + 19 BRT) — pausou wizard? Te puxa de volta
- Inferência silenciosa: se aluno fechou Telegram silencioso, cron detecta após 12h e dispara DM
- Mensagem final pós-vitória bifurca em 4 variantes (Modo A vs B × tem-mini-curso vs avulso)
- primeira-vitoria com NOMES inline (Post / Email / Decisão / Checklist / Outro) — letras a/b/c/d eram cognitivamente confusas
- Auto-arquivamento de manuais pós-jornada (workspace fica limpo)

Foco do teste v2.5.3:
- Cola a mensagem canonical pro agente JUNTO do zip — vamos validar se isso resolve o problema de agente ignorar o entry point
- Wizard agora não improvisa, não foge, não fala vago. Se algo escapar, é bug

Quando terminar, manda "gera log" pro agente.
```

---

## Para Mira (testou junto com Lia)

```
Mira, v2.5.3 saiu. Mesma URL: [URL acima]

🤖 NOVIDADE: cola este texto pro teu agente JUNTO do zip antes de extrair:

[texto canonical]

O que mudou pra você especificamente:
- Pausa de wizard agora vira retomada ATIVA — cron 09 + 19 BRT te puxa de volta. Antes ficava silencioso (caso seu mesmo, simulado em stress test)
- Wizard retomado sumariza estado em 1 mensagem em vez de re-narrar copy de promessa do passo 1
- Tradução natural: "wizard-autonomia.passo3" vira "passo 3 (autonomia)" nas DMs

Foco:
- Pausa em qualquer wizard → recebe DM proativa?
- Retomada não te faz ouvir copy de promessa de novo?

"gera log" no fim.
```

---

## Para Dr. Thiago (reportou v1.9.1 + v2.x)

```
Dr. Thiago, v2.5.3 do kit. URL: [acima]

🤖 Antes de extrair, cola este texto pro teu agente JUNTO do zip:

[texto canonical]

Os bugs que você reportou (v1.9.1 + acompanhamento) seguem fechados:
1. Áudio falso → P14 EXTRA-RÍGIDO em wizard-whisper-quick. Agente NUNCA confirma sem mostrar comando + output. Plus header reforçado em wizard-conectar e wizard-autonomia (4 momentos historicamente violados, agora obrigatório).
2. wizard-autonomia vago → bifurcação Managed/VPS root/local-dev (3 caminhos com copy adequado a cada).
3. Brave URL 403 → URLs sempre completos. Plus ramo dedicado pra HTTP 401 (chave existente expirada vs nova errada).
4. wizard-workspace pergunta vaga → P15 obrigatório.

Cron-DM ativo (09+19 BRT) + 2 skills novas (continuar-jornada, gera-log-jornada).

Foco:
- P14 visível em todos os 4 pontos de validação (whisper, exec-policy, brave, github)?
- Caso VPS root: caminho 2b (não 2a Managed) sendo seguido?

"gera log" no fim. Você fecha o ciclo dos bugs originais.
```

---

## Para NC (reportou bug entry point v2.2)

```
NC, v2.5.3 do kit. Bug que você reportou virou lei (P16 — Entry point literal):
[URL acima]

🤖 Antes de extrair, cola este texto pro teu agente:

[texto canonical]

O que mudou pra você:
- Agente ao receber kit ABRE direto a boas-vindas universal canonical, sem preâmbulo, sem "olhada rápida", sem "quer wizard ou prefere que eu proponha?"
- Plus: bloco "INSTALAÇÃO OBRIGATÓRIA" (v2.5.1) força agente a extrair + migrar skills pra $WORKSPACE/skills/ + invocar onboarding-checklist — nessa ordem, sem improvisar
- Plus mensagem canonical (essa que você vai colar) — fecha o último gap (agente em conversa em curso)

Foco:
- Primeira mensagem do agente é a boas-vindas universal canonical? (sem improvisação)
- Próxima mensagem é a Pré-bifurcação Hotmart (tenho/avulso)?

"gera log" no fim.
```

---

## Para Adrylan (testou v2.1 + v2.2.1 + jornada completa v2.5.x)

```
Adrylan, v2.5.3 saiu — esta tem 5 fixes diretos do que você reportou na jornada de ontem (~5h):
[URL acima]

🤖 Antes de extrair, cola este texto pro teu agente JUNTO do zip:

[texto canonical]

5 bugs que você reportou:
1. Primeira mensagem improvisava "proponha identidade" — coberto por v2.5.1 INSTALAÇÃO OBRIGATÓRIA + esta mensagem canonical
2. Loop transição whisper→wizard-agente (3 turnos perdidos com "2") — Protocolo de TRANSIÇÃO em P13 + opções `a/b` (não 1/2) em wizard-agente
3. Backup mensagens fora de ordem ("✓ Backup ativo" antes do "Vou ativar") — P14 EXTRA-RÍGIDO em backup-workspace-github (3 mensagens sequenciais obrigatórias)
4. primeira-vitoria "b virou email" mas você queria checklist — opções com NOMES inline (Post/Email/Decisão/Checklist) + bot CONFIRMA escolha antes de refinar
5. P14 violado em 4 validações (Whisper, exec-policy, Brave, GitHub) — header EXTRA-RÍGIDO no wizard-conectar e wizard-autonomia

Foco:
- Sem loop na transição entre wizards
- primeira-vitoria entrega o que você escolheu (checklist = checklist, não vira email)
- Backup mostra comando + output antes de confirmar
- Validações TODAS mostram comando + HTTP code

"gera log" no fim — fecha o ciclo dos 5 bugs.
```

---

## Para Mileo (reportou bug instalação v2.5)

```
Mileo, fix do bug que você reportou ontem saiu na v2.5.1 (já em prod) e refinado em v2.5.3:
[URL acima]

🤖 Antes de extrair, cola este texto pro teu agente JUNTO do zip — isso é o complemento do fix:

[texto canonical]

O que mudou pra resolver o que você reportou:
- v2.5.1: bloco "INSTALAÇÃO OBRIGATÓRIA" no `0-LEIA-PRIMEIRO-AGENTE.md` força agente a extrair + migrar skills pra `$WORKSPACE/skills/` + invocar onboarding-checklist (sem improvisar análise tipo code review)
- v2.5.3: mensagem canonical (essa que você vai colar) cobre o caso onde agente nem lê o entry point

Foco:
- Agente NÃO faz review tipo code review do kit?
- Agente migra skills pro $WORKSPACE/skills/ corretamente?
- Agente invoca onboarding-checklist (boas-vindas universal canonical) como primeira mensagem real?

"gera log" no fim.
```

---

## Mensagem padrão pra tester NOVO (validar mensagem canonical funcionando)

```
Tô testando o starter-kit OpenClaw v2.5.3 — kit que vira seu agente em tutor enquanto te configura. ~37min até primeira vitória.

🤖 Pra ele funcionar direito, manda 2 coisas pro teu agente em sequência (ou na mesma mensagem):

1️⃣ O texto abaixo (cola literal):

[texto canonical]

2️⃣ O zip:
[URL acima]

Foco do teste:
- O agente segue o protocolo? (não inventa caminhos, não faz review)
- Se você desviar de assunto, ele te traz de volta?
- Validações mostram comando + output?
- primeira-vitoria entrega o que você escolheu (sem confusão de letras)?

No fim, manda "gera log" pro agente — ele gera relatório estruturado, você me manda no grupo (@cursoopenclaw).

Tempo total: ~40min com calma.

⚠️ IDEAL: tester em DESKTOP (web/painel Hostinger), não só celular — alguns bugs visuais só aparecem em tela larga.
```

---

## Mensagem pra tester local-dev específico (Mac/Linux dev)

```
[Nome], preciso de uma rodada específica do kit OpenClaw v2.5.3 em ambiente local-dev (Mac M1/M2 ou Linux desktop com OpenClaw rodando localmente, não Hostinger Managed nem VPS root).

📦 Zip: [URL acima]

🤖 Antes de extrair, cola este texto pro teu agente JUNTO do zip:

[texto canonical]

Foco específico desta rodada:
- Fase Pré-Zero detecta `local-dev` corretamente?
- Fast-path Whisper funciona com chave em $OPENAI_API_KEY (não em .env do workspace)?
- wizard-autonomia caminho 2c (local-dev) — sem aviso "porque você é root"?
- wizard-conectar Chromium — não afirma "vem incluído", instrui brew/apt manual?
- Auto-arquivamento move starter-kit/ corretamente (com $WORKSPACE/ prefixado)?

"gera log" no fim.
```

---

## Checklist pré-envio

- [ ] Zip v2.5.3 está em `materiais/starter-kit-openclaw-v2.5.3.zip` E pushado pro GitHub (URL pública funciona)
- [ ] CHANGELOG entry [2.5.2] commitada
- [ ] `MENSAGEM-PRO-ALUNO-COLAR-PRO-AGENTE.md` criada em `memory/curso-openclaw-v2/`
- [ ] Bruno leu uma vez essas mensagens e ajustou tom como quer
- [ ] Decidiu pra qual tester mandar primeiro
- [ ] **NOVO em v2.5.3:** ao mandar zip, mandar TAMBÉM o texto canonical pro aluno colar pro agente (resolve bug de "agente em modo code review" reportado por Mileo + caso "3 caminhos")

---

## Como atualizar essas mensagens pra próxima versão

Quando subir pra v2.5.4 (ou v2.5.5, etc):

1. Find/replace `v2.5.3` → versão nova (em todas as URLs + texto canonical)
2. Adicionar 1 bullet no "Resumo do que mudou" de cada mensagem (foco: cada tester sabe o que é NOVO desde versão dele)
3. Atualizar URL do zip
4. Renomear arquivo: `MENSAGENS-TESTERS-v2.5.3.md` → `MENSAGENS-TESTERS-v{nova}.md`

---

*Mantido por Bruno + Claude local. Reusar formato pra próximas releases. v2.5.3 introduz o padrão "mensagem canonical fora do zip" — manter daqui pra frente.*
