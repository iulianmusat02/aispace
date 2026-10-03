# Chatbot pe site-ul clientului

## Cerere tipică de client
"Vreau un chat pe site care răspunde la întrebări", "asistent virtual pe website", "chatbot de suport pentru clienți".

## Ce presupune tehnic
- **Platformă/API oficial:** niciuna impusă din exterior — spre deosebire de Instagram/WhatsApp, nu depinde de aprobare Meta. Cea mai simplă categorie de automatizare din playbook-uri.
- **Cont necesar:** acces la codul/CMS-ul site-ului clientului (ca să integrăm un widget de chat), plus o cheie API Claude (Anthropic) pentru partea de conversație.
- **Conector/MCP disponibil:** nu e nevoie de MCP dedicat — se integrează direct prin Claude API (Messages API), eventual cu Tool Runner dacă chatbot-ul trebuie să caute în documente/bază de date proprie.

## Setup per client
1. Adun materialul sursă al clientului pentru răspunsuri (FAQ, documentație produs, politici de retur etc.) — ori text direct, ori fișiere din `my-context/assets/` dacă ni le dă nouă.
2. Aleg abordarea de acces la conținut: prompt caching cu tot conținutul (dacă e mic) sau RAG/retrieval (dacă e mare — căutare peste documente înainte de fiecare răspuns).
3. Implementez un backend minim (endpoint care primește mesajul userului, apelează Claude API cu context-ul relevant, întoarce răspunsul) — cheia API rămâne pe server, niciodată expusă în frontend.
4. Integrez un widget de chat pe site (JS simplu) care vorbește cu acel endpoint.
5. Clientul găzduiește el backend-ul (sau noi, temporar, până își montează infrastructura proprie) — de clarificat explicit cine deține/plătește găzduirea pe termen lung.

## Abordare de implementare
1. Userul scrie în widget → mesajul ajunge la backend.
2. Backend construiește promptul (system prompt cu tonul/regulile clientului + contextul relevant din materialul sursă).
3. Claude API generează răspunsul; pentru întrebări în afara scopului (ex. o plângere serioasă, o cerere de rambursare) — instrucțiune explicită în system prompt să direcționeze userul spre un om (email/telefon), nu să inventeze.
4. Opțional: buton „vorbește cu un om" mereu vizibil, ca fallback.

## Limitări/riscuri cunoscute
- **Halucinații**: fără system prompt strict + context relevant, poate inventa informații (prețuri, politici) — mereu ancorat în materialul sursă real al clientului, nu în cunoștințe generale.
- **Cost per conversație**: proporțional cu volumul de trafic — de estimat înainte și comunicat clientului.
- **Găzduire/întreținere**: cine ține backend-ul live pe termen lung trebuie stabilit de la început (nu presupun implicit că rămâne responsabilitatea noastră).
- Fără aprobări de platformă (spre deosebire de Instagram/WhatsApp) — timpul de lansare e mult mai scurt.

## Ultima actualizare
2026-09-21
