# Email — triaj automat de inbox (Gmail/Outlook/alte providere)

## Cerere tipică de client
"Vreau ca emailurile primite să fie sortate/etichetate automat", "un asistent care îmi pregătește draft-uri de răspuns", "prea multe emailuri repetitive, vreau automatizare", "avem email pe domeniul nostru, nu Gmail/Outlook — se poate automatiza?".

## Ce presupune tehnic
- **Gmail (Google Workspace) sau Outlook (Microsoft 365)** — cazul comun: Gmail API respectiv Microsoft Graph API. Deja există conectori MCP comuni pentru Gmail (verificat separat per sesiune) — de preferat față de API direct, dacă acoperă nevoia (citit, etichetat, creat draft-uri).
- **Orice alt provider, fără API/MCP dedicat** (email pe domeniu propriu găzduit prin cPanel/hosting, Yahoo, ProtonMail, server de mail intern al clientului etc.) → fallback universal: **IMAP** (citire) + **SMTP** (trimitere/draft-uri). Aproape orice provider de email le suportă, indiferent cât de mic/necunoscut — nu e nevoie de API specific, doar de datele de conectare la server.
- **Cont necesar:** contul de email al clientului (sau al echipei lui), cu acces de admin dacă se conectează la nivel de organizație, nu doar de utilizator individual.

## Setup per client
1. Identific providerul real al clientului — dacă e Gmail/Outlook, merg pe API-ul oficial/conector MCP (mai robust, suportă push notifications). Dacă nu, trec direct pe IMAP/SMTP, fără să caut un conector care probabil nu există.
2. **Pentru Gmail/Outlook**: OAuth consent — clientul autorizează accesul (scop minim necesar: citire + etichetare + draft-uri, NU trimitere automată, dacă nu e cerut explicit).
3. **Pentru IMAP/SMTP generic**: am nevoie de la client — adresa serverului de mail (host IMAP/SMTP, de obicei `mail.domeniulclientului.ro` sau furnizat de hosting), portul (de obicei 993 pentru IMAP SSL, 587 pentru SMTP TLS), user + parolă. Multe providere cer o **parolă specifică aplicației** (app password), nu parola de login normală, mai ales dacă au 2FA activat — de verificat din documentația hosting-ului clientului. Credențialele se stochează ca secret, niciodată în cod/git.
4. Definesc împreună cu clientul regulile de triaj: ce categorii există (ex. suport, facturare, spam-uri de vânzări, urgent), ce se etichetează automat vs. ce generează doar draft de răspuns pentru validare umană.
5. Configurez procesarea: **Gmail/Outlook** — push notifications (Gmail: Pub/Sub; Outlook: webhook subscriptions) pentru reacție aproape instant. **IMAP generic** — nu are push notifications standard, deci polling periodic (verificare la interval, ex. la 1-5 minute) — reacție puțin mai lentă, dar suficientă pentru majoritatea cazurilor.

## Abordare de implementare
1. Email nou → LLM clasifică (categorie, urgență, sentiment).
2. Etichetare automată (label Gmail / categorie Outlook) pe baza clasificării.
3. Pentru categoriile predefinite ca "răspuns standard" → generează un **draft** (nu trimite automat — clientul revizuiește și apasă send).
4. Pentru urgențe/escaladări → notificare separată (ex. Slack/SMS) către persoana responsabilă, nu doar o etichetă pasivă.

## Limitări/riscuri cunoscute
- **Nu trimit emailuri automat în numele clientului** fără cerere explicită și testare — riscul unui răspuns greșit trimis către un client al clientului e mult mai mare decât la un DM social.
- **Confidențialitate**: inbox-ul poate conține date sensibile (contracte, date personale) — de clarificat cu clientul ce se poate procesa prin LLM și ce rămâne exclus.
- Volumul mare de emailuri poate genera costuri semnificative dacă fiecare e trimis integral către LLM — de luat în calcul filtrare/pre-triaj ieftin înainte de clasificarea completă.
- Permisiunile OAuth cerute trebuie să fie minime și explicite — clienții sunt de obicei precauți la "acces total la inbox".
- **IMAP/SMTP generic — riscuri specifice:**
  - Unele providere au IMAP **dezactivat implicit** — clientul trebuie să-l activeze explicit din setările contului/panoul de hosting înainte să pornim orice integrare.
  - Fără push notifications native, "aproape instant" nu e realist — de comunicat clientului că reacția vine la interval de polling (minute), nu secunde.
  - "Etichetare" pe IMAP înseamnă de obicei **mutare în folder** sau flag-uri, nu labels multiple ca la Gmail (un email poate avea mai multe label-uri Gmail simultan, dar de regulă un singur folder IMAP) — de clarificat cu clientul ce comportament vrea, ca să nu promit ceva ce protocolul nu susține direct.
  - Dacă providerul nu suportă parolă de aplicație și clientul are 2FA activat, conectarea directă cu user+parolă poate fi blocată — de verificat din timp, nu presupus că merge.

## Ultima actualizare
2026-09-22
