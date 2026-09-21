# Avatar IV — Saúde Mental no Esporte de Elite (render concluído)

**Status:** concluído em 2026-09-19. MP4 gerado e verificado.

## Job

- Modelo: `heygen/avatar-iv` via OpenRouter
- Job ID: `gen-vid-1789840582-MX76XzNA82ZAcGnPZozd`
- Custo cobrado: **US$ 3,228** (64,57 s × US$ 0,05/s)
- 1080p, 9:16, duração solicitada 65 s

## Insumos

- Foto autorizada: `assets/2026-09-19-referencia-saude-mental-drive.png` (PNG 1086 × 1448, jaqueta oliva de gola alta, camiseta preta, fundo terracota). Origem: link Drive do Dr. Vinícius `1a6ayO1nTSogsb_qFa2zv5qhYLNCkCTiP`.
- Áudio autorizado: `assets/2026-09-19-audio-saude-mental-65s.m4a` (AAC 48 kHz, 64,56 s), transcodificado do original Opus `2026-09-19-audio-saude-mental-bruto.ogg` — sha256 `7f695fe0…b499`, idêntico ao áudio enviado em três mensagens seguidas.
- Rota: lip-sync direto com a faixa de áudio fornecida. **Não** foi usado `voice_id`; o `voice_id` `f969f58e…5596` não existe no catálogo ativo da HeyGen (erro de 2026-09-18).

## Verificação (QA)

- `ffprobe`: MP4 H.264 1080 × 1920, 25 fps, AAC 48 kHz estéreo, **64,578 s**.
- Frames em 0,5 s, 32 s e 62 s: mesma identidade, mesma roupa e mesmo fundo da foto; sem texto, overlay ou marca d'água; expressão neutra no hook e natural no restante.
- Transcrição do áudio do próprio MP4 (`gpt-4o-transcribe`, pt): reproduz a fala gravada pelo Dr. Vinícius na íntegra, incluindo CTA de consultoria na bio.

## Arquivos

- Master 1080p: `renders/2026-09-19-saude-mental-esporte-elite-avatar-iv.mp4` (33,7 MB)
- Versão 720p para envio no Telegram: `renders/2026-09-19-saude-mental-esporte-elite-avatar-iv-720p.mp4` (11,7 MB)
- Frames de QA: `renders/2026-09-19-qa-frame-0.5s.jpg`, `-32s.jpg`, `-62s.jpg`
- Registro do job: `renders/2026-09-19-saude-mental-esporte-elite-avatar-iv-job.json`

## Pendências

- Legendas nativas, overlays e B-roll seguem o plano de edição em `15-saude-mental-esporte-elite-direcao-2026-09-18.md` — feitos fora do Avatar IV.
- Duração final de 64,6 s ficou acima do alvo de 48–53 s do plano; se precisar caber no alvo, é nova gravação, não corte.
