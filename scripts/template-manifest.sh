#!/usr/bin/env bash
# Scrie .claude/template-manifest.txt: amprenta (sha256) a fiecărui fișier livrat cu șablonul.
# /update-template o folosește ca să afle ce fișiere nu a modificat firma. Se rulează o dată la /install,
# înainte ca firma să editeze ceva. Nu include contextul firmei (my-context/, team/) și nici secretele.
# Uz: scripts/template-manifest.sh [url-sablon]   (implicit: adresa din .claude/template-source)
set -e
cd "$(git rev-parse --show-toplevel)"
OUT=.claude/template-manifest.txt
{
  echo "# source: ${1:-$(head -1 .claude/template-source 2>/dev/null)}"
  git ls-files | grep -Ev '^(my-context|team)/|^\.env' | grep -v '^\.claude/template-manifest\.txt$' | while IFS= read -r f; do
    [ -f "$f" ] && shasum -a 256 -- "$f"
  done
} > "$OUT"
echo "Manifest scris în $OUT ($(($(wc -l < "$OUT") - 1)) fișiere)."
