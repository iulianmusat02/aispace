# Facebook Messenger — răspuns automat

## Cerere tipică de client
"Vreau ca Pagina noastră de Facebook să răspundă automat pe Messenger", "avem deja bot pe Instagram, vrem și pe Facebook".

## Ce presupune tehnic
- **Platformă/API oficial:** Messenger Platform, prin Meta Graph API — aceeași familie ca Instagram Messaging API (vezi `instagram-dm-auto-reply.md`), dar NU e configurare identică; se confundă des.
- **Cont necesar:** **Pagină de Facebook**, administrată dintr-un Meta Business Account verificat. Nu e nevoie de cont Instagram (dar dacă clientul are ambele, unele setări din Meta App se pot reutiliza).
- **Conector/MCP disponibil:** verific `mcp-registry`; altfel Graph API direct (webhook + Send API), la fel ca la Instagram.

## Setup per client
1. Dacă am făcut deja setup pentru Instagram al aceluiași client, reutilizez aceeași Meta App — adaug produsul **Messenger** pe lângă Instagram.
2. Dacă e client nou: creez Meta App, adaug produsul Messenger, îl leg de Pagina lui de Facebook.
3. Generez Page Access Token (System User, permanent, nu token de dezvoltator temporar).
4. Configurez webhook pe evenimentul `messages` pentru Pagină.
5. Pentru producție reală (răspuns oricui, nu doar rolurilor de test) → **App Review** pe permisiunea `pages_messaging`, similar cu Instagram.

## Abordare de implementare
Identică structural cu playbook-ul Instagram: webhook primește → LLM clasifică intenția → răspunde din FAQ-ul clientului sau escaladează la om → trimite prin Send API. Diferă doar endpoint-ul/produsul Meta folosit (Messenger vs Instagram) și micile diferențe de payload.

## Limitări/riscuri cunoscute
- Aceeași **fereastră de 24h** ca la Instagram — în afara ei, doar mesaje-tag specifice.
- Aceeași cerință de **App Review** pentru producție.
- **Nu se poate presupune** că setup-ul de Instagram acoperă automat și Messenger — clienții cred des că "e deja făcut" pentru că au bot pe Instagram; de clarificat explicit că sunt produse separate în Meta App, chiar dacă sub aceeași aplicație.

## Ultima actualizare
2026-09-21
