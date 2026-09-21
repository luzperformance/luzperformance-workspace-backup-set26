# Avatar IV — Saúde Mental no Esporte de Elite

**Status:** bloqueado em 2026-09-18; nenhum MP4 foi gerado.

## O que ocorreu

1. A primeira submissão foi recusada com HTTP 400 porque o Avatar IV exige `provider.options.heygen.voice_id` para roteiro em texto.
2. A segunda submissão foi recusada com HTTP 400 porque o `voice_id` disponível não existe no catálogo ativo do provider.
3. Em ambos os casos não houve resposta `202`, `job_id` ou URL de polling — portanto não há job assíncrono a acompanhar.

## Segurança aplicada

- A URL HTTPS temporária da foto foi desligada e a verificação posterior retornou HTTP 530; o servidor local também ficou inacessível.
- O script agora exige `--submit`; a execução padrão não envia render.
- Mesmo com `--submit`, o script bloqueia localmente enquanto não houver uma voz validada.

## Áudio recebido

- Anexo `audio_03ff8f51e41c.ogg`: Opus mono, **4,2665 s** — curto demais para a narração de 48–53 s.
- A transcrição com `gpt-4o-transcribe` foi bloqueada por HTTP 401 (`invalid_api_key`); não houve transcrição alternativa nem render.
- O segundo anexo foi preservado em `assets/2026-09-18-audio-recebido-insonia-testo-59s.m4a`: AAC estéreo, **59,722 s**. A transcrição é um roteiro diferente, sobre insônia/eixo hormonal; não serve como “amostra de voz” para este reel, porque o Avatar IV usa o áudio literalmente.

## Decisão registrada

- Rota escolhida: áudio autorizado da pessoa da foto para lip-sync no Avatar IV; não usar `voice_id` via OpenRouter.

## Para retomar

1. Confirmar o roteiro colável de 48–53 s já arquivado em `15-saude-mental-esporte-elite-2026-09-18.txt`.
2. Confirmar que a pessoa da foto é o avatar autorizado.
3. Fornecer áudio autorizado dessa pessoa para lip-sync (rota recomendada) **ou** um `voice_id` vivo e autorizado.
4. Fazer pré-voo e obter autorização explícita de custo imediatamente antes de um novo job.
