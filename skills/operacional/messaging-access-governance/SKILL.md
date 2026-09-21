---
name: messaging-access-governance
description: "Govern messaging access and delegated authority safely."
version: 0.1.0
author: Dr. Vinícius Luzardi, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [telegram, messaging, allowlist, admin, governance]
    related_skills: []
---

# Messaging Access Governance

Configure who can reach Hermes on messaging platforms and what authority those people have. Treat platform authentication, gateway command privileges, and the agent's operational delegation policy as separate controls.

## When to Use

- Adding, removing, or changing a trusted operator on Telegram or another messaging gateway.
- Granting a secretary, operator, or partner delegated authority.
- Reviewing whether a gateway allowlist actually gives the intended access.

Do not use this for a public channel, guest access, or a one-time chat invitation.

## Prerequisites

- Confirm the person’s immutable platform user ID; never use a display name or `@username` as authorization.
- Obtain explicit approval from the account owner for any change to allowlists, admin tiers, channels, or permissions.
- Load the platform’s current official Hermes documentation before changing configuration.

## Procedure

1. Inspect the existing allowlist and admin list without exposing credentials or unrelated personal IDs. Preserve existing entries unless the owner explicitly asks to remove them.
2. Add the trusted user to the platform allowlist. For Telegram gateway configuration, use both `allow_from` and `allow_admin_from` when the person needs all slash commands.
3. Keep the two lists deliberately aligned only when every allowed user should remain an admin. `allow_admin_from` activates tiering; other allowed users then lose unrestricted slash-command access unless explicitly granted commands.
4. Record delegated authority in project governance, separately from gateway config. State the permitted domains and excluded domains in plain language.
5. Apply/restart the gateway only when required by the documented configuration lifecycle. Warn that a gateway restart can interrupt the active session.
6. Verify persistence by reading the resolved config and report only booleans/counts, not secrets or unrelated IDs. Verify live access with a message from the authorized user when possible.

## Delegated-Authority Template

> Platform ID `<ID>` is an authorized delegate of `<owner>`. Their operational instructions have the owner’s priority for `<permitted domains>`. Direct owner approval remains required for credentials and access, payments or purchases, irreversible deletion, public posting, security changes, integrations, scheduled jobs, channels, and permissions.

Adjust the exclusions only with explicit owner approval. “Full access” at the gateway does not automatically mean unlimited business authority.

## Pitfalls

- **`'*'` é allow-all de verdade, não placeholder.** O runtime resolve a allowlist em `gateway/authz_mixin.py` com `return "*" in allowed or candidate in allowed`. Confirmar a semântica de wildcard lendo o código instalado antes de afirmar o que uma lista concede ou nega.
- **As duas listas são um controle só.** `allow_admin_from` com `'*'` promove todo usuário permitido a admin, com todos os slash commands; `allow_admin_from` ausente desliga o tiering e dá acesso amplo a quem passou pelo `allow_from`. Revisar sempre em par.
- **`approvals.mode: off` é YOLO global**, não por plataforma: vale para gateway, cron e single-query. Num bot com acesso a terminal, allowlist aberta somada a aprovações desligadas deixa qualquer estranho que encontre o bot executar comando sem gate.
- **Antes de abrir uma allowlist, decidir com o dono o que o bot expõe.** Se o workspace tem dado clínico identificável ou caminho de credencial, “abre para todos e depois eu coloco um placeholder” não é caminho: recomendar manter só IDs nomeados e responder com a postura mínima, não com o pedido literal.
- `allow_from` permits contact; it does not necessarily confer full slash-command access once admin/user tiering is enabled.
- DM admin status and group admin status can be distinct gateway scopes.
- Do not put access-control IDs only in `SOUL.md`, `USER.md`, or chat memory: those documents express policy but do not authenticate users.
- Do not overwrite an allowlist with a single new ID; merge and deduplicate it.
- Never print bot tokens, API keys, or the full pre-existing allowlist in the response.

## Verification

- A semântica de `'*'` e do tiering admin/user foi lida no código instalado (`gateway/authz_mixin.py`, `gateway/slash_access.py`), não inferida da documentação.
- The intended ID is present in the resolved allowlist and admin list for the applicable scope.
- Existing allowed users remain present.
- The governance record defines both granted authority and reserved owner approvals.
- The gateway is healthy after configuration is applied, and the delegate can perform an allowed test action.
