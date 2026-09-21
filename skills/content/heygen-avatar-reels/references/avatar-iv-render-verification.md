# Avatar IV — padrão de render validado (foto + áudio curto)

Validação real em 2026-09-18 com `heygen/avatar-iv`, uma foto de referência e áudio pt-BR recortado para 10,000 s.

## Pré-voo

1. Confirmar autorização imediata para o custo e verificar saldo com `GET /api/v1/credits`.
2. Consultar `GET /api/v1/videos/models`; confirmar `1080p`, `9:16` e o preço vigente.
3. Publicar foto e áudio em URLs HTTPS temporárias diretamente baixáveis. Checar `HTTP 200` e `Content-Type` antes do POST.
4. Para duração explicitamente pedida, recortar/reencodar o áudio e confirmar a duração com `ffprobe`.

## Payload que funcionou

```json
{
  "model": "heygen/avatar-iv",
  "prompt": "Direção curta de talking-head, enquadramento de busto, câmera estável, sem texto ou cortes; sincronizar com o áudio fornecido.",
  "duration": 10,
  "resolution": "1080p",
  "aspect_ratio": "9:16",
  "input_references": [
    {"type": "image_url", "image_url": {"url": "<HTTPS_IMAGE_URL>"}},
    {"type": "audio_url", "audio_url": {"url": "<HTTPS_AUDIO_URL>"}}
  ],
  "provider": {
    "heygen": {"motion_prompt": "Talking-head de busto, movimentos naturais e contidos."}
  }
}
```

O áudio M4A hospedado retornou `audio/x-m4a` e foi aceito. Não trocar o áudio do usuário por TTS.

Com áudio fornecido, `voice_id` não entra no payload — a fala vem da faixa. Para render **a partir de roteiro em texto, sem áudio**, a voz é obrigatória e vai em `provider.options.heygen.voice_id`; o formato `provider.heygen.voice_id` (sem `options`) devolve `400`.

## Troca de imagem no mesmo áudio

Quando o pedido for repetir o mesmo recorte de áudio com uma nova foto, trate-o como um novo render — e, portanto, novo custo — mas não recrie nem altere a fala. Salve a imagem recebida como novo asset, publique uma URL HTTPS temporária nova e valide-a antes do POST. O prompt deve preservar os elementos que diferenciam a referência nova (roupa, iluminação e ambiente), não o look do render anterior.

Se a imagem tiver sorriso ou expressão incompatível com uma fala clínica séria, acrescente direção explícita para começar neutro e atento. Em uma validação real, essa instrução preservou a identidade e o cardigan mostarda/camisa branca enquanto reduziu o sorriso de origem, sem texto ou overlay.

## Conclusão e QA

- O POST retornou `202` com `id`, `polling_url` e `status: pending`.
- No polling, `completed` trouxe `unsigned_urls` e `usage.cost` (US$ 0,50 para 10 s nessa validação).
- Baixar o conteúdo via `unsigned_urls[0]` com `Authorization: Bearer <OPENROUTER_API_KEY>`.
- Verificar com `ffprobe`: MP4, H.264, AAC, 1080 × 1920, duração próxima da solicitada.
- Extrair frames no começo, meio e fim para checar identidade, estabilidade e ausência de overlays.
- Se houver STT configurado, transcrever o áudio do MP4 com `gpt-4o-transcribe` em pt-BR para confirmar que a fala entregue é a faixa de origem.

Não preservar URLs temporárias, chaves ou IDs de job em mensagens públicas.