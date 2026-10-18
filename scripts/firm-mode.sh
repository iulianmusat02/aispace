#!/usr/bin/env bash
# Trece un repo creat din șablonul AISpace în „modul firmă": contextul firmei (my-context/, team/,
# manifestul șablonului) încetează să fie ignorat de git, ca să poată fi publicat pentru echipă.
# Șterge din .gitignore blocul dintre marcajele AISPACE-TEMPLATE-ONLY; restul regulilor rămân
# (TASKS.md, assets/, .env, explorer/live/ sunt ignorate mereu).
# Refuză în repo-ul-șablon (adresa din .claude/template-source) și fără un remote origin.
# Rulat de /install, pasul 7. Se poate rula de mai multe ori: a doua oară nu mai are ce face.
# Uz: scripts/firm-mode.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

START='# >>> AISPACE-TEMPLATE-ONLY'
END='# <<< AISPACE-TEMPLATE-ONLY'

norm() {  # https://github.com/a/b.git, git@github.com:a/b.git -> github.com/a/b
  echo "$1" | sed -E 's#^(https?://|ssh://)?(git@)?##; s#:#/#; s#\.git/?$##; s#/$##' | tr 'A-Z' 'a-z'
}

if ! grep -qF "$START" .gitignore 2>/dev/null; then
  echo "Deja în modul firmă: .gitignore nu mai are blocul doar-pentru-șablon."
  exit 0
fi

ORIGIN=$(git remote get-url origin 2>/dev/null || true)
if [ -z "$ORIGIN" ]; then
  echo "Oprit: repo-ul nu are încă un remote origin (spațiul comun al firmei pe GitHub). Creează-l întâi." >&2
  exit 1
fi
TEMPLATE=$(head -1 .claude/template-source 2>/dev/null || true)
if [ -n "$TEMPLATE" ] && [ "$(norm "$ORIGIN")" = "$(norm "$TEMPLATE")" ]; then
  echo "Oprit: ăsta e repo-ul-șablon ($TEMPLATE). Contextul firmei nu se publică aici." >&2
  exit 1
fi

# șterge blocul, cu tot cu marcaje și liniile goale rămase la final
awk -v s="$START" -v e="$END" '$0==s{skip=1; next} $0==e{skip=0; next} !skip' .gitignore > .gitignore.tmp
sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' .gitignore.tmp > .gitignore
rm -f .gitignore.tmp

# TASKS.md rămâne personal: dacă ajunsese cumva urmărit, îl scot din git fără să-l șterg de pe disc
git rm --cached --ignore-unmatch -q my-context/TASKS.md >/dev/null 2>&1 || true

echo "Modul firmă activ pentru $(norm "$ORIGIN")."
echo "Se publică de acum: my-context/ (fără TASKS.md și assets/), team/, .claude/template-manifest.txt."
