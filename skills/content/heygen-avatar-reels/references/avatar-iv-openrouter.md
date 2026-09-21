# Avatar IV via OpenRouter — notas operacionais

## Integração confirmada

- Modelo: `heygen/avatar-iv`.
- Chave: `OPENROUTER_API_KEY`; não requer uma chave HeyGen separada quando chamado via OpenRouter.
- Endpoint de submissão: `POST https://openrouter.ai/api/v1/videos`.
- Fluxo: a submissão devolve um job assíncrono; consultar o estado até a conclusão e só então baixar o MP4.
- Há custo por geração. Confirmar a autorização imediatamente antes de criar o job.

Fonte primária: <https://openrouter.ai/heygen/avatar-iv>.

## Capacidades e insumo de imagem

1. Antes de montar o payload, consultar `GET https://openrouter.ai/api/v1/videos/models` com a chave OpenRouter e filtrar `heygen/avatar-iv`. É a fonte para resolução, proporção, duração, preço e passthroughs vigentes — não a lista genérica de vídeo.
2. Snapshot de 2026-09-18: o endpoint informou `720p` e `1080p`, proporções `16:9`, `9:16` e `1:1`, duração `null`, e tarifa `duration_seconds: 0.05` (US$/s). Não prometer 2K e sempre consultar novamente antes do job.
3. O catálogo de vídeo não expôs as modalidades de entrada; a página oficial do modelo confirmou texto, imagem e áudio, e declarou que uma faixa de áudio fornecida é sincronizada diretamente ao avatar. Para áudio próprio, não substituir por TTS.
4. Referências de foto e áudio exigem URLs HTTPS públicas, diretamente baixáveis, sem cookies, HTML intermediário ou autenticação. Caminho local não pode ser buscado pelo provedor. Com mídia privada, obter autorização explícita para a hospedagem temporária e verificar `200` mais `Content-Type` adequado para ambos.
5. Para estimar custo de áudio fornecido, obter a duração exata com `ffprobe` e multiplicar pela tarifa vigente por segundo. Tratar como estimativa: duração e cobrança finais pertencem ao provedor.

## Payload, voz e autenticação

1. O retorno vivo do modelo também informa os parâmetros aceitos pelo provedor. Na validação de 2026-09-18, `heygen/avatar-iv` aceitou `voice_id`, `voice_settings`, `motion_prompt`, `expressiveness`, `fit`, `remove_background`, `background`, `caption` e `title` como passthroughs. Consultar o retorno atual antes de usar qualquer um deles.
2. **Onde a voz entra:** passthroughs vão sob `provider.options.heygen`. Enviar `provider.heygen.voice_id` (sem o nível `options`) devolve `400` com `avatar-iv requires provider.options.heygen.voice_id when using a text prompt (script)`.
3. **`voice_id` não atravessa contas.** Um ID vivo na conta HeyGen direta pode voltar `400 invalid_parameter` / `Voice not found` via OpenRouter, porque o catálogo de vozes consultado é o do provedor. Não repetir o POST com o mesmo ID e não cair para voz genérica: pedir áudio autorizado da pessoa da foto (lip-sync direto) ou, se o dono autorizar, integrar a API HeyGen da conta dona da voz.
4. Para roteiro sem áudio, Avatar IV usa TTS da HeyGen. Isso não equivale a clonar a voz do usuário: sem áudio fornecido ou `voice_id` previamente autorizado, não prometer a voz do Dr. Vinícius.
5. Áudio fornecido é **fala literal** para lip-sync, não amostra de voz reutilizável. Áudio que narra outro roteiro não serve para a peça atual — pedir a gravação correspondente em vez de recortar para caber na duração.
6. Se `supported_durations` vier `null`, não supor que o campo é proibido. Para `heygen/avatar-iv`, uma duração inteira explicitamente solicitada e correspondente ao áudio recortado foi aceita em 2026-09-18 com `duration: 10`, retornando `202`. Manter esse uso restrito ao Avatar IV e validar o catálogo + resposta antes de generalizar para outro modelo.
7. Se a submissão responder `401` com chave expirada, não repetir o POST. O job não foi criado. Pedir que o usuário renove `OPENROUTER_API_KEY` fora do chat, validar a chave com uma consulta de leitura e só então criar um novo job. Se a mídia temporária puder ter expirado, publicar novas URLs e validá-las antes do reenvio.
8. Se retornar `402 Insufficient credits`, tratar como bloqueio de saldo — não como erro de payload. Nenhum job/URL de polling é retornado: orientar recarga em `https://openrouter.ai/settings/credits` e aguardar uma nova ordem antes de reenviar. Não inferir que saldo acima do preço nominal garante aceitação: em 2026-09-18, `duration: 10` a US$ 0,05/s (US$ 0,50 nominal) continuou em `402` com US$ 2,48 restantes; o endpoint não informou a reserva mínima efetiva. Na confirmação de 2026-09-18, 30,016 s a US$ 0,05/s estimaram US$ 1,5008.
9. Quando o POST devolver `202`, salvar `id` e `polling_url`. Consultar em intervalo razoável (30 s é suficiente) até `status: completed`; então baixar o primeiro `unsigned_urls[]` com a mesma autenticação Bearer. Não declarar entrega a partir do `202`: só após baixar e inspecionar o MP4.

## Preparação de material

1. Guardar separadamente a foto/áudio recebidos e o texto literal do usuário antes de reescrever.
2. Se o Telegram truncar o roteiro, marcá-lo como incompleto e pedir a continuação. Não preencher a fala nem criar um job.
3. Separar o que é **fala** do que é **direção de cena**. O texto enviado ao modelo é apenas a fala limpa.
4. Avatar IV deve ser planejado como talking-head. Para roteiro com caminhada, locações, sofás, árvores, zooms ou cortes múltiplos, reduzir para uma tomada de busto ou gerar cenas independentes; não prometer uma sequência cinematográfica coerente a partir de uma única foto.
5. Uma foto 3:4 pode servir para 9:16 se o rosto estiver centralizado, mas haverá reenquadramento/corte lateral. Preferir cabeça e ombros, olhar frontal, boa luz, fundo simples e roupa alinhada ao look travado.
6. Antes de abrir uma nova peça, comparar o tema com os roteiros HeyGen já existentes. Se a tese já tiver sido publicada ou rascunhada recentemente, propor um ângulo complementar em vez de criar mais uma variação.

## Checagem clínica para TPC/pós-uso

- “TPC/PCT não existe” é uma afirmação incorreta: o termo aparece na literatura científica e em materiais da Endocrine Society.
- A formulação segura é: PCT é um rótulo de uso difundido, mas não há protocolo universalmente aceito nem tratamento-padrão para todos os usuários de AAS; automedicação é inadequada.
- “TPU” pode ser uma lente editorial própria, nunca apresentado como terminologia médica oficialmente correta.
- Não atribuir frequência, duração ou padrão de uso de AAS a atletas históricos sem fonte primária verificável. Falar do contexto histórico amplo é aceitável; cravar a rotina de Arnold, Frank Zane ou outro indivíduo não é.

Fontes consultadas:
- <https://pubmed.ncbi.nlm.nih.gov/41147237/>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC2646607/>
- <https://www.endocrine.org/news-and-advocacy/news-room/2023/endo-2023-press-jayasena>
