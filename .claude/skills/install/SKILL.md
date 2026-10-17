---
name: install
description: Setup inițial (onboarding) al spațiului de lucru - află cine e userul, echipa, proiectele și tool-urile folosite, conectează MCP-urile potrivite, generează my-context/ din templates/ și deschide dashboard-ul pe un live server. Folosește-l când userul scrie /install, cere setup/onboarding/reset, sau automat când my-context/profile.md nu există.
---

# /install — onboarding

`my-context/` poate fi complet gol sau poate lipsi cu totul (clone proaspăt, reset manual) — e o stare validă, nu o eroare. Tot ce e în el se generează din `templates/` la finalul acestui flux.

Dacă `my-context/profile.md` **există deja** când userul rulează /install explicit: întreabă (AskUserQuestion) dacă vrea să completeze contextul existent (reia doar secțiunile lipsă/învechite) sau să-l refacă de la zero. Nu șterge nimic fără confirmare explicită; la „de la zero" șterge doar `profile.md`, `TASKS.md`, `people/`, `projects/`, `context/`, `skills/` — niciodată `assets/`.

## 1. Bun venit

Deschide cu un mesaj de bun venit — nu tehnic, nu „nu găsesc fișierul X". Ceva de genul (adaptează liber tonul, dar păstrează structura: salut, cadrul primei interacțiuni, de ce contează, ce urmează):

> Salut! Aceasta e prima noastră interacțiune, așa că înainte să te ajut concret aș vrea să te cunosc puțin — pe ce lucrezi, cu cine, ce ai pe agendă acum și ce tool-uri folosești. Durează doar câteva minute, iar tot ce îmi spui rămâne strict pe acest calculator, privat — nu se trimite, publică sau distribuie nicăieri. Odată setat, o să pot ține pasul cu contextul tău de la o discuție la alta, fără să reiei mereu aceleași explicații.

## 2. Nu scrie nimic pe disc încă

Adună întâi toate răspunsurile; fișierele se generează toate la final (pasul 4), ca un onboarding întrerupt să nu lase `my-context/` pe jumătate populat (un `profile.md` existent ar opri onboarding-ul automat în sesiunea următoare).

## 3. Întrebări ghidate

Secvență scurtă de întrebări **ghidate**, cu AskUserQuestion, în locul unor întrebări deschise gen "spune-mi tot despre X". Regula de bază: AskUserQuestion se folosește acolo unde răspunsul are variante reale, discrete, de bun-simț (nu inventa opțiuni artificiale gen "îți spun eu / sar peste" — tool-ul oferă deja automat "Other" pentru răspuns liber, nu-l duplica ca opțiune separată). Pentru lucruri intrinsec deschise (nume de proiect, nume de oameni, descrieri libere), pune întrebarea normal, conversațional, fără AskUserQuestion.

**Nu dicta niciodată cuvântul exact de răspuns** — gen "dacă nu, spune 'nu'" sau "dacă nu mai ai nimic, scrie 'nimic'". Userul știe română, orice răspuns negativ ("nu", "nu am", "nimic", "gata", "atât") se înțelege fără să i se dea cuvântul pe tavă. Pentru orice buclă de continuare ("mai ai și alte X?") — proiecte, oameni, tool-uri — folosește **întotdeauna AskUserQuestion cu opțiuni Da/Nu** (are deja exemple mai jos), niciodată o întrebare liberă combinată cu instrucțiunea "dacă nu, scrie X". Dacă simți nevoia să specifici ce să scrie userul la un "nu", e semn că întrebarea aia ar trebui să fie AskUserQuestion, nu text liber.

AskUserQuestion permite maxim 4 opțiuni + "Other" per întrebare — pentru categorii cu mai multe variante plauzibile (ex. domeniu), nu înghesui totul într-o singură întrebare; fă drill-down în 2 pași: întâi o categorie mare (max 4 opțiuni), apoi o a doua AskUserQuestion cu opțiuni specifice ramurii alese (tot max 4, adaptate la răspunsul de la pasul 1).

Nu bombarda userul cu tot deodată — 1 AskUserQuestion sau 1 întrebare liberă pe rând, cu multiSelect unde are sens:

- **Nume** (întrebare liberă, prima din secvență): "Cum ai vrea să-ți spun?" — numele sau prescurtarea cu care se prezintă devine modul standard de adresare de acum încolo, salvat la „Me" în profile.md. Cine rulează install-ul este **primul owner** al contextului firmei: citești emailul lui de lucru din configurarea Git (`git config user.email`; dacă lipsește, îl întrebi: „Care e emailul tău de lucru?"), îl notezi la „Me" cu `Poate face push: da`, fără să explici termeni tehnici.
- **Domeniu — pasul 1** (AskUserQuestion, 4 opțiuni reale — NU adăuga o a 5-a opțiune gen "Altceva", tool-ul oferă deja "Other" cu exact acest rol): Tehnic/Engineering, Business (Product/Vânzări/Marketing), Operațional/Suport (HR/Legal/Finance), Producție/Servicii directe (ex. sănătate, educație, producție, construcții, retail).
- **Domeniu — pasul 2** (AskUserQuestion, opțiuni condiționate de răspunsul de la pasul 1; dacă userul a răspuns prin "Other" la pasul 1, sari peste pasul 2 — folosește direct ce a scris):
  - Dacă Tehnic: Software Development, Infrastructură/DevOps, Data/Analytics, QA/Security.
  - Dacă Business: Product Management, Vânzări/Business Development, Marketing, Customer Success.
  - Dacă Operațional/Suport: HR, Legal/Compliance, Finance, Operațiuni generale.
  - Dacă Producție/Servicii directe: Sănătate, Educație, Producție/Manufacturing, Construcții/Retail/Altele — și tot prin "Other" cine nu se regăsește.
- **Rol/scop** (AskUserQuestion): ex. Lucrez individual, Coordonez o echipă, Coordonez mai multe echipe/proiecte, Rol de management fără coordonare tehnică directă.
- **Mărime echipă** (AskUserQuestion, doar dacă Rol/scop nu a fost "Lucrez individual"): ex. 2-5 oameni, 6-15 oameni, Peste 15 oameni, Variază după proiect. Pusă imediat după Rol/scop, cât timp subiectul echipei e "cald".
- **Oameni cheie** (imediat după Mărime echipă, doar dacă nu lucrează individual) — câte o persoană pe rând, nu toate într-un mesaj bulk:
  1. "Cum o cheamă pe prima persoană cu care lucrezi des?" (doar numele)
  2. "Care e rolul ei?"
  3. "Pe ce anume lucrează sau cu ce te ajută?"
  4. "Ai și emailul ei la îndemână? E opțional, dar util dacă va trebui vreodată să-i trimiți un mesaj direct din context."
  5. AskUserQuestion (Da / Nu): "Poate [nume] să modifice și să publice contextul firmei pentru toată echipa?" Doar cei cu Da vor putea publica (owner-i); ceilalți citesc și lucrează local. Dacă Da, emailul ei de lucru e obligatoriu (e cel cu care se recunoaște ca owner): cere-l dacă lipsește.
  6. AskUserQuestion: "Mai sunt și alți oameni cheie de adăugat?" (Da / Nu, oprește-te după max. 5-6 persoane chiar dacă răspunde Da în continuare — restul pot fi adăugate ulterior, incremental) — dacă Da, repetă 1-5.
- **Proiect(e) principal(e)** — sparge în întrebări mici, punctuale, fiecare cerând explicit UN singur lucru:
  1. "Cum se numește proiectul/produsul principal la care lucrezi acum?" (doar numele)
  2. "Ai cumva vreo documentație scurtă pe acest proiect (README, notițe, spec) pe care ai putea s-o lipești aici? Dacă da, o citesc și extrag ce trebuie direct din ea — sari peste restul întrebărilor pentru acest proiect. Dacă nu ai la îndemână, continuăm cu 2-3 întrebări rapide." Dacă lipește text/link/fișier, extrage descrierea, rolul (dacă reiese) și termenii cheie, apoi confirmă pe scurt ce ai înțeles — nu mai pune 3-5 separat.
  3. Dacă nu are documentație: "Pe scurt, în 1-2 fraze, ce face acest proiect/produs?"
  4. Dacă nu are documentație: "Care e rolul tău concret pe el?"
  5. Dacă nu are documentație: "Sunt acronime sau termeni interni cheie pe care ar trebui să-i știu (ex. nume de coduri, prescurtări)?"
  6. AskUserQuestion: "Mai ai și alte proiecte active pe care ar trebui să le știu?" (Da / Nu) — dacă Da, repetă 1-5.
- **Tool-uri folosite** — ca să știu ce MCP-uri/conectori să instalez:
  1. AskUserQuestion, multiSelect: "Ce tipuri de tool-uri folosești în munca de zi cu zi?" — Email & calendar, Chat & comunicare, Task-uri & proiecte, Documente & cod.
  2. Un singur apel AskUserQuestion cu câte o întrebare multiSelect pentru fiecare categorie bifată (max 4 întrebări):
     - Email & calendar: Gmail, Google Calendar, Outlook / Microsoft 365.
     - Chat & comunicare: Slack, Microsoft Teams, Google Chat.
     - Task-uri & proiecte: Jira / Confluence, Linear, Asana / ClickUp / Monday, Notion.
     - Documente & cod: Google Drive, SharePoint / OneDrive, GitHub / GitLab, Figma.
- **Canale de business** — diferit de întrebarea de mai sus (aia e despre tool-urile TALE de productivitate; asta e despre businessul tău). Procesele manuale concrete NU se întreabă aici: le preia `/process` după install.
  1. AskUserQuestion, multiSelect: "Prin ce canale interacționează businessul tău cu clienții?" — Instagram/Facebook, WhatsApp, Email/Telefon/SMS, Magazin online (Shopify/WooCommerce/altul).
  2. Pentru fiecare canal bifat, verific `playbooks/` după o rețetă potrivită (fără să construiesc nimic acum) — le notez la pasul 4 în tabelul „Automation opportunities" din profile.md, cu playbook-ul găsit (sau "fără playbook încă" dacă nu există unul).
- **Stil de comunicare** (AskUserQuestion): ex. Concis și la obiect, Detaliat cu context, Mix RO/EN natural.

## 4. Generează fișierele

Toate pornind din `templates/` (creează folderele `my-context/`, `my-context/people/`, `my-context/projects/`, `my-context/skills/` dacă lipsesc):

- `my-context/people/<slug>.md` din `templates/people/_person.template.md` — **câte unul pentru fiecare om cheie** (slug kebab-case, ex. `elena-man.md`), cu Rol, Email (dacă a fost dat), Poate face push (da/nu, din răspunsul de la pasul 3), Lucrează pe `[[slug-proiect]]`. Obligatoriu: tab-urile Oameni/Echipă din dashboard citesc doar din acest folder.
- `my-context/projects/<slug>.md` din `templates/projects/_project.template.md` — **câte unul pentru fiecare proiect**, cu descrierea, rolul userului, echipa (`[[slug-persoană]]`) și termenii cheie. Obligatoriu (tab-ul Proiecte).
- `my-context/TASKS.md` din `templates/TASKS.template.md`, **gol** (nu întrebăm de task-uri la install; se adaugă ulterior cu `/planning` sau din conversație).
- `my-context/skills/` rămâne gol — se populează pe măsură ce lucrăm pe task-uri (vezi `reference/skills-and-playbooks.md`).
- `my-context/context/*.md` și `my-context/glossary.md` NU se creează acum — doar ulterior, când apare context stabil suficient de bogat.
- **Ultimul** fișier scris: `my-context/profile.md`, din `templates/profile.template.md`, inclusiv emailul și `Poate face push: da` ale celui care instalează (la „Me"), secțiunea Tools (status inițial „de conectat" pentru fiecare tool ales) și secțiunea Automation opportunities (canalele de la pasul 3, cu playbook-ul potrivit găsit sau "fără playbook încă"). Link-urile `[[slug]]` din tabele trebuie să corespundă exact numelor fișierelor create mai sus. Fiind scris ultimul, existența lui marchează un onboarding complet.
- Asigură-te că `my-context/assets/.gitkeep` există.

## 5. Conectează tool-urile (MCP)

Pentru fiecare tool ales la pasul 3:

1. Verifică dacă e deja disponibil în sesiune (există tool-uri MCP pentru el, sau apare în lista de servere care cer autentificare). Dacă da → marchează „conectat" sau „de autorizat".
2. Altfel, caută conectorul oficial cu tool-urile de registry (`mcp__mcp-registry__search_mcp_registry` / `mcp__mcp-registry__suggest_connectors` — încarcă-le cu ToolSearch dacă sunt deferred).
3. Arată userului o listă scurtă: tool → conector găsit → status (conectat / de autorizat / de instalat / nu există conector). Apoi AskUserQuestion multiSelect: pe care să le conectez acum? Instalarea unui MCP e o schimbare de configurare — nu instala nimic fără OK explicit.
4. Pentru cele alese: conectorii claude.ai se adaugă prin cardul de sugestie / Settings → Connectors; serverele locale cu `claude mcp add` (scope user). Autentificarea (OAuth) o face userul în browser — **nu cere niciodată tokeni, parole sau coduri de autorizare**.
5. Actualizează coloana de status din secțiunea Tools din `my-context/profile.md`.

Dacă userul vrea să sară peste acest pas, notează tool-urile ca „de conectat" și mergi mai departe — se poate relua oricând.

## 6. Pornește dashboard-ul

Urmează secțiunea „Pornire dashboard" din `reference/dashboard.md` (instalează `live-server` dacă lipsește, îl pornește și deschide `dashboard.html` în browser). Apoi spune-i userului, pe scurt: în dashboard, o singură dată, Setări → „📁 Conectează folder" și alege folderul proiectului; dacă browserul oferă „Permite la fiecare vizită", să aleagă asta, ca pagina să se reîncarce singură cu datele noi.

## 7. Publicarea contextului pe GitHub (doar owner-ul care instalează)

Hook-ul `.claude/hooks/sync-context.sh` publică automat contextul firmei, dar doar dacă `my-context/` nu mai e ignorat de Git. Ca să-l activezi:

1. AskUserQuestion (Da / Mai târziu): „Vrei ca firma ta să păstreze contextul într-un spațiu comun, ca toată echipa să-l aibă la zi? Îl pot publica automat, dar doar cei care au voie să-l modifice." La „Mai târziu" treci peste tot pasul; se poate relua oricând.
2. Dacă Da: verifică `git remote get-url origin`.
   - Lipsește → spune că firma are nevoie de un spațiu comun **privat** al ei și oferă să-l creez (cu `gh repo create --private`), dar numai după confirmare explicită; nu publici nimic fără ea.
   - Există → arată-i adresa și întreabă dacă e spațiul comun al firmei ei, nu al șablonului (AskUserQuestion Da / Nu). Dacă e al șablonului, nu activa nimic și explică-i să-și creeze unul propriu.
3. După confirmare, editează `.gitignore`: înlocuiește regulile care ignoră `/my-context/*` și `/team/*` (cu excepțiile lor) cu doar `/my-context/assets/*` și `!/my-context/assets/.gitkeep` (assets/ rămâne în afara Git; se va lega ulterior de un Google Drive). Păstrează ignorat și `/my-context/TASKS.md` (task-urile sunt personale, fiecare își are fișierul lui) și `.env`. Dacă `my-context/TASKS.md` era deja urmărit de Git, scoate-l din urmărire fără să-l ștergi de pe disc: `git rm --cached --ignore-unmatch my-context/TASKS.md`.
4. Nu face tu primul push; hook-ul îl face la finalul turei, doar pentru owner-i (vezi `reference/sync-conflicts.md`). Spune-i userului pe scurt că de acum contextul se salvează singur și că membrii fără drept de publicare lucrează doar local.

## 8. Confirmare și pasul următor

Install-ul se încheie când tot contextul despre user, business și echipă e în proiect (profil, oameni, proiecte, tool-uri). Nu mai întreba de task-uri și nu începe alte lucruri.

Confirmă în termeni de business, nu tehnici — NU menționa git, gitignore, ce fișiere există pe disc sau alte detalii de implementare. Rezumat: ce ai reținut (rol, echipă, proiecte), câți oameni și proiecte ai adăugat, ce tool-uri sunt conectate și care mai trebuie autorizate. Dacă la pasul 3 au ieșit canale cu playbook potrivit, menționează-le ca oportunități de automatizare. Menționează că pagina „Comenzi" din dashboard explică comenzile disponibile.

**Pasul următor: `/process`.** Încheie sugerând-o, în termeni de business: „Contextul e gata. Următorul pas e să-mi povestești un lucru pe care îl faci manual în munca de zi cu zi; îl pot automatiza eu." Apoi AskUserQuestion: „Începem acum cu primul proces?" (Da / Mai târziu). Dacă Da, invocă skill-ul `process` direct, fără să mai aștepți altă cerere. Dacă Mai târziu, spune că îl pornește oricând scriind `/process`.

Onboarding-ul nu trebuie să fie exhaustiv din prima — poate fi completat incremental în sesiuni viitoare.
