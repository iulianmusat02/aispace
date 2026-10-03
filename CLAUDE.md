# Memory

## Onboarding check — rulează asta primul, la fiecare sesiune

Verifică dacă `my-context/profile.md` există.

`my-context/` poate fi complet gol sau poate lipsi cu totul (ex. după un reset manual) — e o stare validă, nu o eroare. Tot ce e în el se generează din `templates/` la onboarding; singurul lucru care trebuie să existe mereu e `my-context/assets/.gitkeep` (îl recreez dacă lipsește).

- **Dacă există**: citește-l — conține contextul personal (Me / Tools / Preferences / Open threads). Citește apoi și `team/profile.md` (dacă există) — contextul comun al echipei (Compania / People / Terms / Projects / Tools / Automation opportunities). Împreună sunt sursa de adevăr pentru contextul de business/echipă. Apoi continuă normal cu cererea userului.
- **Dacă NU există**: acesta e un clone proaspăt sau un reset, netrecut prin onboarding. Oprește-te înainte de orice altă acțiune (cu excepția cazului în care userul cere explicit să sară peste onboarding) și rulează fluxul din skill-ul `/install` (`.claude/skills/install/SKILL.md`) — același flux pe care userul îl poate porni oricând manual cu `/install`.

## Comenzi disponibile

Legenda lor, pe înțelesul userului, e în dashboard, pagina „Comenzi" — când adaug/modific o comandă, actualizez și acea pagină (secțiunea `commandsPanel` din `dashboard.html`).

- `/install` — onboarding: întrebări ghidate, conectare MCP-uri, generare `my-context/`, pornire dashboard.
- `/planning` — adaugă task-uri/rutine noi la `my-context/TASKS.md`, reluând doar partea de task-uri din `/install` (nu tot onboarding-ul).
- `/plan` — comanda nativă Claude Code (plan mode): analizez și propun un plan, fără să modific nimic până la aprobare.
- `/quiz` — întrebări de începător despre AI, interactive, cu explicații și scor.

## Reguli generale de lucru (independente de contextul de business — vezi my-context/profile.md și team/profile.md pentru specific)

### Personal vs. echipă (my-context/ vs. team/)

Setup-ul e folosit de mai mulți colegi din aceeași firmă, fiecare cu propria copie a proiectului. Cunoștințele sunt împărțite în două zone:

- **`team/`** — comun, salvat în git, îl primește fiecare coleg: `team/profile.md` (compania, oamenii, termenii, proiectele, tool-urile echipei), `team/people/<slug>.md`, `team/projects/<slug>.md`, `team/skills/<slug>.md` (moduri de lucru valabile pentru toată echipa).
- **`my-context/`** — personal, niciodată în git: `profile.md` (cine sunt eu, preferințele mele, statusul conectării tool-urilor mele, open threads), `TASKS.md`, `skills/` (moduri de lucru doar ale mele), `assets/`.

Reguli:
- **Oameni și proiecte** se scriu în `team/people/` și `team/projects/` (nu în `my-context/`) — sunt aceiași pentru toți colegii. Dashboard-ul le citește din ambele locuri.
- **Când învăț ceva nou** (skill, termen, persoană, proiect) și nu e evident unde aparține, întreb userul pe scurt (AskUserQuestion): „Doar pentru tine" / „Pentru toată echipa". Ce e clar personal (preferințe, task-uri proprii, fișiere private) merge direct în `my-context/`, fără întrebare.
- **Nu pun niciodată în `team/`** date sensibile: parole, tokeni, date de card, informații private despre clienți, fișiere din `assets/`. Pot ajunge la toți colegii și în istoricul git.
- **Skill-uri**: la un task caut întâi în `my-context/skills/`, apoi în `team/skills/`. Dacă amândouă au un skill potrivit, cel personal are prioritate la detalii, dar respect regulile comune din cel de echipă.

### Fișiere de lucru (my-context/assets/)

`my-context/assets/` e zona de drop pentru fișiere pe care userul vrea să lucrez direct — excel-uri, PDF-uri, alte documente. Dacă userul menționează "excel-ul", "fișierul", "documentul" fără path, verific mai întâi acolo. Folderul e tracked în git (gol, cu `.gitkeep`, ca să existe după clone), dar tot ce se pune înăuntru e gitignored — personal, nu se distribuie.

### Skill-uri învățate (my-context/skills/ și team/skills/)

`my-context/skills/<slug>.md` (personale) și `team/skills/<slug>.md` (comune echipei — vezi „Personal vs. echipă") = modurile de lucru ale userului, învățate din task-uri (explicate de el sau validate după implementare), create din `templates/skills/_skill.template.md`. Scopul: să mă mulez pe felul lui de lucru, nu să reinventez roata sau să impun un mod de lucru care nu e neapărat bun pentru el.
- Slug după **tipul** de task, nu după task-ul concret (ex. `diagrama-infrastructura.md`, nu `as-2.md`), ca să fie reutilizabil.
- Actualizez un skill existent în loc să creez un duplicat; completez „Ultima actualizare".
- Le consult automat înainte de orice task (vezi mai jos) — nu sunt comenzi `/`, dar apar în dashboard pe pagina „Comenzi", secțiunea „Skill-uri învățate".

### Playbook-uri de automatizare pentru clienți (playbooks/)

`playbooks/<slug>.md` = cunoaștere reutilizabilă despre tipuri comune de cereri de automatizare de la clienți (ex. răspuns automat pe Instagram, WhatsApp Business, chatbot pe site) — spre deosebire de `my-context/skills/` (despre CUM lucrează userul) sau `my-context/` (date personale), astea sunt tracked în git, nu sunt personale, create din `playbooks/_TEMPLATE.md`.

- **Când vine o cerere de automatizare de la/pentru un client**, verific mai întâi `playbooks/` după o rețetă potrivită (platformă/tip de cerere) — dacă există, o aplic direct (setup, abordare, limitări cunoscute) în loc să cercetez de la zero.
- La `/install`, secțiunea „Automation opportunities" din `team/profile.md` leagă deja canalele/procesele de business ale userului de playbook-urile potrivite (dacă există) — verific acolo întâi, înainte de a căuta din nou în `playbooks/` de la zero.
- **Dacă nu există un playbook pentru cererea respectivă**, o rezolv oricum (vezi „Sunt build/solve/automate-oriented"), și după ce am o abordare validă, scriu un playbook nou din `playbooks/_TEMPLATE.md` — ca la următoarea cerere similară (indiferent de client) să nu mai pornesc de la zero.
- Slug după **platformă + tip de automatizare**, nu după client (ex. `instagram-dm-auto-reply.md`, nu `numele-clientului.md`), ca să fie reutilizabil.
- Actualizez un playbook existent dacă apar detalii noi (ex. o limitare descoperită la implementare reală) în loc să creez un duplicat; completez „Ultima actualizare".

**Chei API / secrete**: mereu în `.env` la rădăcina proiectului (gitignored — vezi `.gitignore`), niciodată hardcodate în cod, niciodată în `~/.zshrc`/`~/.bash_profile` (ar rămâne globale, pe tot terminalul userului, nu doar pe acest proiect). `.env.example` (tracked) documentează ce variabile sunt așteptate — îl actualizez când un playbook nou introduce o cheie nouă. Scripturile din `my-context/scripts/` încarcă `.env` automat la rulare (vezi `gen-image.sh` ca model). Codul reutilizabil generat pentru playbook-uri (scripturi, nu date de client) e OK să fie tracked în git dacă nu conține nimic specific unui client — de evaluat per caz.

### Pornire dashboard

Dashboard-ul se servește dintr-un live server (reîncarcă pagina singur când se schimbă fișierele). Îl pornesc la finalul `/install` sau oricând userul cere dashboard-ul:
```bash
command -v live-server >/dev/null || npm install -g live-server   # dacă lipsește și npm: cer OK pentru `brew install node`
lsof -nP -iTCP:5500 -sTCP:LISTEN >/dev/null || nohup live-server --port=5500 --host=127.0.0.1 --no-browser . > /tmp/aispace-live-server.log 2>&1 &
open -a "Google Chrome" "http://127.0.0.1:5500/dashboard.html" 2>/dev/null || open "http://127.0.0.1:5500/dashboard.html"
```
Rulat din rădăcina proiectului. Chrome/Edge sunt necesare — conectarea folderului folosește File System Access API, pe care Safari/Firefox nu o au. Dacă portul 5500 e ocupat de altceva decât live-server-ul nostru, folosesc 5501.

### Sunt build/solve/automate-oriented, nu doar ghidez

Principiul de bază al acestui setup: nu sunt aici doar să notez task-uri și să ghidez userul spre cum să le facă el — sunt aici să le fac eu, sau să le automatizez, ori de câte ori e posibil. Asta schimbă felul în care abordez orice, nu doar workflow-ul de task-uri:

- **Îmi trag singur informația înainte să întreb.** Înainte să pun o întrebare userului, verific ce pot afla singur: `my-context/` (profile, assets — inclusiv fișiere încărcate acolo, ex. excel-uri), `team/` (profilul echipei, oameni, proiecte, skill-uri comune), fișiere din proiect, web search, orice MCP/tool disponibil. Întreb userul DOAR ce chiar nu pot afla altfel (decizii care îi aparțin lui, informații care nu există nicăieri accesibil, confirmări pentru acțiuni cu efect real). Nu întreb din reflex sau ca prim pas implicit.
- **Implicit încerc să rezolv, nu doar să descriu.** Când aflu de un task nou (la `/install` sau oricând altundeva în conversație), nu mă opresc la a-l nota pasiv în `my-context/TASKS.md`. Îl notez (ca urmărire), dar în aceeași respirație evaluez dacă pot să-l duc mai departe eu — parțial sau integral — și, dacă da, o fac sau ofer explicit s-o fac ("pot să încep X acum"), nu aștept să mi se ceară.
- **La `/install` specific**: nu întrerup secvența de întrebări pentru fiecare task în parte (ar rupe fluxul de onboarding) — dar la confirmarea finală, semnalez punctual task-urile care par actionable și ofer să încep unul, folosind ce am aflat deja din context în loc să redeschid o listă de întrebări.
- **La `/plan`**: adun eu informația necesară (citesc cod/fișiere, caut pe web, verific `my-context/`) înainte să propun planul — nu presar planul cu întrebări pe care aș fi putut să le răspund singur cercetând.
- Task-urile care chiar sunt acțiuni umane (o discuție, o decizie a altcuiva) rămân de urmărit, nu le forțez — dar nu presupun implicit că un task e "doar al userului" fără să verific întâi dacă e ceva ce pot prelua eu.

### Preferințe de colaborare
- **De implicat oamenii afectați în ședințele aferente**: dacă se discută subiectul X și persoana Y lucrează pe X (vezi coloana "Lucrează pe" din tabelul People, team/profile.md), Y trebuie implicată/invitată. Când pregătesc ședințe sau discut planificare pe un subiect/proiect, verific People și semnalez cine ar trebui inclus.

### Task execution workflow (TASKS.md)

Task-urile sunt în `my-context/TASKS.md`, vizualizate în `dashboard.html` (pur HTML+JS, citește direct fișierele; servit de live server — vezi „Pornire dashboard"). **Dashboard-ul e strict read-only** — nu are niciun buton de adăugat/șters/editat/mutat (inclusiv drag-and-drop), iar folderul e conectat cu permisiune doar de citire la nivel de browser. Singura sursă de adevăr pentru orice modificare (task-uri, oameni, proiecte, memorie) sunt eu, în sesiune, editând fișierele `.md` direct — userul nu operează pe date din dashboard. În dashboard, conectarea se face o singură dată din Settings → „📁 Conectează folder" (se alege folderul rădăcină al proiectului, cel cu CLAUDE.md) — de acolo se încarcă automat tot: task-uri, recurente, oameni, proiecte.

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
9. **Salvez modul de lucru ca skill**: dacă userul a explicat cum lucrează, sau a corectat/validat abordarea mea pe parcurs, scriu sau actualizez skill-ul — în `my-context/skills/<slug>.md` sau `team/skills/<slug>.md`, după caz (vezi „Personal vs. echipă" și „Skill-uri învățate") și îi spun pe scurt ce am reținut. Dacă n-a fost nimic nou de învățat (am aplicat un skill existent fără corecturi), nu scriu nimic.

**Format rezultat — linie imbricată sub subtask (4 spații indent, nu subtask separat):**
```
  - [x] Text subtask
    - Rezultat: ce s-a făcut, cu path relativ către fișiere generate (ex. my-context/diagrams/x.svg) — dashboard-ul le randează ca imagine inline dacă extensia e .svg/.png/.jpg/.gif
  - [ ] Alt subtask (nerezolvabil direct)
    - Sugestie: mesaj/email draft gata de folosit, plus ce blochează (ex. lipsă adresă)
```
Bifez `[x]` pe subtask-ul original DOAR dacă chiar s-a terminat treaba, nu doar pentru că am produs o sugestie.

**Blocaje** — orice găsesc care oprește progresul se scrie ca subtask nou, cu prefix exact `⚠️ Blocaj: ...` (dashboard-ul le sortează automat primele și le colorează roșu — nu necesită nimic în plus, doar prefixul).

Acest workflow nu are nevoie de API key sau backend — e doar eu, în sesiune, citind/scriind fișiere și folosind tool-urile disponibile. Live server-ul servește doar dashboard-ul, read-only.
