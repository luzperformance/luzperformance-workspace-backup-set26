---
name: shift-scheduling
description: Create verified shift schedules as HTML calendars.
version: 0.2.0
author: Dr. Vinícius Luzardi, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scheduling, shifts, calendar, html]
    related_skills: [claude-design, verification-before-completion]
---

# Escalas de Plantão

Transforma horários informados por mensagem em uma escala mensal confiável: registro mestre, calendário HTML portátil e arquivo para download. É para escalas pessoais de trabalho/plantão; não cria eventos externos sem aprovação explícita.

## When to Use

## Quando usar

- Pedido para montar, atualizar ou baixar escala de plantões.
- Datas e horários enviados em linguagem natural, inclusive em blocos e com datas repetidas.
- Pedido para reutilizar o design de uma escala/protocolo HTML existente.

Não use para agenda compartilhada, convites ou Google Calendar sem autorização explícita e integração autenticada.

## Dados mínimos

- Mês e ano da escala.
- Dia, mês e início/fim de cada turno.
- Nome do compromisso: padrão `Plantão` quando o usuário não especificar outro.
- Arquivo HTML de referência, se a exigência for manter um design existente.

Assuma o ano corrente apenas se o contexto mensal já o deixar inequívoco. Pergunte uma vez se a data ou o ano mudar materialmente a escala.

Contexto fixo desta operação:

- Pasta: `/data/workspace/Luzperformanbce/Plantões/` — `agenda.md` é o registro mestre; cada mês tem `escala-<mes>-<ano>.html`.
- Meses anteriores já têm HTML pronto: use o último como referência de design em vez de recriar o layout.

## Padrão recorrente e prévia do mês seguinte

O padrão que o Dr. Vinícius dita é "todos os fins de semana (sábado e domingo) das 07h às 19h, mais duas terças-feiras das 13h às 19h". Quando ele pedir um mês sem informar todas as datas, monte a **prévia** espelhando o mês anterior — fins de semana completos + 1ª e 3ª terças — e entregue dizendo explicitamente o que foi assumido.

- Prévia não entra no registro mestre nem no Google Calendar: só escala confirmada entra.
- Registre a prévia no arquivo mensal de `decisions/` marcada como pendente de confirmação, para o próximo contexto saber o que falta.
- Ao montar a prévia, calcule os dias da semana com uma ferramenta; quando o mês começa no domingo, o calendário não tem células vazias no início.

## Procedimento

1. **Consolidar entradas.** Extraia cada data e horário informados, incluindo mensagens anteriores da mesma sequência. Converta para `DD/MM/AAAA`, valide o dia da semana com uma ferramenta e ordene cronologicamente.
   - Não duplique um plantão que apareça duas vezes com os mesmos dados.
   - Se houver conflito real no mesmo dia, mantenha ambos somente quando o usuário indicou explicitamente dois turnos; caso contrário, peça correção.

2. **Separar o período.** Calcule carga e métricas somente dentro do mês da escala. Plantões informados para o mês seguinte entram em um bloco de continuação, sem contaminar os totais do mês. Quando a escala do mês seguinte for montada, esse mesmo plantão passa a contar na carga do novo mês e sai do bloco de continuação do mês anterior.

3. **Atualizar o registro mestre.** Registre cada plantão no arquivo de agenda da pasta de Plantões, com data completa, horário, rótulo e status do calendário. Preserve registros antigos e mantenha ordem cronológica.

4. **Criar o HTML.** Use `write_file` para criar `escala-<mes>-<ano>.html` dentro da pasta de Plantões.
   - Quando houver um HTML referência, preserve deliberadamente sua paleta, tipografia, densidade, cabeçalho, calendário, cartões de estatística e responsividade; remova blocos que não servem à nova escala em vez de carregar conteúdo médico ou texto irrelevante.
   - A superfície é um **Monitor**: o calendário e a escala detalhada têm prioridade sobre hero, cards decorativos ou métricas inventadas.
   - Mostre legenda, calendário de domingo a sábado, lista detalhada e apenas métricas derivadas dos dados (contagem por duração e carga horária).
   - Use HTML autônomo com CSS embutido. Fontes externas são opcionais; o arquivo precisa continuar abrindo diretamente no navegador.

5. **Verificar antes de entregar.** Valide o HTML e confira: número de linhas da lista = número de plantões únicos no mês; número de tags de turnos no calendário = mesmo total; cada horário confere com o registro mestre; a carga é a soma real das durações; datas do mês seguinte estão claramente fora do total. Só então marque como concluído.

6. **Entregar.** Informe o caminho exato e um resumo mínimo. Quando o usuário pedir o HTML para download, envie o próprio arquivo usando `MEDIA:/caminho/absoluto/arquivo.html`.

## Regras de cálculo

- `07h–19h` = 12h; `07h–13h` e `13h–19h` = 6h. Para outros horários, calcule a diferença real, respeitando virada de dia quando declarada.
- O dia da semana é dado calculado, não texto inferido do usuário. Se divergir do que foi escrito, mantenha a data e corrija o rótulo no arquivo.
- Conte estatísticas apenas com dados da própria escala; não repita números do template.

## Pitfalls

- Não criar ou alterar Google Calendar só porque a escala foi registrada localmente. É ação externa e requer confirmação; se não houver autenticação, mantenha o status como pendente.
- Não entregar um caminho local quando o usuário pediu download: anexe o HTML.
- Não dizer "criado" antes de conferir o caminho real com `ls -la`: a resposta de sucesso da ferramenta de escrita não prova que o arquivo ou a pasta estão no disco.
- Não deixar uma data de outro mês escondida no calendário do mês atual; apresente-a como continuação separada.
- Não reutilizar avisos clínicos, protocolos de medicação ou outras seções do HTML referência que não foram solicitadas para a escala.
- Antes de afirmar que nada foi criado, liste a pasta de Plantões: um turno interrompido pode ter gravado os arquivos antes de parar. Não conclua o estado do trabalho pelo histórico do chat nem por processos em execução — abra o diretório de destino e confira.
- Se o arquivo do mês já existe e confere com os dados informados, valide e entregue. Não regenere por cima do mesmo conteúdo nem apresente como recém-criado algo que já estava no disco; se uma resposta anterior afirmou que nada existia, corrija a afirmação antes de seguir.

## Verificação

A entrega está pronta quando o arquivo existe, o HTML é parseado sem erro, todas as datas e horários informados aparecem exatamente uma vez no período, os totais batem e o arquivo pode ser anexado ao usuário.

## Referências

- `references/checklist-validacao.md` — checklist compacto de consolidação e entrega.
