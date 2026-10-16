# Task execution workflow (TASKS.md)

Încărcat la cerere din CLAUDE.md: citesc acest fișier înainte să creez, modific sau execut un task.

Task-urile sunt în `my-context/TASKS.md`, vizualizate în dashboard (vezi `reference/dashboard.md`). Singura sursă de adevăr pentru orice modificare (task-uri, oameni, proiecte, memorie) sunt eu, în sesiune, editând fișierele `.md` direct — userul nu operează pe date din dashboard.

**Format linie de task**, cu tag-uri opționale la final (orice ordine):
```
- [ ] **Titlu task** - notă opțională (due: YYYY-MM-DD) (@Assignee) (recurrent: descriere interval) (id: AS-N)
```
- `(due: YYYY-MM-DD)` — termen limită, dacă există.
- `(@Assignee)` — cine e responsabil (dacă nu e userul, notează numele).
- `(recurrent: ...)` — DOAR pentru task-uri care sunt o instrucțiune permanentă, repetitivă (nu un livrabil unic) — ex. `(recurrent: zilnic la 10:00)`. În dashboard, tab-ul Task-uri are 2 subtaburi: „📌 Punctuale" (task-urile normale, cu un singur rezultat) și „🔁 Recurente" (cele cu `recurrent` setat) — ca să nu se amestece și să nu pară "terminate" când ajung într-o coloană Done. Un task normal, cu un singur rezultat și eventual un due date, NU e recurent.

**Când user-ul dă un ID/titlu de task** (ex. "AS-3", "ocupă-te de X"):
1. Citesc `my-context/TASKS.md`, găsesc task-ul (după `id: AS-N` sau titlu).
2. Dacă nu e deja în secțiunea `## În lucru`, îl mut acolo (îl scot din secțiunea curentă, îl adaug în „În lucru") — semnalează vizual, în dashboard, că m-am apucat de el. (Secțiunile standard din `templates/TASKS.template.md`: „În așteptare", „Active", „În lucru", „Finalizate" — dar pot fi adaptate/redenumite liber în `my-context/TASKS.md`.)
3. **Caut un skill potrivit** în `my-context/skills/`, apoi în `team/skills/` (după „Când se aplică"). Dacă există, îl urmez și spun pe scurt userului că îl aplic (ex. „aplic modul tău de lucru pentru diagrame de infrastructură").
4. **Dacă nu există skill — întreb înainte să implementez ceva**: AskUserQuestion „Ai un mod de lucru pe care vrei să mi-l explici pentru acest tip de task?" cu opțiunile „Da, îți explic cum lucrez" / „Nu, propune tu o abordare". Dacă explică → urmez întocmai ce a spus. Dacă nu → propun pe scurt abordarea (pașii + cum va arăta rezultatul) și aștept OK înainte să execut.
5. Parcurg subtask-urile lui, unul câte unul.
6. Pentru fiecare, folosesc orice am nevoie (Bash, Read/Write/Edit, WebSearch, MCP-uri precum draw.io/Gmail, skills) ca să chiar rezolv treaba — nu doar descriu ce ar trebui făcut.
7. **Subtask-uri care sunt acțiuni umane** (discuții, "de trimis către X") nu le pot executa direct — pregătesc sugestii concrete (draft de mesaj/email gata de folosit) în loc să le marchez fals ca gata.
8. **Acțiuni cu efect real** (trimis email, postat, etc.) — cer confirmare înainte de send, nu trimit nimic în numele user-ului fără OK explicit.
9. **Salvez modul de lucru ca skill**: dacă userul a explicat cum lucrează, sau a corectat/validat abordarea mea pe parcurs, scriu sau actualizez skill-ul — în `my-context/skills/<slug>.md` sau `team/skills/<slug>.md`, după caz (vezi `reference/personal-vs-team.md` și `reference/skills-and-playbooks.md`) și îi spun pe scurt ce am reținut. Dacă n-a fost nimic nou de învățat (am aplicat un skill existent fără corecturi), nu scriu nimic.

**Format rezultat — linie imbricată sub subtask (4 spații indent, nu subtask separat):**
```
  - [x] Text subtask
    - Rezultat: ce s-a făcut, cu path relativ către fișiere generate (ex. my-context/diagrams/x.svg) — dashboard-ul le randează ca imagine inline dacă extensia e .svg/.png/.jpg/.gif
  - [ ] Alt subtask (nerezolvabil direct)
    - Sugestie: mesaj/email draft gata de folosit, plus ce blochează (ex. lipsă adresă)
```
Bifez `[x]` pe subtask-ul original DOAR dacă chiar s-a terminat treaba, nu doar pentru că am produs o sugestie.

**Blocaje** — orice găsesc care oprește progresul se scrie ca subtask nou, cu prefix exact `⚠️ Blocaj: ...` (dashboard-ul le sortează automat primele și le colorează roșu — nu necesită nimic în plus, doar prefixul).

Acest workflow nu are nevoie de API key sau backend — e doar eu, în sesiune, citind/scriind fișiere și folosind tool-urile disponibile.
