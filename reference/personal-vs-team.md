# Personal vs. echipă (my-context/ vs. team/)

Încărcat la cerere din CLAUDE.md: citesc acest fișier când decid unde să scriu ceva nou (persoană, proiect, skill, termen).

> **Model actual pentru firme:** o firmă are un repo propriu, cu un singur `main`; `my-context/` (fără `assets/`) se publică acolo de către owner-i (`reference/sync-conflicts.md`). Mai jos e împărțirea veche personal/echipă, încă folosită pentru `team/`.

Setup-ul e folosit de mai mulți colegi din aceeași firmă, fiecare cu propria copie a proiectului. Cunoștințele sunt împărțite în două zone:

- **`team/`** — comun, salvat în git, îl primește fiecare coleg: `team/profile.md` (compania, oamenii, termenii, proiectele, tool-urile echipei), `team/people/<slug>.md`, `team/projects/<slug>.md`, `team/skills/<slug>.md` (moduri de lucru valabile pentru toată echipa).
- **`my-context/`** — personal (în repo-urile firmelor se publică de owner-i, fără `assets/` și fără `TASKS.md`, care e personal): `profile.md` (cine sunt eu, preferințele mele, statusul conectării tool-urilor mele, open threads), `TASKS.md`, `skills/` (moduri de lucru doar ale mele), `assets/`.

Reguli:
- **Oameni și proiecte** se scriu în `team/people/` și `team/projects/` (nu în `my-context/`) — sunt aceiași pentru toți colegii. Dashboard-ul le citește din ambele locuri.
- **Când învăț ceva nou** (skill, termen, persoană, proiect) și nu e evident unde aparține, întreb userul pe scurt (AskUserQuestion): „Doar pentru tine" / „Pentru toată echipa". Ce e clar personal (preferințe, task-uri proprii, fișiere private) merge direct în `my-context/`, fără întrebare.
- **Nu pun niciodată în `team/`** date sensibile: parole, tokeni, date de card, informații private despre clienți, fișiere din `assets/`. Pot ajunge la toți colegii și în istoricul git.
- **Skill-uri**: la un task caut întâi în `my-context/skills/`, apoi în `team/skills/`. Dacă amândouă au un skill potrivit, cel personal are prioritate la detalii, dar respect regulile comune din cel de echipă.
