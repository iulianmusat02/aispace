#!/usr/bin/env bash
# Stop hook: după fiecare tură, comite și împinge my-context/ (fără assets/)
# și .claude/skills/ (skill-urile create de /process) în repo-ul clientului. Nu face nimic în repo-ul-șablon (unde my-context/
# e în .gitignore). Iese mereu cu 0, ca să nu blocheze niciodată oprirea.

trap 'exit 0' EXIT
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# Dormant în șablon: dacă my-context/ e ignorat, nu sincronizăm nimic.
git check-ignore -q my-context/profile.md && exit 0

# Fără remote nu avem unde împinge.
git remote get-url origin >/dev/null 2>&1 || exit 0

say() { printf '{"systemMessage": "%s"}\n' "$1"; }

# assets/ rămâne în afara git prin .gitignore; doar my-context/ intră în commit.
PATHS=(my-context .claude/skills)
git add -A -- "${PATHS[@]}" >/dev/null 2>&1
git diff --cached --quiet -- "${PATHS[@]}" && exit 0

# Scanare secrete în ce urmează să fie comis; dacă găsim ceva, nu comitem.
PATTERN='(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(API_KEY|SECRET|TOKEN|PASSWORD)[A-Za-z_]*[[:space:]]*[=:][[:space:]]*[^[:space:]]{8,})'
if git diff --cached -U0 -- "${PATHS[@]}" | grep -E '^\+' | grep -Eq "$PATTERN"; then
  git reset -q -- "${PATHS[@]}" >/dev/null 2>&1
  say "my-context/ NU a fost sincronizat: pare să conțină un secret (cheie/token/parolă). Mută-l în .env și reîncearcă."
  exit 0
fi

git commit -q -m "Update my-context" -- "${PATHS[@]}" >/dev/null 2>&1 || exit 0

# Push simplu, fără force; la eșec (rețea, conflict) doar anunțăm.
if git push -q >/dev/null 2>&1 || git push -q -u origin HEAD >/dev/null 2>&1; then
  say "my-context/ sincronizat pe GitHub."
else
  say "my-context/ salvat local, dar push-ul a eșuat (rețea sau conflict). Se reîncearcă la următoarea tură."
fi
exit 0
