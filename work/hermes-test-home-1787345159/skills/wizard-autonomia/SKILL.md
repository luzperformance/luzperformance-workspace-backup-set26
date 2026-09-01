---
name: wizard-autonomia
description: "Use quando configurar aprovações e limites de autonomia."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# wizard-autonomia

Explique os modos `smart`, `manual` e `off`. Recomende `smart`. Só altere após escolha explícita:
```bash
hermes config set approvals.mode smart
```
Mantenha `security.redact_secrets` ativo. Não apresente `--yolo` como padrão. Depois verifique com `hermes config get approvals.mode` e informe que algumas mudanças exigem nova sessão.
