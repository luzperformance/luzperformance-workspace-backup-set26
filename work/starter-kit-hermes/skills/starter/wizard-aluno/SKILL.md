---
name: wizard-aluno
description: "Use quando registrar preferências estáveis do usuário."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# wizard-aluno

Colete como chamar, idioma, fuso, função, objetivos recorrentes e preferências de resposta. Separe:
- fatos duráveis → ferramenta `memory` no alvo `user`;
- contexto só deste projeto → documento local opcional;
- estado temporário/TODO → `todo` ou sessão, nunca memória persistente.
Leia de volta um resumo e permita correções.
