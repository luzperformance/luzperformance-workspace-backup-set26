# A imagem oficial já inclui a extensão pgvector.
FROM pgvector/pgvector:pg16

COPY init/001-enable-vector.sql /docker-entrypoint-initdb.d/001-enable-vector.sql
