# „Unde e comanda mea" — bot de status comandă

## Cerere tipică de client
"Vreau ca oamenii să poată verifica singuri statusul comenzii", "prea multe mesaje de «unde e coletul meu»", "automatizare pentru magazinul nostru online".

## Ce presupune tehnic
- **Platformă/API oficial:** API-ul platformei de e-commerce a clientului — **Shopify Admin API** sau **WooCommerce REST API** cele mai comune; se adaptează la ce folosește clientul de fapt (verific înainte de a presupune Shopify implicit).
- **Cont necesar:** acces admin la magazinul clientului, pentru generarea unei chei API cu scop limitat (doar citire comenzi, nu acces la plăți/date complete de clienți dacă nu e necesar).
- **Conector/MCP disponibil:** verific `mcp-registry` (Shopify are conectori MCP relativ comuni); altfel REST API direct.

## Setup per client
1. Identific platforma de e-commerce reală a clientului (Shopify, WooCommerce, altă platformă) — nu presupun.
2. Generez API key cu **scop minim**: citire comenzi + status livrare, nu write, nu acces la date de plată.
3. Aleg canalul prin care userul întreabă: widget pe site, WhatsApp/Instagram (dacă are deja playbook-urile alea configurate), sau simplu formular cu număr de comandă + email.
4. Mapez statusurile interne ale platformei (ex. "fulfilled", "partially_fulfilled") la mesaje ușor de înțeles pentru client final.

## Abordare de implementare
1. Userul dă un identificator (nr. comandă + email/telefon, pentru verificare — nu se expune status doar pe baza numărului de comandă, ca oricine să nu poată vedea comenzile altcuiva).
2. Sistemul caută comanda prin API, verifică potrivirea identificatorului secundar.
3. Răspuns cu statusul curent, eventual link de tracking al curierului dacă platforma îl expune.
4. Dacă nu găsește comanda sau apar discrepanțe (ex. comandă anulată, litigiu) → escaladare la om, nu răspuns ambiguu.

## Limitări/riscuri cunoscute
- **Verificare identitate obligatorie** — fără al doilea identificator (email/telefon pe lângă nr. comandă), oricine ar putea afla detalii despre comanda altcuiva doar ghicind numărul.
- Datele de livrare vin adesea de la un curier terț (nu doar platforma de e-commerce) — statusul poate fi cu întârziere față de realitate dacă nu se integrează și API-ul curierului.
- Rate limits API (Shopify în special) — de dimensionat corect dacă magazinul are volum mare de întrebări simultane.
- Nu rezolvă litigii (produs lipsă, deteriorat) — doar informează despre status; orice reclamație reală merge la om.

## Ultima actualizare
2026-09-21
