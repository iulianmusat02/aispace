# Generare de video (AI)

## Cerere tipică de client
"Vreau un video scurt de prezentare a produsului, fără filmare", "clip pentru reclamă pe Instagram/TikTok generat automat", "animăm o imagine de produs într-un video scurt", "teaser video pentru lansare".

## Ce presupune tehnic
- **Platformă/API oficial — implicit Sora (OpenAI)**: aceeași familie de cont/billing ca DALL-E (vezi `image-generation.md`), simplu de integrat dacă clientul e deja pe OpenAI — de folosit ca primă opțiune, fără să deschid discuția de provider decât dacă apare un motiv concret. Alternative, doar când cererea o cere explicit:
  - **Runway (Gen-4)** — control mai fin (camera motion, referințe vizuale multiple, editare video-la-video) — bun pentru cerințe "cinematice" sau când clientul vrea să pornească de la un video/imagine existentă de brand.
  - **Google Veo** (Vertex AI) — dacă clientul e deja pe Google Cloud, sau are nevoie de durate mai lungi/rezoluție mai mare decât oferă alternativele.
  - **Kling / Luma Dream Machine / Pika** — opțiuni mai ieftine, bune pentru volum mare de clipuri scurte (social media) unde calitatea "perfectă" contează mai puțin decât costul per clip.
- **Cont necesar:** cont OpenAI + cheie API (implicit) — celelalte doar dacă se ajunge la o alternativă.
- **Conector/MCP disponibil:** verific `mcp-registry` — dacă nu găsesc conector dedicat, API direct.

## Setup per client
1. Pornesc cu Sora ca implicit — schimb providerul doar dacă apare unul din motivele de mai sus (control cinematic, ecosistem Google, volum mare la cost mic).
2. Client (sau noi, temporar) creează cont + cheie API; cheia se pune în .env la rădăcina proiectului (vezi Chei API / secrete din CLAUDE.md), niciodată în cod/git.
3. Adun materialul sursă: descrierea scenei/produsului, imagini de referință (dacă există — majoritatea modelelor pot porni de la o imagine, nu doar text), branding/paletă de culori, durata dorită.
4. Stabilesc din start durata și formatul (vertical pentru Instagram/TikTok Reels, orizontal pentru YouTube/site) — schimbarea formatului după generare înseamnă regenerare, nu doar crop.

## Abordare de implementare
1. Pentru fiecare clip: construiesc promptul din descriere + eventual imaginea de referință (imagine-la-video, dacă modelul suportă, dă rezultate mult mai consistente cu brandul decât text-la-video pur).
2. Generez clipul; timpul de generare e semnificativ mai mare decât la imagini (poate dura minute, nu secunde) — de comunicat clientului că nu e instant.
3. Arăt clientul rezultatul — la video, iterația costă mult mai mult (timp + bani) decât la imagini, deci încerc să clarific cât mai bine promptul/referința ÎNAINTE de prima generare, nu după.
4. Majoritatea modelelor generează clipuri scurte (de obicei 5-20 secunde) fără audio — dacă clientul vrea muzică/voce, se adaugă separat, post-generare (editare video simplă).

## Limitări/riscuri cunoscute
- **Cost mult mai mare decât la imagini** — per secundă de video generat, nu per bucată; de estimat volumul (câte clipuri, ce durată) și comunicat clientului clar înainte de a promite ceva.
- **Timp de generare** — de la zeci de secunde la câteva minute per clip, spre deosebire de imaginile aproape instant; afectează cât de "live" poate fi orice demo cu clientul.
- **Durată limitată**: majoritatea modelelor generează clipuri scurte (secunde, nu minute) — pentru un video lung (ex. prezentare de 2 minute), se generează pe segmente și se montează separat, crește mult complexitatea/costul.
- **Consistență între cadre/clipuri**: la fel ca la imagini, dar mai vizibil — fără o imagine de referință fixă, produsul poate arăta ușor diferit de la un clip la altul.
- **Fără audio nativ** (majoritatea modelelor) — muzică/voce se adaugă separat.
- **Moderare de conținut mai strictă** decât la imagini — cereri cu persoane reale, mărci recognoscibile sau conținut sensibil sunt respinse mai des; de verificat din timp cu un test simplu înainte de a promite ceva clientului.
- **Drepturi de autor**: aceleași incertitudini ca la imagini pentru modelele antrenate pe date cu proveniență neclară — de discutat explicit dacă clientul are sensibilitate legală pe asta.

## Ultima actualizare
2026-09-22
