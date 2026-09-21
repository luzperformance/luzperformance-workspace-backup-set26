# Kit de cérebro — Secretária | Luz Performance

Este é um cérebro sanitizado para uma instância Hermes independente da secretária. Ele herda estrutura e disciplina operacional do perfil principal, não seus dados, memórias, tokens, sessões, contexto clínico ou permissões.

## Conteúdo

- `SOUL.md`: identidade e tom.
- `USER.md`: contexto mínimo da Luz Performance.
- `AGENTS.md`: fluxo de trabalho, limites e escalonamento.
- `MAPA.md`: organização do workspace operacional.
- `MEMORY.md`: fatos iniciais permitidos e política de memória.
- `TOOLS.md`: ferramentas mínimas e bloqueios iniciais.
- `SKILLS-ALLOWLIST.md`: skills aprovadas para a primeira fase.
- `.env.example`: lembrete de segregação de credenciais; não contém segredo.

## Instalação — somente após aprovação

1. No host de destino, confirmar o fluxo oficial de criação de perfis com a documentação atual ou o comando/painel disponível. Não editar `config.yaml` manualmente.
2. Criar o perfil `secretaria-luzperformance` separado do perfil `default`.
3. Copiar estes arquivos para o diretório de trabalho/perfil novo conforme o fluxo oficial; manter `SOUL.md` no home do perfil e `AGENTS.md` no diretório de trabalho que a sessão usará.
4. Criar memória própria e validar uma escrita/recuperação operacional de teste. Não importar Mem0, backups ou sessões do Dr. Vinícius.
5. Habilitar somente as ferramentas descritas em `TOOLS.md` e as skills da allowlist.
6. Rodar uma sessão de teste: uma entrada de lead, uma pendência de agenda e um rascunho de resposta. Nenhuma mensagem deve ser enviada, e nenhum evento deve ser criado.
7. Só depois, com aprovação direta do Dr. Vinícius, avaliar integrações e canais um a um em modo leitura/rascunho.

## Operação recomendada

Começar uma semana em modo de rascunho. A secretária recebe organização, proposta de resposta e checklist; o Dr. Vinícius aprova tudo que sai para clientes, agenda, conteúdo ou ferramentas externas. Depois dessa semana, as regras podem ser calibradas com base em erros reais, não em suposição.
