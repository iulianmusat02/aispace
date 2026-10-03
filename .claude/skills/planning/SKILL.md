---
name: planning
description: Reia DOAR partea de task-uri/rutine din /install — întreabă ghidat ce task-uri noi sau rutine vrei să adaugi, fără să repete restul onboarding-ului (domeniu, oameni, proiecte, tool-uri). Folosește-l când userul scrie /planning, cere să adauge task-uri noi, sau vrea să revizuiască/completeze ce mai are de făcut.
---

# /planning — task-uri și rutine noi

Presupune că `my-context/profile.md` există deja (contextul de business e deja cunoscut) — reia DOAR blocurile „Task-uri curente" și „Rutine" din `/install` (`.claude/skills/install/SKILL.md`, secțiunea 3), nu tot fluxul de onboarding.

## 0. Verificare

Dacă `my-context/profile.md` **nu există** → nu am încă context de business, nu poate exista un `/planning` fără el. Explic pe scurt și redirecționez spre `/install` complet, nu improvizez o versiune scurtată.

## 1. Context rapid

Citesc `my-context/TASKS.md` curent și arăt userului, pe scurt, ce are deja (câte task-uri active, câte recurente, dacă e ceva cu deadline apropiat) — ca să pornim de la ce există, nu de la o listă goală. Nu repet tot conținutul, doar un rezumat de 2-3 rânduri.

## 2. Task-uri noi

Rulez exact secvența **„Task-uri curente"** din `.claude/skills/install/SKILL.md` (secțiunea 3) — aceleași întrebări punctuale (ce e de făcut → due date → responsabil → recurent? → mai ai altele?), cu aceleași reguli de acolo, în special: **nu dictez niciodată cuvântul exact de răspuns** ("scrie nimic", "spune nu") — bucla de continuare e mereu AskUserQuestion Da/Nu.

## 3. Rutine noi

Rulez exact secvența **„Rutine"** din același fișier, secțiunea 3 — la fel, ghidat, cu aceleași reguli.

## 4. Adaug la TASKS.md

Task-urile/rutinele noi se adaugă în `my-context/TASKS.md`, în secțiunea potrivită (implicit „Active" pentru task-uri punctuale noi), cu ID-uri `AS-N` **continuând numerotarea existentă** (nu reiau de la 1 — verific ultimul ID folosit înainte de a atribui altele noi). Format exact ca în „Task execution workflow" din CLAUDE.md.

## 5. Build/solve, nu doar notez

Pentru fiecare task/rutină nou, aplic „Sunt build/solve/automate-oriented" din CLAUDE.md: verific `playbooks/` dacă e o cerere de automatizare cunoscută, evaluez ce pot face eu direct, și **nu aștept să mi se ceară** — semnalez.

## 6. Confirmare

Rezumat scurt: câte task-uri/rutine noi am adăugat (cu ID-uri), ce am semnalat ca actionable/automatizabil imediat. Ofer explicit să încep pe unul din ele acum, dacă e cazul (vezi „Nu te oprești la un rezumat pasiv" din `/install`, aceeași logică se aplică aici). Dacă userul acceptă, trec direct la treabă („Task execution workflow" din CLAUDE.md), fără să mai aștept altă cerere.
