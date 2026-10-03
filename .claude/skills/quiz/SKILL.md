---
name: quiz
description: Quiz interactiv cu întrebări de începător despre AI (LLM-uri, prompturi, tokeni, halucinații, agenți, MCP, confidențialitate). Folosește-l când userul scrie /quiz sau cere un quiz / test de cunoștințe despre AI. Argumente opționale - un număr de întrebări (ex. "/quiz 5") și/sau o temă (ex. "/quiz prompturi").
---

# /quiz — întrebări de începător despre AI

Scopul: userul (sau un coleg căruia îi arată sistemul) își testează înțelegerea de bază despre AI, într-un format scurt și prietenos. Nivel: începător absolut — fără jargon neexplicat, fără matematică.

## Argumente

- Un număr (ex. `5`) = câte întrebări. Implicit **10**, maxim 20.
- Un cuvânt/temă (ex. `prompturi`, `agenți`) = toate întrebările din acea temă. Implicit: mix din toate temele de mai jos.

## Teme (pentru mix, acoperă cât mai multe, fără să repeți tema de două ori la rând)

1. Ce e un LLM și cum „gândește" (prezice text pe baza a ce a învățat; nu caută pe internet decât dacă are un tool pentru asta)
2. Tokeni și context window (cât „ține minte" într-o conversație, de ce conversațiile lungi se rezumă)
3. Halucinații (răspunsuri sigure pe ele dar greșite — de ce apar, cum verifici)
4. Knowledge cutoff (până când știe modelul lucruri)
5. Prompturi bune (context, exemple, format dorit, rol, pas cu pas)
6. Antrenare vs. folosire (modelul nu învață din conversația ta în timp real; memoria vine din fișiere/instrumente)
7. Tool-uri, MCP și conectori (cum ajunge AI-ul la email, Jira, Slack)
8. Agenți și skill-uri (AI care execută pași, nu doar răspunde; skill = instrucțiuni reutilizabile)
9. Confidențialitate și date sensibile (ce nu pui într-un prompt, date locale vs. trimise)
10. Multimodal (text, imagini, PDF-uri, diagrame)
11. RAG / documente proprii (cum „citește" AI-ul documentele tale fără să fie reantrenat)
12. Limite și verificare (când să nu te bazezi pe AI, human-in-the-loop)

## Cum rulezi quiz-ul

1. Un mesaj scurt de start: câte întrebări sunt și că e doar pentru învățare, nu se notează nicăieri.
2. Pune **o singură întrebare pe rând** cu AskUserQuestion: 3-4 variante, exact una corectă, variantele greșite plauzibile (nu evident absurde). Poziția răspunsului corect variază de la o întrebare la alta. Fără „(Recommended)" pe nicio variantă. În `header` pune „Q3/10" etc.
3. După fiecare răspuns: ✅ sau ❌, varianta corectă, și o explicație de 2-3 fraze pe înțelesul unui începător — ideal cu un exemplu din munca de zi cu zi (email, task-uri, documente). Dacă userul a răspuns prin „Other" cu text liber, evaluează ce a scris și explică.
4. Întrebările trebuie să fie diferite de la o rulare la alta — formulează-le proaspăt, nu recita un set fix.
5. La final: scorul (ex. 7/10), temele la care a greșit, câte o recomandare concretă pentru fiecare (ce să încerce practic), și o întrebare dacă vrea o rundă nouă doar pe temele greșite.

## Reguli

- Limba: română, termenii tehnici uzuali pot rămâne în engleză (prompt, token), dar explicați la prima apariție.
- Răspunsurile corecte trebuie să fie factual corecte și general valabile — nu depinde de un anumit produs/versiune decât dacă întrebarea o spune explicit.
- Nu salva nimic pe disc; quiz-ul nu modifică `my-context/`.
