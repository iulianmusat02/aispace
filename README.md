# aispace

Sistem personal de task management + memorie de lucru pentru Claude Code, folosit conversațional (fără server/backend propriu — doar fișiere `.md` + `dashboard.html` local).

## Setup (prima dată după clone)

Nu trebuie rulat nimic manual. Deschide folderul cu Claude Code — la prima interacțiune, `CLAUDE.md` verifică dacă `my-context/profile.md` există. Dacă nu există (clone proaspăt sau `my-context/` golit), pornește automat onboarding-ul — același flux ca `/install`, pe care îl poți rula și manual oricând. Te întreabă:

- pe ce lucrezi (context business/proiect, terminologie),
- cu cine lucrezi (oameni, roluri),
- ce tool-uri folosești (Gmail, Jira, Slack…), ca să conecteze MCP-urile potrivite.

La final pornește un live server (`live-server`, instalat dacă lipsește) și deschide `dashboard.html` în browser.

Din răspunsuri generează `my-context/profile.md`, `my-context/TASKS.md` și, unde are sens, fișiere individuale în `my-context/people/` și `my-context/projects/` — toate pornind din șabloanele din `templates/`.

## Structură

| Path | Tracked în git? | Ce e |
|------|:---:|------|
| `CLAUDE.md` | ✅ | Doar regulile care se aplică mereu + check-ul de onboarding + tabelul „când citesc ce" (se încarcă la fiecare sesiune, deci ținut mic) |
| `reference/` | ✅ | Detaliile din spatele regulilor (workflow task-uri, personal vs. echipă, skill-uri/playbook-uri, dashboard, compliance furnizori) — citite doar când subiectul apare |
| `templates/` | ✅ | Șabloane pentru profil, oameni, proiecte, context, task-uri, skill-uri |
| `.claude/skills/` | ✅ | Comenzile `/install`, `/planning`, `/process`, `/conectori` și `/quiz` (legenda lor e în dashboard, pagina „Comenzi") |
| `playbooks/` | ✅ | Rețete reutilizabile pentru cereri comune de automatizare de la clienți (ex. Instagram DM, WhatsApp, chatbot pe site) — cunoaștere generică, nu date personale |
| `dashboard.html` | ✅ | Unealtă generică, read-only — citesc fișierele locale direct, fără server. Nicio modificare (task-uri, oameni, proiecte) nu se face din dashboard; toate vin din sesiunile de Claude Code |
| `my-context/profile.md` | ❌ | Contextul tău personal/de business (Me/People/Terms/Projects/Preferences) |
| `my-context/people/*.md`, `my-context/projects/*.md`, `my-context/context/*.md` | ❌ | Detalii per persoană/proiect |
| `my-context/TASKS.md` | ❌ | Task-urile tale curente |
| `my-context/skills/*.md` | ❌ | Modurile tale de lucru, învățate de Claude din task-uri și aplicate automat data viitoare |
| `my-context/diagrams/`, `my-context/docs/` | ❌ | Output-uri generate din task-uri (specifice ție) |
| `my-context/assets/` (folderul) | ✅ | Zonă de drop pentru fișiere pe care vrei să lucrezi cu Claude (ex. excel-uri) — folderul există după clone, ca să ai unde pune fișiere |
| `my-context/assets/*` (conținutul) | ❌ | Fișierele propriu-zise puse acolo — personale, nu se distribuie prin git |

Fișierele marcate ❌ sunt în `.gitignore` — sunt specifice fiecărei persoane/business și se regenerează local prin onboarding, nu se distribuie prin git.

## Actualizare context

Ca să completezi sau corectezi memoria (oameni noi, proiecte noi, task-uri sincronizate dintr-un tracker), spune-i pur și simplu lui Claude ce s-a schimbat, sau folosește skill-ul `productivity:update`.
