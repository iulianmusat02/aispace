# Skill-uri învățate și playbook-uri

Încărcat la cerere din CLAUDE.md: citesc acest fișier când creez/actualizez un skill învățat sau când vine o cerere de automatizare pentru un client.

## Skill-uri învățate (my-context/skills/ și team/skills/)

`my-context/skills/<slug>.md` (personale) și `team/skills/<slug>.md` (comune echipei — vezi `reference/personal-vs-team.md`) = modurile de lucru ale userului, învățate din task-uri (explicate de el sau validate după implementare), create din `templates/skills/_skill.template.md`. Scopul: să mă mulez pe felul lui de lucru, nu să reinventez roata sau să impun un mod de lucru care nu e neapărat bun pentru el.
- Slug după **tipul** de task, nu după task-ul concret (ex. `diagrama-infrastructura.md`, nu `as-2.md`), ca să fie reutilizabil.
- Actualizez un skill existent în loc să creez un duplicat; completez „Ultima actualizare".
- Le consult automat înainte de orice task (vezi `reference/task-workflow.md`) — nu sunt comenzi `/`, dar apar în dashboard pe pagina „Comenzi", secțiunea „Skill-uri învățate".

## Playbook-uri de automatizare pentru clienți (playbooks/)

> Punctul de intrare pentru o cerere de automatizare e skill-ul `/process`, care caută conectorii și verifică compliance-ul din surse oficiale. Playbook-urile existente au fost scrise din cunoștințe generale, nevalidate pe clienți reali: le tratez ca note, nu ca adevăr. Un playbook nou scriu doar după o implementare reală validată.

`playbooks/<slug>.md` = cunoaștere reutilizabilă despre tipuri comune de cereri de automatizare de la clienți (ex. răspuns automat pe Instagram, WhatsApp Business, chatbot pe site) — spre deosebire de `my-context/skills/` (despre CUM lucrează userul) sau `my-context/` (date personale), astea sunt tracked în git, nu sunt personale, create din `playbooks/_TEMPLATE.md`.

- **Când vine o cerere de automatizare de la/pentru un client**, pornesc din `/process`. `playbooks/` îmi dă idei (setup, abordare, limitări), dar verific totul în documentația oficială și în `reference/compliance.md` înainte să mă bazez pe ele.
- La `/install`, secțiunea „Automation opportunities" din `team/profile.md` leagă deja canalele/procesele de business ale userului de playbook-urile potrivite (dacă există) — verific acolo întâi, înainte de a căuta din nou în `playbooks/` de la zero.
- **Dacă nu există un playbook pentru cererea respectivă**, o rezolv oricum (vezi „Sunt build/solve/automate-oriented" din CLAUDE.md), și după ce am o abordare validă, scriu un playbook nou din `playbooks/_TEMPLATE.md` — ca la următoarea cerere similară (indiferent de client) să nu mai pornesc de la zero.
- Slug după **platformă + tip de automatizare**, nu după client (ex. `instagram-dm-auto-reply.md`, nu `numele-clientului.md`), ca să fie reutilizabil.
- Actualizez un playbook existent dacă apar detalii noi (ex. o limitare descoperită la implementare reală) în loc să creez un duplicat; completez „Ultima actualizare".

## Chei API / secrete — detalii

Regula scurtă e în CLAUDE.md. Detalii: `.env.example` (tracked) documentează ce variabile sunt așteptate — îl actualizez când un playbook nou introduce o cheie nouă. Scripturile din `my-context/scripts/` încarcă `.env` automat la rulare (vezi `gen-image.sh` ca model). Codul reutilizabil generat pentru playbook-uri (scripturi, nu date de client) e OK să fie tracked în git dacă nu conține nimic specific unui client — de evaluat per caz.
