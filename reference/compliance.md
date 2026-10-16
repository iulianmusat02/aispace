# Compliance furnizori (GDPR / DPA / antrenare pe date)

Citit de skill-ul `/conectori` și oricând întreabă userul dacă un tool e sigur cu date de client.

**Cum să-l folosesc:** verificat de la sursă pe **2026-10-04**, din pagini oficiale ale furnizorilor, prin cercetare automată. Unde pagina n-a putut fi citită, scrie „neverificat". Nu completez din memorie. Termenii se schimbă: după 6 luni sau înainte de un client sensibil, re-verific și actualizez rândul (cu data și sursa).

**Regulă de decizie:** dacă prin automatizare nu trec date personale sau confidențiale (ex. poze de legume), orice furnizor e acceptabil. Cu date personale/confidențiale: doar „OK cu rezerve", respectând condițiile. Orice LLM din lanț (inclusiv Claude) trebuie să apară în DPA-ul și lista de subprocesori ai clientului. Consimțământul pentru înregistrarea apelurilor/ședințelor e al agenției, la orice furnizor.

Verdicte: **OK** = utilizabil cu condițiile din coloana a 3-a · **Acord** = doar cu opt-out/contract enterprise · **Nu** = nu pentru date de client · **Neclar** = n-am putut verifica.

## Imagini și video

| Furnizor | Verdict | De știut |
|---|---|---|
| OpenAI API | OK | Nu antrenează pe date API decât cu opt-in; loguri abuz până la 30 zile; Zero Data Retention la cerere; proiect cu regiune UE. DPA: pagina oficială n-a putut fi citită. |
| Google Vertex AI (Imagen, Nano Banana, Veo) | OK | DPA pe servicii plătite; nu antrenează pe plătit; endpoint multi-regiune UE; ZDR doar pe Vertex. |
| Google Gemini API | OK doar plătit | Tier-ul gratuit antrenează și oameni pot citi conținutul. Loguri 30 zile, nedezactivabile. |
| Black Forest Labs (Flux) | Acord | SOC 2 T2 + ISO 27001:2022 declarate. Politica permite antrenare pe prompturi/imagini; opt-out prin email la privacy@blackforestlabs.ai, subiect „Training Opt Out". Termenii API dau licență de antrenare. DPA neconfirmat; retenție API nespecificată; endpoint UE neconfirmat. Flux prin Bedrock/Azure: neverificat. |
| Adobe Firefly (enterprise) | OK cu contract | Conținutul enterprise nu intră în antrenare (FAQ 2024, din rezumat). DPA, UE: neverificate. Indemnizare IP pentru enterprise. |
| Runway | Neclar | SOC 2 T2 + ISO 27001:2022 pe site. DPA, antrenare, UE: neverificate. |
| Stability AI | Acord | Antrenează implicit, opt-out din cont. Fără endpoint UE; DPA nu apare în termeni. |
| Ideogram (API) | Acord | Termenii API: nu antrenează pe input/output. Fără DPA, fără certificări găsite, fără rezidență. |
| Midjourney | Nu | Licență perpetuă pe conținut, imagini publice implicit. Fără API/DPA găsit; site-ul a blocat citirea. |
| Luma | Nu | Licență irevocabilă pentru antrenare, chiar pe planuri plătite. Doar SUA. |
| Pika | Nu | Neverificat (pagini inaccesibile); tratat ca consumer. |
| Kling | Neclar | Posibilă procesare în China (surse secundare). Risc ridicat pentru date UE. |

## Voce, audio, transcriere, telefonie

| Furnizor | Verdict | De știut |
|---|---|---|
| ElevenLabs | OK | DPA public cu SCC. Pentru date de client: Enterprise + rezidență UE + Zero Retention Mode. Termenii standard au licență „to improve the Services", cu opt-out din setări. Vocile clonate persistă. |
| OpenAI audio (Realtime/Whisper/TTS) | OK | Transcriere/Realtime fără retenție în logurile de abuz; TTS 30 zile. ZDR și rezidență UE doar cu aprobare. |
| Retell AI | OK | DPA semnabil online, cu SCC. **Nu operează în UE** (tot în SUA, AWS): cere evaluare de transfer. Retenție configurabilă 1 zi–2 ani. |
| Recall.ai | OK | Regiune Frankfurt. Conturile create după 2025-06-12 păstrează implicit nelimitat: setează retenția explicit. DPA neverificat. |
| Fireflies.ai | OK | DPA public; declară că nu folosește date personale pentru antrenare. UE doar prin Private Storage (sursă secundară). |
| Twilio | OK | DPA acoperă conținutul clientului. Regiune IE1 (Irlanda) pentru Voice/Media Streams. SOC 2 neverificat. |
| Otter.ai | Acord | Antrenează pe înregistrări de-identificate. Fără rezidență UE. |
| Vapi, Bland AI | Neclar | Certificări declarate pe site; DPA-ul pentru client, antrenarea și UE neverificate. |
| Suno | Nu | Licență perpetuă pe ce încarci, inclusiv pentru modele ML; planul gratuit e non-comercial. |
| Udio | Neclar | Termenii n-au putut fi citiți. |

## Mesagerie, social, automatizare

| Furnizor | Verdict | De știut |
|---|---|---|
| WhatsApp Cloud API | OK | Meta e processor; DPA (WhatsApp Business Data Processing Terms) + SCC. Mesaje reținute max 30 zile. Presa scrie că din 2026-01-15 termenii interzic asistenții AI de uz general; boturile de suport pentru clienți sunt permise. Textul termenilor n-a putut fi citit: confirmă-l înainte de a promite. |
| Messenger / Instagram | OK | Fereastră 24h, bot declarat la început, răspuns în 30 s, App Review. DPA specific neverificat. |
| Telegram Bot API | OK | **Fără DPA**: ești controller singur. Bot ToS interzice colectarea de date pentru ML. |
| Hootsuite | OK | Cel mai bine documentat: SOC 2 T2, ISO 27001, DPA GDPR presemnat. Verifică opt-out-ul pentru funcțiile AI. |
| Zapier | OK | DPA în ToS cu SCC; SOC 2 T2. Găzduit în SUA. Enterprise e opt-out automat din antrenare; verifică ce furnizori AI sunt activi. |
| Make | OK | DPA + SCC, SOC 2 T2. Rezidență UE (Dublin) doar din surse secundare. |
| Buffer | Neclar | Doar publicare. Certificări și DPA semnabil neverificate. |

## LLM, email, CRM, plăți, e-commerce

| Furnizor | Verdict | De știut |
|---|---|---|
| Anthropic (Claude API) | OK | Nu antrenează pe date API implicit; ștergere în 30 zile; ZDR prin acord. DPA în termenii comerciali cu SCC (confirmat prin rezumate terțe). **Fără inferență doar-UE pe API-ul direct** (`inference_geo`: global sau us); Bedrock/Vertex: neverificat. |
| Gmail API | OK | Scope-urile Gmail sunt „restricted": verificare OAuth, plus audit anual CASA dacă stochezi datele. Alternativă la scară mică: IMAP sau aplicații interne per client. |
| Microsoft Graph / 365 | OK | Consimțământ de admin obligatoriu pentru permisiuni de aplicație; publisher verificat. |
| HubSpot | OK | DPA în ToS cu SCC; Frankfurt; terții nu pot antrena. |
| Salesforce | OK | DPA cu SCC; Hyperforce cu rezidență UE; termenii variază pe ediție. |
| Pipedrive | OK | DPA cu SCC și DPF; datacenter în Germania, dar DPA permite procesare globală. |
| Stripe | OK | DPA cu SCC. Antrenează propriile modele antifraudă pe date personale, fără opt-out. **Nu generează e-Factura**: cere aplicație terță. |
| QuickBooks Online | Neclar | DPA pentru QBO de bază neclar; date în SUA; fără suport e-Factura găsit. |
| Xero | OK | DPA automat în termeni; interzice antrenarea AI pe datele din API; date UE posibil procesate în Noua Zeelandă. **Fără e-Factura România.** |
| Shopify | OK | DPA cu anexă EEA/UK/CH; interzice antrenarea AI pe datele comercianților; date la repaus în Europa pentru comercianți noi. Date personale ale clienților cer aprobare „protected customer data". |
| Trustpilot | OK | DPA în toate contractele; nu antrenează pe datele businessului. |
| Google Business Profile API | Neclar | Acces doar pe aplicare (~14 zile). DPA, antrenare, retenție neverificate. |

## Surse principale (la 2026-10-04)

OpenAI: developers.openai.com/api/docs/guides/your-data, trust.openai.com · Google: ai.google.dev/gemini-api/terms, ai.google.dev/gemini-api/docs/zdr · BFL: bfl.ai/legal/privacy-policy, bfl.ai/legal/flux-api-service-terms · ElevenLabs: elevenlabs.io/dpa · Retell: docs.retellai.com/general/compliance · Recall: docs.recall.ai/docs/regions · Twilio: twilio.com/en-us/legal/data-protection-addendum · Meta: developers.facebook.com/documentation/business-messaging/whatsapp/data-privacy-and-security · Telegram: telegram.org/tos/bot-developers · Hootsuite: trustcenter.hootsuite.com · Zapier: zapier.com/legal/data-processing-addendum · Anthropic: privacy.claude.com, platform.claude.com/docs/en/manage-claude/data-residency · Gmail: developers.google.com/workspace/gmail/api/auth/scopes · HubSpot: legal.hubspot.com/dpa · Stripe: docs.stripe.com/invoicing/e-invoicing · Xero: xero.com/us/legal/terms/data-processing · Shopify: shopify.com/legal/dpa
