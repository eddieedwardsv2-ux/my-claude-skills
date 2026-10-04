# Teaching notes

## Learner
- Complete beginner to AI. Has set up Claude Code (cloud, from phone), connected this GitHub repo, and installed some of Matt Pocock's skills (grill-me, teach, to-tickets, find-skills) without fully understanding them yet.
- Mission drafted in MISSION.md (session 1), awaiting confirmation.

## Background (from session 1)
- Works full time for a solar panel company doing roofing. Good wages now. Previously self-employed painter & decorator for years; before that 5 years employed at a company with poor wages.
- Has lost driving licence — limits van-based side businesses for now.
- Past start-up ideas: car valeting, green waste removal / garden clearances, flipping cheap cars from Marketplace.
- Why those stalled: too much for one person (doing the job AND driving the van AND finding work) before affording staff; struggled to get leads with no before/after proof-of-work photos.
- Stated goal: "build things like trackers and dashboards to help me."
- Feels blocked by: tech/business jargon and acronyms, code, not understanding how office jobs, hierarchy and departments work, and how office-based businesses differ from trade/subcontractor businesses.
- Writes long, honest, stream-of-thought messages — welcome this, then reflect it back tidily.

## Setup / constraints
- Until end of October 2026: iPhone 16 Plus, Claude app only. No local files, no browser for opening HTML.
- MacBook Air M4 arriving end of October 2026 — hands-on lessons can expand then.

## Delivery preferences
- Publish every lesson and reference sheet as a **private artifact** and send the link.
- Also save the HTML in the repo (`lessons/`, `reference/`) and **commit + push to `main`**.
- Lessons short and phone-friendly (single column, big tap targets, no wide tables).
- Explain all jargon in plain English.
- Ask **one question at a time**.

## Safety (important)
- Previously had a GitHub account banned after "messing about forking random skill repos" in early Claude Code use. Learner is very keen to always follow platform rules/T&Cs.
- Never suggest scraping or anything that breaks a site's terms. Flag T&C risks proactively and explain them.
- Be cautious about bulk forking/cloning/automated GitHub actions; explain before doing anything outward-facing.

## Interests
- Cars: Audi TT Mk1 (BAM 225bhp engine), Mini Cooper S R53. Also petrol garden tools (strimmers) — good examples to use in lessons.
- Practice project: listings tracker/dashboard from eBay / Gumtree / Copart (legal sources only).
- Also wants to understand Claude's own replies — keep my chat jargon-free or define terms inline.

## Setup audit (session 1, checked against mattpocock/skills upstream)
- "Watch" skill found: bradautomates/claude-video (`/watch`), seen on a "Next New Thing" YouTube video. NOT installed: its default route downloads YouTube videos with yt-dlp, which YouTube's Terms forbid; the Gemini route needs a Google API key; it doesn't run in the Claude chat app. Revisit on MacBook, Gemini route only, if learner still wants it.
- `teach` skill matches upstream exactly. MISSION.md + NOTES.md done. Still to do before lesson 1: RESOURCES.md, glossary reference sheet, shared stylesheet in assets/.
- `setup-matt-pocock-skills` was run before (docs/agents/*). Two quirks: triage-labels.md was written though `triage` isn't installed (harmless); issue-tracker.md says to use the `gh` CLI, which isn't available in cloud sessions (Claude uses GitHub tools instead). Engineering skills are for coding projects and aren't needed for the current mission.
- `git-guardrails-claude-code` (Matt's safety skill) would block `git push`, which conflicts with the push-to-main workflow, so don't install it for now.
