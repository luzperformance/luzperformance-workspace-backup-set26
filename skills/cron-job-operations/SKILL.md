---
name: cron-job-operations
description: "Manage Hermes cron jobs: create, update, list, remove, run."
version: 1.0.0
---

# Cron Job Operations in Hermes

Manage scheduled jobs using the `cronjob` tool. This skill covers common operations and pitfalls.

## Prerequisites

- Understand the `cronjob` tool parameters: `action`, `schedule`, `model`, `provider`, `deliver`, `skills`, `prompt`, `workdir`, `no_agent`, etc.
- Know that `model` and `provider` are set at job creation/update time.
- Be aware that updating `model` or `provider` on an existing job may fail with "No updates provided" (see Pitfalls).

## Operations

### List Jobs

```
- action: list
```
Returns all jobs with details like `job_id`, `name`, `schedule`, `next_run_at`, `last_status`.

### Create a Job

Required: `action: create`, `schedule`, `prompt`.

Optional but recommended:
- `name`: human-friendly identifier
- `model`: e.g., `nvidia/nemotron-3-super-120b-a12b:free`
- `provider`: e.g., `OpenRouter`
- `deliver`: where output goes (e.g., `origin`, `local`, `telegram:chat_id`)
- `skills`: array of skill names to load before running the prompt
- `workdir`: directory to run from (defaults to session cwd)
- `no_agent`: set to `true` for watchdog-style scripts (stdout only, no LLM)

Example: create a lead monitoring cron with model/provider

```
- action: create
- name: monitor-leads-novos
- schedule: every 15m
- prompt: "Execute o monitor de novos leads conforme a skill lead-monitoring. Entregue somente o lead novo detectado em formato estruturado..."
- model: nvidia/nemotron-3-super-120b-a12b:free
- provider: OpenRouter
- deliver: origin
- skills: ["lead-monitoring"]
- workdir: /data/Luzperformance/new-leads
```

### Pinned-model crons

When the user explicitly requests a model/provider but the exposed `cronjob` tool schema does not offer those fields, create the job through the Hermes CLI instead of silently falling back to the default model:

```bash
hermes cron create '0 10,17 * * *' 'Self-contained task prompt' \
  --name daily-task \
  --deliver telegram \
  --model gpt-5.6-luna \
  --provider openai-codex
```

The CLI supports `--model` and `--provider`. Read the job back with `cronjob(action='list')` and confirm both values before reporting completion. Use an explicit delivery destination (`telegram`, `origin`, or a platform target) when creating from an automation context where the originating chat may be unavailable.

### Recurring local times on UTC hosts

Cron expressions run in the scheduler host's timezone. Establish that timezone before converting a requested local schedule. For a UTC host and a UTC-3 user, daily 07:00 and 14:00 local becomes:

```text
0 10,17 * * *
```

Verify the next UTC run corresponds to the requested local time; do not report the raw UTC expression as though it were local time.

### Reminders tied to shifts or events

When the request is "on my shift days" or otherwise depends on dates not included in the message:

1. Find the authoritative existing record first (shift schedule, calendar, or designated tracker). Do not infer a repeating pattern or create a generic daily reminder.
2. If no usable record exists, report that precise gap before creating anything; ask only for the dates or the authoritative source.
3. Do not list unrelated jobs or perform broader diagnostics unless they are needed to avoid a duplicate or to identify the schedule source.
4. A mid-task instruction to stop cancels discovery and creation immediately. Confirm only whether any job was created.

### Update a Job

Use `action: update` with `job_id` or `name`.

You can update most fields (schedule, prompt, deliver, etc.) directly.

**Pitfall**: Updating `model` or `provider` on an existing job often results in "No updates provided" and no change. This is a known limitation of the `cronjob` tool when those fields are present.

**Workaround**: To change `model` or `provider`, you must:
1. Remove the existing job (`action: remove`).
2. Create a new job with the desired `model`/`provider` (`action: create`).

### Remove a Job

```
- action: remove
- job_id: <job_id_or_name>
```

### Run a Job Immediately

```
- action: run
- job_id: <job_id_or_name>
```
Returns immediately; the job runs in the background and output arrives later.

### Pause/Resume a Job

```
- action: pause
- job_id: <job_id_or_name>

- action: resume
- job_id: <job_id_or_name>
```

## Common Patterns

### Watchdog Scripts (no_agent=true)

Use `no_agent: true` when the job is a script that should output only when there's something to report (empty stdout = no delivery).

Example: a script that checks for new leads and prints only when found.

### Agent-Based Jobs

Default (`no_agent: false`) runs the prompt through the LLM with the specified `model`/`provider`. Use when you need reasoning, tool use, or dynamic behavior.

## Pitfalls

1. **Model/Provider Updates Fail Silently**
   - The `cronjob` tool's `update` action ignores changes to `model` and `provider` fields.
   - Always remove and recreate to change AI model/provider.

2. **Schedule Syntax**
   - Use `every 15m` for recurring, `in 30m` for one-shot.
   - Avoid ambiguous forms like `15m` (must be `every 15m` for recurrence).

3. **Workdir Matters**
   - If your prompt or script relies on relative paths, set `workdir` explicitly.
   - The job runs in a fresh session; `workdir` ensures correct context.

4. **Delivery Destinations**
   - `deliver: origin` sends back to the chat/topic where the cron was created.
   - For Telegram groups, use `telegram:chat_id:thread_id` if needed.

5. **Skills are Loaded Fresh**   
   - Each job run starts with a clean context; listed skills are loaded before the prompt executes.

## One-Day Reminders at Fixed Local Times

For a reminder requested only on one calendar day, create one absolute ISO one-shot job per intended firing time. Do not use an annual cron expression unless the user explicitly asks for recurrence.

1. List existing jobs first to prevent duplicates.
2. Resolve the user's timezone and the current local date. If the request omits a year and that date has passed, use the next calendar occurrence and state the selected date in the completion message.
3. Convert every requested local time to UTC before creating jobs. Treat midnight rollover as a separate UTC date; never silently lose the last local reminder.
4. Give each job an unambiguous name containing the local date and hour, set `deliver: origin` unless a different destination was requested, and instruct the agent to emit the reminder text exclusively.
5. Verify the complete set with `cronjob(action='list')`: count, one-shot status, destination, and every `next_run_at` timestamp.

For a worked Brazil-time example, see [references/one-day-local-reminders.md](references/one-day-local-reminders.md).

## Verification

After creating or updating a job:
- Run `cronjob(action='list')` and confirm the job appears with correct `model`, `provider`, `schedule`.
- For agent-based jobs, check that the `skills` array is present.
- For `no_agent` jobs, ensure the script is in `~/.hermes/scripts/` (or use absolute path in `script:` field).

## Example: Lead Monitoring Cron (from session)

See the `lead-monitoring` skill for the monitoring logic. This cron job runs the monitor every 15m, uses the Nemotron model via OpenRouter, and delivers new leads to the originating chat.

---
*Tip: If you need to change the model/provider of an existing cron, remove and recreate rather than trying to update.*