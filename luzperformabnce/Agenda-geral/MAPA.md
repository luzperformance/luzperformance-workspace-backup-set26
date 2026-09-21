# MAPA — Agenda-geral/

> Central operacional de agenda: lembretes, marcações e acesso ao Google Calendar.
> Tópico correspondente no Telegram: **Agenda Geral**.

## Estrutura

- `lembretes.md` — lembretes e marcações avulsas, ordem cronológica, append-only.

## Fronteiras

- Escala de plantões **não** mora aqui: fica em `/data/workspace/Luzperformanbce/Plantões/` (registro mestre `agenda.md` + HTML mensal).
- Esta pasta é para compromissos gerais, prazos e lembretes que não são plantão.

## Regras

- Nenhum evento é criado, alterado ou apagado no Google Calendar sem confirmação explícita do Dr. Vinícius.
- Status do calendário: **conectado em 20/09/2026** — token em `/data/google_token.json` (escopos Gmail, Calendar, Drive, Contacts, Sheets, Docs). Escala de outubro ainda **não** lançada no Calendar: aguardando confirmação.
- Escalas: outubro 2026 confirmada (11 plantões, 120h) e novembro 2026 confirmada (4 plantões, 36h). Ambas registradas no mestre `Plantões/agenda.md`; nenhuma lançada no Calendar.
