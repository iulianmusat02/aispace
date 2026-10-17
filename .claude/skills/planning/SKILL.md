---
name: planning
description: Adaugă task-uri noi și task-uri repetitive în TASKS.md — întreabă ghidat ce ai pe agendă și ce se repetă periodic. /install nu mai întreabă de task-uri, deci aici e locul lor. Folosește-l când userul scrie /planning, cere să adauge task-uri, sau vrea să revizuiască ce mai are de făcut.
---

# /planning — task-uri și task-uri repetitive

Presupune că `my-context/profile.md` există deja (contextul de business e deja cunoscut). Secvențele „Task-uri curente" și „Task-uri repetitive" sunt definite aici (au fost scoase din `/install`).

## 0. Verificare

Dacă `my-context/profile.md` **nu există** → nu am încă context de business. Explic pe scurt și redirecționez spre `/install`, nu improvizez o versiune scurtată.

## 1. Context rapid

`my-context/TASKS.md` e **personal**: nu se publică și fiecare utilizator are al lui. Dacă lipsește (de exemplu la un coleg care tocmai a clonat proiectul), îl creez acum din `templates/TASKS.template.md`, gol.

Citesc `my-context/TASKS.md` curent și arăt userului, pe scurt, ce are deja (câte task-uri active, câte recurente, dacă e ceva cu deadline apropiat), 2-3 rânduri.

## 2. Secvențele de întrebări

Reguli: **nu dictez niciodată cuvântul exact de răspuns**; bucla de continuare e mereu AskUserQuestion Da/Nu; o întrebare pe rând.

- **Task-uri curente** — câte un task pe rând:
  1. "Ce ai pe agendă acum? Dă-mi primul lucru."
  2. "Are un termen limită (due date)?"
  3. "Cine e responsabil — tu, sau altcineva din echipă?" (dacă a menționat deja un nume, doar confirmă)
  4. Dacă e ceva care se repetă periodic (o instrucțiune permanentă — ex. "verifică emailurile în fiecare zi la 10:00"), marchează-l ca recurent și notează intervalul exact; altfel e un task normal cu due date.
  5. Notează intern (nu întrerupe secvența acum) dacă task-ul pare ceva ce ai putea face tu direct (scris, research, draft, cod, diagramă, procesare fișier) — le semnalezi grupat la pasul 7 (Confirmare), nu pe rând aici.
  6. AskUserQuestion: "Mai ai și alte task-uri de adăugat acum?" (Da / Nu, max. 5-6) — dacă Da, repetă 1-5.
  Nu întreba aici despre modul de lucru pe fiecare task — asta se întreabă la momentul execuției (vezi `reference/task-workflow.md`), ca onboarding-ul să rămână scurt.
- **Task-uri repetitive** — întrebare separată, explicită, nu doar sub-pas la task-urile curente (oamenii gândesc diferit „ce am de făcut" de „ce fac regulat" și uită des să le menționeze dacă nu sunt întrebați punctual):
  1. "Ai vreun task sau vreo verificare care se repetă (zilnic, săptămânal, lunar)? De ex. verificare emailuri la o oră fixă, raport săptămânal, backup, monitorizare a ceva."
  2. Pentru fiecare task repetitiv descris: notează intervalul exact (ex. "zilnic la 10:00", "lunea dimineața") și adaug-o ca task recurent (vezi formatul `(recurrent: ...)` din `reference/task-workflow.md`) — ajunge automat în subtab-ul „🔁 Recurente" din dashboard, nu se amestecă cu task-urile punctuale.
  3. AskUserQuestion: "Mai ai și alte task-uri repetitive de adăugat?" (Da / Nu) — dacă Da, repetă 1-2.

## 3. Adaug la TASKS.md

Task-urile noi și cele repetitive se adaugă în `my-context/TASKS.md`, în secțiunea potrivită (implicit „Active" pentru task-uri punctuale), cu ID-uri `AS-N` **continuând numerotarea existentă** (verific ultimul ID folosit; dacă fișierul e gol, încep de la `AS-1`). Format exact ca în `reference/task-workflow.md` (îl citesc înainte să scriu).

## 4. Build/solve, nu doar notez

Pentru fiecare task nou (punctual sau repetitiv), aplic „Sunt build/solve/automate-oriented" din CLAUDE.md: evaluez ce pot face eu direct. Dacă e un proces manual care se repetă, propun `/process`. Nu aștept să mi se ceară.

## 5. Confirmare

Rezumat scurt: câte task-uri noi și repetitive (cu ID-uri), ce am semnalat ca actionable sau automatizabil. Ofer explicit să încep pe unul acum; dacă acceptă, trec direct la treabă (`reference/task-workflow.md`).
