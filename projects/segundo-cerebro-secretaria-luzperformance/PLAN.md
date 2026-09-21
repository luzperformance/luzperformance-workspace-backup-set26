# Plano: Segundo Cérebro da Secretária | Luz Performance

> Criado em 2026-09-17. Status: execução parcial — kit pronto; provisionamento do perfil pendente.

## Objetivo

Entregar à secretária um Hermes operacional, segregado e seguro, que assuma organização de agenda, leads e fluxo de conteúdo da Luz Performance sem expor dados clínicos ou permitir ações externas autônomas.

## Sucesso =

- [x] Kit sanitizado do cérebro criado com regras, memória inicial e mapa operacional.
- [x] Papéis, aprovações e bloqueios clínicos definidos explicitamente.
- [x] Plano de implantação com verificações e pontos de aprovação documentado.
- [ ] Perfil Hermes independente criado e iniciado com o kit.
- [ ] Credenciais próprias, permissões mínimas e canais aprovados configurados e testados.

## Tarefas

### Fase 1: Fundamento seguro

- [x] **T1.1** — Separar o que pode ser herdado do cérebro principal do que é privado ou clínico.
  - Verificação: o kit não contém tokens, dados de pacientes, conversas, casos clínicos ou memórias pessoais.
  - Estimativa: 30 min.
  - Depende de: nenhuma.

- [x] **T1.2** — Criar persona, instruções operacionais, memória inicial e limites de ferramenta para a secretária.
  - Verificação: os arquivos `SOUL.md`, `AGENTS.md`, `MEMORY.md` e `TOOLS.md` definem claramente execução, escalonamento e aprovação.
  - Estimativa: 45 min.
  - Depende de: T1.1.

### Fase 2: Provisionamento do perfil

- [ ] **T2.1** — Criar o perfil Hermes `secretaria-luzperformance` pelo fluxo oficial disponível no host.
  - Verificação: o comando ou painel oficial mostra o perfil independente e um diretório próprio, sem alterar o perfil `default`.
  - Estimativa: 30 min.
  - Depende de: T1.2; aprovação direta do Dr. Vinícius.

- [ ] **T2.2** — Copiar apenas o conteúdo de `profile-template/` para o novo perfil e apontar o diretório de trabalho operacional.
  - Verificação: uma nova sessão carrega a identidade da secretária e as regras do projeto; nenhum arquivo privado do perfil principal é referenciado.
  - Estimativa: 20 min.
  - Depende de: T2.1.

- [ ] **T2.3** — Criar memória Mem0 própria, isolada e vazia de dados clínicos.
  - Verificação: uma escrita e uma recuperação de um fato operacional de teste funcionam no banco do perfil; revisão negativa não encontra dados de paciente.
  - Estimativa: 30 min.
  - Depende de: T2.2.

### Fase 3: Permissões e integrações

- [ ] **T3.1** — Habilitar apenas ferramentas mínimas: arquivos, memória, tarefas e skills aprovadas.
  - Verificação: o perfil não possui terminal, cron, integrações de mensageria ou calendário liberados por padrão.
  - Estimativa: 20 min.
  - Depende de: T2.2.

- [ ] **T3.2** — Se aprovado, conectar um canal exclusivo da secretária e testar somente rascunhos internos.
  - Verificação: a origem/destino está correto e nenhuma mensagem externa foi enviada no teste.
  - Estimativa: 30 min.
  - Depende de: T3.1; aprovação direta do Dr. Vinícius.

- [ ] **T3.3** — Se aprovado, conectar agenda/CRM com credenciais próprias e aplicar modo de leitura primeiro.
  - Verificação: leitura de teste retorna dados autorizados; criar/alterar agenda continua exigindo aprovação.
  - Estimativa: 45 min.
  - Depende de: T3.1; aprovação direta do Dr. Vinícius.

### Fase 4: Operação assistida

- [ ] **T4.1** — Rodar uma semana em modo de rascunho: triagem, resumo diário e preparação de respostas.
  - Verificação: 100% das ações externas são revisadas antes de envio; falhas e dúvidas viram ajustes nos arquivos do cérebro.
  - Estimativa: 5 dias úteis.
  - Depende de: T3.2.

- [ ] **T4.2** — Revisar autorização por tipo de ação e decidir o que pode ganhar autonomia limitada.
  - Verificação: decisão registrada com ações permitidas, ações sempre aprovadas e responsável pela revisão.
  - Estimativa: 30 min.
  - Depende de: T4.1; aprovação direta do Dr. Vinícius.

## Dependências externas

- Dr. Vinícius define o canal que a secretária usará e aprova qualquer conexão externa.
- Instalação Hermes acessível no host de destino; o `hermes` CLI não está disponível no terminal desta sessão, portanto o comando de criação do perfil deve ser confirmado no host antes da execução.
- Credenciais novas e segregadas para agenda, CRM ou mensageria, quando e se aprovadas.

## Riscos

- **Mistura de contexto clínico e operacional** — mitigação: sem RAG clínico, sem dados de pacientes e bloqueio explícito no SOUL/AGENTS.
- **Autonomia excessiva em mensagens ou agenda** — mitigação: rascunho primeiro; ações externas sempre aprovadas.
- **Vazamento entre perfis** — mitigação: não copiar `.env`, `auth.json`, sessões ou Mem0; criar credenciais e memória independentes.
- **Perfil criado manualmente com configuração quebrada** — mitigação: usar somente comando ou painel oficial, nunca editar `config.yaml` à mão.

## Estado atual

Fase 1 concluída. O kit está em `profile-template/`. Fases 2–4 aguardam a autorização de ativação e a definição do canal/credenciais da secretária.
