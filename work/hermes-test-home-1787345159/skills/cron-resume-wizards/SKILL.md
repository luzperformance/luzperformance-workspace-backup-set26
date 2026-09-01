---
name: cron-resume-wizards
description: "Use quando agendar lembrete respeitoso de retomada."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# cron-resume-wizards

Crie job durável com `cronjob`; não use heartbeat. Prompt deve citar a finalidade, ler somente contexto permitido e enviar mensagem apenas quando houver etapa realmente pendente. Limite tentativas, ofereça opt-out e use `attach_to_session` quando o lembrete deve aceitar resposta. Liste e teste o job após criar.
