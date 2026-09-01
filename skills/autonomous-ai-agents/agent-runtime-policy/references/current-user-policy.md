# Current User Runtime Policy

## Model aliases and routing

| Routing name | Behavior |
|---|---|
| Terra | Default and fallback for ordinary tasks |
| Sol | Coding/software-development and long-running tasks |
| Luna | Use only when explicitly requested by name |

Precedence: explicit Luna → explicit Sol → coding/long task uses Sol → Terra.
An explicit request for Terra overrides the automatic Sol route.

Known corrected alias spelling: `luna`, not `luns`. The conversation proposed `openai-codex/gpt-5.6-luna` for Luna and `openai-codex/gpt-5.6-sol` for Sol, but future configuration work must verify these against the live provider. No exact provider model ID for Terra was established, so do not invent one.

## Request pacing

- General API interval: 5 seconds minimum.
- Web-search interval: 10 seconds minimum.
- Search batch: at most 5 searches, followed by a 2-minute pause.
- Prefer bulk/batched requests for similar work.
- HTTP 429: stop for 5 minutes before retrying.

## Source note

This reference condenses user corrections from the session. The durable behavioral rules are in the parent `SKILL.md`; update both if the user's routing or pacing policy changes.
