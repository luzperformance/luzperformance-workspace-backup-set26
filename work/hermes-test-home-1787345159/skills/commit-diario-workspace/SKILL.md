---
name: commit-diario-workspace
description: "Use quando criar rotina diária de commit do projeto."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# commit-diario-workspace

Pré-requisito: repositório privado já validado. Crie um job com `cronjob` ou `hermes cron` cujo prompt seja autocontido e cujo `workdir` seja a raiz do projeto. O job deve sair silenciosamente se não houver mudanças, bloquear arquivos sensíveis e nunca fazer force-push. Teste manualmente uma execução antes de ativar recorrência.
