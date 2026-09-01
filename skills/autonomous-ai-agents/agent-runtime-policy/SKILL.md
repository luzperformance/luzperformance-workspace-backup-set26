---
name: agent-runtime-policy
description: "Use when routing models or pacing external API calls."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-routing, api, rate-limits, runtime-policy]
    related_skills: [codex, hermes-agent]
---

# Agent Runtime Policy

## Overview

Use this skill to select among configured model aliases and to pace external API work predictably. It separates two concerns that are easy to conflate:

1. **Model routing** chooses the least surprising configured model for the task.
2. **Request pacing** batches related operations and respects explicit call/search limits.

The current user-specific values are summarized in `references/current-user-policy.md`; the governing behavior is kept here so it loads with the skill.

## When to Use

Load this skill when:

- choosing between the user's model aliases;
- drafting or reviewing an agent/model routing configuration;
- deciding whether a task warrants an automatic model switch;
- performing repeated API calls or web searches;
- handling an HTTP 429 response.

Do not use this skill to invent provider model IDs, credentials, quotas, or platform capabilities. Discover those from authoritative configuration or documentation.

## Model Routing

### Current policy

- **Terra is the default.** Start with Terra and use it for all work not covered by a more specific rule.
- **Sol is task-routed.** Use Sol for coding/software-development work and long-running tasks.
- **Luna is explicit-only.** Never select Luna automatically. Use it only when the user asks for Luna by name.

### Precedence

Apply the first matching rule:

1. If the user explicitly requests **Luna**, use Luna.
2. If the user explicitly requests **Sol**, use Sol.
3. If the task is coding/software development or long-running, use Sol.
4. Otherwise, use Terra.

An explicit request to use Terra overrides automatic routing to Sol. Never reinterpret “Terra is the default” as “Terra makes the Sol rule unreachable”; default means the fallback after explicit and task-specific routing.

### Configuration discipline

Treat agent names, aliases, and provider model IDs as different fields:

- **Agent name** identifies an agent/persona, such as `terra`.
- **Alias** is the short selector, such as `sol` or `luna`.
- **Provider model ID** is the exact backend identifier.

Do not infer one from another. If the provider ID for Terra has not been supplied, preserve Terra as the routing name and ask for or inspect the exact ID before writing executable configuration. Correct obvious typos only after the user confirms the correction.

### Completion criterion

Model routing is complete only when the selected model follows the precedence above and every model identifier written into configuration was supplied by the user or verified from the live provider/configuration.

## External API Pacing

### Current limits

- Wait at least **5 seconds between API calls**.
- Wait at least **10 seconds between web searches**.
- Run no more than **5 web searches per batch**, then pause for **2 minutes** before another search batch.
- Batch similar work into one request whenever the API supports it; prefer one request for ten comparable items over ten single-item requests.
- On HTTP **429**, stop issuing requests, wait **5 minutes**, then retry conservatively.

### Scheduling requests

1. Group independent, similar operations into the smallest number of supported calls.
2. Classify each outgoing operation as a general API call or web search; apply the stricter applicable interval.
3. Count searches within the current batch and pause after the fifth.
4. Reset neither the batch count nor the 429 cooldown merely because the query wording changed.
5. After a 429 retry, reduce concurrency or batch pressure when possible rather than immediately repeating the same burst.

### Completion criterion

API work is complete only when all required operations have results or a clearly reported blocker, and the request timeline complies with the minimum intervals, batch pause, and 429 cooldown.

## Common Pitfalls

1. **Selecting Luna because a task is difficult.** Difficulty does not authorize Luna; only an explicit user request does.
2. **Leaving Terra for every coding task despite the Sol rule.** Terra is the default, while Sol is the automatic coding/long-task route unless the user explicitly requests Terra.
3. **Making Sol the global default because it handles coding.** Keep Terra as the fallback for ordinary work.
4. **Inventing a Terra provider ID.** A routing label is not proof of an executable backend identifier.
5. **Treating parallel calls as exempt from pacing.** Parallel requests still count as calls and can create a burst; batch at the API level instead.
6. **Retrying immediately after 429.** Observe the full five-minute cooldown.
7. **Serializing batchable work into many calls.** Prefer a supported bulk request and filter/reduce locally.

## Verification Checklist

- [ ] Terra remains the default fallback.
- [ ] Sol is selected for coding or long-running work unless explicitly overridden.
- [ ] Luna appears only after an explicit request by name.
- [ ] No provider model ID was guessed.
- [ ] Similar operations were batched where supported.
- [ ] API and search spacing meets the stated minimums.
- [ ] Search batches contain at most five searches and are separated by two minutes.
- [ ] Any 429 triggered a five-minute stop before retry.
