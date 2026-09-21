# PRD — Segundo Cérebro da Secretária | Luz Performance

> Criado em 2026-09-17. Status: kit de provisionamento preparado; ativação do perfil, acessos e canais dependem de aprovação direta do Dr. Vinícius.

## Objetivo

Criar uma instância independente do Hermes para a secretária da Luz Performance. Ela deve organizar operação, agenda, leads e conteúdo, reduzindo a carga operacional do Dr. Vinícius sem receber acesso clínico, credenciais do perfil principal ou autonomia para ações externas.

## Resultado esperado

Um kit de cérebro sanitizado e portátil, com persona, regras, memória inicial, mapa de workspace, limites de ferramentas e roteiro de implantação. O kit pode ser instalado em um perfil Hermes próprio da secretária, sem copiar conversas, tokens, bancos de memória ou dados de pacientes do perfil principal.

## Escopo inicial

- Triagem e organização de demandas operacionais.
- Rascunhos de respostas, follow-ups, conteúdos e relatórios.
- Registro de tarefas, decisões e informações operacionais aprovadas.
- Preparação de agenda, sem criar, editar ou cancelar eventos sem aprovação explícita.
- Triagem de leads para encaminhamento e acompanhamento.

## Fora do escopo

- Orientação médica, prescrição, interpretação de exames ou atendimento clínico.
- Armazenamento ou indexação de dados de pacientes.
- Envio de mensagens, publicação, agenda, pagamentos, compras, credenciais, mudanças de segurança, integrações, canais, permissões ou crons sem aprovação direta do Dr. Vinícius.
- Compartilhamento de memória, credenciais ou sessões com o perfil principal.

## Arquitetura

- Perfil: `secretaria-luzperformance`.
- Cérebro: arquivos em `profile-template/`.
- Memória: banco Mem0 independente, apenas contexto operacional permitido.
- Conhecimento clínico: nenhum RAG compartilhado na fase inicial.
- Credenciais: novas e segregadas; nunca copiadas de `.env`, `auth.json`, tokens ou arquivos do perfil principal.
- Ferramentas: princípio do menor privilégio; iniciar com leitura, arquivos e rascunhos. Ações externas permanecem sob aprovação.

## Critérios de aceite

- [x] O kit contém SOUL, USER, AGENTS, MAPA, MEMORY, TOOLS, allowlist de skills e roteiro de instalação.
- [x] Nenhum segredo, conversa, dado de paciente, caso clínico ou memória pessoal do Dr. Vinícius foi copiado.
- [x] A persona sabe quando executar, registrar, escalar e pedir autorização.
- [ ] O perfil instalado terá memória e credenciais próprias.
- [x] O processo de ativação descreve verificações antes de liberar calendário, mensageria ou automações.
