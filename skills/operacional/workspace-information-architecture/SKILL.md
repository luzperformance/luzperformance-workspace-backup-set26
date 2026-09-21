---
name: workspace-information-architecture
description: Use when organizing durable workspace folders and maps.
version: 0.2.0
author: Vinícius Luzardi, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workspace, organization, operations, knowledge]
    related_skills: []
---

# Arquitetura de Informação do Workspace

Organiza frentes duráveis de trabalho sem criar pastas órfãs ou deixar decisões apenas no chat. Aplica-se a áreas operacionais e de conhecimento; não substitui o PRD de um projeto novo nem a estrutura editorial de conteúdo.

## Quando usar

- O usuário define para que servirá uma pasta existente ou pede uma nova frente de trabalho.
- Materiais recorrentes — aulas, referências, SOPs, pesquisas ou ativos operacionais — precisam de um lugar permanente.
- Uma área passa a ter finalidade própria e precisa ser descoberta no mapa do workspace.

Não usar para um arquivo isolado, material transitório ou projeto de software/produto que exige `projects/{nome}/PRD.md`.

## Princípios

- Pasta sem finalidade explícita vira cemitério de arquivos; registrar propósito antes de acumular material.
- Não salvar entregáveis na raiz do workspace.
- Cada frente recorrente recebe um `MAPA.md` local, e seus índices-pai precisam apontar para ela.
- Uma decisão durável deve entrar no registro mensal de `decisions/`, em vez de ficar apenas na conversa.

## Procedimento

1. **Mapear o destino.** Leia o `MAPA.md` raiz e o mapa da pasta-pai antes de criar ou classificar uma frente. Confirme o caminho com `search_files` e preserve as convenções já existentes.
   - Quando o usuário citar um caminho que não existe no disco, não presuma renomeação nem corrija a grafia por conta própria: procure o diretório de migração/arquivo, crie no caminho pedido e registre a divergência junto com o caminho atual equivalente.

2. **Criar somente a estrutura necessária.** Quando a pasta for uma frente recorrente, crie o diretório e um `MAPA.md` que declare: finalidade, tipos de material aceitos e destino de derivados. Use `write_file`; não crie subpastas especulativas.

3. **Tornar a frente navegável.** Atualize com `patch` o `MAPA.md` da pasta-pai e o mapa raiz quando este indexar áreas ativas. Cada entrada deve dizer claramente o que a pasta guarda e apontar para o mapa local.

4. **Registrar a decisão.** Leia `decisions/MAPA.md` e o arquivo mensal vigente antes de acrescentar uma nota curta e append-only: data, nome da frente e escopo aprovado. Não registre tarefas em aberto como decisões.

5. **Separar material derivado.** Quando um ensino virar roteiro, post ou rascunho editorial, mova o derivado para a área indicada no mapa de conteúdo; mantenha nesta frente as fontes, anotações e aplicações práticas.

6. **Verificar e comunicar.** Confirme que o diretório, o `MAPA.md` local e todas as entradas de índice existem. Entregue o caminho criado e a finalidade registrada, sem narrar etapas intermediárias.

## Padrão de mapa local

Um mapa local deve conter, no mínimo:

- Uma frase de finalidade.
- Os materiais que pertencem à frente.
- Convenções de nomes ou organização apenas quando forem necessárias agora.
- O destino dos derivados e decisões, quando esses ativos cruzarem para outras áreas.

Veja `references/recurring-front-pattern.md` para o padrão condensado.

## Armadilhas

- Não assumir que toda pasta nova é um projeto: projetos exigem PRD; frentes de conhecimento normalmente exigem apenas mapa e decisão.
- Não criar taxonomia de módulos, aulas ou subpastas antes de haver material real.
- Não atualizar somente o mapa local: uma frente não indexada deixa de ser encontrável no próximo contexto.
- Não gravar em pasta de registros pelo caminho citado no mapa: confirme o diretório real com `ls` — mapas podem apontar para um nome antigo (`decisions/` vs `decisoes/`) e o registro termina em um lugar que ninguém lê.
- Não comunicar "criado" sem conferir o caminho exato com `ls -la` depois da escrita.
- Se o usuário disser para parar, interrompa a execução atual. Só retome diante de uma nova instrução clara.

## Verificação

A organização está concluída somente quando:

- O diretório está no destino aprovado, conferido com `ls -la` depois da escrita.
- O `MAPA.md` local explica sua finalidade.
- Os mapas-pai aplicáveis listam a nova frente.
- A decisão de criar ou definir a frente está registrada no arquivo mensal de decisões.
