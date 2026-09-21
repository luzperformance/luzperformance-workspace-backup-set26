# PRD — pgvector compartilhado para Mem0

## Objetivo
Substituir o Qdrant local por PostgreSQL com pgvector em um serviço compartilhado, mantendo a memória conversacional no Mem0.

## Escopo inicial
- Um PostgreSQL 16 com extensão `vector`.
- Dados persistentes em volume Docker.
- Porta vinculada apenas a `127.0.0.1` por padrão.
- Sem credenciais no repositório.

## Fora de escopo
- Base clínica documental/RAG.
- Exposição pública da porta PostgreSQL.
- Migração sem backup e sem teste de recuperação.

## Critérios de aceite
- `pg_isready` saudável dentro do container.
- `CREATE EXTENSION vector` disponível no banco.
- Mem0 consegue gravar e recuperar uma memória de teste.
