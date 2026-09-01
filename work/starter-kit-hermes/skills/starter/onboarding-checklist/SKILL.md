---
name: onboarding-checklist
description: "Use quando iniciar ou revisar a configuração do Hermes."
version: 3.0.0
author: Starter Kit Hermes PT-BR
license: MIT
metadata:
  hermes:
    tags: [starter-kit, pt-br]
---

# onboarding-checklist

## Objetivo
Conduzir o onboarding sem sobrescrever configuração existente.

## Fluxo
1. Rode `hermes doctor` e `hermes status --all`; mostre o resultado.
2. Confirme o perfil/home ativo por `$HERMES_HOME` e `hermes config path`.
3. Verifique modelo com `hermes model`/`hermes auth` sem pedir segredo no chat.
4. Ofereça, um passo por vez: `wizard-agente`, `wizard-aluno`, `wizard-autonomia`, `wizard-workspace`, `wizard-conectar`, `wizard-whisper-quick` e `primeira-vitoria`.
5. Use a ferramenta `todo` para progresso da sessão, não um `MEMORY.md` improvisado.
6. Grave em memória apenas preferências e fatos estáveis, com consentimento quando aplicável.

## Critério de conclusão
`hermes doctor` sem bloqueios, skill carregável e uma tarefa real executada/verificada. Inicie nova sessão após instalar ou habilitar skills.
