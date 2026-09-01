# Mensagens pros testers da v2.2

> Rascunhos pra Bruno enviar via Telegram/WhatsApp pros testers que receberam versões anteriores.
> Tom direto, sem floreio, sem teatro de "você é especial". Foco no que mudou + o que olhar.

---

## Para Lia (já testou v1.6, v1.7, v1.8, v1.9)

```
Lia, saiu a v2.2 do starter-kit. Zip atualizado:
https://github.com/okjpg/repo-amora-cos/raw/main/memory/curso-openclaw-v2/materiais/starter-kit-openclaw-v2.2.zip

O que mudou desde a v1.9 que você testou:
- 4 princípios novos (13/14/15 + 11 estendido) explícitos NO TOPO de cada wizard — antes ficavam só no arquivo de referência, agente esquecia
- Cron-DM ATIVO (skill nova `cron-resume-wizards`): se você pausa um wizard, agente te puxa de volta no dia seguinte às 9h em vez de morrer silencioso
- 2 skills novas que você ainda não viu: `continuar-jornada` (resolve "wizard morreu pós-vitória") e `gera-log-jornada` (gera feedback estruturado pra você me mandar)

Se quiser testar de novo, foco no que tinha quebrado antes: agente fugia do passo, improvisava versão simplificada, fazia pergunta vaga. Tudo isso era P13/P14/P15 — agora é explícito.

Quando terminar, manda "gera log" pro agente — ele gera relatório estruturado da sua jornada, você cola no Tally ou no grupo.
```

---

## Para Mira (testou junto com Lia)

```
Mira, v2.2 do kit saiu. Mesma URL: https://github.com/okjpg/repo-amora-cos/raw/main/memory/curso-openclaw-v2/materiais/starter-kit-openclaw-v2.2.zip

Resumo do que mudou:
- Wizards agora SÃO guard rails — se você desviar de assunto no meio, agente anota a pergunta, te traz de volta, e só pausa se você desviar 3x seguidas (com lembrete proativo no dia seguinte)
- Smoke tests SEMPRE visíveis — agente mostra o comando que rodou + output literal antes de dizer "validei". Antes ele inventava resultado às vezes
- Mensagens canonical são literais — perguntas-âncora não viram improviso

O que olhar especificamente:
- O agente respeita o Cenário B (Caminho 2 — wizard review) que você testou? Sem improviso?
- Se você pausar no meio, recebe DM no dia seguinte?
- Smoke tests aparecem (com curl + HTTP code) ou ainda escapa?

Manda "gera log" no fim pra eu receber feedback estruturado.
```

---

## Para Dr. Thiago (reportou os bugs que viraram v2.1)

```
Dr. Thiago, saiu v2.2 do kit. Os bugs que você reportou agora viraram lei:
https://github.com/okjpg/repo-amora-cos/raw/main/memory/curso-openclaw-v2/materiais/starter-kit-openclaw-v2.2.zip

Os 4 problemas que você levantou na v1.9.1:
1. **Áudio falso (wizard-whisper-quick)** → P14 obrigatório agora. Agente SÓ pode dizer "validei" depois de mostrar `curl` + output literal. Se não rodou, ABORTA. Não tem mais alucinação.
2. **wizard-autonomia vago** → P15 obrigatório nas 3 opções (conservador/moderado/yolo) — texto literal, sem reformular. Plus bifurcação Managed vs ROOT (sua VPS deve ir pelo caminho ROOT direto).
3. **Brave URL 403** → URLs sempre completos no wizard-conectar (com path + query params). Foi a causa-raiz do 403.
4. **wizard-workspace pergunta vaga** → P15 obrigatório na pergunta-âncora.

Bonus que veio depois:
- Cron-DM ativo: se você pausa wizard, agente te puxa de volta no dia seguinte 9h
- 2 skills novas: `continuar-jornada` (post-vitória) + `gera-log-jornada` (feedback estruturado)

Se puder retestar pelo menos os 4 pontos acima e me mandar log via "gera log", você fecha o ciclo do bug pra mim.
```

---

## Mensagem padrão pra tester novo (validar guard rail funcionando)

```
Tô lançando o starter-kit OpenClaw v2.2 — kit que ensina seu agente IA a ser tutor enquanto te configura. ~37min até primeira vitória.

Estou em busca de testers que NUNCA viram versões anteriores — preciso de olhar fresco em 4 coisas:
1. O agente segue o passo (não foge pra outro tema)? Se você desviar, ele te traz de volta?
2. Quando agente diz "validei", ele mostra evidência (comando + output)?
3. Mensagens dele são consistentes (canonical) ou parecem improviso a cada vez?
4. Se você pausa um wizard, recebe lembrete depois?

Zip: https://github.com/okjpg/repo-amora-cos/raw/main/memory/curso-openclaw-v2/materiais/starter-kit-openclaw-v2.2.zip

No fim, manda "gera log" pro agente — ele gera relatório estruturado, você me manda no grupo do curso (@cursoopenclaw, marca pra mim).

Tempo total: ~40min com calma.
```

---

## Checklist pré-envio

- [ ] Zip v2.2 está em `materiais/starter-kit-openclaw-v2.2.zip` E pushado pro GitHub (URL pública funciona)
- [ ] CHANGELOG entry [2.2] commitada
- [ ] Eu (Bruno) li uma vez essas mensagens e ajustei o tom como quero
- [ ] Decidi pra qual tester mandar primeiro (Dr. Thiago é o melhor candidato — ele já reportou bugs específicos, fechamento de loop é forte)

---

*Mantido por Bruno + Claude local. Reusar formato pra próximas releases — só atualizar nome de versão e o que mudou.*
