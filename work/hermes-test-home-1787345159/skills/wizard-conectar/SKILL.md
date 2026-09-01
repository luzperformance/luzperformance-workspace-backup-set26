---
name: wizard-conectar
description: "Use quando conectar modelo, ferramentas, busca e gateway."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# wizard-conectar

## Ordem segura
1. `hermes setup` e `hermes model`.
2. Credenciais por `hermes auth` ou caminho de ambiente oficial. Em hPanel, use Dashboard → Environment.
3. `hermes tools list` e habilite somente toolsets necessários.
4. `hermes gateway setup` para Telegram, WhatsApp ou outro canal.
5. `hermes gateway status` e `hermes logs errors` para validar.

Nunca peça ao usuário para colar tokens no chat. Mudanças de ferramentas exigem `/reset`/nova sessão.
