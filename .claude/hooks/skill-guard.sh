#!/usr/bin/env bash
# Pe scurt: înainte să pornească un skill al firmei, verifică să nu conțină instrucțiuni suspecte; dacă găsește ceva, îți cere aprobarea.
# PreToolUse (Skill): paza de prompt injection la apelarea unui skill al proiectului.
# Dacă SKILL.md conține semne suspecte, cere explicit aprobarea userului și îi arată ce a găsit.
# Nu blochează nimic singur și iese mereu cu 0. Skill-urile livrate cu șablonul (install, planning,
# process, recommend-process, quiz, guide, add-context, sync, history, add-teammate, update-template) sunt sărite; pentru ele răspunde proprietarul repo-ului la review-ul modificărilor.

trap 'exit 0' EXIT
INPUT=$(cat 2>/dev/null)
SKILL=$(printf '%s' "$INPUT" | sed -n 's/.*"skill" *: *"\([^"]*\)".*/\1/p' | head -1)
SKILL=${SKILL##*:}
[ -n "$SKILL" ] || exit 0
case "$SKILL" in install|planning|process|recommend-process|quiz|guide|add-context|sync|history|add-teammate|update-template) exit 0;; esac
FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/skills/$SKILL/SKILL.md"
[ -f "$FILE" ] || exit 0

# semne tipice: suprascrierea regulilor, ascunderea față de user, trimitere de date în afară,
# cod ofuscat/executat, acțiuni distructive, comentarii HTML sau caractere invizibile
PATTERN='ignor[aă]|ignore (all |any |the )?(previous|prior|above)|disregard|dezactiveaz[aă]|nu (spune|ar[aă]ta|men[țt]iona)|do not (tell|show|mention|reveal)|without (telling|asking)|f[aă]r[aă] s[aă] (spui|[îi]ntrebi)|curl |wget |base64|eval[ (]|webhook|--force|--no-verify|rm -rf|<!--|authorized_keys|id_rsa|~/\.ssh|\.env'
HITS=$(grep -n -iE "$PATTERN" "$FILE" | cut -c1-110)
if LC_ALL=C grep -q $'\xe2\x80[\x8b-\x8f\xaa-\xae]' "$FILE" 2>/dev/null; then HITS="$HITS
caractere invizibile (zero-width)"; fi
[ -n "$HITS" ] || exit 0

REASON=$(printf 'Skill-ul %s contine pasaje care pot fi prompt injection. Verifica-le inainte sa aprobi: %s' "$SKILL" "$(printf '%s' "$HITS" | head -6 | tr '\n' ' ' | tr -d '"\\')")
printf '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": "%s"}}\n' "$REASON"
exit 0
