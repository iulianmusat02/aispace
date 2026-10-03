# Agent vocal conversațional (voce naturală, nu meniu cu taste)

## Cerere tipică de client
"Vreau un robot telefonic care chiar vorbește natural, nu apasă 1 pentru...", "recepționist virtual care preia apelurile", "agent vocal AI pentru programări/suport telefonic".

## Ce presupune tehnic
Diferit de `sms-voice-twilio.md` (acela e IVR clasic, cu taste) — aici userul vorbește liber, iar agentul înțelege și răspunde natural, în timp real.

- **Implicit: OpenAI Realtime API** (voce-la-voce, aceeași familie de cont ca DALL-E/Sora) — de folosit ca primă opțiune, fără să deschid discuția de provider decât dacă apare un motiv concret. Nu gestionează singur telefonia — se combină cu **Twilio** (Media Streams) pentru partea de apel telefonic efectiv.
- Alternative, doar când cererea o cere explicit:
  - **Vapi** sau **Bland AI** — orchestrare all-in-one (telefonie + voce + LLM incluse) — setup mult mai rapid, dar mai puțin control și cost mai mare per minut; bun când clientul vrea ceva funcțional repede, nu control fin.
  - **ElevenLabs Conversational AI** — dacă vocea trebuie să fie foarte naturală/expresivă (brand-uri unde calitatea vocii contează mult) sau clientul vrea o voce custom (clonată).
  - **Retell AI** — orientat pe call-center (transfer către operator, analytics pe apeluri) — relevant pentru clienți cu volum mare de apeluri și nevoie de raportare.
- **Cont necesar:** cont OpenAI (implicit) + cont Twilio (telefonie) + număr de telefon Twilio; pentru alternative, cont la providerul respectiv (de obicei include și telefonia).
- **Conector/MCP disponibil:** verific `mcp-registry` înainte de integrare directă.

## Setup per client
1. Cumpărare număr de telefon Twilio (dacă nu se folosește un provider all-in-one care include telefonia).
2. Configurare Twilio Media Streams → conectare la OpenAI Realtime API (stream audio bidirecțional).
3. Definesc împreună cu clientul: ce poate face agentul (informații, programări, transfer către om), tonul/persoana vocii, ce declanșează transferul către un operator uman.
4. Integrare cu sistemul clientului dacă agentul trebuie să acceseze date reale (ex. calendar pentru programări, status comandă — reutilizez `order-status-bot.md` dacă e cazul).

## Abordare de implementare
1. Apel primit → Twilio deschide stream audio → trimis către modelul vocal (OpenAI Realtime sau alternativa aleasă).
2. Modelul ascultă, decide intenția, răspunde vocal în timp real (latență mică e critică — orice întârziere >1-2s se simte nenatural).
3. Pentru acțiuni concrete (programare, verificare status) → apel de tool/function calling către sistemul clientului, nu doar conversație liberă.
4. Transfer către om explicit configurat pentru: cereri ambigue, nemulțumiri, orice cu efect financiar/contractual.

## Limitări/riscuri cunoscute
- **Latență**: orice combinație cu componente separate (STT + LLM + TTS, în loc de un model voce-la-voce nativ) adaugă întârziere vizibilă — de testat cu apeluri reale înainte de a promite "instant".
- **Cost per minut** semnificativ mai mare decât SMS/IVR clasic — de estimat volumul de apeluri așteptat și comunicat clar clientului.
- **Halucinații în timp real**: fără function calling strict pentru acțiuni concrete, agentul poate "inventa" informații vorbind natural — la fel de periculos ca la chat, dar mai greu de verificat post-factum (nu există transcript vizibil pentru client în timp real).
- **Accente/zgomot de fundal**: calitatea recunoașterii vocale scade cu zgomot/accente puternice — de testat cu condiții reale, nu doar în liniște.
- **Percepție/etică**: multe jurisdicții cer dezvăluirea că interlocutorul e AI, nu om — de clarificat cu clientul din start, nu adăugat ulterior.

## Ultima actualizare
2026-09-22
