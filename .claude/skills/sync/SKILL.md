---
name: sync
description: Salvează și partajează modificările contextului firmei și aduce modificările colegilor. Pentru owner-i publică (după verificarea datelor personale și a cheilor, cu o notă clară: ce, de ce, cine a cerut); pentru membri doar descarcă. Când doi oameni au schimbat aceleași rânduri, întreabă ce variantă rămâne. Folosește-l când userul scrie /sync sau vrea să publice ori să primească ultimele modificări.
---

# /sync — salvează și partajează

Hook-ul `.claude/hooks/sync-context.sh` face deja asta automat după fiecare tură, la owner-i, cu o notă generică. `/sync` e varianta manuală, pentru o modificare importantă cu o notă bună, sau când automatul a eșuat. Procedura conflictelor e în `reference/sync-conflicts.md`.

## 0. Rolul

`reference/roluri.md`. **Membru**: doar primește (pasul 2). **Owner**: parcurge toți pașii.

## 1. Ce s-a schimbat

`git status` și `git diff` pe `my-context/` și `.claude/skills/` (nu `assets/`, nu `TASKS.md`). Rezum în limbaj de business. Dacă nu e nimic, trec direct la primire.

## 2. Primire (toți)

`git fetch`, apoi aduc modificările celorlalți. La membri: doar adăugare fără suprascrieri (`git merge --ff-only`); dacă are modificări locale care blochează, le explic și propun să le păstrăm separat, fără să șterg ceva.

## 3. Publicare (doar owner-i)

1. **Verific datele**: caut în ce urmează să se publice date personale (CNP, adrese, telefoane de clienți) și secrete (chei, tokeni, parole). Dacă găsesc, opresc și le mut: secretele în `.env`, datele personale scoase (regula din CLAUDE.md).
2. **Notă clară**: scriu mesajul cu *ce* s-a schimbat, *de ce* și *cine a cerut*. Ce nu reiese din conversație întreb scurt, într-o singură întrebare.
3. **Întâi primesc, apoi public.** La conflict urmez `reference/sync-conflicts.md`: rezolv singur ce nu se contrazice; unde două persoane au schimbat aceleași rânduri cu informații diferite, arăt ambele variante și userul alege (AskUserQuestion).
4. Publicare simplă, **fără forțare** (`git push`, niciodată `--force`). Dacă e respinsă, repet primirea și încerc o dată; dacă nu merge, spun clar de ce.

## 4. Încheiere

Spun ce s-a publicat sau primit, în câteva rânduri, și ce a rămas local (dacă e cazul).
