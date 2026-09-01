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

Antes de qualquer peça: USER.md (tom, vocabulário, NUNCA receita). Humanizer só como filtro anti-slop — a voz é a do Vinícius, não a do humanizer.

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
6. **Reescrita = artefato colável.** Um arquivo por peça em `content/drafts/heygen/NN-slug.txt`. Bloco `COLA ISTO` + 3 linhas de `CAPTION`. Como colar: `content/drafts/heygen/00-como-colar.md`.
7. **Não reescrever no escuro.** Sem SRT e sem caption legível → não inventa o roteiro; pede o arquivo ou pula.

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

- Telegram corta arquivo >20 MB. Pedir recorte, link Drive/YouTube, ou 720p. Não ficar pedindo o mesmo arquivo.
- Pasta Drive sem `?usp=sharing` parece login wall; com sharing o HTML lista os arquivos.
- `gdown.download(..., fuzzy=True)` quebra em gdown 6.x.
- Não misturar clones na análise — polui o diagnóstico.
- Não improvisar tom. USER.md manda: papo reto, sem clichê coaching, sem emoji.
- Entrega no chat: os roteiros coláveis. Arquivo em `content/drafts/heygen/` é registro, não substitui o texto na resposta.

## Verificação

- Cada roteiro lê em voz alta sem tag, sem receita, com CTA de consultoria.
- Caption 3 linhas cabe no terço inferior.
- Peças sem fonte de fala não foram "completadas" com chute.
- Análise registrada em `content/archive/heygen-analise/` quando o lote for novo.

## Referências

- `templates/cola-isto.txt` — stub de arquivo por peça
- `references/drive-publico.md` — IDs e download de pasta pública
