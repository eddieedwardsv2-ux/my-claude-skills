# Teaching notes

## Learner
- Complete beginner to AI. Has set up Claude Code (cloud, from phone), connected this GitHub repo, and installed some of Matt Pocock's skills (grill-me, teach, to-tickets, find-skills) without fully understanding them yet.
- Mission confirmed by learner (session 1).

## Background (from session 1)
- Works full time for a solar panel company doing roofing. Good wages now. Previously self-employed painter & decorator for years; before that 5 years employed at a company with poor wages.
- Not driving at the moment, so van-based side businesses are off for now.
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
- Learner decides on personal-use risk once informed (e.g. accepted YouTube terms risk for /watch). Inform, then respect the choice.
- Learner is very keen to always follow platform rules/T&Cs.
- Never suggest scraping or anything that breaks a site's terms. Flag T&C risks proactively and explain them.
- Be cautious about bulk forking/cloning/automated GitHub actions; explain before doing anything outward-facing.

## Interests
- Cars: Audi TT Mk1 (BAM 225bhp engine), Mini Cooper S R53. Also petrol garden tools (strimmers) — good examples to use in lessons.
- Practice project: listings tracker/dashboard from eBay / Gumtree / Copart (legal sources only).
- Also wants to understand Claude's own replies — keep my chat jargon-free or define terms inline.

## Setup audit (session 1, checked against mattpocock/skills upstream)
- "Watch" skill found: bradautomates/claude-video (`/watch`), seen on a "Next New Thing" YouTube video. NOT installed: its default route downloads YouTube videos with yt-dlp, which YouTube's Terms forbid; the Gemini route needs a Google API key; it doesn't run in the Claude chat app. UPDATE: verified it's the popular one (~18k stars, 1.9k forks on GitHub). Learner has heard the YouTube-terms risk and accepts it for personal learning, so that's their call. Can't run in this cloud session: the network policy blocks www.youtube.com. Best home is Claude Code on the MacBook.
- `teach` skill matches upstream exactly. MISSION.md + NOTES.md done. Still to do before lesson 1: RESOURCES.md, glossary reference sheet, shared stylesheet in assets/.
- `setup-matt-pocock-skills` was run before (docs/agents/*). Two quirks: triage-labels.md was written though `triage` isn't installed (harmless); issue-tracker.md says to use the `gh` CLI, which isn't available in cloud sessions (Claude uses GitHub tools instead). Engineering skills are for coding projects and aren't needed for the current mission.
- `git-guardrails-claude-code` (Matt's safety skill) would block `git push`, which conflicts with the push-to-main workflow, so don't install it for now.

## Learner insight
- Wants Claude conversations that build on each other instead of starting fresh every time. This teaching workspace (MISSION/NOTES/learning records in the repo) is exactly that pattern. Make it an early lesson.

## Publishing workflow
- Lessons and reference sheets are written in `lessons/` and `reference/`, linking `assets/course.css` and `assets/quiz.js`.
- To publish: `python3 assets/publish.py <page> <scratchpad>/pub`, then publish that output with the Artifact tool (same path each time keeps the URL). Published URLs are kept in `assets/links.json` so pages link to each other.
- Lesson 1: https://claude.ai/artifact/CRvv2AY6mrwp2azFjsXHRa · Reference 1: https://claude.ai/artifact/RYSSnQtwR5a7RDqRJELzkZ
