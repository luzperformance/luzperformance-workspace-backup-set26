---
name: heygen-avatar-reels
description: Use when Vinícius manda criativo HeyGen ou pede roteiro.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [heygen, reels, avatar, roteiro, instagram]
    related_skills: [humanizer]
---

# HeyGen avatar reels (Luz Performance)

Classe: analisar e reescrever talking-head 9:16 do gêmeo digital no HeyGen. Não é geração de imagem, não é carrossel, não é YouTube longo.

Antes de qualquer peça: USER.md (tom, vocabulário, NUNCA receita). Humanizer só como filtro anti-slop — a voz é a do profissional retratado e autorizado, não a do humanizer.

## When to Use

- Tópico Criativos + menção a HeyGen / gêmeo digital
- Link de pasta Drive com mp4/srt de avatar
- "analisa esses vídeos" / "reescreve os roteiros" / "pra eu passar no heygen"

## Passos

1. **Inventário, não dump.** Listar arquivos. Clones do mesmo master (ex.: `comuns4`, `with_captions`, `(1)`) → abrir **um** por peça. Registrar o critério.
2. **Fonte de texto, nesta ordem:** SRT na pasta → caption queimada (crop do terço inferior + frames a cada 4–8s) → transcrição de áudio se o ambiente tiver modelo. Não inventar falas de vídeo sem fonte.
3. **Pasta Drive pública (sem OAuth):** IDs vêm do HTML (`aria-label` + `ssk='5:auSv138:FILEID'`). Download: `gdown.download(id=FILE_ID, output=path)` — sem `fuzzy`. Pasta: `https://drive.google.com/drive/folders/<id>?usp=sharing`.
4. **Ver o vídeo de verdade.** ffprobe (duração, 1080x1920, 25fps típico) + frames em 0.3s, 2s, 5s, meio, fim. Analisar look, caption na tela, expressão no frame 0, overlays.
5. **Diagnóstico curto:** o que segura, o que mata, template. Sem menu de opções. Sem emoji.
6. **Checar completude e repetição.** Se o roteiro chegou truncado, registrar literalmente como incompleto e pedir a continuação — nunca completar ou renderizar. Antes de abrir uma nova tese, comparar com os roteiros HeyGen já existentes e propor um ângulo complementar quando houver duplicidade.
7. **Reescrita = artefato colável.** Um arquivo por peça em `content/drafts/heygen/NN-slug.txt`. Bloco `COLA ISTO` + 3 linhas de `CAPTION`. Como colar: `content/drafts/heygen/00-como-colar.md`.
8. **Não reescrever no escuro.** Sem SRT e sem caption legível → não inventa o roteiro; pede o arquivo ou pula.

## Formato COLA ISTO (HeyGen Script)

- Frases curtas, vocabulário do USER (TPC, eixo, hematócrito, TRAVERSE, redução de danos).
- 45–60s. Se passar de 65s no HeyGen, cortar o parágrafo antes do CTA.
- Hook 0–3s com corte ou número. 1 ideia por vídeo. Lista de 3 erros ok; manifesto de 90s não.
- CTA só consultoria / link na bio. **Nunca receita. Nunca posologia.**
- Caption nativa sempre (3 linhas). Reel mudo sem texto morre.
- Zero tag de TTS no script: nada de `[sarcastic]`, `[thoughtful]`, stage directions. Isso vaza no áudio.
- Sem "Não Não", sem duplicação de síntese.

Template: `templates/cola-isto.txt`.

## Look (trava um)

Master atual: **Roleta** — close, fundo escuro, blazer. Um gêmeo só. Cardigan mostarda / suéter terracota / blazer misturados = três identidades. Não recomenda looks novos no mesmo lote.

## Análise (o que cobrar)

- Identidade visual inconsistente
- Caption ausente vs queimada
- SRT com prompt de TTS ou typo (infato, universals)
- Sorriso no frame 0 em tema grave (infarto, morte)
- CTA genérico ("salva esse vídeo agora") vs Luz
- Tom CDF/coaching ("está matando milhares") vs médico de emergência + redução de danos

## Pitfalls

- **Orientação do AI Agent em screenshot não é chute para rebater.** Quando Vinícius trouxer uma resposta do agente/UI da HeyGen sobre créditos, prévia, SSML ou fluxo do editor, primeiro leia literalmente e responda em cima do que ela diz. Não contradizer com ressalvas genéricas sem evidência; se houver dúvida real, separar claramente o que está confirmado no screenshot do que precisa ser validado no produto.
- Telegram corta arquivo >20 MB. Pedir recorte, link Drive/YouTube, ou 720p. Não ficar pedindo o mesmo arquivo.
- Pasta Drive sem `?usp=sharing` parece login wall; com sharing o HTML lista os arquivos.
- `gdown.download(..., fuzzy=True)` quebra em gdown 6.x.
- Não misturar clones na análise — polui o diagnóstico.
- Não improvisar tom. USER.md manda: papo reto, sem clichê coaching, sem emoji.
- Entrega no chat: os roteiros coláveis. Arquivo em `content/drafts/heygen/` é registro, não substitui o texto na resposta.
- **Parada imediata:** se o usuário disser “pare”, “cancela”, “peraí” ou avisar que ainda vai mandar material, congelar a operação — não continuar com texto acumulado, não fazer pré-voo e não iniciar render. Retomar só quando o insumo chegar ou ele reautorizar. Se um job pago já tiver sido enviado, dizer isso de forma explícita.
- **Nunca submeter render pago por padrão.** O script de render roda em modo “não submetido” sem uma flag explícita (`--submit`); mesmo com a flag, bloqueia localmente enquanto voz e assets não estiverem validados. Um teste que prova que a execução padrão não envia job é mais barato que um render indesejado — e render disparado depois de um “peraí” custa confiança, não só crédito.
- **Nunca afirmar “não houve cobrança” sem auditoria.** O que a resposta prova é que nenhum job foi criado (sem `202`, sem `job_id`, sem `polling_url`). Saldo só se confirma consultando créditos.

## Identidade, voz e credenciais

Antes de preparar ou enviar um render com alguém diferente do Dr. Vinícius, confirmar explicitamente:

1. A pessoa na foto é o avatar nominal da peça.
2. O `voice_id` é dessa pessoa ou há autorização explícita dela para este vídeo.
3. Toda credencial profissional ou alegação clínica narrada pertence ao profissional retratado — nunca copiar a trajetória do solicitante ou da marca por associação.

Se qualquer ponto estiver pendente, marcar o rascunho como **PENDÊNCIA OBRIGATÓRIA** e não publicar mídia temporária, fazer pré-voo nem enviar job. Uma foto pode ser tecnicamente utilizável e ainda visualmente errada para a tese; separar essas duas avaliações e recomendar nova referência quando expressão, roupa ou luz conflitarem com o tema.

## Avatar IV via OpenRouter

Para renderizar vídeo com o Avatar IV sem usar uma chave HeyGen separada:

- Modelo: `heygen/avatar-iv`.
- Endpoint: `POST https://openrouter.ai/api/v1/videos` — **não** é o endpoint de Chat Completions.
- Autenticação: `OPENROUTER_API_KEY`, mantida apenas no `.env`; nunca pedir nem expor chave no chat.
- A geração é assíncrona: enviar o job, consultar até finalizar e baixar o vídeo retornado.
- A conta OpenRouter precisa ter saldo. Gerar vídeo é ação externa com custo: confirmar com Vinícius imediatamente antes do envio do job.
- Se Vinícius disser “inclui a chave”, não pedir nem exibir chave no chat: usar apenas a `OPENROUTER_API_KEY` já configurada no `.env` e validar seu estado com uma requisição de leitura. Reportar somente “válida”, “ausente” ou o código de erro.
- Fazer o pré-voo com duas fontes: `GET https://openrouter.ai/api/v1/videos/models` para resolução, proporção, duração, preço e passthroughs vigentes; e a página atual do modelo para confirmar modalidades. O catálogo de vídeo pode não listar `input_modalities`, mas a página do Avatar IV confirma foto + faixa de áudio fornecida para lip-sync direto. Não concluir que áudio não é aceito só pela omissão no catálogo.
- Para referência visual e áudio, o provedor precisa buscar URLs HTTPS públicas, estáveis e diretamente baixáveis. Caminho local não serve: pedir autorização antes de publicar mídia privada temporariamente e verificar `200` com `Content-Type` adequado para os dois antes de criar o job.
- Estimar custo pela duração exata do recorte (`ffprobe`) vezes a tarifa por segundo vigente; a estimativa não substitui a cobrança final.
- Se o POST retornar `401`, não repetir: corrigir a chave no `.env` e validar por leitura. Se retornar `402 Insufficient credits`, nenhum job foi criado: orientar recarga em `https://openrouter.ai/settings/credits` e só reenviar após nova ordem do Vinícius.
- **Onde a voz entra no payload:** para roteiro em texto, a voz vai em `provider.options.heygen.voice_id`. Mandar `provider.heygen.voice_id` (sem o nível `options`) devolve `400` com `avatar-iv requires provider.options.heygen.voice_id when using a text prompt (script)`. Sem áudio fornecido e sem `voice_id`, o provedor usa o TTS dele — isso não é a voz clonada de ninguém.
- **`voice_id` não atravessa contas.** Um ID vivo na conta HeyGen direta pode voltar `400 invalid_parameter` / `Voice not found` pela rota OpenRouter, porque o catálogo consultado é o do provedor. Não repetir o POST com o mesmo ID e não cair para voz genérica: a saída correta é pedir áudio autorizado da pessoa da foto para lip-sync ou, se o dono autorizar, integrar a API HeyGen da conta dona da voz.
- **Áudio fornecido é fala literal, não amostra de voz.** Um áudio que narra outro roteiro não vira clonagem para a peça atual. Se conteúdo e duração não batem com a peça, o insumo está errado — pedir a gravação correspondente em vez de recortar para caber.
- Planejar Avatar IV como talking-head: mandar somente fala limpa ao modelo. Direções de cena não entram no script; quando a ideia depende de caminhada, troca de locação, câmera recuando ou cortes, simplificar para uma tomada de busto ou produzir cenas independentes.
- Foto 3:4 é utilizável em 9:16 quando o rosto está centralizado, mas exige reenquadramento. Preferir cabeça e ombros, olhar frontal e boa luz.
- Em conteúdos clínicos, checar termos e alegações históricas antes de renderizar. PCT é termo de uso documentado; não apresentar TPU como nomenclatura médica oficial.

### Áudio de referência e duração curta

Quando Vinícius mandar **áudio + foto** e definir uma duração, esses são os insumos do render. Não trocar para TTS, reescrever o áudio ou voltar a discutir o roteiro sem necessidade.

1. Rodar `ffprobe` no áudio e salvar uma cópia de trabalho; nunca cortar o original.
2. Para um limite de 30 s, criar um recorte reencodado (`ffmpeg -i input -t 30 -c:a aac output.m4a`) e verificar a duração com `ffprobe`. Se ele não disser qual trecho quer, usar os primeiros 30 s somente quando o corte terminar numa frase completa; caso contrário, pedir que indique o trecho ou escolher o primeiro fechamento de frase dentro do limite.
3. Transcrever o recorte que será renderizado, não apenas o áudio integral. A transcrição confirma o conteúdo e impede um vídeo que termina no meio da ideia.
4. Em conteúdo clínico, validar as alegações da fala antes de renderizar. Lip-sync preserva exatamente o áudio: uma revisão textual em separado não corrige uma afirmação problemática. Se houver claim clínico impreciso, recortar outro trecho ou pedir uma nova gravação.
5. Publicar foto **e áudio** em URLs HTTPS temporárias, diretamente baixáveis; checar `200` e o `Content-Type` correto para os dois antes de enviar o job.
6. Se o pedido for apenas “N segundos com aquela foto”, executar esse pacote e responder com o resultado ou com o bloqueio material. Não reabrir opções criativas nem devolver um roteiro longo.
7. Para `heygen/avatar-iv`, quando Vinícius define uma duração inteira curta e o recorte de áudio corresponde a ela, enviar também `duration` com esse inteiro (ex.: `10`). Em 2026-09-18, isso foi aceito mesmo com `supported_durations: null` no catálogo. É uma exceção confirmada para este modelo, não uma regra para todos os provedores.
8. Se ele pedir “os mesmos N segundos com esta imagem”, reutilizar o **arquivo de áudio já verificado**, mas criar um novo job pago e uma nova URL temporária da foto. Salvar a nova referência em `content/drafts/heygen/assets/` com nome descritivo, validar seu `200`/tipo MIME e adaptar o prompt à roupa e ao ambiente realmente presentes. Não reutilizar o vídeo nem assumir que a foto antiga continua sendo a desejada.
9. Se a expressão da foto conflitar com o tom da fala — por exemplo, um sorriso leve num tema clínico grave — orientar explicitamente uma expressão neutra e focada no `prompt`/`motion_prompt`. Isso preserva a identidade e evita trocar o áudio ou burocratizar uma decisão criativa pequena.

Veja `references/avatar-iv-openrouter.md` para o fluxo, os limites de cena e as fontes clínicas; e `references/avatar-iv-render-verification.md` para o padrão verificado de submissão, polling, download, QA e troca de foto.

## Verificação

- Cada roteiro lê em voz alta sem tag, sem receita, com CTA de consultoria.
- Caption 3 linhas cabe no terço inferior.
- Peças sem fonte de fala não foram "completadas" com chute.
- Análise registrada em `content/archive/heygen-analise/` quando o lote for novo.

## Referências

- `templates/cola-isto.txt` — stub de arquivo por peça
- `references/drive-publico.md` — IDs e download de pasta pública
- `references/avatar-iv-openrouter.md` — integração, preparação de insumos e guardrails clínicos do Avatar IV via OpenRouter
- `references/avatar-iv-render-verification.md` — padrão validado de render curto com foto + áudio, polling, download e QA
