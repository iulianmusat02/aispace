# Roluri: owner și membru

Încărcat la cerere din CLAUDE.md și din skill-uri: citesc acest fișier când trebuie să știu ce are voie userul curent să facă.

## Cine e owner

**Owner** = persoană a cărei fișă (`my-context/profile.md`, `my-context/people/<slug>.md`, `team/profile.md` sau `team/people/<slug>.md`) conține emailul ei de lucru și `**Poate face push:** da`. Emailul trebuie să fie cel din configurarea ei de Git. Oricine altcineva e **membru**.

Verificare (afișează fișa potrivită dacă e owner, nimic altfel):

```bash
E=$(git config user.email); [ -n "$E" ] && grep -rliF --include='*.md' -- "$E" my-context team 2>/dev/null | while read -r f; do grep -qiE 'Poate face push:?\*\*:? *da' "$f" && echo "$f"; done
```

Dacă `git config user.email` e gol, nu pot recunoaște userul: îl întreb emailul de lucru, în limbaj simplu, și nu presupun că e owner.

## Ce poate fiecare

| Acțiune | Owner | Membru |
|---|---|---|
| Citește contextul, folosește skill-urile, `/guide`, `/history`, `/quiz` | da | da |
| `/planning` (task-uri personale, rămân pe calculatorul lui) | da | da |
| `/sync`: primește modificările celorlalți | da | da |
| `/sync`: publică modificări în spațiul comun | da | nu |
| `/process`: construiește automatizarea sau skill-ul | da | nu, scrie o cerere către un owner |
| `/add-context`, `/add-teammate`, `/update-template`, restaurare din `/history` | da | nu |

Un membru poate lucra local, dar nu publică: hook-ul de sync îl oprește, iar la `/add-teammate` membrii primesc pe GitHub acces doar de citire.

## Limite

Rolul se verifică după emailul din Git, deci e o regulă de lucru, nu un control de acces. Controlul real e accesul de pe GitHub (scriere doar pentru owner-i). Fiecare firmă răspunde de cum folosesc membrii ei AISpace.
