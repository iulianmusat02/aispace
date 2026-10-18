---
name: process
description: Transformă munca repetitivă a firmei în skill-uri și automatizări. Două intrări - userul povestește un proces pe care îl face manual (îl automatizez prin skill-uri, MCP-uri, conectori, API-uri directe și extensia Claude în Chrome), sau știe deja ce skill vrea (îl scriu direct, în formatul firmei, fără dubluri). Verifică și dacă un tool/conector e sigur cu date de client (GDPR, DPA). Folosește-l când userul scrie /process, vrea să automatizeze ceva ce face manual, vrea să-și facă un skill, o comandă sau un mod de lucru reutilizabil, întreabă dacă un tool e sigur cu datele unui client, sau după /install ca pas următor.
---

# /process — skill-uri și automatizări pentru firmă

Principiu din CLAUDE.md: nu doar ghidez, construiesc. Duc treaba cât pot de departe singur.

## 0. Verificare și intrarea potrivită

Aleg intrarea după ce spune userul; dacă nu e clar, întreb o dată (AskUserQuestion): „Povestesc un proces pe care îl fac de mână" / „Știu deja ce skill vreau".
- **A. Proces manual** („fac X de mână și durează"): pașii 1-5 de mai jos. Eu aleg uneltele; skill-ul e de obicei una dintre ele.
- **B. Skill direct** („vreau un skill care face X", o comandă sau un mod de lucru reutilizabil): sar la „Cum scriu un skill". Dacă pe parcurs reiese că e nevoie de conectori, API sau programare, trec la pașii 2-4 pentru acea parte.
- **Nu știe ce să automatizeze**: îi propun `/recommend-process`, care caută în context și îi dă top 3 idei; ideea aleasă revine aici, cu povestea deja adunată.
- **Doar o întrebare de compliance** (e sigur tool-ul X cu datele clienților?): sar direct la „Compliance", fără poveste.

**Rolul** (`reference/roluri.md`): un **owner** construiește (automatizări și skill-uri). Un **membru** povestește procesul sau descrie skill-ul dorit și primește propunerea, dar nu construiește nimic în spațiul comun: scriu o **cerere** către un owner (pasul 2b) și mă opresc.

Dacă `my-context/profile.md` lipsește, redirecționez spre `/install`: fără context nu știu cu cine și pe ce lucrează. Citesc `my-context/profile.md`, `team/profile.md` (dacă există) și `my-context/processes/` ca să nu reiau un proces deja descris.

## 1. Povestea procesului

Citesc `templates/process/interview.template.md` și urmez ghidul de acolo: îi cer userului să povestească liber (poate dicta) un proces pe care îl face manual acum, cu declanșator, pași, tool-uri, excepții, frecvență, date sensibile. Nu e formular: nu pun toate întrebările pe rând. Las povestea să curgă, apoi:

1. Rezum în 5-8 rânduri și confirm (AskUserQuestion: corect / lipsește ceva).
2. Pun cel mult 1-2 întrebări, doar pentru golurile care blochează automatizarea.
3. Tot ce pot afla singur (contextul, fișiere atașate, tool-uri conectate) aflu fără să întreb.

Nu dictez cuvinte de răspuns; buclele de continuare sunt mereu AskUserQuestion cu Da/Nu.

## 2. Propun automatizarea

Împart procesul pe pași și aleg pentru fiecare cea mai simplă unealtă care funcționează, în ordinea asta:

| Ordine | Unealtă | Când |
|---|---|---|
| 1 | **Skill** în `.claude/skills/<slug>/SKILL.md` | Orice logică repetabilă: pașii, regulile, formatul rezultatului. Aproape fiecare proces primește unul, ca să-l pot rula la cerere. |
| 2 | **MCP / conector existent** | Tool-ul are conector (vezi „Cum găsesc conectorul" mai jos). |
| 3 | **API direct** | Nu există MCP, dar există API oficial. Documentația o citesc acum, nu din memorie; cheia merge în `.env` (placeholder și în `.env.example`), niciodată în chat sau în cod. |
| 4 | **Extensia Claude în Chrome** | Nu există nici conector, nici API utilizabil, doar interfață web. Se folosește sesiunea deja logată a userului; nu introduc parole, nu trec de CAPTCHA, cer confirmare înainte de orice trimitere sau ștergere. Când o propun, o explic pe scurt ca la `/install` (pasul 5) și spun cât costă. |
| 5 | **Rămâne manual** | Pasul cere judecată sau acțiune pe care userul vrea să o păstreze. Spun clar care și de ce. |

### Cum găsesc conectorul

Pentru fiecare conector propus spun și **cât costă**, citit acum din sursa oficială: conectorul (gratuit / plătit, de la cât / gratuit până la o limită), separat de abonamentul tool-ului în sine; ce nu pot verifica marchez „cost neverificat”. Dacă e oferit de o firmă terță, o spun.


Caut eu, nu întreb din reflex. Verific, în ordine:
1. **Ce am deja**: tool-urile MCP din sesiune (conectate sau în lista celor care cer autentificare) și tabelele „Tools" din `my-context/profile.md` și `team/profile.md`.
2. **Registry**: încarc cu ToolSearch `mcp__mcp-registry__search_mcp_registry` și `mcp__mcp-registry__suggest_connectors` și caut după platformă.
3. **Fără conector** → API oficial. Citesc documentația oficială acum (WebSearch/WebFetch), nu din memorie: limite, aprobări (ex. App Review), costuri.
4. **Fără API utilizabil** → fallback generic: IMAP/SMTP pentru email, webhook, Zapier/Make ca adaptor; la nevoie, extensia Chrome.
5. `playbooks/` conține note mai vechi, scrise din cunoștințe generale și nevalidate pe clienți reali: le folosesc ca idei, nu ca adevăr. Unde contrazic documentația oficială sau `reference/compliance.md`, au prioritate acestea.

### Compliance

Cât de strict e verdictul depinde de date:
- **Fără date personale sau confidențiale** (poze de legume, texte publice): orice furnizor e acceptabil; contează calitatea și costul.
- **Cu date personale sau confidențiale** (clienți finali, emailuri, apeluri, produse nelansate): doar furnizorii cu verdict „OK" din `reference/compliance.md`, respectând condițiile lor.

Caut furnizorul în `reference/compliance.md`:
- E acolo și rândul are mai puțin de 6 luni → îl folosesc și spun userului data verificării.
- Lipsește sau e vechi → cercetez din surse oficiale (trust center, DPA, termeni API, retenție, antrenare pe date, rezidență UE) și actualizez rândul cu data și sursa. Ce nu pot citi marchez „neverificat"; nu completez din memorie.
- Reamintesc mereu: orice LLM din lanț (inclusiv Claude) trebuie adăugat în DPA-ul clientului; consimțământul pentru înregistrări e al agenției.

Prezint **2-3 variante** (de exemplu: A. doar un skill, îl rulezi tu la cerere; B. skill plus conector, pornește singur la un eveniment; C. complet automat, programat). Pentru fiecare: pas → unealtă → stare (gata / de autorizat / de construit), **timpul** de construit și **costul** (abonamente, apeluri API, timpul userului), riscul principal și ce trebuie să facă userul. Timpul și costul sunt estimări; spun asta și le marchez cum le-am obținut (preț oficial citit acum sau aproximare). Recomand una. Apoi AskUserQuestion: care variantă construiesc? Construiesc **doar** varianta aleasă și nimic cu efect real fără acest OK.

### 2b. Dacă userul e membru: cererea

Scriu `my-context/processes/<slug>.md` din `templates/process/_process.template.md` cu `Stare: cerere` (povestea, variantele, recomandarea) și un mesaj scurt, gata de trimis unui owner. Îi spun că cererea rămâne pe calculatorul lui până o preia un owner și mă opresc aici.

## 3. Construiesc

Pentru ce a aprobat:

1. **Skill-ul procesului**: urmez „Cum scriu un skill" de mai jos. Corpul conține pașii, regulile și excepțiile din poveste, uneltele alese și ce cere confirmare. Rămâne în proiect, deci ajunge și în repo-ul clientului prin sincronizare.
2. **Conectori / MCP**: nu instalez nimic fără OK explicit (instalarea unui MCP schimbă configurarea). OAuth îl face userul în browser; nu cer niciodată tokeni, parole sau coduri de autorizare în chat.
3. **API direct**: scriu scriptul în `my-context/scripts/`, care încarcă `.env` (model: `my-context/scripts/gen-image.sh` dacă există). Secretele urmează regula din CLAUDE.md: adaug doar placeholder-ul în `.env` și `.env.example`, îi dau userului calea ca link clickabil ([.env](.env)) și îi recomand să-și pună singur cheia acolo, manual.
4. **Hook** (o regulă care pornește singură la un moment anume, de exemplu înainte de o editare): scriptul merge în `.claude/hooks/`, cu o linie `# Pe scurt: ...` pe înțelesul userului (apare în sertarul de hooks din camera Custom Skills a biroului 3D), și se înregistrează în `.claude/settings.json` doar cu OK explicit (schimbă configurarea). Iese mereu cu 0 și nu blochează nimic fără să explice.
5. **Chrome**: pașii se descriu în skill ca instrucțiuni pentru extensie; încarc uneltele prin ToolSearch într-un singur apel și respect regulile skill-ului `chrome-browser`.
6. **Dacă procesul e recurent** (o oră fixă, o zi): îl notez în `my-context/TASKS.md` ca task recurent (formatul din `reference/task-workflow.md`, pe care îl citesc înainte să scriu) și propun programarea prin `/schedule` sau `/loop`, cu OK explicit.

## 4. Verific și documentez

- Rulez o probă pe un exemplu real, dat de user sau găsit de mine, cu acțiunile cu efect real oprite la confirmare. Raportez cinstit ce a mers și ce nu.
- Scriu `my-context/processes/<slug>.md` din `templates/process/_process.template.md`: povestea, tabelul pas → unealtă, skill-ul creat, conectorii cu verdictul de compliance, ce rămâne manual, cum am verificat.
- Dacă soluția a mers pe un caz real, actualizez rândul din `reference/compliance.md` cu ce am aflat și propun (nu creez singur) un playbook, conform `reference/skills-and-playbooks.md`.

## 5. Mai departe

AskUserQuestion: „Mai ai un proces de automatizat sau un skill de făcut?" (Da / Nu). Dacă Da, reiau de la pasul 0.

Închei cu: ce rulează acum, ce mai așteaptă o acțiune de la user (autorizare, cheie în `.env`) și cum pornește procesul de acum încolo (numele skill-ului).

## Cum scriu un skill

Folosit la intrarea B și la pasul 3.1. **Doar owner-i**; un membru primește cererea din pasul 2b.

1. **Ce trebuie să facă.** Aflu, fără formular lung: ce face skill-ul, când se declanșează (ce scrie userul sau ce situație), ce primește și ce produce, ce nu are voie să facă singur. Ce pot deduce din `my-context/`, din conversație sau din fișiere, deduc.
2. **Nu dublez.** Citesc `.claude/skills/*/SKILL.md` (frontmatter). Dacă există un skill asemănător, propun să-l actualizez, nu să creez altul (AskUserQuestion: actualizez / fac unul separat). Skill-urile livrate cu șablonul (install, planning, process, recommend-process, quiz, guide, add-context, sync, history, add-teammate, update-template) nu le suprascriu; dacă cererea le acoperă, o redirecționez spre ele.
3. **De ce are nevoie.** Listez înainte de scriere: conectori sau MCP-uri (verific ce e conectat; pentru unul nou aplic „Cum găsesc conectorul"), chei API (placeholder în `.env` și `.env.example`, userul le pune manual, cu link [.env](.env)), fișiere sau foi de calcul folosite, permisiuni. Dacă atinge date de client, aplic „Compliance". Ce lipsește, spun explicit.
4. **Scriu** `.claude/skills/<slug>/SKILL.md`, slug după **tipul** de lucru, nu după client:
   - Frontmatter cu `name` (= slug) și `description` în română, care spune când se folosește, ca să se declanșeze corect.
   - Corp în română: pași numerotați, reguli, excepții, ce cere confirmare (acțiunile cu efect real).
   - Fără secrete în text. Fără instrucțiuni de ocolire a regulilor sau de ascundere față de user (paza de injecție îl va semnala).
   - Buclele de continuare cu AskUserQuestion, niciodată cuvinte dictate de răspuns.
5. **Test și predare.** Rulez skill-ul o dată cu userul pe un exemplu real, cu acțiunile cu efect real oprite la confirmare, și corectez ce iese prost. Spun că skill-ul se publică automat prin sincronizarea contextului; membrii îl primesc la următorul `/sync`. În biroul 3D apare în camera Custom Skills.
