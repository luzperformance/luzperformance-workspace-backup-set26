---
name: memory-architecture
description: "Use when configuring agent memory or RAG storage."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, mem0, rag, embeddings, qdrant, pgvector, privacy]
---

# Memory Architecture

Design and operate memory systems without mixing conversational facts, clinical documents, credentials, or retrieval stores.

## When to Use

- Configuring Mem0, semantic memory, embedding providers, Qdrant, pgvector, or a document RAG.
- Migrating an agent from a local vector-store path to a shared service.
- Defining what data may enter an embedding index.

## Architecture Boundary

Use **Mem0** for durable personal and conversational context: preferences, operating decisions, business context, and delegated authority.

Use a **separate RAG system** for traceable clinical or documentary knowledge. Its records must carry source, version/date, and retrieval citations. Never treat retrieval results as patient records or as clinical advice without the appropriate workflow.

Patient-specific material is excluded from general conversational-memory indexes. Do not index cases, identifiers, histories, results, or narrative details merely because they appear in a broad context document.

## Provider and Credential Rules

1. Test the configured embedding model with a real minimal embedding request before importing data.
2. OpenAI embedding clients use `OPENAI_API_KEY`. Voice-specific credentials may be resolved differently; do not assume they authenticate embeddings.
3. Never display keys, tokens, or vectors in output or logs.
4. Store only metadata needed for source tracing: source path/ID, content hash, index date, and scope.

## Storage Choice

- A local Qdrant `path` is appropriate only for one process owning that store.
- For multiple Hermes processes, workers, or hosts, use a shared Qdrant server or PostgreSQL with pgvector.
- Keep the database private by default. Do not expose PostgreSQL directly to the public internet; use a private network, VPN, SSH tunnel, or tightly restricted firewall rules.
- Before changing vector-store backends, preserve the old store and reindex from approved source documents instead of deleting it blindly.

## Safe Indexing Procedure

1. Define the allowed sources and explicit exclusions before reading content.
2. Split mixed files into approved and excluded sections before creating embeddings.
3. Assert excluded patient markers or sections are absent from the material sent to the embedding provider.
4. Write each import with scope metadata such as `operational-only` or `clinical-rag`.
5. Run one semantic retrieval query that should succeed.
6. Run a negative review for excluded material. If exclusion cannot be verified, do not enable the index.
7. Retain original files unchanged; an index is derived data, not the source of truth.

## Migration Checklist

See `references/shared-vector-store-migration.md` before moving from local Qdrant to pgvector or shared Qdrant.

## Pitfalls

- Do not index all of `USER.md` or equivalent blindly when it includes clinical cases.
- Do not use one memory index for both agent preferences and an evidence base.
- Do not run two processes against the same local Qdrant path.
- Do not call a migration complete until write, semantic retrieval, and exclusion checks all pass.
