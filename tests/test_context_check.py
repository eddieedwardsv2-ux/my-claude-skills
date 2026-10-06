"""Tests for scripts/context_check.py, using a small fictional Second Brain.

Run: python3 -m unittest discover tests
"""
import datetime as dt, json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from context_check import Snapshot, check

TODAY = dt.date(2026, 10, 6)
LINK = "https://docs.google.com/document/d/{}/edit"

DOCS = {
    "router": ("00 — START HERE — Index",
               "Current focus: Bakery pilot (P2). Waiting on a decision.\n"
               f"- Rules → [Core]({LINK.format('core')})\n"
               f"- Projects → [SB-B]({LINK.format('projects')})\n"
               f"- Decisions → [SB-C]({LINK.format('decisions')})\n"
               "Test: 'Did we pick a database?' → should answer D002.\n"),
    "core": ("Canonical Core",
             "Canonical Core · 2 rules · Last reviewed 2026-10-05\n"
             "1\\. OUTCOME FIRST\nDo the thing.\n2\\. VERIFY\nCheck it.\nAPPENDIX\n1\\. Dormant rule\n"),
    "projects": ("SB-B — Projects (CURRENT)",
                 "Last reviewed 2026-10-05\n## P1 — Website — PARKED\n## P2 — Bakery pilot — ACTIVE, current focus\n"),
    "decisions": ("SB-C — Decisions (CURRENT)",
                  "Last reviewed 2026-10-05\n### D001 — Use docs\n2026-10-01 · ACTIVE\n"
                  "### D002 — No database yet\n2026-10-02 · ACTIVE\n"
                  "### D003 — Core compressed to 2 rules\n2026-10-03 · ACTIVE\n"),
    "capabilities": ("SB-E — Capabilities (CURRENT)",
                     "Last reviewed 2026-10-05\n## E6 — Friction log\n- 2026-10-05 · repo missing · access · OPEN: ask owner\n"),
}


def run(edit=None, extra_index=()):
    """Build a snapshot, let `edit` change doc texts/titles, run the checks."""
    docs = {k: list(v) for k, v in DOCS.items()}
    if edit:
        edit(docs)
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "docs").mkdir()
        index = [{"id": k, "title": t, "modified": "2026-10-05"} for k, (t, _) in docs.items()]
        (Path(d) / "index.json").write_text(json.dumps(index + list(extra_index)))
        for k, (_, text) in docs.items():
            (Path(d) / "docs" / f"{k}.md").write_text(text)
        return check(Snapshot(d), TODAY, max_age=14)


def fails(results):
    return [(name, ev) for s, name, ev in results if s == "FAIL"]


class ContextCheck(unittest.TestCase):
    def test_healthy_brain_passes(self):
        results = run()
        self.assertEqual(fails(results), [])
        self.assertIn(("INFO", "friction-open", "2026-10-05 · repo missing · access · OPEN: ask owner"), results)

    def test_router_pointing_at_superseded_doc_fails(self):
        def edit(docs):
            docs["router"][1] += f"- Old rules → [v3]({LINK.format('old')})\n"
        results = run(edit, [{"id": "old", "title": "SUPERSEDED — Core v3", "modified": "2026-10-01"}])
        self.assertIn(("route", "router links a superseded doc: SUPERSEDED — Core v3"), fails(results))

    def test_route_to_missing_doc_fails(self):
        def edit(docs):
            docs["router"][1] += f"- Ghost → [x]({LINK.format('ghost')})\n"
        self.assertTrue(any("ghost" in ev for _, ev in fails(run(edit))))

    def test_focus_disagreement_fails(self):
        def edit(docs):
            docs["projects"][1] = docs["projects"][1].replace("P2 — Bakery pilot — ACTIVE, current focus",
                                                              "P2 — Bakery pilot — ACTIVE").replace(
                                                              "P1 — Website — PARKED", "P1 — Website — current focus")
        self.assertIn(("focus", "router says P2; projects doc marks ['P1'] as current focus"), fails(run(edit)))

    def test_stale_core_rule_count_fails(self):
        # Regression: an old Core whose header and body disagree must not pass as current.
        def edit(docs):
            docs["core"][1] = docs["core"][1].replace("2 rules", "36 rules")
        self.assertIn(("core-rules", "header says 36, body has 2 numbered rules"), fails(run(edit)))

    def test_decisions_log_rule_count_mismatch_fails(self):
        def edit(docs):
            docs["decisions"][1] = docs["decisions"][1].replace("compressed to 2 rules", "compressed to 14 rules")
        self.assertIn(("core-rules", "decisions log says 14 rules, Core says 2"), fails(run(edit)))

    def test_expected_decision_superseded_fails(self):
        def edit(docs):
            docs["decisions"][1] = docs["decisions"][1].replace(
                "### D002 — No database yet\n2026-10-02 · ACTIVE", "### D002 — No database yet\n2026-10-02 · SUPERSEDED BY D009")
        self.assertIn(("decision", "router relies on D002, which is no longer ACTIVE"), fails(run(edit)))

    def test_old_review_date_warns(self):
        def edit(docs):
            docs["projects"][1] = docs["projects"][1].replace("2026-10-05", "2026-08-01")
        results = run(edit)
        self.assertIn(("WARN", "freshness", "SB-B — Projects (CURRENT): reviewed 66 days ago"), results)
        self.assertEqual(fails(results), [])

    def test_two_current_routers_fails_safely(self):
        results = run(extra_index=[{"id": "r2", "title": "00 — START HERE — copy", "modified": "2026-10-06"}])
        self.assertIn(("find-doc", "no single current doc found for 'router'"), fails(results))


if __name__ == "__main__":
    unittest.main()
