#!/usr/bin/env python3
"""Read-only context check for Charlie's Second Brain.

Answers one question with evidence: "If a fresh AI starts at 00 START HERE,
will it land on current, consistent context?" It never edits anything.

It works on a local snapshot, because scripts can't reach Google Drive
directly (only Claude's Drive connector can). Snapshot layout:

  SNAPSHOT/index.json      [{"id": ..., "title": ..., "modified": "YYYY-MM-DD..."}]
                           one row per doc, from a Drive title search
  SNAPSHOT/docs/<id>.md    full text of the docs the checks read

Keep snapshots outside any public repo: they contain private context.

Usage: python3 scripts/context_check.py SNAPSHOT [--today YYYY-MM-DD] [--max-age DAYS]
Exit code 1 if any check FAILs.
"""
import argparse, datetime as dt, json, re, sys
from pathlib import Path

DOC_LINK = re.compile(r"docs\.google\.com/document/d/([A-Za-z0-9_-]+)")


class Snapshot:
    def __init__(self, root):
        root = Path(root)
        self.index = {row["id"]: row for row in json.loads((root / "index.json").read_text())}
        self.text = {p.stem: p.read_text() for p in (root / "docs").glob("*.md")}

    def find(self, must, exclude="SUPERSEDED"):
        """The one current doc whose title contains `must`."""
        hits = [i for i, r in self.index.items() if must in r["title"] and exclude not in r["title"]]
        return hits[0] if len(hits) == 1 else None


def check(snap, today, max_age):
    results = []  # (status, check name, evidence)
    add = lambda status, name, evidence: results.append((status, name, evidence))

    ids = {k: snap.find(t) for k, t in [("router", "START HERE"), ("core", "Canonical Core"),
                                        ("projects", "SB-B —"), ("decisions", "SB-C"),
                                        ("capabilities", "SB-E")]}
    for key, doc_id in ids.items():
        if doc_id is None:
            add("FAIL", "find-doc", f"no single current doc found for '{key}'")
        elif doc_id not in snap.text:
            add("FAIL", "find-doc", f"'{key}' ({snap.index[doc_id]['title']}) has no text in snapshot")
    if any(i is None or i not in snap.text for i in ids.values()):
        return results
    router, core, projects, decisions, capabilities = (snap.text[ids[k]] for k in
        ("router", "core", "projects", "decisions", "capabilities"))

    # 1. Every route in START HERE points at a doc that exists and is not superseded.
    for doc_id in dict.fromkeys(DOC_LINK.findall(router)):
        row = snap.index.get(doc_id)
        if row is None:
            add("FAIL", "route", f"router links {doc_id}, which is not in the index (moved, deleted or no access)")
        elif "SUPERSEDED" in row["title"]:
            add("FAIL", "route", f"router links a superseded doc: {row['title']}")
        else:
            add("PASS", "route", row["title"])

    # 2. Routed docs say when they were last reviewed, and it isn't too long ago.
    for doc_id in dict.fromkeys(DOC_LINK.findall(router)):
        if doc_id not in snap.text or doc_id not in snap.index:
            continue
        title = snap.index[doc_id]["title"]
        m = re.search(r"Last reviewed (\d{4}-\d{2}-\d{2})", snap.text[doc_id])
        if not m:
            add("WARN", "freshness", f"{title}: no 'Last reviewed' date")
            continue
        age = (today - dt.date.fromisoformat(m.group(1))).days
        add("WARN" if age > max_age else "PASS", "freshness", f"{title}: reviewed {age} days ago")

    # 3. START HERE and the projects doc agree on the current focus.
    m = re.search(r"Current focus[^\n]*?\((P\d+)", router)
    if not m:
        add("FAIL", "focus", "router has no 'Current focus' line naming a project code like (P6")
    else:
        code = m.group(1)
        marked = re.findall(r"(P\d+)\b[^\n]*current focus", projects, re.I)
        if marked == [code]:
            add("PASS", "focus", f"router and projects doc both say {code}")
        else:
            add("FAIL", "focus", f"router says {code}; projects doc marks {marked or 'nothing'} as current focus")

    # 4. The Core really has the number of rules its header claims (stale-Core guard).
    m = re.search(r"(\d+) rules", core)
    body = core.split("APPENDIX")[0]
    numbered = re.findall(r"^\s*(\d+)\\?\.\s+[A-Z]", body, re.M)
    if not m:
        add("WARN", "core-rules", "Core header doesn't state a rule count")
    elif len(numbered) == int(m.group(1)):
        add("PASS", "core-rules", f"header says {m.group(1)}, body has {len(numbered)}")
    else:
        add("FAIL", "core-rules", f"header says {m.group(1)}, body has {len(numbered)} numbered rules")
    stated = re.findall(r"compressed (?:from \d+ )?to (\d+) rules", decisions)
    if m and stated and stated[-1] != m.group(1):
        add("FAIL", "core-rules", f"decisions log says {stated[-1]} rules, Core says {m.group(1)}")

    # 5. Decisions the router's test prompts expect are still active.
    for code in dict.fromkeys(re.findall(r"\b(D\d{3})\b", router)):
        block = re.search(rf"{code}\b.*?(?=\n#+ |\Z)", decisions, re.S)
        if not block:
            add("FAIL", "decision", f"router relies on {code}, which isn't in the decisions log")
        elif "SUPERSEDED BY" in block.group(0) or not re.search(r"\bACTIVE\b", block.group(0)):
            add("FAIL", "decision", f"router relies on {code}, which is no longer ACTIVE")
        else:
            add("PASS", "decision", f"{code} is ACTIVE")

    # 6. Open friction items (information, not a failure).
    log = capabilities.split("Friction log", 1)[-1]
    open_items = [l.strip(" -*") for l in log.splitlines() if re.search(r"\bOPEN\b", l)]
    for item in open_items:
        add("INFO", "friction-open", item[:160])
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("snapshot")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--max-age", type=int, default=14)
    a = ap.parse_args()
    results = check(Snapshot(a.snapshot), a.today, a.max_age)
    for status, name, evidence in results:
        print(f"{status:4}  {name:13} {evidence}")
    counts = {s: sum(r[0] == s for r in results) for s in ("PASS", "WARN", "FAIL", "INFO")}
    print("\n" + "  ".join(f"{k} {v}" for k, v in counts.items()))
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()
