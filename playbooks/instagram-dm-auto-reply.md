# Instagram — răspuns automat la mesaje directe (DM)

## Cerere tipică de client
"Vreau ca Instagram-ul nostru să răspundă automat la mesaje", "un bot pe Instagram care răspunde la întrebări frecvente", "automatizare DM Instagram".

## Ce presupune tehnic
- **Platformă/API oficial:** Instagram Messaging API, prin Meta Graph API (Messenger Platform).
- **Cont necesar:** cont Instagram **Professional** (Business sau Creator), conectat la o **Pagină de Facebook**, ambele administrate dintr-un **Meta Business Account** verificat.
- **Conector/MCP disponibil:** verific `mcp-registry` (`search_mcp_registry` / `suggest_connectors`) — dacă nu există conector gata, se lucrează direct cu Graph API (REST, webhook + Send API).

## Setup per client
1. Client creează/confirmă cont Instagram Professional, legat la o Pagină Facebook.
2. Creez o Meta App în [developers.facebook.com](https://developers.facebook.com), adaug produsele **Messenger** și **Instagram**.
3. Configurez webhook-ul (URL propriu, ex. un endpoint găzduit de noi) pe evenimentul `messages` pentru Instagram.
4. Generez Page Access Token pentru pagina clientului; îl stochez ca secret (niciodată în cod/git).
5. Pentru funcționalitate completă (răspuns automat în afara ferestrei de 24h, mesaje către oricine i-a scris vreodată) e nevoie de **App Review** de la Meta pe permisiunea `instagram_manage_messages` — clientul trebuie să fie proprietarul aplicației aprobate, sau să ne autorizeze ca System User în Business Manager.

## Abordare de implementare
1. Webhook primește mesajul → identifică conversația/userul.
2. LLM clasifică intenția (întrebare frecventă / preț / program / plângere / altceva).
3. Pentru intențiile acoperite de FAQ-ul clientului → răspuns automat, generat/ales din baza de cunoștințe a clientului.
4. Pentru orice ce nu se încadrează clar (plângeri, negocieri, cereri complexe) → escaladare către un om, cu context (nu răspunde "orbește").
5. Răspunsul se trimite prin Send API (Graph API), în numele Pagină/contului Instagram al clientului.

## Limitări/riscuri cunoscute
- **Fereastra de 24h**: se poate răspunde liber doar în primele 24h de la ultimul mesaj al userului; după aceea, doar mesaje-tag specifice (ex. `HUMAN_AGENT`), nu conversație liberă.
- **App Review**: obligatoriu pentru producție reală, poate dura zile–săptămâni; fără el, funcționează doar în modul de test (roluri de dezvoltator/tester pe aplicație).
- **Politica Meta** interzice automatizări care mimează un om fără disclosure, sau spam; recomand mereu să fie clar (chiar dacă subtil) că e un asistent automat.
- Rate limits per aplicație/pagină — de verificat volumul așteptat de client înainte de a promite timp de răspuns instant la scară mare.

## Ultima actualizare
2026-09-21
