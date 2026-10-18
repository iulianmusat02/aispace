---
name: history
description: Răspunde la „ce s-a schimbat, când, cine și de ce" în contextul firmei, din istoricul salvărilor, în cuvinte simple. Nu modifică nimic; doar un owner poate restaura o versiune veche, ca modificare nouă. Folosește-l când userul scrie /history sau întreabă ce s-a schimbat, cine a modificat ceva, sau vrea să revină la o versiune anterioară.
---

# /history — ce s-a schimbat și de ce

Citesc istoricul (`git log`, `git show`, `git blame` pe `my-context/` și `.claude/skills/`) și răspund în cuvinte simple: ce, când, cine, de ce. Nu modific nimic în această parte.

## 1. Întrebarea

Aflu ce vrea: o persoană, un fișier, o perioadă, „ce e nou de ieri". Ce pot deduce, deduc; nu pun întrebări în plus.

## 2. Răspunsul

- Dau o listă scurtă, cronologică: data, autorul, ce s-a schimbat (rezumat al diferenței, nu mesajul brut).
- „De ce": din mesajul salvării, dacă are unul clar. Salvările automate au nota generică „Update my-context", deci motivul îl deduc din diferență și spun că e o deducere. Pentru note mai bune recomand `/sync` la modificările importante.
- **Ce nu apare în istoric**: `TASKS.md` (personal) și `assets/` nu sunt salvate în spațiul comun, deci nu au istoric.

## 3. Restaurare (doar owner-i)

Un membru care vrea să revină la o versiune: îl îndrept spre un owner.

Un owner: arăt diferența dintre versiunea veche și cea de acum și cer confirmare (AskUserQuestion). Restaurez **ca modificare nouă**: aduc conținutul vechi al fișierului (`git show <versiune>:<fișier>`) și îl scriu peste cel curent. Nu rescriu istoricul, nu folosesc `reset --hard`, nu forțez nimic. Apoi se publică normal (hook-ul sau `/sync`), iar notei îi adaug motivul restaurării.
