# WhatsApp Business — automatizare conversații

## Cerere tipică de client
"Vreau un bot pe WhatsApp Business", "automatizare comenzi/suport pe WhatsApp", "să răspundem automat clienților pe WhatsApp".

## Ce presupune tehnic
- **Platformă/API oficial:** WhatsApp Business Platform — **Cloud API** (găzduită de Meta; varianta modernă, recomandată în locul vechiului On-Premises API).
- **Cont necesar:** **WhatsApp Business Account (WABA)** + număr de telefon dedicat (nu poate fi folosit simultan cu WhatsApp normal/Business app), toate sub un Meta Business Account verificat.
- **Conector/MCP disponibil:** verific `mcp-registry` pentru un conector WhatsApp existent înainte să implementez direct pe Cloud API.

## Setup per client
1. Client (sau noi, în numele lui) creează un Meta Business Account și un WABA.
2. Verificare număr de telefon dedicat (SMS/voce) — nu poate fi cel personal al clientului dacă vrea să păstreze și WhatsApp normal pe el.
3. Creez/configurez Meta App cu produsul **WhatsApp**, obțin token de acces permanent (System User, nu token temporar de dezvoltator).
4. Configurez webhook pentru mesaje primite.
5. Pentru mesaje **inițiate de business** (nu ca răspuns la client) în afara ferestrei de 24h → e nevoie de **message templates** pre-aprobate de Meta (ex. confirmare comandă, reminder programare) — le trimit spre aprobare din timp, durează de obicei ore, uneori zile.

## Abordare de implementare
1. Webhook primește mesajul → identifică userul/conversația.
2. În fereastra de 24h de la ultimul mesaj al clientului → conversație liberă, LLM răspunde direct pe baza FAQ/context-ului clientului.
3. În afara ferestrei → doar template-uri pre-aprobate (ex. „Comanda ta e gata de ridicare").
4. Escaladare la om pentru cereri ambigue, plângeri, sau orice cu efect financiar (anulări, rambursări) — niciodată confirmate automat fără validare.
5. Trimitere prin Cloud API (`POST /messages`).

## Limitări/riscuri cunoscute
- **Rating de calitate**: Meta acordă un "quality rating" per număr, care limitează câte conversații/24h poți iniția — un rating slab (multe blocări/raportări) reduce drastic volumul permis.
- **Opt-in obligatoriu**: nu se poate trimite primul mesaj către cineva care n-a inițiat contact sau nu și-a dat acordul explicit (ex. printr-un formular) — risc de suspendare a numărului.
- **Aprobare template-uri**: poate întârzia lansarea dacă nu e planificată din timp.
- Costuri per conversație (Meta taxează pe categorie de conversație, nu per mesaj) — de comunicat clientului înainte de a promite "gratuit".

## Ultima actualizare
2026-09-21
