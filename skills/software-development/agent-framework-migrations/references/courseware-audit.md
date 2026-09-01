# Courseware and Archive Migration Audit

Use this when an agent-runtime migration includes lessons, transcripts, shared HTML/CSS, indexes, and legacy archives—not just runnable config.

## Coverage contract

1. Inventory every file in both active courseware and archives.
2. Read every text file fully; paginate large transcripts until the final line.
3. For each file report: source-runtime references, incompatible commands/config, concepts requiring semantic replacement, and a concrete destination-native outline or text direction.
4. Audit shared templates, footers, CSS comments, indexes, and empty/binary-looking files; branding and stale support links often live outside lesson bodies.
5. Keep archives out of active retrieval. If an archive remains searchable by the agent, add an unmistakable “historical—do not execute” banner or exclude it from indexes/context.
6. Treat transcripts as re-record/rewrite candidates when runtime details dominate. Do not globally replace product names inside spoken history.

## Extraction passes

Run separate passes for:

- Product names and transcription variants/misspellings.
- CLI commands and slash commands.
- Config paths, environment variables, secrets, and provider assumptions.
- Context/identity files, memory files, schedulers/heartbeats, channel behavior, and multi-agent primitives.
- External documentation/support/community links.
- Unsafe operational guidance: blanket YOLO, broad non-expiring PATs, “Docker makes risk nearly zero,” identity text as prompt-injection protection, or claims that skills are universally portable.

Count hits as a scope indicator, not proof of semantic completeness. A single sentence can encode several incompatible assumptions.

## Course-specific dispositions

- **Index/README:** rewrite first; they determine what the tutor retrieves.
- **Setup/cockpit lessons:** full operational rewrite against destination docs/CLI.
- **Identity, memory, cron, channels, multi-agent lessons:** semantic rewrite; these rarely have one-to-one primitives.
- **Case studies:** preserve only as clearly labeled historical evidence, or replace with destination-native demonstrations.
- **Shared HTML/CSS:** usually preserve layout, replace branding, support links, and platform-specific “paste here” labels.
- **Transcript:** regenerate from migrated lessons; preserve old transcript only in a clearly historical area.
- **Legacy cheatsheets:** exclude from active retrieval or rebuild from authoritative destination docs.

## Hermes-oriented safety corrections

- Separate project workdir from `$HERMES_HOME`.
- Keep settings in Hermes config and credentials in the Hermes secret path or managed deployment secret surface.
- Prefer smart approvals; never infer low risk merely from a source platform’s container model.
- Treat `SOUL.md` as identity, not a security boundary.
- Treat `AGENTS.md` as project instructions, not an agent org chart.
- Replace heartbeat files with durable cron/Kanban behavior when migrating to Hermes.
- Validate skills for tools, dependencies, paths, and triggers; `SKILL.md` portability is conditional.

## Verification boundary

Verify commands with official docs and live CLI help when available. If the binary is absent, state that boundary and avoid inventing flags. Missing local binaries are environment state, not a durable limitation.

Some readers may classify valid UTF-8 text as binary. If content search finds matches but the text reader returns “binary,” inspect the byte signature/encoding with a non-mutating probe before excluding the file. Record the classification discrepancy rather than silently skipping it.
