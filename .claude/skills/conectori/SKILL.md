---
name: conectori
description: Găsește singur ce conectori, MCP-uri sau API-uri sunt necesare pentru o automatizare sau pentru tool-urile unui client, verifică compliance-ul lor (GDPR, DPA, antrenare pe date) și propune soluția. Folosește-l când userul scrie /conectori, cere o automatizare (mesaje, email, CRM, facturi, imagini, voce, transcriere) sau întreabă dacă un tool e sigur cu date de client.
---

# /conectori — găsește conectorii și verifică compliance-ul

Principiu din CLAUDE.md: caut eu, nu întreb din reflex. Întreb doar ce nu pot afla singur: ce date trec prin automatizare, ce conturi are clientul, ce aprobări are.

## 1. Ce trebuie conectat

Din cerere deduc platformele/canalele, acțiunile (citește, scrie, trimite) și volumul. Dacă lipsește ceva esențial, pun o singură întrebare (AskUserQuestion), nu mai multe.

## 2. Ce date trec prin automatizare

Decide cât de strict e verdictul:
- **Fără date personale sau confidențiale** (ex. poze de legume, texte publice) → orice furnizor e acceptabil; contează calitatea și costul.
- **Date personale sau confidențiale** (clienți finali, emailuri, apeluri, produse nelansate) → doar furnizorii cu verdict „OK" din `reference/compliance.md`, respectând condițiile lor.

Întreb doar dacă nu reiese din cerere.

## 3. Ce am deja

Verific, în ordine: tool-urile MCP din sesiune (conectate sau în lista celor care cer autentificare), apoi tabelele „Tools" din `my-context/profile.md` și `team/profile.md`.

## 4. Caut conectorul

1. **Registry**: încarc cu ToolSearch `mcp__mcp-registry__search_mcp_registry` și `mcp__mcp-registry__suggest_connectors` și caut după platformă.
2. **Fără conector** → API oficial. Citesc documentația oficială acum (WebSearch/WebFetch), nu din memorie: limite, aprobări (ex. App Review), costuri.
3. **Fără API utilizabil** → fallback generic: IMAP/SMTP pentru email, webhook, Zapier/Make ca adaptor.
4. `playbooks/` conține note mai vechi, scrise din cunoștințe generale și nevalidate pe clienți reali. Le folosesc ca idei, nu ca adevăr; unde contrazic documentația oficială sau `reference/compliance.md`, au prioritate acestea.

## 5. Compliance

Caut furnizorul în `reference/compliance.md`.
- E acolo și rândul are mai puțin de 6 luni → îl folosesc și spun userului data verificării.
- Lipsește sau e vechi → cercetez din surse oficiale (trust center, DPA, termeni API, retenție, antrenare pe date, rezidență UE) și actualizez rândul cu data și sursa. Ce nu pot citi marchez „neverificat"; nu completez din memorie.
- Reamintesc mereu: orice LLM din lanț (inclusiv Claude) trebuie adăugat în DPA-ul clientului; consimțământul pentru înregistrări e al agenției.

## 6. Propun

Listă scurtă: nevoie → conector → stare (conectat / de autorizat / de instalat / API direct / fallback) → verdict de compliance și capcana principală → ce trebuie să facă userul. Apoi AskUserQuestion multiSelect: ce conectez acum?

## 7. Reguli de siguranță

- Nu instalez nimic fără OK explicit (instalarea unui MCP schimbă configurarea).
- OAuth îl face userul în browser. Nu cer niciodată tokeni, parole sau coduri de autorizare în chat.
- Chei API: userul le pune în `.env`; eu adaug doar placeholder-ul în `.env` și `.env.example`.
- Acțiuni cu efect real (trimis mesaje, postat) doar după confirmare.

## 8. După implementare

Dacă soluția a funcționat pe un caz real: actualizez rândul din `reference/compliance.md` cu ce am aflat și propun (nu creez singur) un playbook, conform `reference/skills-and-playbooks.md`.
