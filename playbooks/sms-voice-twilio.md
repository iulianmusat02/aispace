# SMS/Voce (Twilio) — remindere, confirmări, IVR simplu

## Cerere tipică de client
"Vreau SMS-uri automate de confirmare/reminder", "un robot telefonic simplu (apasă 1 pentru...)", "clienții noștri nu sunt pe social media, dar sunăm/scriem mult".

## Ce presupune tehnic
- **Platformă/API oficial:** Twilio (cel mai comun furnizor pentru SMS + voce programabile; alternative: Vonage, AWS SNS/Connect — aleg Twilio ca implicit pentru că are cea mai bună documentație și cel mai simplu onboarding).
- **Cont necesar:** cont Twilio (al nostru sau al clientului — de discutat cine plătește/deține numărul), număr de telefon închiriat prin Twilio (SMS și/sau voce, în funcție de nevoie).
- **Conector/MCP disponibil:** verific `mcp-registry`; altfel Twilio API direct (REST, SDK-uri oficiale în majoritatea limbajelor).

## Setup per client
1. Cumpărare număr de telefon Twilio (cu suport SMS/voce, în țara relevantă pentru client).
2. Pentru SMS: configurare webhook pe numărul respectiv, pe evenimentul de mesaj primit.
3. Pentru voce/IVR: configurare TwiML (XML-ul care descrie fluxul de apel — "apasă 1 pentru...") sau un endpoint care generează TwiML dinamic.
4. Integrare cu sistemul clientului (ex. platforma de comenzi/programări) pentru date reale (nu textele hardcodate) — ex. status comandă, oră programare.

## Abordare de implementare
- **SMS**: mesaj primit → clasificare simplă (STOP/opt-out, întrebare, comandă) → răspuns automat sau escaladare. Pentru remindere/confirmări (outbound), triggerite de evenimente din sistemul clientului (comandă plasată, programare creată).
- **Voce/IVR**: apel primit → meniu TwiML cu opțiuni → fiecare opțiune duce la o acțiune (informație redată, transfer către un om, colectare de date prin taste). Pentru ceva mai sofisticat (voce naturală, nu doar taste), se poate integra speech-to-text + LLM + text-to-speech, dar creș complexitatea și costul semnificativ.

## Limitări/riscuri cunoscute
- **Opt-in/compliance**: SMS-urile de marketing/remindere necesită consimțământul destinatarului (legislație tip TCPA în SUA, GDPR + reguli locale de telecom în UE) — de verificat explicit cu clientul că are consimțământul, nu presupun automat.
- **STOP obligatoriu**: orice SMS automat trebuie să respecte cererile de dezabonare (`STOP`) — implementat din prima versiune, nu adăugat ulterior.
- Cost per SMS/minut de apel — variază mult pe țară; de comunicat clientului un estimat înainte de a promite volum mare.
- IVR-ul cu doar taste e ieftin și rapid de livrat; IVR conversațional (voce naturală) e un proiect mult mai mare — de clarificat cu clientul care variantă vrea, ca să nu se creeze o așteptare greșită de scop/preț.

## Ultima actualizare
2026-09-21
