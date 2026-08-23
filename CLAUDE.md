# Memory

## Onboarding check — rulează asta primul, la fiecare sesiune

Verifică dacă `my-context/profile.md` există.

- **Dacă există**: citește-l — conține Me / People / Terms / Projects / Preferences / Open threads — și tratează-l ca sursă de adevăr pentru contextul de business/echipă. Apoi continuă normal cu cererea userului.
- **Dacă NU există**: acesta e un clone proaspăt, netrecut prin onboarding. Oprește-te înainte de orice altă acțiune (cu excepția cazului în care userul cere explicit să sară peste onboarding) și rulează fluxul de mai jos.

### Flux de onboarding

1. Deschide cu un mesaj de bun venit — nu tehnic, nu „nu găsesc fișierul X". Ceva de genul (adaptează liber tonul, dar păstrează structura: salut, cadrul primei interacțiuni, de ce contează, ce urmează):

   > Salut! Aceasta e prima noastră interacțiune, așa că înainte să te ajut concret aș vrea să te cunosc puțin — pe ce lucrezi, cu cine, și ce ai pe agendă acum. Durează doar câteva minute, iar tot ce îmi spui rămâne strict pe acest calculator, privat — nu se trimite, publică sau distribuie nicăieri. Odată setat, o să pot ține pasul cu contextul tău de la o discuție la alta, fără să reiei mereu aceleași explicații.
   >
   > Hai să începem cu partea de business — pe ce proiect/produs lucrezi acum și ce faci concret?

2. Dacă `my-context/TASKS.md` nu există, copiază `templates/TASKS.template.md` → `my-context/TASKS.md`.
4. Rulează onboarding-ul ca o secvență scurtă de întrebări **ghidate**, cu AskUserQuestion, în locul unor întrebări deschise gen "spune-mi tot despre X". Regula de bază: AskUserQuestion se folosește acolo unde răspunsul are variante reale, discrete, de bun-simț (nu inventa opțiuni artificiale gen "îți spun eu / sar peste" — tool-ul oferă deja automat "Other" pentru răspuns liber, nu-l duplica ca opțiune separată). Pentru lucruri intrinsec deschise (nume de proiect, nume de oameni, descrieri libere), pune întrebarea normal, conversațional, fără AskUserQuestion.

   AskUserQuestion permite maxim 4 opțiuni + "Other" per întrebare — pentru categorii cu mai multe variante plauzibile (ex. domeniu), nu înghesui totul într-o singură întrebare; fă drill-down în 2 pași: întâi o categorie mare (max 4 opțiuni), apoi o a doua AskUserQuestion cu opțiuni specifice ramurii alese (tot max 4, adaptate la răspunsul de la pasul 1).

   Secvență recomandată (nu bombarda userul cu tot deodată — 1 AskUserQuestion sau 1 întrebare liberă pe rând, cu multiSelect unde are sens):
   - **Domeniu — pasul 1** (AskUserQuestion, 4 opțiuni reale — NU adăuga o a 5-a opțiune gen "Altceva", tool-ul oferă deja "Other" cu exact acest rol): Tehnic/Engineering, Business (Product/Vânzări/Marketing), Operațional/Suport (HR/Legal/Finance), Producție/Servicii directe (ex. sănătate, educație, producție, construcții, retail).
   - **Domeniu — pasul 2** (AskUserQuestion, opțiuni condiționate de răspunsul de la pasul 1; dacă userul a răspuns prin "Other" la pasul 1, sari peste pasul 2 — folosește direct ce a scris):
     - Dacă Tehnic: Software Development, Infrastructură/DevOps, Data/Analytics, QA/Security.
     - Dacă Business: Product Management, Vânzări/Business Development, Marketing, Customer Success.
     - Dacă Operațional/Suport: HR, Legal/Compliance, Finance, Operațiuni generale.
     - Dacă Producție/Servicii directe: Sănătate, Educație, Producție/Manufacturing, Construcții/Retail/Altele — și tot prin "Other" cine nu se regăsește.
   - **Rol/scop** (AskUserQuestion): ex. Lucrez individual, Coordonez o echipă, Coordonez mai multe echipe/proiecte, Rol de management fără coordonare tehnică directă.
   - **Mărime echipă** (AskUserQuestion, doar dacă Rol/scop nu a fost "Lucrez individual"): ex. 2-5 oameni, 6-15 oameni, Peste 15 oameni, Variază după proiect — dictează cât de detaliat merită structurat `my-context/people/`. Pusă imediat după Rol/scop, cât timp subiectul echipei e "cald" — nu împinsă la coadă după toate întrebările de proiect.
   - **Oameni cheie** (imediat după Mărime echipă, doar dacă nu lucrează individual) — la fel ca la proiecte, câte o persoană pe rând, nu toate 3-5 într-un mesaj bulk:
     1. "Cum o cheamă pe prima persoană cu care lucrezi des?" (doar numele)
     2. "Care e rolul ei?"
     3. "Pe ce anume lucrează sau cu ce te ajută?"
     4. "Ai și emailul ei la îndemână? E opțional, dar util dacă va trebui vreodată să-i trimiți un mesaj direct din context. Dacă nu, spune 'nu'."
     5. AskUserQuestion: "Mai sunt și alți oameni cheie de adăugat?" (Da / Nu, oprește-te după max. 5-6 persoane chiar dacă răspunde Da în continuare — restul pot fi adăugate ulterior, incremental) — dacă Da, repetă 1-4 pentru următoarea persoană.
   - **Proiect(e) principal(e)** — chiar dacă răspunsul e liber (nume/descrieri nu se pot enumera), tot trebuie ghidat: nu pune o singură întrebare largă care cere 3 lucruri deodată ("pe ce lucrați + cum se numesc + ce termeni folosiți"). Sparge în întrebări mici, punctuale, fiecare cerând explicit UN singur lucru, ca omul să știe exact ce să răspundă:
     1. "Cum se numește proiectul/produsul principal la care lucrezi acum?" (doar numele)
     2. Întreabă dacă are deja documentație pe undeva (README, wiki, spec, notițe) — dacă da, mai rapid pentru el să o lipească direct decât să răspundă la întrebări una câte una: "Ai cumva vreo documentație scurtă pe acest proiect (README, notițe, spec) pe care ai putea s-o lipești aici? Dacă da, o citesc și extrag ce trebuie direct din ea — sari peste restul întrebărilor de mai jos pentru acest proiect. Dacă nu ai la îndemână, continuăm cu 2-3 întrebări rapide." Dacă lipește text/link/fișier, extrage din el descrierea, rolul (dacă reiese) și termenii cheie, apoi confirmă pe scurt ce ai înțeles înainte să treci mai departe — nu mai pune 3-5 separat.
     3. Dacă nu are documentație: "Pe scurt, în 1-2 fraze, ce face acest proiect/produs?"
     4. Dacă nu are documentație: "Care e rolul tău concret pe el?"
     5. Dacă nu are documentație: "Sunt acronime sau termeni interni cheie pe care ar trebui să-i știu (ex. nume de coduri, prescurtări)? Dacă nu, spune direct 'nu'." — dă exemplul concret ca omul să înțeleagă genul de răspuns așteptat, nu doar categoria.
     6. Dacă e cazul, AskUserQuestion: "Mai ai și alte proiecte active pe care ar trebui să le știu?" (Da / Nu) — dacă Da, repetă 1-5 pentru următorul.
   - **Task-uri curente** — câte un task pe rând, ca la proiecte/oameni, nu totul deodată:
     1. "Ce ai pe agendă acum? Dă-mi primul lucru." (ce e de făcut)
     2. "Are un termen limită (due date)? Dacă nu, spune 'nu'."
     3. "Cine e responsabil — tu, sau altcineva din echipă?" (dacă a menționat deja un nume la pasul 1, doar confirmă, nu întreba din nou)
     4. Dacă e ceva care se repetă periodic (nu un task cu un singur rezultat, ci o instrucțiune permanentă — ex. "verifică emailurile în fiecare zi la 10:00 și spune-mi ce e important"), marchează-l ca recurent și notează intervalul exact (ex. "zilnic la 10:00", "lunea dimineața"); altfel e un task normal cu due date.
     5. AskUserQuestion: "Mai ai și alte task-uri de adăugat acum?" (Da / Nu, oprește-te după max. 5-6 chiar dacă răspunde Da în continuare — restul se adaugă incremental) — dacă Da, repetă 1-4 pentru următorul.
   - **Stil de comunicare** (AskUserQuestion): ex. Concis și la obiect, Detaliat cu context, Mix RO/EN natural — ca să setez tonul răspunsurilor viitoare.
5. Completează `templates/profile.template.md` cu răspunsurile și salvează rezultatul ca `my-context/profile.md`.
6. Pentru proiectele/persoanele menționate cu suficient detaliu, creează câte un fișier din `templates/projects/_project.template.md` / `templates/people/_person.template.md` în `my-context/projects/` / `my-context/people/` (slug kebab-case, ex. `elena-man.md`). Nu e obligatoriu pentru fiecare mențiune — doar unde are sens să existe context extins.
7. Populează `my-context/TASKS.md` cu task-urile curente descrise, inclusiv due date/assignee/recurent unde au fost date, folosind formatul din secțiunea "Task execution workflow" de mai jos.
8. Confirmă userului că setup-ul e gata, în termeni de business, nu tehnici — NU menționa git, gitignore, ce e „ignorat", ce fișiere există pe disc sau alte detalii de implementare; userul nu trebuie să știe și nici nu-l ajută cu nimic să afle asta. Un rezumat de genul: ce ai reținut (rol, echipă, proiecte), câți oameni și proiecte ai adăugat, câte task-uri sunt notate — apoi treci direct la cererea lui originală (dacă a avut una) sau întreabă cu ce vrea să înceapă.

Onboarding-ul nu trebuie să fie exhaustiv din prima — poate fi reluat/completat incremental în sesiuni viitoare (vezi skill-ul `productivity:update`).

## Reguli generale de lucru (independente de contextul de business — vezi my-context/profile.md pentru specific)

### Fișiere de lucru (my-context/assets/)

`my-context/assets/` e zona de drop pentru fișiere pe care userul vrea să lucrez direct — excel-uri, PDF-uri, alte documente. Dacă userul menționează "excel-ul", "fișierul", "documentul" fără path, verific mai întâi acolo. Folderul e tracked în git (gol, cu `.gitkeep`, ca să existe după clone), dar tot ce se pune înăuntru e gitignored — personal, nu se distribuie.

### Preferințe de colaborare
- **De implicat oamenii afectați în ședințele aferente**: dacă se discută subiectul X și persoana Y lucrează pe X (vezi coloana "Lucrează pe" din tabelul People, my-context/profile.md), Y trebuie implicată/invitată. Când pregătesc ședințe sau discut planificare pe un subiect/proiect, verific People și semnalez cine ar trebui inclus.

### Task execution workflow (TASKS.md)

Task-urile sunt în `my-context/TASKS.md`, vizualizate în `dashboard.html` (board local, fără server/Node — pur HTML+JS, citește direct fișierul). **Dashboard-ul e strict read-only** — nu are niciun buton de adăugat/șters/editat/mutat (inclusiv drag-and-drop), iar folderul e conectat cu permisiune doar de citire la nivel de browser. Singura sursă de adevăr pentru orice modificare (task-uri, oameni, proiecte, memorie) sunt eu, în sesiune, editând fișierele `.md` direct — userul nu operează pe date din dashboard. În dashboard, conectarea se face o singură dată din Settings → „📁 Conectează folder" (se alege folderul rădăcină al proiectului, cel cu CLAUDE.md) — de acolo se încarcă automat tot: task-uri, recurente, oameni, proiecte.

**Format linie de task**, cu tag-uri opționale la final (orice ordine):
```
- [ ] **Titlu task** - notă opțională (due: YYYY-MM-DD) (@Assignee) (recurrent: descriere interval) (id: AS-N)
```
- `(due: YYYY-MM-DD)` — termen limită, dacă există.
- `(@Assignee)` — cine e responsabil (dacă nu e userul, notează numele).
- `(recurrent: ...)` — DOAR pentru task-uri care sunt o instrucțiune permanentă, repetitivă (nu un livrabil unic) — ex. `(recurrent: zilnic la 10:00)`. În dashboard, tab-ul Task-uri are 2 subtaburi: „📌 Punctuale" (task-urile normale, cu un singur rezultat) și „🔁 Recurente" (cele cu `recurrent` setat) — ca să nu se amestece și să nu pară "terminate" când ajung într-o coloană Done. Un task normal, cu un singur rezultat și eventual un due date, NU e recurent.

**Când user-ul dă un ID/titlu de task** (ex. "AS-3", "ocupă-te de X"):
1. Citesc `my-context/TASKS.md`, găsesc task-ul (după `id: AS-N` sau titlu).
2. Dacă nu e deja în secțiunea `## În lucru`, îl mut acolo (îl scot din secțiunea curentă, îl adaug în „În lucru") — semnalează vizual, în dashboard, că m-am apucat de el. (Secțiunile standard din `templates/TASKS.template.md`: „În așteptare", „Active", „În lucru", „Finalizate" — dar pot fi adaptate/redenumite liber în `my-context/TASKS.md`.)
3. Parcurg subtask-urile lui, unul câte unul.
4. Pentru fiecare, folosesc orice am nevoie (Bash, Read/Write/Edit, WebSearch, MCP-uri precum draw.io/Gmail, skills) ca să chiar rezolv treaba — nu doar descriu ce ar trebui făcut.
5. **Subtask-uri care sunt acțiuni umane** (discuții, "de trimis către X") nu le pot executa direct — pregătesc sugestii concrete (draft de mesaj/email gata de folosit) în loc să le marchez fals ca gata.
6. **Acțiuni cu efect real** (trimis email, postat, etc.) — cer confirmare înainte de send, nu trimit nimic în numele user-ului fără OK explicit.

**Format rezultat — linie imbricată sub subtask (4 spații indent, nu subtask separat):**
```
  - [x] Text subtask
    - Rezultat: ce s-a făcut, cu path relativ către fișiere generate (ex. my-context/diagrams/x.svg) — dashboard-ul le randează ca imagine inline dacă extensia e .svg/.png/.jpg/.gif
  - [ ] Alt subtask (nerezolvabil direct)
    - Sugestie: mesaj/email draft gata de folosit, plus ce blochează (ex. lipsă adresă)
```
Bifez `[x]` pe subtask-ul original DOAR dacă chiar s-a terminat treaba, nu doar pentru că am produs o sugestie.

**Blocaje** — orice găsesc care oprește progresul se scrie ca subtask nou, cu prefix exact `⚠️ Blocaj: ...` (dashboard-ul le sortează automat primele și le colorează roșu — nu necesită nimic în plus, doar prefixul).

Acest workflow nu are nevoie de Node.js/server/API key — e doar eu, în sesiune, citind/scriind fișiere și folosind tool-urile disponibile.
