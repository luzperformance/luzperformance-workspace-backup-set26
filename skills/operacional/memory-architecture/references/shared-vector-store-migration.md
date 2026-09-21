# Shared Vector Store Migration Checklist

## Decide first

- **Conversational memory:** Mem0 with an approved shared backend.
- **Document RAG:** separate collection/database namespace, source metadata, and citation policy.
- **Sensitive data:** patient-specific content stays out of the conversational-memory index.

## Before migration

1. Back up or preserve the existing vector-store directory/database; do not overwrite it.
2. Inventory approved source files and exclusions.
3. Verify the embedding credential with a one-input request to the target model.
4. Create a private database/service endpoint and a dedicated least-privilege database role.

## pgvector baseline

- Enable the `vector` extension in the target database.
- Restrict network access; never bind PostgreSQL broadly unless a controlled private-network policy exists.
- Store connection credentials outside source control.
- Use an application-specific database and role rather than a superuser.

## Cutover validation

- Import only approved sources with source hash and scope metadata.
- Confirm a known operational query returns a relevant result.
- Confirm excluded patient markers are absent from imported payloads and retrieval results.
- Keep the old index intact until the new index has passed validation and a recovery test.
