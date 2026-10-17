#!/usr/bin/env bash
# Stop hook pentru repo-urile firmelor care folosesc AISpace (trunk-based, un singur main).
# După fiecare tură, DOAR un owner (vezi „Poate face push" în fișa lui):
#   1. comite my-context/ și .claude/skills/ (assets/ rămâne în afara git prin .gitignore),
#   2. aduce ce a publicat altcineva (merge),
#   3. publică. La conflict: oprește merge-ul și îi cere lui Claude să urmeze
#      reference/sync-conflicts.md (userul alege când informațiile se contrazic).
# Nu forțează niciodată push-ul. Inactiv în repo-ul-șablon (my-context/ e acolo în .gitignore).
# Iese mereu cu 0.

trap 'exit 0' EXIT
INPUT=$(cat 2>/dev/null)
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
git check-ignore -q my-context/profile.md && exit 0          # dormant în șablon
git remote get-url origin >/dev/null 2>&1 || exit 0

say() { printf '{"systemMessage": "%s"}\n' "$1"; }

PATHS=(); for d in my-context .claude/skills; do [ -d "$d" ] && PATHS+=("$d"); done   # git add pică dacă o cale lipsește
[ ${#PATHS[@]} -gt 0 ] || exit 0

# --- doar owner-ii publică: emailul din git trebuie să apară într-o fișă cu „Poate face push: da"
EMAIL=$(git config user.email 2>/dev/null)
is_owner() {
  [ -n "$EMAIL" ] || return 1
  local f
  for f in my-context/profile.md my-context/people/*.md team/profile.md team/people/*.md; do
    [ -f "$f" ] || continue
    grep -qiF -- "$EMAIL" "$f" && grep -qiE 'Poate face push:?\*\*:? *da' "$f" && return 0
  done
  return 1
}
if ! is_owner; then
  [ -n "$(git status --porcelain -- "${PATHS[@]}" 2>/dev/null)" ] && \
    say "Nu ești owner: modificările din my-context/ rămân doar pe calculatorul tău. Spune-i unui owner să le publice."
  exit 0
fi

# --- stage + verifică că în index nu e nimic în afară de căile permise
git add -A -- "${PATHS[@]}" >/dev/null 2>&1
if git diff --cached --name-only | grep -Ev '^(my-context|\.claude/skills)/' | grep -q .; then
  say "Sincronizare oprită: ai fișiere pregătite pentru commit în afara my-context/ și .claude/skills/. Comite-le sau scoate-le din staging."
  exit 0
fi

if ! git diff --cached --quiet; then
  # plasă de siguranță: secretele ar trebui să fie oricum doar în .env
  PATTERN='(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|://[^/[:space:]]+:[^@/[:space:]]+@|(API_KEY|SECRET|TOKEN|PASSWORD)[A-Za-z_]*[[:space:]]*[=:][[:space:]]*[^[:space:]]{8,})'
  if git diff --cached -U0 --text | grep -E '^\+' | grep -Eiq "$PATTERN"; then
    git reset -q >/dev/null 2>&1
    say "Nimic nu a fost publicat: pare că există un secret în context (cheie, token, parolă). Mută-l în .env și reîncearcă."
    exit 0
  fi
  git commit -q -m "Update my-context" >/dev/null 2>&1 || exit 0   # comite exact indexul scanat
fi

# --- trunk-based: întâi pull (merge), apoi push
BR=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
git fetch -q origin >/dev/null 2>&1 || { say "my-context/ salvat local; nu am putut contacta GitHub. Se reîncearcă la tura următoare."; exit 0; }

if git rev-parse -q --verify "origin/$BR" >/dev/null 2>&1; then
  BEHIND=$(git rev-list --count "HEAD..origin/$BR")
  AHEAD=$(git rev-list --count "origin/$BR..HEAD")
  [ "$BEHIND" = 0 ] && [ "$AHEAD" = 0 ] && exit 0
  if [ "$BEHIND" -gt 0 ] && ! git merge -q --no-edit "origin/$BR" >/dev/null 2>&1; then
    CONFLICTS=$(git diff --name-only --diff-filter=U | tr '\n' ' ')
    git merge --abort >/dev/null 2>&1
    if [ -n "$CONFLICTS" ] && ! printf '%s' "$INPUT" | grep -Eq '"stop_hook_active" *: *true'; then
      printf '{"decision": "block", "reason": "Sincronizarea contextului a gasit conflicte cu trunk-ul (%s). Urmeaza reference/sync-conflicts.md: rezolva singur ce nu se contrazice, iar unde informatiile se suprapun lasa userul sa aleaga."}\n' "${CONFLICTS% }"
    else
      say "Nu am putut aduce modificările celorlalți (merge eșuat). Contextul tău e salvat local, nepublicat."
    fi
    exit 0
  fi
  AHEAD=$(git rev-list --count "origin/$BR..HEAD")
  [ "$AHEAD" = 0 ] && exit 0
fi

if git push -q origin HEAD >/dev/null 2>&1; then
  say "my-context/ publicat pe GitHub."
else
  say "Publicarea a eșuat (rețea, permisiuni sau altcineva a publicat între timp). Se reîncearcă la tura următoare."
fi
exit 0
