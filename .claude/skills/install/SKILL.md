---
name: install
description: Setup inițial (onboarding) al spațiului de lucru - află cine e userul, echipa, proiectele, task-urile și tool-urile folosite, conectează MCP-urile potrivite, generează my-context/ din templates/ și deschide dashboard-ul pe un live server. Folosește-l când userul scrie /install, cere setup/onboarding/reset, sau automat când my-context/profile.md nu există.
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

**Nu dicta niciodată cuvântul exact de răspuns** — gen "dacă nu, spune 'nu'" sau "dacă nu mai ai nimic, scrie 'nimic'". Userul știe română, orice răspuns negativ ("nu", "nu am", "nimic", "gata", "atât") se înțelege fără să i se dea cuvântul pe tavă. Pentru orice buclă de continuare ("mai ai și alte X?") — task-uri, proiecte, oameni, rutine — folosește **întotdeauna AskUserQuestion cu opțiuni Da/Nu** (are deja exemple mai jos), niciodată o întrebare liberă combinată cu instrucțiunea "dacă nu, scrie X". Dacă simți nevoia să specifici ce să scrie userul la un "nu", e semn că întrebarea aia ar trebui să fie AskUserQuestion, nu text liber.

AskUserQuestion permite maxim 4 opțiuni + "Other" per întrebare — pentru categorii cu mai multe variante plauzibile (ex. domeniu), nu înghesui totul într-o singură întrebare; fă drill-down în 2 pași: întâi o categorie mare (max 4 opțiuni), apoi o a doua AskUserQuestion cu opțiuni specifice ramurii alese (tot max 4, adaptate la răspunsul de la pasul 1).

Nu bombarda userul cu tot deodată — 1 AskUserQuestion sau 1 întrebare liberă pe rând, cu multiSelect unde are sens:

- **Nume** (întrebare liberă, prima din secvență): "Cum ai vrea să-ți spun?" — numele sau prescurtarea cu care se prezintă devine modul standard de adresare de acum încolo, salvat la „Me" în profile.md.
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
  5. AskUserQuestion: "Mai sunt și alți oameni cheie de adăugat?" (Da / Nu, oprește-te după max. 5-6 persoane chiar dacă răspunde Da în continuare — restul pot fi adăugate ulterior, incremental) — dacă Da, repetă 1-4.
- **Proiect(e) principal(e)** — sparge în întrebări mici, punctuale, fiecare cerând explicit UN singur lucru:
  1. "Cum se numește proiectul/produsul principal la care lucrezi acum?" (doar numele)
  2. "Ai cumva vreo documentație scurtă pe acest proiect (README, notițe, spec) pe care ai putea s-o lipești aici? Dacă da, o citesc și extrag ce trebuie direct din ea — sari peste restul întrebărilor pentru acest proiect. Dacă nu ai la îndemână, continuăm cu 2-3 întrebări rapide." Dacă lipește text/link/fișier, extrage descrierea, rolul (dacă reiese) și termenii cheie, apoi confirmă pe scurt ce ai înțeles — nu mai pune 3-5 separat.
  3. Dacă nu are documentație: "Pe scurt, în 1-2 fraze, ce face acest proiect/produs?"
  4. Dacă nu are documentație: "Care e rolul tău concret pe el?"
  5. Dacă nu are documentație: "Sunt acronime sau termeni interni cheie pe care ar trebui să-i știu (ex. nume de coduri, prescurtări)?"
  6. AskUserQuestion: "Mai ai și alte proiecte active pe care ar trebui să le știu?" (Da / Nu) — dacă Da, repetă 1-5.
- **Task-uri curente** — câte un task pe rând:
  1. "Ce ai pe agendă acum? Dă-mi primul lucru."
  2. "Are un termen limită (due date)?"
  3. "Cine e responsabil — tu, sau altcineva din echipă?" (dacă a menționat deja un nume, doar confirmă)
  4. Dacă e ceva care se repetă periodic (o instrucțiune permanentă — ex. "verifică emailurile în fiecare zi la 10:00"), marchează-l ca recurent și notează intervalul exact; altfel e un task normal cu due date.
  5. Notează intern (nu întrerupe secvența acum) dacă task-ul pare ceva ce ai putea face tu direct (scris, research, draft, cod, diagramă, procesare fișier) — le semnalezi grupat la pasul 7 (Confirmare), nu pe rând aici.
  6. AskUserQuestion: "Mai ai și alte task-uri de adăugat acum?" (Da / Nu, max. 5-6) — dacă Da, repetă 1-5.
  Nu întreba aici despre modul de lucru pe fiecare task — asta se întreabă la momentul execuției (vezi `reference/task-workflow.md`), ca onboarding-ul să rămână scurt.
- **Rutine** — întrebare separată, explicită, nu doar sub-pas la task-urile curente (oamenii gândesc diferit „ce am de făcut" de „ce fac regulat" și uită des să menționeze rutinele dacă nu sunt întrebați punctual):
  1. "Ai vreo rutină sau verificare care se repetă (zilnic, săptămânal, lunar)? De ex. verificare emailuri la o oră fixă, raport săptămânal, backup, monitorizare a ceva."
  2. Pentru fiecare rutină descrisă: notează intervalul exact (ex. "zilnic la 10:00", "lunea dimineața") și adaug-o ca task recurent (vezi formatul `(recurrent: ...)` din `reference/task-workflow.md`) — ajunge automat în subtab-ul „🔁 Recurente" din dashboard, nu se amestecă cu task-urile punctuale.
  3. AskUserQuestion: "Mai ai și alte rutine de adăugat?" (Da / Nu) — dacă Da, repetă 1-2.
- **Tool-uri folosite** — ca să știu ce MCP-uri/conectori să instalez:
  1. AskUserQuestion, multiSelect: "Ce tipuri de tool-uri folosești în munca de zi cu zi?" — Email & calendar, Chat & comunicare, Task-uri & proiecte, Documente & cod.
  2. Un singur apel AskUserQuestion cu câte o întrebare multiSelect pentru fiecare categorie bifată (max 4 întrebări):
     - Email & calendar: Gmail, Google Calendar, Outlook / Microsoft 365.
     - Chat & comunicare: Slack, Microsoft Teams, Google Chat.
     - Task-uri & proiecte: Jira / Confluence, Linear, Asana / ClickUp / Monday, Notion.
     - Documente & cod: Google Drive, SharePoint / OneDrive, GitHub / GitLab, Figma.
- **Canale de business & procese repetitive** — diferit de întrebarea de mai sus (aia e despre tool-urile TALE de productivitate; asta e despre businessul tău, ca să identific din start ce se poate automatiza — vezi `playbooks/`):
  1. AskUserQuestion, multiSelect: "Prin ce canale interacționează businessul tău cu clienții?" — Instagram/Facebook, WhatsApp, Email/Telefon/SMS, Magazin online (Shopify/WooCommerce/altul).
  2. "Ai vreun proces repetitiv, consumator de timp, pe care ți-ar plăcea să-l automatizăm? (ex. răspuns la mesaje repetitive, status comenzi, remindere, recenzii)" — întrebare liberă, poate răspunde și "nu, nimic acum".
  3. Pentru fiecare canal bifat sau proces descris, verific `playbooks/` după o rețetă potrivită (fără să construiesc nimic acum) — le notez la pasul 4 în tabelul „Automation opportunities" din profile.md, cu playbook-ul găsit (sau "fără playbook încă" dacă nu există unul).
- **Stil de comunicare** (AskUserQuestion): ex. Concis și la obiect, Detaliat cu context, Mix RO/EN natural.

## 4. Generează fișierele

Toate pornind din `templates/` (creează folderele `my-context/`, `my-context/people/`, `my-context/projects/`, `my-context/skills/` dacă lipsesc):

- `my-context/people/<slug>.md` din `templates/people/_person.template.md` — **câte unul pentru fiecare om cheie** (slug kebab-case, ex. `elena-man.md`), cu Rol, Email (dacă a fost dat), Lucrează pe `[[slug-proiect]]`. Obligatoriu: tab-urile Oameni/Echipă din dashboard citesc doar din acest folder.
- `my-context/projects/<slug>.md` din `templates/projects/_project.template.md` — **câte unul pentru fiecare proiect**, cu descrierea, rolul userului, echipa (`[[slug-persoană]]`) și termenii cheie. Obligatoriu (tab-ul Proiecte).
- `my-context/TASKS.md` din `templates/TASKS.template.md`, populat cu task-urile adunate (formatul din `reference/task-workflow.md`, pe care îl citesc înainte să scriu), cu ID-uri `AS-1`, `AS-2`, … în ordine.
- `my-context/skills/` rămâne gol — se populează pe măsură ce lucrăm pe task-uri (vezi `reference/skills-and-playbooks.md`).
- `my-context/context/*.md` și `my-context/glossary.md` NU se creează acum — doar ulterior, când apare context stabil suficient de bogat.
- **Ultimul** fișier scris: `my-context/profile.md`, din `templates/profile.template.md`, inclusiv secțiunea Tools (status inițial „de conectat" pentru fiecare tool ales) și secțiunea Automation opportunities (canalele/procesele de la pasul 3, cu playbook-ul potrivit găsit sau "fără playbook încă"). Link-urile `[[slug]]` din tabele trebuie să corespundă exact numelor fișierelor create mai sus. Fiind scris ultimul, existența lui marchează un onboarding complet.
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

## 7. Confirmare

Confirmă că setup-ul e gata, în termeni de business, nu tehnici — NU menționa git, gitignore, ce fișiere există pe disc sau alte detalii de implementare. Rezumat: ce ai reținut (rol, echipă, proiecte), câți oameni și proiecte ai adăugat, câte task-uri sunt notate, ce tool-uri sunt conectate și care mai trebuie autorizate. Dacă la pasul 3 au ieșit canale/procese cu playbook potrivit, menționează-le punctual ca oportunități deja identificate de automatizare (fără să te apuci de ele acum, doar semnalezi că există rețeta). Menționează că pagina „Comenzi" din dashboard explică ce comenzi are la dispoziție.

**Nu te oprești la un rezumat pasiv.** Dacă la pasul „Task-uri curente" ai marcat vreun task ca fiind ceva ce poți face tu direct (vezi „Sunt build/solve/automate-oriented, nu doar ghidez" din CLAUDE.md), numește-l explicit acum și oferă-te să te apuci de el pe loc — ex. „Văd că ai «X» pe listă — e ceva ce pot face eu acum, vrei să mă apuc?" Dacă spune da, treci direct la treabă (urmează `reference/task-workflow.md`), fără să mai aștepți altă cerere. Dacă n-a fost niciun task de genul ăsta, sau spune nu, treci la cererea lui originală (dacă a avut una) sau întreabă cu ce vrea să înceapă.

Onboarding-ul nu trebuie să fie exhaustiv din prima — poate fi completat incremental în sesiuni viitoare.
