---
name: add-teammate
description: Adaugă un coleg în echipă (fișa lui, dacă poate publica sau doar citi), îl invită pe GitHub cu accesul potrivit și scrie un mesaj de bun venit cu un singur lucru de lipit în AI-ul lui. Tratează și plecarea cuiva din echipă. Doar pentru owner-i. Folosește-l când userul scrie /add-teammate, vrea să adauge un om nou sau spune că cineva pleacă.
---

# /add-teammate — om nou sau plecare din echipă

**Doar owner-i** (`reference/roluri.md`). Pentru oamenii adăugați la `/install` nu e nevoie; acesta e pentru cei ce vin după.

## A. Adăugare

1. **Date** (câte una pe rând, ce reiese deja nu mai întreb): nume, rol, emailul de lucru, proiectele pe care lucrează.
2. **Poate publica?** AskUserQuestion (Da / Nu): „Poate [nume] să modifice și să publice contextul firmei?" La Da, emailul e obligatoriu. Implicit recomand **Nu** (doar citire).
3. **Fișa**: creez `my-context/people/<slug>.md` din `templates/people/_person.template.md`, cu `Poate face push: da/nu`, și o adaug în tabelul People din `my-context/profile.md` și în proiectele lui (`[[slug]]`). Dacă mi-a dat date personale în plus (telefon privat, adresă), nu le scriu.
4. **Invitația pe GitHub**: întreb numele lui de utilizator GitHub. Arăt ce voi face și cer confirmare explicită, apoi invit cu `gh api -X PUT repos/<owner>/<repo>/collaborators/<utilizator> -f permission=push` pentru cei care pot publica, respectiv `permission=pull` pentru restul (doar citire: asta aplică regula și pe GitHub). Fără `gh` conectat, îi dau pașii de făcut manual și link către setările de acces.
5. **Mesajul de bun venit**, gata de trimis (nu îl trimit eu), scurt și prietenos, cu: ce e spațiul de lucru, acceptarea invitației, și **un singur lucru de lipit în AI-ul lui**:

   > Clonează proiectul <adresa repo-ului> într-un folder, deschide-l cu Claude Code și scrie /guide.

   Plus nota: emailul din Git trebuie să fie cel din fișa lui (`<email>`), ca să fie recunoscut.
6. Un coleg nou nu are `TASKS.md`; `/planning` i-l creează.

## B. Plecare din echipă

1. Confirmare explicită (AskUserQuestion) cu numele persoanei.
2. Scot accesul de pe GitHub (`gh api -X DELETE repos/<owner>/<repo>/collaborators/<utilizator>`), doar după confirmare.
3. În fișa lui pun `**Poate face push:** nu` și `**Stare:** a plecat` (nu șterg fișa: istoricul rămâne). Întreb cine preia proiectele și procesele pe care le deținea și actualizez legăturile.
4. Spun că orice cheie sau parolă la care avea acces trebuie schimbată.
