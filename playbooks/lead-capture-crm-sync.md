# Captare lead-uri → CRM

## Cerere tipică de client
"Vreau ca lead-urile de pe site/social media să ajungă automat în CRM", "prea multe lead-uri se pierd pentru că nu le introducem manual", "vreau follow-up automat la lead-uri noi".

## Ce presupune tehnic
- **Implicit: HubSpot** — cel mai comun CRM la clienți mici/mijlocii, API bine documentat, are și un tier gratuit generos — de folosit ca primă opțiune.
- Alternative, doar când cererea o cere explicit:
  - **Salesforce** — dacă clientul îl folosește deja (mai ales la companii mai mari) — nu introduc Salesforce dacă clientul n-are deja cont, e mult mai complex de configurat pentru cazuri simple.
  - **Pipedrive** — dacă clientul vrea ceva orientat strict pe vânzări, mai simplu decât HubSpot, fără featureset de marketing.
  - **Notion sau un simplu tabel** — pentru clienți foarte mici, fără CRM real, unde un HubSpot ar fi supradimensionat.
- **Sursele de lead-uri** se leagă de playbook-urile deja existente: formulare de pe site, DM-uri (`instagram-dm-auto-reply.md`, `whatsapp-business-automation.md`), email (`email-inbox-triage.md`).
- **Conector/MCP disponibil:** verific `mcp-registry` pentru CRM-ul ales.

## Setup per client
1. Confirm CRM-ul folosit de client (nu presupun HubSpot dacă are deja altceva configurat).
2. Client generează cheie API / acordă acces OAuth pentru CRM-ul respectiv.
3. Identific sursele reale de lead-uri ale clientului (formular site, DM, email, altceva) și, pentru fiecare, verific dacă avem deja un playbook de automatizare pe canalul respectiv.
4. Stabilesc câmpurile minime necesare pentru un lead valid (nume, contact, sursă, interes) și ce se întâmplă cu lead-uri incomplete.

## Abordare de implementare
1. Lead nou (formular/DM/email) → extrag datele relevante (LLM pentru mesaje nestructurate, ex. un DM care conține implicit un interes de cumpărare).
2. Verific duplicate în CRM înainte de a crea un lead nou (același contact pe canale diferite nu trebuie să devină 2 lead-uri separate).
3. Creez/actualizez lead-ul în CRM cu sursa exactă și contextul (ex. mesajul original), nu doar un nume gol.
4. Opțional: notificare către echipa de vânzări pentru lead-uri "fierbinți" (intenție clară de cumpărare), nu doar înregistrare pasivă.

## Limitări/riscuri cunoscute
- **Duplicate**: fără o strategie clară de matching (email/telefon), lead-uri de pe canale diferite pot polua CRM-ul cu intrări duplicate.
- **Calitatea datelor**: mesaje nestructurate (DM-uri, emailuri) pot avea informații lipsă sau ambigue — de decis explicit cu clientul ce se întâmplă cu lead-uri incomplete (se creează oricum, sau se cere follow-up automat pentru info lipsă).
- **GDPR/confidențialitate**: date personale colectate automat trebuie să respecte consimțământul și politica de date a clientului — de clarificat din start, nu presupus.
- **Cost CRM**: planurile plătite (peste tier-ul gratuit) au cost recurent proporțional cu numărul de contacte — de comunicat clientului dacă volumul de lead-uri crește.

## Ultima actualizare
2026-09-22
