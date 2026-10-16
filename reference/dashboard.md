# Dashboard

Încărcat la cerere din CLAUDE.md: citesc acest fișier când userul cere dashboard-ul, sau la finalul `/install`.

## Ce e

`dashboard.html` — pur HTML+JS, citește direct fișierele; servit de live server. **Strict read-only** — nu are niciun buton de adăugat/șters/editat/mutat (inclusiv drag-and-drop), iar folderul e conectat cu permisiune doar de citire la nivel de browser. Orice modificare o fac eu, în sesiune, editând fișierele `.md`. În dashboard, conectarea se face o singură dată din Settings → „📁 Conectează folder" (se alege folderul rădăcină al proiectului, cel cu CLAUDE.md) — de acolo se încarcă automat tot: task-uri, recurente, oameni, proiecte.

Pagina „Comenzi" din dashboard (secțiunea `commandsPanel` din `dashboard.html`) e legenda comenzilor, pe înțelesul userului — când adaug/modific o comandă, actualizez și acea pagină.

## Pornire dashboard

Dashboard-ul se servește dintr-un live server (reîncarcă pagina singur când se schimbă fișierele). Îl pornesc la finalul `/install` sau oricând userul cere dashboard-ul:
```bash
command -v live-server >/dev/null || npm install -g live-server   # dacă lipsește și npm: cer OK pentru `brew install node`
lsof -nP -iTCP:5500 -sTCP:LISTEN >/dev/null || nohup live-server --port=5500 --host=127.0.0.1 --no-browser . > /tmp/aispace-live-server.log 2>&1 &
open -a "Google Chrome" "http://127.0.0.1:5500/dashboard.html" 2>/dev/null || open "http://127.0.0.1:5500/dashboard.html"
```
Rulat din rădăcina proiectului. Chrome/Edge sunt necesare — conectarea folderului folosește File System Access API, pe care Safari/Firefox nu o au. Dacă portul 5500 e ocupat de altceva decât live-server-ul nostru, folosesc 5501.
