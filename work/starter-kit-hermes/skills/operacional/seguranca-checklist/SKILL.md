---
name: seguranca-checklist
description: "Use para auditar segurança e privacidade do Hermes."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# seguranca-checklist

Verifique: `security.redact_secrets`, `approvals.mode`, `privacy.redact_pii`, toolsets ativos, arquivos versionados, permissões do ambiente, gateway e destinos de cron. Não imprima valores secretos. Recomende `smart`, redaction ativa e menor privilégio. Produza achados com severidade, evidência e correção; não aplique mudanças de alto impacto sem autorização.
