# Hosted Hermes + Keycloak OAuth notes

## Managed/one-click deployments

A web console can be a headless management shell even when it displays a prompt. If `hermes mcp login <name>` prints “Headless environment detected” and does not offer the paste-back prompt, do not treat it as a usable interactive OAuth terminal. The documented preferred route is the Hermes Dashboard or Desktop MCP connector, which performs the authorization in the user’s browser and relays the result to the remote gateway.

Before recommending any CLI workaround, inspect `hermes mcp login --help` on that exact deployment. Do not assume browser-flow or device-flow flags exist from a different Hermes version.

## Keycloak `invalid_scope`

If Keycloak returns a callback URL containing:

```text
error=invalid_scope
error_description=Invalid scopes: <scope-a> <scope-b>
```

the authorization request reached Keycloak but the client is not allowed to request those scopes. Fix the Keycloak client configuration, not the tunnel or redirect URI:

1. Open the relevant client.
2. Add each requested scope under **Client scopes** as a default or optional client scope, according to the provider policy.
3. Keep the exact redirect URI required by the registered client.
4. Retry authorization and only then test the MCP connection.

Realm discovery advertising a scope does not prove that every client may request it.

## Session-specific provider values

For the Luz CRM integration, the non-secret OAuth parameters supplied by the provider were:

```yaml
mcp_servers:
  luz_crm:
    url: "https://mcp.transformandoemsaude.com/mcp"
    auth: oauth
    oauth:
      client_id: "luz-crm-codex"
      token_endpoint_auth_method: "none"
      scope: "espocrm"
      redirect_port: 4321
      redirect_uri: "http://127.0.0.1:4321/callback"
```

The authorizer requested `espocrm` plus `offline_access`. The Keycloak client must permit every requested scope, including scopes added by the OAuth client for refresh-token support. No completed token exchange or successful MCP test was verified in this case; do not represent the integration as connected until the skill’s verification criteria pass.
