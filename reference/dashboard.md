# Dashboard

Încărcat la cerere din CLAUDE.md: citesc acest fișier când userul cere dashboard-ul, sau la finalul `/install`.

## Ce e

`dashboard.html` — pur HTML+JS, citește direct fișierele; servit de live server. **Strict read-only** — nu are niciun buton de adăugat/șters/editat/mutat (inclusiv drag-and-drop), iar folderul e conectat cu permisiune doar de citire la nivel de browser. Orice modificare o fac eu, în sesiune, editând fișierele `.md`. În dashboard, conectarea se face o singură dată din Settings → „📁 Conectează folder" (se alege folderul rădăcină al proiectului, cel cu CLAUDE.md) — de acolo se încarcă automat tot: task-uri, recurente, oameni, proiecte.

Pagina „Comenzi" din dashboard (secțiunea `commandsPanel` din `dashboard.html`) e legenda comenzilor, pe înțelesul userului — când adaug/modific o comandă, actualizez și acea pagină.

## Pornire dashboard

Dashboard-ul se servește dintr-un live server (reîncarcă pagina singur când se schimbă fișierele). Îl pornesc la finalul `/install` sau oricând userul cere dashboard-ul:
```bash
command -v live-server >/dev/null || npm install -g live-server   # dacă lipsește și npm: cer OK pentru `brew install node`
lsof -nP -iTCP:5500 -sTCP:LISTEN >/dev/null || nohup live-server --port=5500 --host=127.0.0.1 --no-browser --ignore=explorer/live . > /tmp/aispace-live-server.log 2>&1 &
open -a "Google Chrome" "http://127.0.0.1:5500/dashboard.html" 2>/dev/null || open "http://127.0.0.1:5500/dashboard.html"
```
Rulat din rădăcina proiectului. `--ignore=explorer/live` e obligatoriu: hook-ul biroului 3D rescrie acolo starea sesiunilor la fiecare pas, iar fără el live-server ar reîncărca dashboard-ul continuu. Chrome/Edge sunt necesare — conectarea folderului folosește File System Access API, pe care Safari/Firefox nu o au. Dacă portul 5500 e ocupat de altceva decât live-server-ul nostru, folosesc 5501.

## Tab-ul „Birou" (biroul 3D)

`explorer/index.html`, afișat în tab-ul „Birou" (iframe încărcat la prima deschidere; merge și deschis direct). Arată sistemul ca un birou 3D: camerele sunt legate de structura proiectului (camera firmei, numită după firmă → `team/` + `my-context/`, cu Documentele (`my-context/assets/`), Echipa și Seiful (`.env`) în ea, plus un hol liber spre conectori; Foundation Skills → skill-urile venite cu șablonul, din `.claude/skills/`; Custom Skills → skill-urile firmei (`team/skills/`, `my-context/skills/`, plus ce e în `.claude/skills/` dar nu în `.claude/template-manifest.txt`); fiecare cameră de skill-uri are un dulap cu sertare de hooks (din `.claude/settings.json`; Foundation = scripturile venite cu șablonul, Custom = ale firmei sau din `settings.local.json`; descrierea vine din linia `# Pe scurt:` a scriptului); Recepția → `CLAUDE.md`, cabina Internet (căutări web, pagini, browser), camera Routines, în dreapta-față a biroului (taskurile programate din aplicația Claude și routines-urile din cloud; programul vine din `explorer/live/routines.json`, scris de hook-ul PostToolUse după ce Claude le listează), plus poarta de siguranță, GitHub și șablonul). Fiecare sesiune Claude Code deschisă în proiect apare ca robot care merge în camera în care lucrează. Pagina se deschide pe „Cum fac": ghiduri pas cu pas (lista `GUIDES` din `explorer/index.html`); un pas apăsat luminează camera în care se întâmplă. Când adaug sau schimb o comandă, actualizez și ghidul ei. Al treilea mod, „Vezi cum merge", are scene animate (lista `SCENES`): un robot „exemplu" și bilețele galbene arată pas cu pas cum lucrează sistemul (întrebare, skill, document nou, cheie oprită la poartă, sync la coleg, versiune nouă).

Date: biroul citește **direct folderul proiectului** conectat în dashboard (același acces, din IndexedDB `productivity-dashboard`/`handles`/`memoryDir`, sau primit de la dashboard prin `postMessage`), la 5 secunde: firma, echipa, cunoștințele, skill-urile, hook-urile, documentele, seiful. Ce e în afara folderului vine din hook. Fără permisiune de citire, biroul arată un buton care o cere. Hook-ul `.claude/hooks/explorer-live.py` (înregistrat în `.claude/settings.json` pe SessionStart, UserPromptSubmit, PreToolUse, Notification, Stop, SessionEnd) scrie `explorer/live/live.js` (sesiunile) și, la SessionStart și Stop, `explorer/live/data.js` (skill-uri, fișiere, echipă). Tot el adună conectorii (zona „Conectori", în stânga biroului): `.mcp.json` din proiect, `~/.claude.json` (ai tăi și cei claude.ai), MCP-urile pluginurilor active, plus ce a fost folosit (`explorer/live/connectors-used.json`). Scrie doar numele, sursa și tipul, niciodată url-uri, comenzi, argumente sau chei. Folderul e în `.gitignore`. Deocamdată doar Claude (Anthropic); 3D-ul vine din CDN (Three.js 0.170.0), deci are nevoie de internet. Regenerare manuală a datelor: `python3 .claude/hooks/explorer-live.py --data < /dev/null`.

## Tab-ul „Conectori"

Lista conectorilor (MCP-uri, conectori claude.ai, MCP-urile pluginurilor), grupați după sursă, cu logo, tip și când au fost folosiți ultima dată. Citește aceleași date ca biroul 3D, `explorer/live/data.js` (scris de `.claude/hooks/explorer-live.py`), reîncărcate la 20 de secunde cât timp tab-ul e deschis. Ruta: `#/connectors`.
