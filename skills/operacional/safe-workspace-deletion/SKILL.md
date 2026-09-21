---
name: safe-workspace-deletion
description: Use when safely deleting workspace items.
version: 1.0.0
---

# Remoção Segura do Workspace

Remove arquivos, diretórios e frentes duráveis sem perda irreversível, índices quebrados ou decisões apagadas. O padrão é **lixeira recuperável**, nunca `rm`.

## Quando usar

- O usuário pede para excluir um diretório, seus conteúdos ou uma frente de trabalho.
- Uma área durável deixa de existir e seus mapas ou registros precisam refletir isso.
- O pedido usa contexto relativo, como “exclua tudo aqui”, após discutir uma pasta ou frente específica.

Não usar para limpeza de arquivos transitórios que já possuem política própria de retenção, nem para exclusão que não tenha aprovação direta do usuário autorizado.

## Regras de escopo e autorização

- Excluir é uma ação destrutiva: confirmar que o pedido veio de quem tem autoridade para isso.
- Se o referente imediato da conversa aponta inequivocamente para uma pasta ou frente, trate-o como o escopo. Não amplie para a pasta-pai ou para o workspace inteiro.
- Se houver duas interpretações materialmente diferentes, faça uma única pergunta de escopo antes de mover algo.
- “Tudo” inclui os arquivos de mapa dentro do alvo. O diretório-alvo também sai, salvo se o usuário pedir explicitamente para manter a pasta vazia.

## Procedimento

1. **Delimitar e inspecionar.** Confirme a existência do alvo e leia os `MAPA.md` aplicáveis antes de alterar o estado. Identifique os índices-pai e o arquivo mensal de decisões que precisarão ser atualizados.

2. **Mover para uma lixeira recuperável.** Prefira o utilitário nativo de lixeira disponível no ambiente. Não substitua uma lixeira ausente por exclusão permanente. Quando não houver utilitário e o ambiente Linux usar a convenção XDG, siga o fallback seguro em `references/xdg-trash-fallback.md`.

3. **Sincronizar a arquitetura.** Depois de confirmar que o alvo saiu do local original:
   - remova sua entrada dos `MAPA.md` pais e do mapa raiz, quando aplicável;
   - preserve decisões históricas de criação;
   - acrescente uma decisão curta de desativação, informando que o conteúdo foi movido para lixeira recuperável.

4. **Verificar antes de concluir.** Com evidência real, confirme:
   - o caminho original não existe;
   - a cópia recuperável e seus metadados existem na lixeira;
   - nenhum mapa ativo continua apontando para o alvo;
   - a desativação foi registrada sem apagar o histórico anterior.

## Armadilhas

- Não usar `rm -rf`, mesmo quando a pasta pareça vazia.
- Não deixar uma referência para um `MAPA.md` que acabou de ser removido.
- Não apagar o registro histórico de criação para “limpar” a decisão: decisões são append-only.
- Não marcar como concluído apenas porque o comando de movimentação retornou sucesso; verifique origem, destino, índices e registro.

## Comunicação

Informe em uma frase o que saiu, que foi para a lixeira recuperável e que os índices foram atualizados. Só informe o caminho interno da lixeira se isso ajudar na recuperação.

## Referência

- `references/xdg-trash-fallback.md` — fallback Linux com XDG Trash quando não há utilitário nativo.
