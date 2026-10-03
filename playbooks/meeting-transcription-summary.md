# Transcriere + sumarizare întâlniri

## Cerere tipică de client
"Vreau notițe automate la fiecare apel", "un recap cu action items după fiecare ședință", "nu mai prindem timp să luăm notițe la întâlniri".

## Ce presupune tehnic
- **Dacă clientul are deja Zoom AI Companion sau Microsoft Teams Copilot licențiat** → nu se construiește nimic, se activează/configurează ce are deja (implicit de verificat primul, evită muncă redundantă).
- **Altfel, implicit: Recall.ai** (pentru "bot care se alătură apelului" cross-platform — Zoom, Meet, Teams) **+ OpenAI Whisper** (transcriere, aceeași familie de cont ca restul playbook-urilor OpenAI-implicite) **+ Claude** (sumarizare, extragere action items).
- Alternative, doar când cererea o cere explicit:
  - **Otter.ai / Fireflies.ai** — unelte SaaS gata făcute, fără nicio integrare custom — de recomandat dacă clientul vrea ceva instant, fără dezvoltare, și nu are nevoie de personalizare pe formatul recap-ului.
  - **Integrare nativă per platformă** (Zoom API, Google Meet API) — dacă clientul folosește o singură platformă exclusiv și vrea control maxim fără un bot terț care se alătură vizibil la apel.

## Setup per client
1. Verific ce platformă(e) de video folosește clientul (Zoom/Meet/Teams/mix).
2. Dacă alege soluția custom: conectez Recall.ai (sau echivalent) pentru "join & record", configurez webhook la finalul înregistrării.
3. Stabilesc formatul recap-ului dorit de client (rezumat scurt, action items cu responsabili, decizii cheie, citate importante) — nu un format generic.
4. Stabilesc canalul de livrare (email, Slack, direct în `my-context/docs/` dacă e pentru uz intern).

## Abordare de implementare
1. Bot-ul se alătură apelului (cu consimțământul participanților — vezi riscuri) și înregistrează.
2. La final, audio → Whisper → transcript brut.
3. Transcript → Claude → recap structurat conform formatului stabilit cu clientul, cu action items extrase explicit (cine, ce, până când).
4. Livrare automată pe canalul ales, la scurt timp după încheierea apelului.

## Limitări/riscuri cunoscute
- **Consimțământ obligatoriu**: înregistrarea apelurilor fără acordul participanților e ilegală în multe jurisdicții — bot-ul trebuie să anunțe explicit (mesaj în chat-ul apelului sau prompt vocal), nu doar să se alăture silențios.
- **Confidențialitate**: apelurile pot conține informații sensibile (contracte, date personale, strategie internă) — de clarificat cu clientul unde se stochează transcriptele și cât timp.
- **Acuratețe transcriere**: accente puternice, vorbire suprapusă (mai mulți vorbind deodată), sau conexiune audio slabă reduc calitatea — de setat așteptări realiste, nu "100% perfect".
- **Cost**: proporțional cu numărul/durata apelurilor — de estimat volumul lunar înainte de a promite ceva nelimitat.

## Ultima actualizare
2026-09-22
