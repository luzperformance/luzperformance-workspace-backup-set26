STT: OpenAI `gpt-4o-transcribe` pt-BR. Arquitetura: Mem0 para memória pessoal/conversacional; RAG clínico rastreável separado com embeddings OpenAI e pgvector/Qdrant compartilhado (nunca Qdrant local por path em múltiplos processos).
§
Onboarding completo (passos 0-6). Workspace estruturado, SOUL.md Chief of Staff, GitHub backup ativo. Whisper STT, YOLO, primeira vitória Dr Luiz. Pendência: Chromium opcional.
§
Scripts de cron no_agent devem estar em /data/scripts/ (ou ~/.hermes/scripts/) — o cron busca lá, não no workdir. workdir define onde o script executa, não onde está salvo. Pitfall comum: script existe no workdir mas cron não acha porque procura em paths errados.
§
Dr Vinícius Luzardi Lopes: médico performance/hormonal, Imbituba UTC-3; Luz Performance (luzperformance.com.br=blog, .com=LP Google Ads). Nunca vende receitas, só consultorias. Hermes roda via OneClick da Hostinger; o terminal é lshell restrito (usar `hermes ...`, sem atribuição `HERMES_HOME=` nem caminho absoluto).
§
Vinícius prefere escalas mensais de plantões em HTML, mantendo o visual navy/dourado do protocolo de sono; arquivos ficam em /data/workspace/Luzperformanbce/Plantões/ e são enviados para download via Telegram.
§
Lead monitoring: planilha Google `19SrwzlrcTT9ttRo_C_oVSmPqFzrWZ8wupYyZ7Ew9A1U`, aba Lead (~278). Cron `912f8bc6684e` a cada 15 min e watchdog `a873f118228f` a cada 30 min, no_agent, scripts em `/data/scripts/`; após 3 falhas tenta corrigir token/deps/script e alerta se não conseguir.
§
Vinícius administra Hermes self-hosted em VPS/headless e costuma executar instruções por SSH; integrações OAuth com callback loopback podem exigir autorização no ambiente ou fornecimento manual do retorno.
§
A pasta /data/Luzperformance/AvatarHype/ centraliza os ensinamentos e materiais do curso AvatarGen; o fluxo de produção usa roteiro + foto no `heygen/avatar-iv` via OpenRouter, com entrega padrão 9:16 (1080×1920).
§
Vinícius pretende usar o modelo `heygen/avatar-iv` via chave OpenRouter para recriar/alterar vídeos existentes; renders têm custo e exigem confirmação antes do job.