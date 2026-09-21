# One-day, multi-fire local reminders

## Verified pattern

A user wanted the same reminder throughout a single 12 September, every two hours from 08:00 through 22:00, in Brazil time (America/Sao_Paulo, UTC-3 in September 2027). The current local date was already after 12 September 2026, so the next occurrence was selected: 12 September 2027.

Use **eight absolute one-shot jobs** rather than a recurring cron expression. This avoids accidental annual repetition and makes each intended fire auditable.

| Local time (America/Sao_Paulo) | Absolute UTC schedule |
| --- | --- |
| 08:00 | `2027-09-12T11:00:00Z` |
| 10:00 | `2027-09-12T13:00:00Z` |
| 12:00 | `2027-09-12T15:00:00Z` |
| 14:00 | `2027-09-12T17:00:00Z` |
| 16:00 | `2027-09-12T19:00:00Z` |
| 18:00 | `2027-09-12T21:00:00Z` |
| 20:00 | `2027-09-12T23:00:00Z` |
| 22:00 | `2027-09-13T01:00:00Z` |

The final local 22:00 firing belongs to the following UTC date. It must still be named and reported as the 22:00 local reminder on 12 September.

Each job prompt should constrain delivery to the exact reminder body, with no heading or commentary. After creation, use `cronjob(action='list')` and verify all eight jobs are enabled, `repeat: once`, routed to the intended destination, and have these timestamps.