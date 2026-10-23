# AISpace

**Spațiul de lucru AI al firmei tale.** Îi explici o singură dată ce face firma, cine lucrează cu tine și cum lucrați. De acolo, AI-ul ține minte, face treaba și automatizează ce se repetă.

## Ce primești

- **Memoria firmei**: echipa, proiectele, clienții tip, termenii voștri. Nu mai explici de la zero în fiecare discuție.
- **Lucrează, nu doar sfătuiește**: citește emailuri, cercetează pe web, completează în browser, generează oferte și documente.
- **Automatizări din povești**: îi povestești un proces pe care îl faci de mână și îl transformă într-o comandă pe care o folosești oricând.
- **Conectori**: Gmail, Calendar, Jira, Slack și altele. Unde nu există conector, lucrează direct în Chrome, ca un om.
- **Pentru toată echipa**: contextul se publică pe GitHub, iar colegii pornesc cu tot ce s-a învățat deja.
- **Cu garduri de protecție**: cere acordul înainte să trimită sau să modifice ceva, ține cheile în seif și oprește instrucțiunile ascunse în documente.

## Cum începi (5 minute)

1. Apasă **Use this template** și creează repo-ul firmei tale (recomandat privat).
2. Deschide-l în [Claude Code](https://claude.com/claude-code), din aplicația desktop sau din terminal.
3. Scrie `/install`. Onboarding-ul te ghidează de acolo.

## Comenzi

| Comandă | Ce face |
|---|---|
| `/install` | Te cunoaște: firma, echipa, tool-urile. Conectează ce folosești. |
| `/process` | Transformă un proces manual într-o automatizare. |
| `/recommend-process` | Îți spune ce merită automatizat la tine. |
| `/planning` | Task-uri noi și task-uri care se repetă. |
| `/add-context` | Învață din documente, linkuri sau din memoria altui AI. |
| `/add-teammate` | Adaugă un coleg, cu accesul potrivit. |
| `/sync` · `/history` | Publică și primește modificări; vezi cine a schimbat ce și de ce. |
| `/guide` · `/quiz` | Ghid pentru începători și un quiz despre AI. |
| `/update-template` | Aduce îmbunătățirile noi ale șablonului, fără să atingă ce ai construit. |

## Transparență

Totul e text: poți citi orice regulă, comandă sau protecție din acest repo. Șablonul nu conține date personale; ce află AI-ul despre firma ta rămâne în repo-ul firmei tale. Fiecare firmă răspunde de cum folosesc membrii ei AISpace; șablonul oferă aceste măsuri, nu garanții.

---

## Detalii tehnice

Sistem personal de task management + memorie de lucru pentru Claude Code, folosit conversațional (fără server/backend propriu — doar fișiere `.md` + `dashboard.html` local).

### Setup (prima dată după clone)

Nu trebuie rulat nimic manual. Deschide folderul cu Claude Code — la prima interacțiune, `CLAUDE.md` verifică dacă `my-context/profile.md` există. Dacă nu există (clone proaspăt sau `my-context/` golit), pornește automat onboarding-ul — același flux ca `/install`, pe care îl poți rula și manual oricând. Te întreabă:

- pe ce lucrezi (context business/proiect, terminologie),
- cu cine lucrezi (oameni, roluri),
- ce tool-uri folosești (Gmail, Jira, Slack…), ca să conecteze MCP-urile potrivite.

La final pornește un live server (`live-server`, instalat dacă lipsește) și deschide `dashboard.html` în browser.

Din răspunsuri generează `my-context/profile.md`, `my-context/TASKS.md` și, unde are sens, fișiere individuale în `my-context/people/` și `my-context/projects/` — toate pornind din șabloanele din `templates/`.

### Structură

| Path | Tracked în git? | Ce e |
|------|:---:|------|
| `CLAUDE.md` | ✅ | Doar regulile care se aplică mereu + check-ul de onboarding + tabelul „când citesc ce" (se încarcă la fiecare sesiune, deci ținut mic) |
| `reference/` | ✅ | Detaliile din spatele regulilor (workflow task-uri, personal vs. echipă, skill-uri/playbook-uri, dashboard, compliance furnizori) — citite doar când subiectul apare |
| `templates/` | ✅ | Șabloane pentru profil, oameni, proiecte, context, task-uri, skill-uri |
| `.agents/skills/adapt-to-codex/` | ✅ | Skill rulat în Codex: generează local `AGENTS.md` și `.agents/skills/` din `CLAUDE.md` și `.claude/skills/` (rămân în `.gitignore`) |
| `.claude/skills/` | ✅ | Comenzile `/install`, `/planning`, `/process`, `/recommend-process`, `/guide`, `/add-context`, `/sync`, `/history`, `/add-teammate`, `/update-template` și `/quiz` (legenda lor e în dashboard, pagina „Comenzi") |
| `playbooks/` | ✅ | Rețete reutilizabile pentru cereri comune de automatizare de la clienți (ex. Instagram DM, WhatsApp, chatbot pe site) — cunoaștere generică, nu date personale |
| `dashboard.html` | ✅ | Unealtă generică, read-only — citesc fișierele locale direct, fără server. Nicio modificare (task-uri, oameni, proiecte) nu se face din dashboard; toate vin din sesiunile de Claude Code |
| `my-context/profile.md` | ❌ | Contextul tău personal/de business (Me/People/Terms/Projects/Preferences) |
| `my-context/people/*.md`, `my-context/projects/*.md`, `my-context/context/*.md` | ❌ | Detalii per persoană/proiect |
| `my-context/TASKS.md` | ❌ | Task-urile tale curente — personale, nu se publică nici în repo-ul firmei |
| `my-context/skills/*.md` | ❌ | Modurile tale de lucru, învățate de Claude din task-uri și aplicate automat data viitoare |
| `my-context/diagrams/`, `my-context/docs/` | ❌ | Output-uri generate din task-uri (specifice ție) |
| `my-context/assets/` (folderul) | ✅ | Zonă de drop pentru fișiere pe care vrei să lucrezi cu Claude (ex. excel-uri) — folderul există după clone, ca să ai unde pune fișiere |
| `my-context/assets/*` (conținutul) | ❌ | Fișierele propriu-zise puse acolo — personale, nu se distribuie prin git |

Fișierele marcate ❌ sunt ignorate în **repo-ul-șablon**, printr-un bloc marcat `AISPACE-TEMPLATE-ONLY` din `.gitignore`: sunt specifice fiecărei firme și nu se distribuie prin șablon. Într-un repo creat din șablon, `/install` (pasul „Publicarea contextului") rulează `scripts/firm-mode.sh`, care șterge acel bloc: de acum `my-context/` și `team/` se publică automat de către owner-i, pe un singur `main` (conflictele după `reference/sync-conflicts.md`). Rămân ignorate mereu `TASKS.md`, conținutul din `assets/`, `.env` și datele locale ale biroului 3D. Scriptul recunoaște repo-ul-șablon după adresa din `.claude/template-source` și refuză să ruleze acolo.

### Actualizare context

Ca să completezi sau corectezi memoria (oameni noi, proiecte noi, task-uri sincronizate dintr-un tracker), spune-i pur și simplu lui Claude ce s-a schimbat, sau folosește `/add-context`.
