# Facturare automată

## Cerere tipică de client
"Vreau facturi generate automat la fiecare comandă/contract", "prea mult timp pierdut cu facturarea manuală", "sincronizare automată cu contabilitatea".

## Ce presupune tehnic
- **Implicit: Stripe Invoicing** — dacă clientul procesează deja plăți prin Stripe (foarte comun), facturarea vine "gratis" din același ecosistem, API simplu — de folosit ca primă opțiune.
- Alternative, doar când cererea o cere explicit:
  - **QuickBooks / Xero** — dacă clientul are nevoie de **contabilitate completă** (nu doar facturi — reconciliere, rapoarte financiare, integrare cu contabilul lui), nu doar de generat un PDF de factură.
  - **Facturare locală/e-Factura** (relevant pentru clienți din România) — dacă există cerințe legale specifice de facturare electronică (ex. sistemul e-Factura ANAF) — de verificat explicit, Stripe/QuickBooks nu acoperă automat conformitatea locală.

## Setup per client
1. Confirm ce sistem de plăți/contabilitate folosește deja clientul — nu presupun Stripe dacă are deja altceva.
2. Client generează cheie API pentru platforma aleasă; se stochează ca secret.
3. **Verific cerințele legale locale** (mai ales pentru clienți din România/UE — facturare electronică obligatorie, TVA, numerotare secvențială) — asta poate schimba complet alegerea de platformă, de clarificat înainte de a construi ceva.
4. Stabilesc evenimentul declanșator: comandă plasată, contract semnat, sfârșit de lună (abonamente) etc.

## Abordare de implementare
1. Eveniment declanșator (comandă, semnare contract) → colectez datele necesare facturii (client, produse/servicii, sumă, TVA).
2. Generez factura prin API-ul platformei alese, cu numerotare secvențială corectă (obligatoriu legal în majoritatea jurisdicțiilor).
3. Trimit factura automat către client (email, sau prin canalul deja stabilit — ex. WhatsApp dacă are acel playbook configurat).
4. Sincronizare cu contabilitatea (dacă e cazul) — nu doar generare, ci și reflectare corectă în evidențele financiare ale clientului.

## Limitări/riscuri cunoscute
- **Conformitate legală e critică aici, mai mult decât la orice alt playbook** — o factură greșită (numerotare, TVA, format) are consecințe fiscale reale pentru client, nu doar o experiență proastă. Nu implementez nimic în zona asta fără să confirm cerințele legale exacte cu clientul (sau recomand un contabil/consultant fiscal pentru validare).
- **e-Factura (România)**: dacă e aplicabilă, adaugă un pas de raportare către ANAF — de tratat ca cerință separată, nu presupusă automat inclusă în Stripe/QuickBooks.
- **Erori de date** (sumă greșită, client greșit) sunt mult mai costisitoare aici decât la un mesaj auto-reply greșit — de construit cu validare/confirmare înainte de emitere, nu 100% "fire and forget" fără verificare.
- **Sincronizare dublă**: dacă factura se generează în două sisteme (ex. Stripe + contabilitate separată) fără reconciliere corectă, apar discrepanțe greu de depistat ulterior.

## Ultima actualizare
2026-09-22
