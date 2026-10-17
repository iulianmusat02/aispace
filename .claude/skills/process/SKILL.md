---
name: process
description: Ascultă cum face userul un proces manual din munca lui de zi cu zi, propune cum se poate automatiza și îl automatizează efectiv, prin skill-uri instalate în acest proiect, MCP-uri, conectori, API-uri directe și extensia Claude în Chrome. Verifică și dacă un tool/conector e sigur cu date de client (GDPR, DPA). Folosește-l când userul scrie /process, vrea să automatizeze ceva ce face manual, întreabă dacă un tool e sigur cu datele unui client, sau după /install ca pas următor.
---

# /process — din proces manual în automatizare

Principiu din CLAUDE.md: nu doar ghidez, construiesc. Pornesc de la povestea userului și duc procesul cât pot de departe singur.

## 0. Verificare

Dacă userul doar întreabă dacă un tool e sigur cu date de client, sar direct la „Compliance" de mai jos, fără povestea procesului.

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
| 4 | **Extensia Claude în Chrome** | Nu există nici conector, nici API utilizabil, doar interfață web. Se folosește sesiunea deja logată a userului; nu introduc parole, nu trec de CAPTCHA, cer confirmare înainte de orice trimitere sau ștergere. |
| 5 | **Rămâne manual** | Pasul cere judecată sau acțiune pe care userul vrea să o păstreze. Spun clar care și de ce. |

### Cum găsesc conectorul

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

Prezint propunerea scurt: pas → unealtă → stare (gata / de autorizat / de construit) → riscul principal → ce trebuie să facă userul. Apoi AskUserQuestion: ce construiesc acum? Nu construiesc nimic cu efect real fără acest OK.

## 3. Construiesc

Pentru ce a aprobat:

1. **Skill-ul procesului**: creez `.claude/skills/<slug>/SKILL.md` (slug după tipul procesului, nu după client; dacă există unul asemănător, îl actualizez). Frontmatter cu `name` și o `description` care spune clar când se declanșează; corpul conține pașii, regulile și excepțiile din poveste, uneltele alese și ce cere confirmare. Rămâne în proiect, deci ajunge și în repo-ul clientului.
2. **Conectori / MCP**: nu instalez nimic fără OK explicit (instalarea unui MCP schimbă configurarea). OAuth îl face userul în browser; nu cer niciodată tokeni, parole sau coduri de autorizare în chat.
3. **API direct**: scriu scriptul în `my-context/scripts/`, care încarcă `.env` (model: `my-context/scripts/gen-image.sh` dacă există). Secretele urmează regula din CLAUDE.md: adaug doar placeholder-ul în `.env` și `.env.example`, îi dau userului calea ca link clickabil ([.env](.env)) și îi recomand să-și pună singur cheia acolo, manual.
4. **Chrome**: pașii se descriu în skill ca instrucțiuni pentru extensie; încarc uneltele prin ToolSearch într-un singur apel și respect regulile skill-ului `chrome-browser`.
5. **Dacă procesul e recurent** (o oră fixă, o zi): îl notez în `my-context/TASKS.md` ca task recurent (formatul din `reference/task-workflow.md`, pe care îl citesc înainte să scriu) și propun programarea prin `/schedule` sau `/loop`, cu OK explicit.

## 4. Verific și documentez

- Rulez o probă pe un exemplu real, dat de user sau găsit de mine, cu acțiunile cu efect real oprite la confirmare. Raportez cinstit ce a mers și ce nu.
- Scriu `my-context/processes/<slug>.md` din `templates/process/_process.template.md`: povestea, tabelul pas → unealtă, skill-ul creat, conectorii cu verdictul de compliance, ce rămâne manual, cum am verificat.
- Dacă soluția a mers pe un caz real, actualizez rândul din `reference/compliance.md` cu ce am aflat și propun (nu creez singur) un playbook, conform `reference/skills-and-playbooks.md`.

## 5. Mai departe

AskUserQuestion: „Mai ai un proces de automatizat?" (Da / Nu). Dacă Da, reiau de la pasul 1.

Închei cu: ce rulează acum, ce mai așteaptă o acțiune de la user (autorizare, cheie în `.env`) și cum pornește procesul de acum încolo (numele skill-ului).
