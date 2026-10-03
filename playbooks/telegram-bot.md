# Telegram — bot de automatizare

## Cerere tipică de client
"Vreau un bot pe Telegram", "automatizare rapidă fără aprobări complicate", "un chat-bot ca la WhatsApp dar mai simplu".

## Ce presupune tehnic
- **Platformă/API oficial:** Telegram Bot API — cel mai simplu din toate playbook-urile de mesagerie: fără cont de business, fără aprobare de platformă, funcțional în minute.
- **Cont necesar:** doar un cont Telegram (al clientului sau al nostru) care creează botul prin **@BotFather**.
- **Conector/MCP disponibil:** verific `mcp-registry` — Telegram are integrări MCP relativ comune; dacă nu găsesc una potrivită, se lucrează direct pe Bot API (REST, foarte simplu).

## Setup per client
1. Deschid conversație cu **@BotFather** în Telegram, comanda `/newbot`, aleg nume + username (trebuie să se termine în `bot`).
2. BotFather întoarce un **token** — se stochează ca secret, niciodată în cod/git.
3. Configurez fie **webhook** (`setWebhook`, URL propriu HTTPS) fie **long polling** (mai simplu de testat local, dar necesită un proces mereu pornit).
4. Botul e găsit de useri prin username-ul lui (`t.me/numebot`) — clientul îl promovează pe canalele lui.
5. Pentru bot pe un **grup/canal**, clientul trebuie să-l adauge manual și să-i dea drepturile necesare (ex. admin dacă trebuie să modereze).

## Abordare de implementare
1. Update-uri (mesaje) vin prin webhook sau polling.
2. LLM clasifică intenția și răspunde direct pentru FAQ/comenzi predefinite (Telegram suportă și `/comenzi` native, bune pentru acțiuni structurate: `/comanda`, `/status`, `/contact`).
3. Escaladare la om pentru orice ambiguu, prin transfer de context (nu doar "vorbește cu un operator").
4. Trimitere răspuns prin `sendMessage` (Bot API).

## Limitări/riscuri cunoscute
- **Foarte puține limitări de platformă** comparativ cu Instagram/WhatsApp — nu există fereastră de 24h, nu există aprobare de template, rate limit e generos (relevant doar la volum foarte mare).
- Botul nu poate iniția conversație cu cineva care nu i-a scris deja primul (regulă generală anti-spam) — de comunicat clientului: promovarea link-ului `t.me/...` e responsabilitatea lui.
- Fără verificare de identitate business — mai puțin potrivit pentru clienți care au nevoie de badge/verificare oficială (acolo Instagram/WhatsApp Business sunt varianta corectă).

## Ultima actualizare
2026-09-21
