---
name: remote-mcp-oauth
description: Use when OAuth MCP needs authorization on remote Hermes.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, MCP, OAuth, remote, managed-hosting]
    related_skills: [hermes-agent]
---

# Remote OAuth MCP

Connect OAuth-protected HTTP MCP servers when Hermes runs on a remote, managed, or headless host. Treat the browser and the Hermes runtime as separate machines unless proven otherwise; a loopback callback belongs to the machine that received it.

## When to Use

- An MCP server uses `auth: oauth` and Hermes runs on a VPS, a hosted container, or a managed one-click deployment.
- The browser reaches `127.0.0.1:<port>/callback` but Hermes is elsewhere.
- The authorization server returns `invalid_scope`, `invalid_client`, or a loopback callback error.

Do not use this for API-key MCPs or for OAuth when the browser and Hermes truly run on the same host.

## Prerequisites

- Identify the exact Hermes deployment and profile being configured. Do not reuse an IP address, shell path, or profile from another VPS or gateway.
- Load the native MCP guidance and inspect the installed CLI rather than assuming flags from newer documentation:

  `terminal(command="hermes mcp login --help", timeout=30)`

- Configure non-secret MCP settings through `hermes config set`; secrets belong in the Hermes secret store or OAuth token store.

## Procedure

1. **Ground the runtime.** Confirm which managed instance owns the active `config.yaml` and token store. A web terminal showing “headless” is a remote-runtime signal, not a browser-local terminal.
   - Completion: the intended Hermes profile and deployment are identified before changing its MCP configuration.

2. **Configure the server explicitly.** Set the endpoint, `auth: oauth`, and only provider-supplied OAuth fields such as `client_id`, scope, redirect URI, or token-endpoint auth method. Preserve existing unrelated MCP entries.
   - Completion: `terminal(command="hermes config get mcp_servers.<name>", timeout=30)` returns the intended values.

3. **Choose the authentication surface in this order.**
   - **Dashboard or Hermes Desktop MCP connector:** preferred for hosted deployments; the browser-side UI relays the callback to the remote gateway.
   - **Paste-back:** use only when `hermes mcp login <name>` shows an explicit prompt to paste the callback URL. Copy the full final callback URL from the browser after consent, even if the browser shows a loopback error, and paste it into that same interactive terminal.
   - **SSH forwarding:** use only when Hermes has actually opened its callback listener and the remote host is reachable by SSH. A tunnel reporting connection refused means there is no listener; stop and switch methods rather than retrying the tunnel.
   - **Device code:** use only if the locally installed `hermes mcp login --help` exposes that flow and the authorization server supports it.
   - Completion: a token is written by the selected flow; an authorization URL alone is not a completed login.

4. **Classify authorization errors before changing networking.**
   - `invalid_scope`: the authorization server rejected the client’s requested scopes. Correct the OAuth client’s allowed/default/optional scopes at the provider; changing ports, SSH tunnels, or callback hosts will not fix it.
   - `invalid_client`: check client registration, client identification mode, and any configured client secret or token-endpoint method.
   - callback `connection refused`: distinguish browser-to-localhost routing from a provider-side authorization error.
   - Completion: the fix targets the layer that emitted the error.

5. **Verify only after login succeeds.** Run:

  `terminal(command="hermes mcp test <name>", timeout=60)`

  then `terminal(command="hermes mcp list", timeout=30)`. If the gateway needs reloading, use the supported MCP reload path for that deployment, not an unverified global restart.
   - Completion: the test discovers the server successfully and the MCP tools are listed or otherwise available in the active agent.

## Pitfalls

- Do not claim a hosted terminal is an SSH shell or direct the user to an unrelated VPS. Hosted one-click consoles commonly differ from the agent runtime and may not provide a usable OAuth TTY.
- Do not assume `--flow browser`, device-code flags, or other options exist; installed Hermes versions can differ from current documentation.
- A successful `config set` does not authenticate the server. Token acquisition and `mcp test` are separate acceptance criteria.
- OAuth authorization URLs, callback `code` values, access tokens, refresh tokens, and client secrets are sensitive. Do not persist them in notes, skills, or chat transcripts.

## Verification

Authentication is complete only when all are true:

- `hermes mcp test <name>` connects without asking for authorization;
- `hermes mcp list` shows the configured server; and
- a real MCP tool discovery or invocation succeeds from the target Hermes deployment.

See `references/hosted-hermes-keycloak.md` for the managed-hosting and Keycloak-specific notes captured from this case.
