# Generare de imagini (AI)

## Cerere tipică de client
"Vreau imagini pentru produse fără sesiune foto", "poze pentru social media generate automat", "am nevoie de vizualuri pentru un produs care nu există fizic încă", "descrieri + imagini pentru catalog".

## Ce presupune tehnic
Nu există un provider implicit universal — alegerea depinde de **tipul de imagini cerute** (vezi pasul 1 din Setup per client, unde întreb explicit, nu presupun). Opțiuni, cu punctul forte al fiecăreia:

- **Flux (Black Forest Labs, Pro/Ultra)** — cel mai bun echilibru realism + API curat (Replicate, fal.ai, sau direct BFL) — de recomandat ca prima opțiune pentru **fotorealism** (produse, natură, texturi organice), unde DALL-E tinde să pară "digital/glossy".
- **Midjourney (v6.1+)** — considerat standardul de aur pentru realism estetic, dar API-ul e mai puțin matur/enterprise-friendly (pornit din Discord, API propriu mai nou) — de ales când clientul vrea calitatea maximă absolută și acceptă un flux de lucru puțin mai puțin automatizat decât Flux/DALL-E.
- **Google Imagen** (Vertex AI) — foarte realist, API oficial curat — bun dacă clientul e deja pe Google Cloud.
- **Nano Banana / Nano Banana Pro** (Gemini 2.5 Flash Image, Google DeepMind — model diferit de Imagen, deși tot de la Google) — foarte bun la fotorealism ȘI la **editare de imagini existente** cu păstrarea consistenței (ex. schimbi fundalul unui produs păstrând produsul identic) — de luat în calcul specific când cererea implică editare, nu doar generare de la zero. Disponibil prin Gemini API.
- **DALL-E (OpenAI Images API)** — cel mai simplu de integrat (același cont ca restul playbook-urilor OpenAI-implicite), bun la "ascultat promptul", dar mai puțin fotorealist pe texturi organice decât Flux/Imagen/Midjourney — bun pentru ilustrații/stil grafic, nu neapărat pentru foto-realism.
- **Ideogram** — cel mai bun la text lizibil în imagine (etichete, prețuri) — celelalte au des probleme cu textul.
- **Adobe Firefly** — cel mai sigur legal (antrenat doar pe conținut licențiat/Adobe Stock), dar vizual mai "ilustrativ comercial", nu cel mai realist — de ales când clientul e sensibil la risc de copyright, nu la realism maxim.
- **Stability AI / Stable Diffusion** — control total (model custom, fine-tuning, self-hosted) — de ales doar dacă clientul chiar are nevoie de asta, nu ca implicit.
- **Conector/MCP disponibil:** verific `mcp-registry` pentru providerul ales — dacă nu găsesc conector dedicat, API direct (REST, chei simple).

## Setup per client
1. **Întreb explicit ce fel de imagini vrea** (nu presupun un provider implicit) — AskUserQuestion: "Ce fel de imagini vrei să generezi?"
   - **Fotorealiste** (produse, natură, oameni reali) → recomand **Flux**; dacă vrea calitatea maximă absolută și acceptă un flux mai puțin automatizat, alternativa e **Midjourney**.
   - **Ilustrații / stil grafic / branding** → **DALL-E** (simplu) sau **Adobe Firefly** (dacă contează siguranța legală).
   - **Text important în imagine** (etichete, prețuri) → **Ideogram**.
   - **Nu sunt sigur / prioritate cost-volum** → **DALL-E** ca fallback rapid de testat, cu opțiunea de a trece la Flux dacă rezultatul nu e suficient de realist.
   
   Indiferent de răspuns: dacă cererea e despre **editarea unei imagini existente** (nu generare de la zero — ex. schimbă fundalul, păstrează produsul identic), trec pe **Nano Banana** în locul opțiunii alese mai sus, indiferent de categorie — e punctul lui forte specific.
2. Client (sau noi, temporar) creează cont + cheie API la providerul ales; cheia se pune în `.env` la rădăcina proiectului (vezi „Chei API / secrete" din CLAUDE.md), niciodată în cod/git, niciodată cerută/afișată direct în conversație dacă se poate evita.
3. Adun materialul sursă necesar: descrierea produsului, eventual poze de referință reale (pentru context/stil), branding/paletă de culori dacă există.
4. Pentru consistență de brand pe mai multe imagini (ex. catalog întreg), stabilesc un prompt-template reutilizabil (stil, unghi, fundal) în loc să generez fiecare imagine ad-hoc.

## Abordare de implementare
1. Pentru fiecare produs: construiesc promptul din descrierea produsului + stilul stabilit cu clientul.
2. Generez imaginea prin API-ul ales; salvez rezultatul (ex. în `my-context/assets/` sau alt folder de livrabile al task-ului).
3. Arăt clientul rezultatul înainte de a-l considera final — generarea AI variază, aproape mereu e nevoie de 2-3 iterații de prompt până la un rezultat acceptabil.
4. Pentru volum mare (catalog întreg), procesez pe rând, nu tot deodată — mai ușor de verificat calitatea și de oprit dacă ceva nu merge.

## Limitări/riscuri cunoscute
- **Consistență de brand**: fiecare generare e independentă — fără prompt-template strict, produsele dintr-un catalog pot arăta vizual inconsistent (stiluri diferite, unghiuri diferite).
- **Drepturi de autor**: unele modele (nu Firefly) sunt antrenate pe date cu proveniență neclară — risc pentru clienți care vor folosi imaginile comercial la scară mare; de discutat explicit ce provider e potrivit.
- **Text în imagine**: majoritatea modelelor (exceptând Ideogram) generează text ilizibil/greșit — de evitat cereri cu text important pe imagine, altfel de adăugat text separat, post-generare (ex. suprapus grafic).
- **Fețe/persoane reale**: majoritatea providerilor au restricții pe generarea de persoane recognoscibile/celebrități — de clarificat cu clientul dacă are nevoie de modele umane în imagini (poate necesita altă abordare, ex. poze reale + AI doar pentru fundal/retuș).
- **Fotorealism produse naturale (legume, fructe)**: GPT Image iese des „prea perfect”/lucios, ca de plastic, chiar cu prompt de realism. FLUX.2 Pro (Black Forest Labs, `api.bfl.ai`, header `x-key`, cheie `BFL_API_KEY`) iese vizibil mai real — dar exagerează imperfecțiunile (pete, crăpături) dacă promptul le cere explicit; de dozat. BFL returnează implicit JPEG — cer `output_format: png` sau salvez ca `.jpg`.
- **Cost per imagine**: variază semnificativ între provideri — de estimat volumul așteptat (ex. catalog de 200 produse) și comunicat clientului înainte de a promite "gratuit" sau "nelimitat".

## Ultima actualizare
2026-09-23
