---
name: lead-monitoring
description: "Use when monitoring a lead spreadsheet for new rows."
version: 1.0.0
---

# Monitoramento de leads por planilha

Use quando o usuário quiser vigiar uma Google Sheet/CSV/XLSX, detectar um novo lead na última linha e receber uma notificação estruturada.

## Princípios

- Antes de escrever o monitor, descubra: origem da planilha, aba/range, cabeçalhos, frequência e canal de entrega.
- Para Google Sheets, carregue `google-workspace`, valide a autenticação antes de tentar ler a planilha e use acesso somente de leitura quando o fluxo não precisa alterar dados.
- Nunca envie mensagens para um canal externo sem autorização explícita. Um pedido como “me informe aqui” autoriza a entrega no chat de origem, mas ainda exige configurar corretamente o destino do cron.
- Não presuma nomes de colunas: leia o cabeçalho e a última linha antes de mapear o lead.

## Fluxo

1. **Inspecionar a fonte.** Extraia o ID da planilha e o `gid` da URL. Para Google Sheets, consulte os metadados (`sheets.properties`) e associe o `gid` ao nome real da aba antes da primeira leitura; então use uma faixa explícita como `Nome da aba!A:ZZ`. Leia cabeçalho e as duas últimas linhas e confirme se há ao menos uma linha de dados.
2. **Definir a regra de detecção.** No modo “última vs. penúltima”, compare as duas linhas após normalizar espaços e valores vazios. Se forem iguais, produza saída vazia; se forem diferentes, produza apenas o lead da última linha.
3. **Mapear a mensagem.** Preserve os campos da planilha e apresente-os com os nomes do cabeçalho. Omitir colunas inteiramente vazias.
4. **Normalizar telefone.** Remova caracteres não numéricos. Se solicitado, remova o prefixo internacional `55` somente quando ele estiver no início e sobrar um número brasileiro válido. Formate o resultado conforme a política escolhida; não invente dígitos, DDD ou país quando o dado estiver incompleto.
5. **Evitar duplicidade.** O cron deve enviar mensagem somente quando o script imprimir conteúdo. Para detecção robusta além da comparação de linhas, salve um identificador/hash do último lead notificado em arquivo de estado dentro do diretório do projeto.
6. **Testar antes de agendar.** Rode casos com linhas iguais, linhas diferentes, celular de 11 dígitos, telefone de 10 dígitos, número com `+55`, e valor inválido/vazio. Só então configure o cron na frequência aprovada.

## Telefone brasileiro

Há duas políticas possíveis e elas não são equivalentes; confirme a intenção se o pedido for ambíguo:

- **Nacional (recomendada quando “retire +55/55”):** `(DD) 9XXXX-XXXX` ou `(DD) XXXX-XXXX`.
- **Internacional legível:** `55 (DD) 9XXXX-XXXX`.

Após limpar, um número brasileiro válido tem normalmente 10 ou 11 dígitos, incluindo DDD. Se começar com `55` e tiver 12 ou 13 dígitos, remova apenas esse prefixo antes de formatar. Para outro tamanho, devolva o valor limpo marcado como inválido, sem mascará-lo como um telefone válido.

## Exemplo de saída

```text
Novo lead
Nome: Ana Souza
Telefone: (48) 99999-1234
E-mail: ana@exemplo.com
Origem: Instagram
```

## Verificação

- A leitura retorna cabeçalho e as duas últimas linhas corretas.
- Linhas iguais geram stdout vazio e nenhuma entrega.
- Linhas diferentes geram uma única mensagem com os campos da última linha.
- Telefones `+55 (48) 99999-1234`, `5548999991234` e `(48) 99999-1234` resultam em `(48) 99999-1234` sob a política nacional.
- Após habilitar o cron, faça uma execução manual e confirme que o destino é o chat autorizado.

## Pitfalls

- A comparação simples entre última e penúltima linha não avisa um novo lead se ele for idêntico ao anterior; use estado por ID/hash quando essa possibilidade importar.
- Não exponha tokens OAuth ou conteúdo integral da planilha nos logs.
- Uma planilha sem linhas de dados não deve gerar aviso nem erro ruidoso.
- Para cron `no_agent`, o script precisa ficar em `~/.hermes/scripts/` ou `/data/scripts/` e ser referenciado pelo nome relativo (ex: `monitor_leads_novos.sh`). O `workdir` define onde o script executa, não onde ele está salvo — pitfall comum: script existe no `workdir` mas o cron não acha porque só procura nos paths de scripts. Use `every 15m` (não `15m`) para recorrência e leia o job criado de volta para confirmar `repeat: forever`, `no_agent: true`, e `script` definido.
- Após criar o cron `no_agent`, confirme que o job tem `script` definido e `no_agent: true`. O script deve estar em `~/.hermes/scripts/` ou `/data/scripts/` e ser executável (`chmod +x`).

## Auditoria e recuperação de falhas

Antes de concluir que “não há lead novo”, diferencie **silêncio saudável** de **falha silenciosa**:

1. Leia o job e confirme `last_status`, `script`, `no_agent`, `workdir` e o próximo agendamento.
2. Execute o script manualmente e preserve `stdout`, `stderr` e código de saída. `stdout` vazio + saída 0 significa que não houve novidade; saída não-zero exige diagnóstico antes de falar de leads.
3. Para auditar sem alterar o estado de deduplicação, leia a última linha e compare com `last_notified_row.json`; não rode o comando de notificação só para inspecionar, pois ele pode gravar o estado.
4. Em Google Sheets, `invalid_grant` significa que o refresh token expirou ou foi revogado. Gere uma nova URL de autorização com o fluxo OAuth já configurado, peça a URL completa de retorno em `localhost:1` e só então troque o token. Trocar modelo/LLM não corrige OAuth.

## Watchdog de saúde do cron

Para crons críticos como monitor de leads, crie um segundo cron `no_agent` que audita a saúde do principal a cada 30 min. Veja implementações de referência em `references/watchdog_example.py` e `references/watchdog_wrapper.sh`. Comportamento:

- **Silencioso quando OK**: testa conectividade com a fonte de dados (ex: lê a planilha). Se funcionar, stdout vazio = nenhuma entrega.
- **Acumula falhas**: salva contagem de falhas consecutivas em arquivo de estado JSON.
- **Na 3ª falha seguida**: audita e tenta consertar automaticamente: verifica se o script existe nos paths corretos e recria se necessário; tenta renovar token OAuth expirado; checa dependências Python. Se conseguir consertar, zera o contador e segue silencioso.
- **Se não conseguir consertar**: imprime no stdout a mensagem exata combinada com o usuário: "Não foi possível concertar o Cron". Pode incluir o último erro e as tentativas feitas em linhas seguintes. O cron entrega esse alerta no chat de origem.
- **Estado**: salvo no diretório do projeto como `watchdog_state.json`. Reset manual: deletar o arquivo de estado.
