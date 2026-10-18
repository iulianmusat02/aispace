---
name: guide
description: Ghidul AISpace pentru oricine din echipă. Explică pe scurt ce este spațiul de lucru, ce comenzi și skill-uri poate folosi rolul userului (owner sau membru) și propune următorul pas potrivit. Folosește-l când userul scrie /guide, întreabă „ce pot face aici?" sau e nou în echipă.
---

# /guide — ce poți face aici

Doar citesc și explic; nu modific nimic. Limbaj de business: fără termeni tehnici.

## 1. Cine e userul

Citesc `reference/roluri.md` și stabilesc dacă e **owner** sau **membru**. Citesc `my-context/profile.md` ca să-l salut pe nume și să știu contextul firmei. Dacă profilul lipsește, îl trimit la `/install`.

## 2. Ce este AISpace (3-4 propoziții)

Un spațiu de lucru în care Claude cunoaște firma (oameni, proiecte, termeni), ține evidența procesului fiecăruia și automatizează munca repetitivă. Contextul firmei e comun și îl întreține un grup mic de owner-i; task-urile fiecăruia rămân personale.

## 3. Ce poate folosi rolul lui

Arăt doar comenzile rolului lui, cu o frază pe fiecare (legenda completă e în dashboard, pagina „Comenzi"). Regulile sunt în `reference/roluri.md`.

Pe lângă comenzile de bază, listez skill-urile firmei: cele din `.claude/skills/` care nu sunt livrate cu șablonul (nume + ce fac, din `description`), adică procesele deja automatizate.

## 4. Următorul pas

Propun un singur pas, după situația reală:
- fără profil → `/install`;
- `my-context/TASKS.md` lipsește sau e gol → `/planning`;
- nu există procese automatizate → `/process` (owner) sau o cerere către un owner (membru);
- există modificări nepublicate (`git status` pe `my-context/`) → `/sync`;
- altfel → întreb ce are de făcut azi.

Închei cu AskUserQuestion: „Începem cu acest pas?" (Da / Mai târziu). La Da, pornesc skill-ul respectiv direct.
