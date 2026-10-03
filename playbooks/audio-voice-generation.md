# Generare de voce/audio (AI)

## Cerere tipică de client
"Vreau voiceover pentru un video de produs, fără actor de voce", "reclamă audio generată automat", "vocea brandului nostru, consistentă pe toate materialele", "conversie text-articole în podcast".

## Ce presupune tehnic
Se leagă de `video-generation.md` (majoritatea modelelor video nu au audio nativ — asta acoperă partea de voce/muzică) și de `voice-conversational-agent.md` (acolo vocea e în timp real, aici e conținut pre-generat, offline).

- **Implicit: ElevenLabs** — cea mai naturală calitate de voce din piață la momentul actual, suportă clonare de voce (voce custom de brand) și multilingv — de folosit ca primă opțiune pentru orice cerere de voiceover/audio.
- Alternative, doar când cererea o cere explicit:
  - **OpenAI TTS** — dacă clientul e deja în ecosistemul OpenAI (același cont ca DALL-E/Sora) și nu are nevoie de o voce custom/clonată — mai simplu, dar mai puțin natural decât ElevenLabs.
  - **Suno / Udio** — dacă cererea e despre **muzică** (jingle, fundal muzical), nu voce — categorie diferită de "text-to-speech".

## Setup per client
1. Confirm dacă cererea e voce (narațiune, voiceover) sau muzică (jingle) — determină providerul.
2. Client (sau noi, temporar) creează cont + cheie API la providerul ales; cheia se pune în .env la rădăcina proiectului (vezi Chei API / secrete din CLAUDE.md), niciodată în cod/git.
3. Dacă clientul vrea o **voce de brand consistentă** (aceeași "voce" pe toate materialele), configurez o voce fixă din biblioteca providerului, sau clonez o voce reală (cu consimțământul explicit, scris, al persoanei — vezi riscuri) — nu regenerez o voce diferită de fiecare dată.
4. Stabilesc formatul de livrare (fișier audio pentru video, sau audio de sine stătător pentru podcast/reclamă radio).

## Abordare de implementare
1. Text sursă (scenariu, articol, script) → generez audio prin API-ul ales, cu vocea stabilită cu clientul.
2. Pentru conținut lung (ex. articol → podcast), împart pe segmente naturale (nu tot dintr-o bucată), verific coerența la îmbinare.
3. Dacă audio-ul e pentru un video generat (`video-generation.md`), sincronizez separat (majoritatea modelelor video nu acceptă audio ca input direct) — montaj audio+video ca pas distinct.
4. Arăt clientul rezultatul înainte de a-l considera final — tonul/emfaza pot necesita 2-3 iterații de prompt/setări.

## Limitări/riscuri cunoscute
- **Clonare de voce = zonă sensibilă**: clonarea vocii unei persoane reale necesită consimțământul ei explicit, în scris — nu se clonează o voce (angajat, influencer, celebritate) doar pentru că avem o mostră audio disponibilă. Multe platforme cer verificare de consimțământ înainte de a permite clonarea.
- **Sincronizare cu video**: audio generat separat de video (majoritatea cazurilor) poate necesita ajustări de timing la montaj — nu presupun sincronizare perfectă automată.
- **Limbi/accente**: calitatea variază pe limbă — de testat explicit pe limba țintă a clientului (română inclusă) înainte de a promite calitate "perfectă".
- **Cost**: de obicei per caracter/minut generat — de estimat volumul (ex. un podcast săptămânal de 20 min) și comunicat clientului.
- **Drepturi de autor pe muzică** (Suno/Udio): la fel ca la imagini/video, incertitudini legale pe conținutul generat comercial — de discutat explicit dacă clientul are sensibilitate pe asta.

## Ultima actualizare
2026-09-22
