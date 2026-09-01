# OpenClaw → Hermes Agent Migration Reference

Use this reference only when the source package is OpenClaw-oriented and the destination is Hermes Agent. Re-check official Hermes docs because exact commands and limits can evolve.

## Artifact Mapping

| OpenClaw convention | Hermes destination | Migration action |
|---|---|---|
| Root instruction/entry-point file | `HERMES.md` or `.hermes.md` in project | Rewrite as concise project context; choose one source. Hermes context discovery is first-match-wins. |
| `AGENTS.md` as boot sequence | Hermes project context | Keep only portable project rules or convert to HERMES context. Remove manual reads of files Hermes injects automatically. |
| `IDENTITY.md` | `$HERMES_HOME/SOUL.md` | Merge name, role, voice, boundaries, and identity. Model/provider remains config, not identity text. |
| `SOUL.md` | `$HERMES_HOME/SOUL.md` | Preserve and adapt; it is independently auto-loaded. |
| Long `USER.md` | Built-in user profile plus optional project reference | Compact durable preferences into Hermes user memory; move extensive business context to an on-demand document. |
| Long `MEMORY.md` and daily notes | Hermes built-in memory + session search + dedicated state files | Do not force large logs or wizard state into bounded memory. |
| `HEARTBEAT.md`, `HEARTBEAT_OK`, polling loop | Durable Hermes cron jobs | Convert each useful check into a scheduled job/skill with schedule, delivery, silence criteria, and kill criteria. |
| OpenClaw channel commands | Hermes gateway | Rewrite around `hermes gateway setup` and gateway lifecycle commands. |
| OpenClaw config editing | `hermes config set section.key value` | Never translate keys blindly or hand-edit YAML as the default workflow. |
| `.openclaw/workspace` | Project workdir and `$HERMES_HOME` | Separate project files from profile-owned SOUL, memories, skills, config, and logs. |

## Current Hermes Constraints to Check

- Project context files are capped; split oversized entry-point documents instead of accepting head/tail truncation.
- Built-in memory is intentionally compact: agent memory and user profile have strict character limits. Verify current limits in the official Persistent Memory docs.
- Context/memory is frozen at session start; writes persist immediately but affect prompt injection on the next session.
- Historical changelogs should preserve old OpenClaw commands as history. Archive them and begin a Hermes changelog rather than applying product-name substitution.

## Telegram Gateway

Typical environment variables:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_USERS`
- `TELEGRAM_HOME_CHANNEL`
- `TELEGRAM_CRON_THREAD_ID` for topic-specific cron delivery
- `TELEGRAM_WEBHOOK_URL` and `TELEGRAM_WEBHOOK_SECRET` for webhook mode

Also account for BotFather privacy mode, numeric allowlists, group mention gating, `/sethome`, and topic routing. Deployment-managed environments may require secrets in their Environment panel rather than a local `.env`; document the actual platform contract.

## hPanel-Managed Deployments

- Put credentials/tokens in **hPanel Environment** when that is the deployment's managed secret surface.
- Put non-secret settings through `hermes config set`.
- Do not ship a populated `.env`, tell users to append secrets by shell, or conflate project files with `$HERMES_HOME`.

## Skill Package Compatibility Audit

When the source includes a skill tree, audit it as a runtime package rather than ordinary Markdown:

1. Parse every `SKILL.md` frontmatter with YAML, not regex alone. Unquoted `description:` or `source:` values containing colons commonly make otherwise readable skills undiscoverable.
2. Enforce Hermes limits: `name` present and valid, `description` present and at most 1,024 characters, non-empty body, and total file at most 100,000 characters. Keep the complete trigger within the first 57 description characters.
3. Treat `_registry.md` files as human indexes only. Hermes discovers `SKILL.md` under `$HERMES_HOME/skills/`; copying a tree into a project's `skills/` directory does not install it.
4. Do not assume prose references to another skill load it. Use explicit skill loading, preload/bundles, or make the orchestration self-contained.
5. Inventory `references/`, `templates/`, `scripts/`, `evals/`, and binary assets separately. `evals.json` is not a native Hermes skill-runtime contract unless the repository ships and runs its own evaluator.
6. Compare registry versions, eval versions, and behavior against each current `SKILL.md`; stale metadata often exposes larger semantic drift.
7. Resolve every relative Markdown link from the containing file. Distinguish genuinely missing files from schematic workspace links, which should be shown as code/templates rather than clickable repository links.

## Operational Mappings Worth Verifying

| Source behavior | Hermes-oriented replacement |
|---|---|
| `exec-policy show/preset yolo/reset` | `hermes config get approvals.mode`; prefer `smart`, use `hermes config set approvals.mode off` or per-run `--yolo` only when deliberately requested |
| Source cron plus direct Telegram API calls | Hermes cron/`cronjob` with explicit `workdir`, skills, delivery target, silence criteria, and durable state file |
| Wizard progress in conversational `MEMORY.md` | A kit-owned structured state file read explicitly; cron jobs may skip conversational memory by default |
| Source browser install/status commands | Enable the Hermes `browser` toolset and test the actual tool in a fresh session |
| API key required for Whisper | Configure Hermes STT independently (`stt.enabled` plus a supported local or hosted provider); configure memory separately |
| Project-local `.env` as universal secret store | Resolve the profile secret path with `hermes config env-path`, or use the deployment's managed secret surface/auth manager |

Exact command shapes can change. Verify with official docs and live `hermes <command> --help` when available; if the local binary is absent, report that verification boundary without turning it into a persistent claim about Hermes.

## Common Traps

1. Renaming `AGENTS.md` to `HERMES.md` while retaining a source-runtime boot sequence.
2. Keeping both HERMES and AGENTS files and assuming Hermes composes them.
3. Moving an oversized user dossier directly into bounded USER memory.
4. Treating a heartbeat markdown file as an active Hermes scheduler.
5. Replacing `openclaw` with `hermes` inside historical CLI examples without validating the command shape.
6. Reporting “no images” after inspecting extensions but missing base64 SVG/PNG data URIs in HTML.
7. Preserving tester outreach, expired download URLs, and internal release notes in an end-user distribution.
8. Missing README/on-disk mismatches such as reversed template suffixes or declared-but-absent `.env` templates.
9. Declaring a skill package migrated while its frontmatter is invalid, its registries are stale, or its eval fixtures still assert source-runtime commands.
10. Treating channel-specific copy and raw platform API calls as portable gateway behavior.
