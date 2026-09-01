---
name: agent-framework-migrations
description: "Use when migrating agent kits between runtimes."
version: 1.1.0
created_by: agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [migration, agent-frameworks, compatibility, audit, configuration]
---

# Agent Framework Migrations

Migrate starter kits, workspaces, operational docs, templates, and examples between agent runtimes. Treat this as a semantic/runtime migration, never a global product-name replacement.

## Core Rule

Map every source artifact to a destination runtime primitive. A file can be renamed only when its loading semantics, lifecycle, limits, security model, and operational behavior remain equivalent. Otherwise rewrite, split, convert, archive, or remove it.

## Workflow

1. **Freeze scope and exclusions.** Record the exact root, excluded directory components, whether editing is allowed, and the required deployment assumptions.
2. **Build a complete inventory.** Walk recursively, excluding directories by path component. Record path, byte size, text/binary classification, MIME guess, and checksum. Include embedded data URIs and externally loaded assets.
3. **Read every text artifact.** Large files must be paginated. For generated-looking HTML, inspect all semantic markup/CSS and separately decode or fingerprint embedded base64 assets; do not mistake “no standalone binaries” for “no binary assets.”
4. **Extract runtime dependencies.** Per file, identify product CLI commands, config paths, environment variables, context files, memory conventions, scheduler behavior, gateway/channel behavior, provider assumptions, and internal links.
5. **Verify destination semantics from authoritative sources.** Load the destination framework skill/docs. Check context discovery order and size caps, identity loading, memory limits, secret storage, config CLI, scheduling, gateway setup, and deployment-specific environment management.
6. **Assign a disposition to every file:** preserve, rename, rewrite, split, convert to runtime primitive, archive as legacy, or remove. Never leave an inventoried file unclassified.
7. **Check cross-file integrity.** Detect filenames declared in READMEs but absent on disk, missing referenced files, stale version counts, obsolete download links, and historical commands that must not be “translated.”
8. **Validate in isolation.** Run a destination-aware static validator, install into a temporary profile/home, and run the installer twice to prove safe defaults and idempotency. Never test against the user's live profile.
9. **Package and read back.** Reopen each archive, assert one stable top-level directory and required entries, then compute size/checksum. Archive creation without readback is not verification.
10. **Produce the migration contract.** Include file-by-file actions, destination-native content required, standalone and embedded asset handling, blockers/verification limits, files modified, static checks, isolated install result, native CLI result or boundary, and archive readback evidence.

## Semantic Mapping Questions

For each artifact ask:

- Is it auto-loaded, loaded on demand, or merely documentation?
- Does the destination support composition or first-match-wins context discovery?
- Is identity separate from project rules?
- Is memory file-based, tool-managed, bounded, or session-indexed?
- Is polling/heartbeat native, or should each check become a durable scheduled job?
- Are secrets local files, a platform environment panel, or a credential manager?
- Are settings supposed to be changed by CLI rather than hand-edited YAML?
- Does a channel integration need allowlists, home-channel routing, topic routing, mention gating, or webhook secrets?

## File Disposition Guidance

- **Rename** only for true semantic equivalents.
- **Rewrite** operational docs dominated by source-runtime CLI/config behavior.
- **Split** files that exceed destination context/memory limits or mix auto-loaded rules with long history.
- **Convert** pseudo-runtime conventions (heartbeat files, manual boot sequences) into native scheduler/context/memory features.
- **Archive** historical changelogs rather than globally replacing old product names inside factual history.
- **Remove** tester scripts, expired distribution messages, and internal release artifacts from end-user packages.
- **Preserve** runtime-neutral branded HTML/media, changing only product labels and integration instructions.

## Verification and Reporting

- Ground inventory counts and sizes in tool output.
- State when destination CLI verification was unavailable; use authoritative docs without turning a missing local binary into a durable limitation.
- Do not claim images are absent until checking both standalone files and embedded data URIs.
- End with: scope audited, key outcomes, files changed/created, and issues encountered.

## References

- `references/openclaw-to-hermes.md` — concrete OpenClaw → Hermes Agent mappings, limits, gateway variables, and common migration traps.
- `references/courseware-audit.md` — exhaustive audit pattern for lessons, transcripts, shared web assets, indexes, and legacy archives.
- `references/validation-and-packaging.md` — static checks, isolated/idempotent installer testing, archive readback, and completion evidence.
