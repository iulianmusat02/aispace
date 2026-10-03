# Generare + programare conținut social media

## Cerere tipică de client
"Vreau postări automate pe Instagram/Facebook/LinkedIn", "un calendar de conținut care se publică singur", "generați voi postările și le programați".

## Ce presupune tehnic
Se leagă direct de `image-generation.md` / `video-generation.md` (partea de conținut vizual) — acest playbook e despre partea de **programare/publicare**, nu despre răspuns la mesaje (acela e `instagram-dm-auto-reply.md`).

- **Implicit: Buffer** — cel mai simplu API, acoperă platformele comune (Instagram, Facebook, LinkedIn, X, TikTok), billing simplu — de folosit ca primă opțiune.
- Alternative, doar când cererea o cere explicit:
  - **Hootsuite** — relevant pentru clienți mai mari, cu echipe multiple și nevoie de aprobare/flux de lucru pe conținut (approval workflows).
  - **API-uri native per platformă** (Meta Graph API pentru Instagram/Facebook, LinkedIn API) — control maxim, dar mult mai multă muncă de integrare per platformă; de folosit doar dacă Buffer/Hootsuite nu acoperă o nevoie specifică (ex. tip de postare nesuportat de agregator).
- **Cont necesar:** cont Buffer (implicit) conectat la conturile sociale ale clientului (fiecare platformă cere autorizare separată prin OAuth, din contul clientului).
- **Conector/MCP disponibil:** verific `mcp-registry`.

## Setup per client
1. Client autorizează Buffer să posteze pe conturile lui (OAuth per platformă — Instagram/Facebook prin Meta Business, LinkedIn separat etc.).
2. Stabilim împreună: frecvența de postare, tonul/stilul brandului, ce tip de conținut (text, imagine generată, video generat, mix).
3. Definesc un flux de aprobare: conținutul generat trece prin client înainte de programare, sau se publică direct? (implicit: **trece prin aprobare** — publicare 100% automată fără revizuire e un risc de reputație prea mare pentru majoritatea clienților).

## Abordare de implementare
1. Generez conținutul (text + vizual, folosind playbook-urile de imagini/video unde e cazul) conform calendarului stabilit cu clientul.
2. Prezint conținutul pentru aprobare (draft, nu publicat) — batch, nu unul câte unul, ca clientul să vadă tot calendarul dintr-o dată.
3. După aprobare, programez prin Buffer la orele/zilele stabilite.
4. Urmăresc performanța de bază (dacă API-ul o expune) și ajustez tipul de conținut în timp, nu doar "setează și uită".

## Limitări/riscuri cunoscute
- **Limitări per platformă**: fiecare rețea are propriile reguli (Instagram nu permite postare de Stories prin unele API-uri terțe, LinkedIn are limite de rate diferite) — de verificat per platformă înainte de a promite acoperire completă.
- **Consistență vizuală**: dacă folosim generare AI pentru imagini/video, riscurile din acele playbook-uri se aplică și aici (consistență de brand, drepturi de autor).
- **Aprobare vs. viteză**: fluxul de aprobare adaugă latență — de clarificat cu clientul câtă independență îi dă botului (complet automat = risc mai mare, aprobare manuală = mai lent dar mai sigur).
- **Cost Buffer/Hootsuite**: abonament recurent, separat de costul de generare a conținutului — de comunicat ca linie de cost continuă.

## Ultima actualizare
2026-09-22
