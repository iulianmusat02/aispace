# Publicarea contextului și conflictele (trunk-based)

Încărcat la cerere din CLAUDE.md: citesc acest fișier când hook-ul de sincronizare raportează conflicte, sau când userul întreabă cum se publică contextul.

## Modelul

- Un singur branch, `main`, în care publică toți owner-ii. Fără branch-uri, fără pull request-uri.
- **Doar owner-ii publică.** Owner = persoană a cărei fișă (`my-context/people/<slug>.md` sau `my-context/profile.md`) are `**Poate face push:** da` și `**Email:**` egal cu emailul ei din Git. Ceilalți membri citesc și lucrează local; modificările lor nu se publică singure.
- După fiecare tură, hook-ul `.claude/hooks/sync-context.sh`, la un owner: comite `my-context/` și `.claude/skills/` (nu `assets/`), apoi **întâi aduce ce au publicat ceilalți (merge), apoi publică**. Nu forțează niciodată push-ul.

## Când hook-ul raportează conflicte

Hook-ul a oprit merge-ul (nimic nu e pe jumătate) și mi-a dat lista fișierelor. Procedura mea:

1. Rulez `git fetch` și `git merge origin/main`. Pentru fiecare fișier cu conflict, citesc cele două versiuni ale fiecărui bloc.
2. **Conflict tehnic, fără decizie de business** (au editat același fișier, dar informațiile nu se contrazic: rânduri diferite adăugate în același loc, o persoană adăugată de doi oameni, câmpuri diferite ale aceleiași fișe) → le combin eu, păstrând ambele, fără duplicate.
3. **Informații care se suprapun sau se contrazic** (același câmp cu valori diferite: alt termen, alt rol, altă stare, două variante de text pentru același lucru) → NU aleg eu. Îi arăt userului, într-un limbaj de business, ambele variante (cine a scris fiecare, dacă reiese din `git log`) și îl las să aleagă cu AskUserQuestion: varianta lui, varianta celuilalt, sau „le combin" cu un text pe care îl confirmă.
4. După ce toate blocurile sunt rezolvate: `git add` pe fișierele rezolvate, `git commit` (mesajul implicit de merge) și publicare cu `git push`. Fără `--force`.
5. Dacă userul nu poate decide acum, las merge-ul neîncheiat nepublicat (`git merge --abort`) și îi spun că modificările lui rămân locale până se hotărăște.

## Alte situații

- **Push respins** (altcineva a publicat între timp): hook-ul reîncearcă la tura următoare, cu același pas de pull.
- **Fișiere pregătite în afara `my-context/` și `.claude/skills/`**: hook-ul nu publică nimic până nu sunt comise sau scoase din staging.
- **Secret găsit în context**: nimic nu se publică; îl mut în `.env` conform regulii din CLAUDE.md.
