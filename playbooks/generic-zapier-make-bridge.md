# Punte generică prin Zapier/Make

## Cerere tipică de client
"Vrem să conectăm tool-ul X cu Y, dar nu au integrare directă", "folosim un tool mai puțin comun, aveți cum să-l automatizați?", cereri pentru platforme fără API public accesibil sau fără conector MCP disponibil.

## Ce presupune tehnic
- **Platformă/API oficial:** nu unul singur — Zapier sau Make (fostul Integromat) sunt platforme de automatizare "glue" care au deja conectori pre-construiți pentru mii de tool-uri (inclusiv multe fără API public direct accesibil altfel).
- **Cont necesar:** cont Zapier/Make al clientului (planurile plătite au nevoie de abonament activ pentru volum/frecvență reală, nu doar de test).
- **Conector/MCP disponibil:** ambele platforme au propriile API-uri de management (creare/editare de "zap"-uri/scenarii programatic), dar de obicei mai simplu e configurarea prin UI-ul lor decât prin API.

## Setup per client
1. Verific dacă tool-urile pe care vrea clientul să le conecteze au deja conector nativ în Zapier/Make (marea majoritate au).
2. Aleg platforma (Zapier — mai simplu, mai popular; Make — mai flexibil pentru logică complexă, dar curbă de învățare mai mare) în funcție de complexitatea fluxului cerut.
3. Configurez trigger-ul (evenimentul care pornește automatizarea) și acțiunile (ce se întâmplă în urma lui) direct în UI-ul platformei.
4. Pentru logică ce depășește ce oferă nativ Zapier/Make (ex. clasificare LLM a conținutului) — inserez un pas de tip "webhook către un endpoint propriu" care apelează Claude API, apoi returnează rezultatul înapoi în flux.

## Abordare de implementare
Această rețetă e diferită de celelalte — nu construim cod de la zero, ci **orchestrăm** conectori existenți. Rolul nostru: proiectăm fluxul (ce declanșează ce), configurăm pașii în platformă, și adăugăm inteligență (LLM) doar unde platforma nu poate decide singură (ex. "e această recenzie negativă?", "ce categorie de email e asta?").

## Limitări/riscuri cunoscute
- **Cost recurent** al abonamentului Zapier/Make, separat de orice cost API — de comunicat clientului ca linie de cost continuă, nu doar cost unic de implementare.
- **Limite de execuții/lună** pe planurile mai mici — pot bloca automatizarea la volum mare neașteptat.
- Debugging mai greoi decât cod propriu — când ceva nu merge, depinde de logging-ul platformei, nu de al nostru.
- Nu e soluția potrivită dacă clientul are nevoie de control fin sau volum foarte mare (acolo cod propriu, integrare directă cu API-ul platformei, e mai eficient pe termen lung) — de recomandat ca soluție de pornire rapidă, nu neapărat finală.

## Ultima actualizare
2026-09-21
