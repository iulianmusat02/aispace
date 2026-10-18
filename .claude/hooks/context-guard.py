#!/usr/bin/env python3
"""Hook PreToolUse (Edit, Write, MultiEdit): As is / To be pe contextul firmei.
Pe scurt: înainte să se schimbe o informație despre firmă, echipă sau procese, îți arată As is / To be și îți cere acordul.

Când Claude vrea să schimbe o informație existentă despre firmă, echipă sau procese, cere acordul userului
și îi arată în fereastra de aprobare ce e acum (As is) și ce se propune (To be).
Fișiere urmărite (doar dacă există deja; un fișier nou nu actualizează nimic):
  Firma:   team/profile.md, team/projects/*, my-context/profile.md, my-context/projects/*
  Echipa:  team/people/*, my-context/people/*
  Procese: my-context/processes/*, team/processes/*
TASKS.md, assets/, scripts/ și skill-urile nu trec pe aici. Iese mereu cu 0; nu scrie nimic dacă nu e cazul.
"""
import difflib, json, os, re, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
WATCH = [
    (r"^(team|my-context)/profile\.md$", "Firma"),
    (r"^(team|my-context)/projects/[^/]+\.md$", "Firma"),
    (r"^(team|my-context)/people/[^/]+\.md$", "Echipa"),
    (r"^(team|my-context)/processes/[^/]+\.md$", "Procese"),
]
MAX_LINES = 14


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def short(line):
    line = line.rstrip()
    return line if len(line) <= 160 else line[:157] + "..."


def changes(before, after):
    """Rândurile scoase și cele adăugate (fără context), ca listă de text."""
    gone, new = [], []
    for op in difflib.ndiff(before.splitlines(), after.splitlines()):
        if op.startswith("- ") and op[2:].strip():
            gone.append(short(op[2:]))
        elif op.startswith("+ ") and op[2:].strip():
            new.append(short(op[2:]))
    return gone, new


def block(title, lines):
    if not lines:
        return f"{title}\n  (nimic)"
    shown = lines[:MAX_LINES]
    more = f"\n  ... încă {len(lines) - MAX_LINES} rânduri" if len(lines) > MAX_LINES else ""
    return title + "\n" + "\n".join("  " + l for l in shown) + more


def main():
    ev = json.loads(sys.stdin.read() or "{}")
    tool, inp = ev.get("tool_name", ""), ev.get("tool_input") or {}
    path = inp.get("file_path", "")
    if not path:
        return
    full = os.path.abspath(os.path.join(ROOT, path))
    if not full.startswith(ROOT + os.sep):
        return
    rel = os.path.relpath(full, ROOT)
    kind = next((k for pat, k in WATCH if re.match(pat, rel)), None)
    current = read(full)
    if not kind or current is None:
        return  # nu e context urmărit, sau e un fișier nou

    if tool == "Write":
        proposed = inp.get("content", "")
    elif tool == "Edit":
        old, new = inp.get("old_string", ""), inp.get("new_string", "")
        proposed = current.replace(old, new) if inp.get("replace_all") else current.replace(old, new, 1)
    elif tool == "MultiEdit":
        proposed = current
        for e in inp.get("edits") or []:
            o, n = e.get("old_string", ""), e.get("new_string", "")
            proposed = proposed.replace(o, n) if e.get("replace_all") else proposed.replace(o, n, 1)
    else:
        return
    if proposed == current:
        return

    gone, new = changes(current, proposed)
    reason = (
        f"Actualizare de context ({kind}): {rel}\n\n"
        + block("AS IS (acum):", gone) + "\n\n"
        + block("TO BE (propus):", new) + "\n\n"
        + "Ești de acord cu actualizarea?"
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
