# Recenzii (Google Business Profile / Trustpilot) — răspuns automat

## Cerere tipică de client
"Vreau să răspundem automat la recenzii noi", "nu mai prindem timp să răspundem la toate review-urile", "un asistent pentru recenzii Google".

## Ce presupune tehnic
- **Platformă/API oficial:** Google Business Profile API (pentru recenzii Google) sau Trustpilot API (dacă e platforma folosită de client) — aleg în funcție de unde primește clientul recenzii.
- **Cont necesar:** acces la **Google Business Profile** al clientului (rol de manager, acordat de proprietarul profilului) sau cont business Trustpilot.
- **Conector/MCP disponibil:** verific `mcp-registry`; altfel API direct.

## Setup per client
1. Clientul acordă acces de management pe profilul lui (Google Business Profile: adaugă contul nostru/al aplicației ca manager; Trustpilot: API key din contul business).
2. Configurez polling periodic (recenziile noi nu au întotdeauna webhook nativ — de verificat per platformă) sau webhook dacă e disponibil.
3. Stabilesc împreună cu clientul **tonul** răspunsurilor (formal/prietenos) și exemple de răspunsuri bune anterioare, ca LLM-ul să scrie în stilul lui, nu generic.

## Abordare de implementare
1. Recenzie nouă detectată → LLM analizează sentimentul (pozitiv/neutru/negativ) și conținutul.
2. **Recenzii pozitive** (4-5 stele, fără plângere specifică) → răspuns automat de mulțumire, personalizat pe baza conținutului (nu un text identic de fiecare dată — arată fals).
3. **Recenzii negative sau cu plângere concretă** → NU se răspunde automat public fără validare umană — se pregătește un draft și se notifică persoana responsabilă (risc de reputație prea mare pentru răspuns 100% automat).
4. Publicare răspuns prin API, doar pentru categoriile aprobate ca "automate" de client.

## Limitări/riscuri cunoscute
- **Recenziile negative sunt cea mai sensibilă zonă** — un răspuns automat prost formulat poate agrava public o problemă; implicit tratate ca "draft + validare om", niciodată auto-publicate fără acord explicit.
- Politicile platformelor interzic recenzii/răspunsuri false sau manipulative — răspunsurile trebuie să fie genuine, legate de conținutul real al recenziei.
- Rate limits și cote API — Google Business Profile API are cote relativ stricte, de verificat pentru clienți cu volum mare de recenzii.
- Nu toate platformele au API public accesibil ușor (ex. unele agregatoare de recenzii nu oferă write access) — de verificat disponibilitatea reală înainte de a promite automatizare completă.

## Ultima actualizare
2026-09-21
