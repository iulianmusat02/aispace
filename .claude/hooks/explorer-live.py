#!/usr/bin/env python3
"""Hook Claude Code pentru Biroul 3D (explorer/index.html).
Pe scurt: ține biroul 3D la zi, cu unde lucrează fiecare sesiune Claude și ce e în fiecare cameră.

Primește pe stdin evenimentul hook-ului (SessionStart, UserPromptSubmit, PreToolUse,
Notification, Stop, SessionEnd) și scrie:
  explorer/live/sessions/<id>.json  starea fiecărei sesiuni Claude deschise în proiect
  explorer/live/live.js             window.AIOS_LIVE, citit de pagină la 1,5 secunde
  explorer/live/data.js             window.AIOS_DATA (skill-uri, fișiere, echipă), la SessionStart și Stop
explorer/live/ e în .gitignore și live-server îl ignoră (--ignore), ca dashboard-ul să nu se reîncarce.
Nu scrie nimic pe stdout (la SessionStart/UserPromptSubmit ar intra în contextul lui Claude) și iese mereu cu 0.
"""
import glob, json, os, re, subprocess, sys, time

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
OUT = os.path.join(ROOT, "explorer", "live")
SESS = os.path.join(OUT, "sessions")
STALE = 3 * 3600  # o sesiune fără niciun eveniment de 3 ore e considerată închisă


def write_atomic(path, text):
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def git(*args):
    try:
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, timeout=3).stdout.strip()
    except Exception:
        return ""


def person():
    # numele din „## Me" (my-context/profile.md, ex. **Iulian**), altfel userul git
    me = re.search(r"^## Me\s*\n+\*\*([^*]+)\*\*", read(os.path.join(ROOT, "my-context/profile.md")), re.M)
    return (me.group(1).strip() if me else "") or git("config", "user.name") or os.environ.get("USER", "")


# ---------- unde merge robotul ----------

def rel(p):
    if not p:
        return ""
    p = os.path.abspath(os.path.join(ROOT, p))
    return os.path.relpath(p, ROOT) if p.startswith(ROOT + os.sep) else ""


def room_for_path(r):
    if not r:
        return "desk"
    base = os.path.basename(r)
    if base == ".env" or base.startswith(".env."):
        return "safe"
    if r.startswith("my-context/assets/"):
        return "inbox"
    if r.startswith(("team/people/",)) or r == "team/profile.md":
        return "team"
    if r.startswith(("team/skills/", "my-context/skills/", "my-context/scripts/", "playbooks/")):
        return "custom"
    if r.startswith(".claude/skills/"):
        return "workshop" if is_template_skill(r.split("/")[2] if r.count("/") >= 2 else "") else "custom"
    if r.startswith(("team/", "my-context/", "reference/", "templates/")):
        return "library"
    return "desk"  # CLAUDE.md, TASKS.md, dashboard și restul


def is_template_skill(name):
    """Foundation Skill = vine cu șablonul (în .claude/template-manifest.txt). Fără manifest, toate din .claude/skills/ sunt Foundation."""
    manifest = read(os.path.join(ROOT, ".claude/template-manifest.txt"))
    return (f".claude/skills/{name}/SKILL.md" in manifest) if manifest else True


def skill_target(r):
    m = re.match(r"(?:\.claude/skills/([^/]+)/|team/skills/([^/]+?)(?:\.md)?$|my-context/skills/([^/]+?)(?:\.md)?$)", r)
    return next((g for g in (m.groups() if m else ()) if g), "")


def where(tool, inp):
    """(stare, cameră, țintă, etichetă) pentru un PreToolUse."""
    inp = inp if isinstance(inp, dict) else {}
    if tool == "Skill":
        s = str(inp.get("skill", "")).split(":")[-1]
        return "working", "workshop" if is_template_skill(s) else "custom", s, f"Folosește /{s}"
    if tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
        r = rel(inp.get("file_path") or inp.get("notebook_path", ""))
        room = room_for_path(r)
        verb = "Citește" if tool == "Read" else "Scrie în"
        name = os.path.basename(r) or "un fișier din afara proiectului"
        target = skill_target(r) if room in ("workshop", "custom") else (r if room == "library" else "")
        return "working", room, target, f"{verb} {name}"
    if tool in ("Grep", "Glob"):
        r = rel(inp.get("path", ""))
        return "working", room_for_path(r) if r else "library", "", "Caută prin fișiere"
    if tool == "Bash":
        cmd = str(inp.get("command", ""))
        if re.search(r"\bgit\s+push\b", cmd):
            return "working", "github", "", "Urcă pe GitHub"
        if re.search(r"\bgit\s+(pull|fetch|clone)\b", cmd):
            return "working", "github", "", "Aduce modificările de pe GitHub"
        if re.search(r"\bgit\s+commit\b", cmd):
            return "working", "gate", "", "Verifică și salvează o versiune"
        if re.search(r"\.env\b", cmd):
            return "working", "safe", "", "Lucrează cu cheile"
        return "working", "desk", "", "Rulează o comandă"
    if tool == "WebSearch":
        return "working", "web", "", "Caută pe internet"
    if tool == "WebFetch":
        return "working", "web", "", "Citește o pagină web"
    if re.match(r"mcp__(claude_browser|claude-in-chrome)__", tool, re.I):
        return "working", "web", "", "Navighează pe internet"
    if tool.startswith("mcp__"):
        name = connector_name(tool)
        if name:
            note_usage(name)
            return "working", "connectors", name, f"Folosește {name}"
        return "working", "desk", "", "Lucrează în aplicația Claude"
    if tool == "AskUserQuestion":
        return "waiting", "desk", "", "Te întreabă ceva"
    if tool in ("Agent", "Task"):
        return "working", "desk", "", "Trimite un ajutor"
    if tool == "TodoWrite":
        return "working", "desk", "", "Își face lista"
    return "working", "desk", "", "Lucrează"


# ---------- conectori (MCP) ----------
# Conectorii claude.ai apar în numele tool-urilor doar ca un id (mcp__<uuid>__tool); îi recunosc după tool-uri.
CLAUDE_AI_HINTS = [
    ("Gmail", ("thread", "draft", "label", "spam")),
    ("Atlassian Rovo", ("jira", "confluence", "atlassian", "compass", "teamworkgraph")),
    ("draw.io", ("diagram", "drawio", "shapes")),
    ("Postman", ("collection", "postman", "workspace", "mock", "spec")),
    ("GoDaddy", ("domains_",)),
    ("AWS Marketplace", ("marketplace",)),
    ("Claude Docs", ("batch", "guide", "export", "query")),
]
# Unelte ale aplicației Claude, nu conectori ai firmei.
APP_INTERNAL = re.compile(r"^(ccd_|claude_browser|claude_code_ios|computer-use|terminal|visualize|mcp-registry|scheduled-tasks)", re.I)


def connector_name(tool):
    parts = tool.split("__")
    if len(parts) < 3:
        return ""
    server, fn = parts[1], parts[2].lower()
    if server.startswith("plugin_"):
        plugin, _, srv = server[7:].partition("_")
        return srv or plugin
    if re.fullmatch(r"[0-9a-f-]{20,}", server):
        for name, hints in CLAUDE_AI_HINTS:
            if any(h in fn for h in hints):
                return name
        return "Conector claude.ai"
    if APP_INTERNAL.match(server):
        return ""
    return server.replace("_", " ")


def note_usage(name):
    path = os.path.join(OUT, "connectors-used.json")
    try:
        used = json.loads(read(path) or "{}")
    except ValueError:
        used = {}
    used[name] = int(time.time())
    write_atomic(path, json.dumps(used, ensure_ascii=False))


def gather_connectors():
    """Doar numele, sursa și tipul. Niciodată url, comandă, argumente, env sau headere (pot conține chei)."""
    out, seen = [], set()

    def add(name, source, cfg=None, plugin=""):
        if not name or name.lower() in seen:
            return
        seen.add(name.lower())
        cfg = cfg if isinstance(cfg, dict) else {}
        kind = "la distanță" if cfg.get("type") in ("http", "sse") or source == "claude.ai" else "local"
        out.append({"name": name, "source": source, "kind": kind, "plugin": plugin, "off": cfg.get("disabled") is True})

    def servers(path):
        try:
            d = json.loads(read(path) or "{}")
        except ValueError:
            return {}
        d = d.get("mcpServers", d) if isinstance(d, dict) else {}
        return d if isinstance(d, dict) else {}

    for n, c in servers(os.path.join(ROOT, ".mcp.json")).items():
        add(n, "proiect", c)
    try:
        cj = json.loads(read(os.path.expanduser("~/.claude.json")) or "{}")
    except ValueError:
        cj = {}
    for n, c in (cj.get("projects", {}).get(ROOT, {}).get("mcpServers") or {}).items():
        add(n, "doar pe acest calculator", c)
    for n, c in (cj.get("mcpServers") or {}).items():
        add(n, "toate proiectele tale", c)
    for n in cj.get("claudeAiMcpEverConnected") or []:
        add(re.sub(r"^claude\.ai\s+", "", n), "claude.ai")
    try:
        enabled = json.loads(read(os.path.expanduser("~/.claude/settings.json")) or "{}").get("enabledPlugins") or {}
        installed = json.loads(read(os.path.expanduser("~/.claude/plugins/installed_plugins.json")) or "{}").get("plugins") or {}
    except ValueError:
        enabled, installed = {}, {}
    for key, on in enabled.items():
        if not on:
            continue
        for inst in installed.get(key) or []:
            for n, c in servers(os.path.join(inst.get("installPath", ""), ".mcp.json")).items():
                add(n, "plugin", c, key.split("@")[0])
    try:
        used = json.loads(read(os.path.join(OUT, "connectors-used.json")) or "{}")
    except ValueError:
        used = {}
    for n in used:
        add(n, "folosit din aplicație")
    for c in out:
        c["last"] = used.get(c["name"], 0)
    return out


# ---------- hook-uri (sertarele din camerele de skill-uri) ----------
EVENT_RO = {
    "SessionStart": "la pornirea unei sesiuni", "UserPromptSubmit": "la fiecare mesaj trimis",
    "PreToolUse": "înainte de o acțiune", "PostToolUse": "după o acțiune", "Notification": "la notificări",
    "Stop": "la finalul fiecărui răspuns", "SubagentStop": "când termină un ajutor", "SessionEnd": "la închiderea sesiunii",
    "PreCompact": "înainte de rezumarea conversației",
}


def hook_summary(path):
    """Linia „Pe scurt:" din script; altfel primul comentariu."""
    text = read(path)
    m = re.search(r"Pe scurt:\s*(.+)", text)
    if m:
        return m.group(1).strip()
    for l in text.splitlines()[1:8]:
        l = l.strip().lstrip("#").strip().strip('"')
        if l:
            return l
    return ""


def gather_hooks():
    """Hook-urile din .claude/settings.json (proiect) și settings.local.json (doar pe acest calculator), grupate pe script."""
    manifest = read(os.path.join(ROOT, ".claude/template-manifest.txt"))
    out = {}
    for fname, local in ((".claude/settings.json", False), (".claude/settings.local.json", True)):
        try:
            cfg = json.loads(read(os.path.join(ROOT, fname)) or "{}")
        except ValueError:
            continue
        for event, entries in (cfg.get("hooks") or {}).items():
            for entry in entries or []:
                matcher = entry.get("matcher", "")
                for h in entry.get("hooks") or []:
                    cmd = h.get("command", "")
                    m = re.search(r"\.claude/hooks/([\w.-]+)", cmd)
                    key = m.group(1) if m else cmd[:40]
                    file = f".claude/hooks/{m.group(1)}" if m else ""
                    if key not in out:
                        template = (not local) and ((file in manifest) if manifest else bool(file))
                        out[key] = {"name": os.path.splitext(key)[0] if m else key, "file": file,
                                    "summary": hook_summary(os.path.join(ROOT, file)) if file else "",
                                    "template": template, "personal": local, "when": []}
                    when = EVENT_RO.get(event, event)
                    if event in ("PreToolUse", "PostToolUse") and matcher and matcher != "*":
                        parts = set(matcher.split("|"))
                        pre = "înainte" if event == "PreToolUse" else "după"
                        if parts <= {"Edit", "Write", "MultiEdit", "NotebookEdit"}:
                            when = f"{pre} de editarea unui fișier"
                        elif parts == {"Skill"}:
                            when = f"{pre} de pornirea unui skill"
                        elif parts == {"Bash"}:
                            when = f"{pre} de o comandă în terminal"
                        else:
                            when += f" ({matcher.replace('|', ', ')})"
                    if when not in out[key]["when"]:
                        out[key]["when"].append(when)
    return list(out.values())


# ---------- routines (sarcini pe care Claude le face singur, la ore fixe) ----------
# Taskurile programate din aplicația Claude stau în ~/.claude/scheduled-tasks/<id>/SKILL.md, dar fără program.
# Programul îl prind din răspunsul uneltelor: după ce Claude le listează (scheduled-tasks sau RemoteTrigger pentru
# routines în cloud), hook-ul PostToolUse salvează lista în explorer/live/routines.json.
ROUTINES_CACHE = os.path.join(OUT, "routines.json")


def json_in(text):
    """Primul obiect sau listă JSON dintr-un text (răspunsurile pot avea un antet, de ex. „HTTP 200")."""
    for i, ch in enumerate(text):
        if ch in "[{":
            try:
                return json.JSONDecoder().raw_decode(text[i:])[0]
            except ValueError:
                continue
    return None


def response_text(resp):
    if isinstance(resp, str):
        return resp
    if isinstance(resp, list):  # blocuri de conținut MCP
        return "\n".join(b.get("text", "") for b in resp if isinstance(b, dict))
    if isinstance(resp, dict):
        if "content" in resp:
            return response_text(resp["content"])
        return json.dumps(resp)
    return ""


def cache_routines(ev):
    tool, inp = ev.get("tool_name", ""), ev.get("tool_input") or {}
    data = json_in(response_text(ev.get("tool_response")))
    try:
        cache = json.loads(read(ROUTINES_CACHE) or "{}")
    except ValueError:
        cache = {}
    if tool.endswith("list_scheduled_tasks") and isinstance(data, list):
        cache["local"] = [{
            "id": t.get("taskId", ""), "title": t.get("title") or t.get("taskId", ""),
            "description": t.get("description", ""), "schedule": t.get("schedule", ""),
            "cron": t.get("cronExpression", ""), "enabled": t.get("enabled", True),
            "next": t.get("nextRunAt", ""), "last": t.get("lastRunAt", ""),
        } for t in data if isinstance(t, dict)]
    elif tool == "RemoteTrigger" and inp.get("action") == "list" and isinstance(data, dict):
        cache["cloud"] = [{
            "id": t.get("id", ""), "title": t.get("name") or t.get("title") or t.get("id", ""),
            "description": (t.get("job_config") or {}).get("prompt", "")[:160] if isinstance(t.get("job_config"), dict) else "",
            "schedule": t.get("cron_expression") or t.get("schedule", ""), "cron": t.get("cron_expression", ""),
            "enabled": t.get("enabled", True), "next": t.get("next_run_at", ""), "last": t.get("last_run_at", ""),
        } for t in data.get("data", []) if isinstance(t, dict)]
    else:
        return
    cache["updated"] = int(time.time())
    write_atomic(ROUTINES_CACHE, json.dumps(cache, ensure_ascii=False))


def gather_routines():
    try:
        cache = json.loads(read(ROUTINES_CACHE) or "{}")
    except ValueError:
        cache = {}
    out = [dict(r, source="aplicația Claude") for r in cache.get("local", [])]
    out += [dict(r, source="cloud") for r in cache.get("cloud", [])]
    known = {r["id"] for r in out}
    # taskuri locale care nu apar încă în listă: din fișiere, fără program
    if "local" not in cache:
        for p in sorted(glob.glob(os.path.expanduser("~/.claude/scheduled-tasks/*/SKILL.md"))):
            fm = frontmatter(read(p))
            tid = fm.get("name") or os.path.basename(os.path.dirname(p))
            if tid not in known:
                out.append({"id": tid, "title": tid, "description": fm.get("description", ""), "schedule": "",
                            "cron": "", "enabled": None, "next": "", "last": "", "source": "aplicația Claude"})
    return out


# ---------- sesiuni ----------

def update_session(ev):
    sid = re.sub(r"[^A-Za-z0-9_-]", "", str(ev.get("session_id", "")))[:64]
    if not sid:
        return
    path = os.path.join(SESS, sid + ".json")
    name = ev.get("hook_event_name", "")
    if name == "SessionEnd":
        try:
            os.remove(path)
        except OSError:
            pass
        return
    now = int(time.time())
    try:
        s = json.loads(read(path))
    except ValueError:
        s = {}
    s.setdefault("id", sid)
    s.setdefault("app", "claude")
    s.setdefault("since", now)
    s.setdefault("person", person())
    s.setdefault("room", "desk")
    s.setdefault("target", "")
    s["last"] = now
    if name == "SessionStart":
        s.update(state="arriving", room="desk", target="", label="A intrat în birou")
    elif name == "UserPromptSubmit":
        s.update(state="thinking", label="Se gândește")
    elif name == "PreToolUse":
        st, room, target, label = where(ev.get("tool_name", ""), ev.get("tool_input"))
        s.update(state=st, room=room, target=target, label=label)
    elif name == "Notification":
        s.update(state="waiting", label="Așteaptă răspunsul tău")
    elif name == "Stop":
        s.update(state="waiting", room="desk", target="", label="Gata, așteaptă următoarea cerere")
    else:
        return
    write_atomic(path, json.dumps(s, ensure_ascii=False))


def write_live():
    now = int(time.time())
    sessions = []
    for f in glob.glob(os.path.join(SESS, "*.json")):
        try:
            s = json.loads(read(f))
        except ValueError:
            s = None
        if not s or now - int(s.get("last", 0)) > STALE:
            try:
                os.remove(f)
            except OSError:
                pass
            continue
        sessions.append(s)
    sessions.sort(key=lambda s: s.get("since", 0))
    live = {"updated": now, "sessions": sessions}
    write_atomic(os.path.join(OUT, "live.js"), "window.AIOS_LIVE = " + json.dumps(live, ensure_ascii=False) + ";\n")


# ---------- date despre birou ----------

def strip_md(t):
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return re.sub(r"[*_`]", "", t).strip()


def body_lines(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return [l for l in text.splitlines()]


def md_info(path):
    text = read(path)
    lines = body_lines(text)
    title = next((strip_md(l[2:]) for l in lines if l.startswith("# ")), os.path.basename(path))
    summary = next((strip_md(re.sub(r"^\s*[-*]\s+", "", l)) for l in lines if l.strip() and not l.startswith(("#", "|", "---", ">"))), "")
    return {"file": os.path.relpath(path, ROOT), "title": title, "summary": summary[:160],
            "lines": len([l for l in text.splitlines() if l.strip()])}


def section(text, heading):
    m = re.search(r"^## " + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for l in block.splitlines():
        l = l.strip()
        if not l.startswith("|") or re.match(r"^\|[\s:|-]+\|$", l):
            continue
        rows.append([strip_md(c) for c in l.strip("|").split("|")])
    return rows[1:]  # fără antet


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text, flags=re.S)
    fm = {}
    for l in (m.group(1).splitlines() if m else []):
        k, _, v = l.partition(":")
        fm[k.strip()] = v.strip().strip('"')
    return fm


def skill_entry(name, desc, template):
    when = ""
    m = re.search(r"Folosește-l când (.*?)(?:\.|$)", desc)
    if m:
        when = m.group(1).strip()
    who = "owner" if re.search(r"doar pentru owner", desc, re.I) else "toți"
    first = re.split(r"(?<=\.)\s", desc, 1)[0]
    return {"name": name, "who": who, "when": when, "description": first, "template": template}


def gather():
    team_text = read(os.path.join(ROOT, "team/profile.md"))
    me_text = read(os.path.join(ROOT, "my-context/profile.md"))
    comp = [l for l in section(team_text, "Compania").splitlines() if l.strip()]
    company_line = strip_md(comp[0]) if comp else ""
    company = {"name": re.split(r"\s+[—-]\s+", company_line, 1)[0] if company_line else "",
               "about": company_line}

    manifest = read(os.path.join(ROOT, ".claude/template-manifest.txt"))
    skills = []
    for p in sorted(glob.glob(os.path.join(ROOT, ".claude/skills/*/SKILL.md"))):
        fm = frontmatter(read(p))
        d = os.path.basename(os.path.dirname(p))
        template = (f".claude/skills/{d}/SKILL.md" in manifest) if manifest else True
        skills.append(skill_entry(fm.get("name", d), fm.get("description", ""), template))
    for p in sorted(glob.glob(os.path.join(ROOT, "team/skills/*.md")) + glob.glob(os.path.join(ROOT, "my-context/skills/*.md"))):
        fm = frontmatter(read(p))
        info = md_info(p)
        e = skill_entry(fm.get("name") or os.path.splitext(os.path.basename(p))[0],
                        fm.get("description") or info["summary"], False)
        e["file"] = info["file"]
        e["personal"] = p.startswith(os.path.join(ROOT, "my-context"))
        skills.append(e)

    context = []
    for p in ["team/profile.md", *sorted(glob.glob(os.path.join(ROOT, "team/projects/*.md"))), "my-context/profile.md"]:
        p = p if os.path.isabs(p) else os.path.join(ROOT, p)
        if os.path.isfile(p):
            context.append(md_info(p))

    team = []
    for row in table_rows(section(team_text, "People")):
        if not row or not row[0]:
            continue
        name = re.sub(r"^\(Eu\)\s*", "", row[0])
        slug = re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-"))
        card = read(os.path.join(ROOT, f"team/people/{slug}.md"))
        admin = bool(re.search(r"Poate face push:?\*?\*?:? *da", card, re.I))
        team.append({"name": name, "role": row[1] if len(row) > 1 else "", "admin": admin})

    recent = []
    for l in git("log", "-6", "--date=short", "--format=%ad\t%an\t%s").splitlines():
        parts = l.split("\t")
        if len(parts) == 3:
            recent.append({"date": parts[0], "author": parts[1], "subject": parts[2]})

    unsaved = [l[3:] for l in git("status", "--porcelain").splitlines() if l.strip()]
    assets = [f for f in os.listdir(os.path.join(ROOT, "my-context/assets"))
              if not f.startswith(".")] if os.path.isdir(os.path.join(ROOT, "my-context/assets")) else []

    return {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "setUp": os.path.isfile(os.path.join(ROOT, "my-context/profile.md")),
        "company": company,
        "inboxCount": len(assets),
        "hasEnv": os.path.isfile(os.path.join(ROOT, ".env")),
        "repoUrl": git("remote", "get-url", "origin"),
        "viewer": {"name": person()},
        "context": context,
        "skills": skills,
        "team": team,
        "connectors": gather_connectors(),
        "hooks": gather_hooks(),
        "routines": gather_routines(),
        "recent": recent,
        "work": {"unsaved": unsaved[:30], "unsavedCount": len(unsaved)},
    }


def main():
    try:
        ev = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        ev = {}
    os.makedirs(SESS, exist_ok=True)
    if ev.get("hook_event_name") == "PostToolUse":
        cache_routines(ev)
        write_atomic(os.path.join(OUT, "data.js"),
                     "window.AIOS_DATA = " + json.dumps(gather(), ensure_ascii=False, indent=1) + ";\n")
        return
    update_session(ev)
    write_live()
    # data.js: la începutul/sfârșitul turei, la cerere, și altfel cel mult o dată la 10 s
    # (prinde și fișierele șterse sau mutate de mână între ture)
    data_path = os.path.join(OUT, "data.js")
    try:
        stale = time.time() - os.path.getmtime(data_path) > 10
    except OSError:
        stale = True
    if stale or ev.get("hook_event_name") in ("SessionStart", "Stop") or "--data" in sys.argv:
        write_atomic(data_path,
                     "window.AIOS_DATA = " + json.dumps(gather(), ensure_ascii=False, indent=1) + ";\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
