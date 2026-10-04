#!/usr/bin/env python3
"""Turn a lesson/reference page into a single self-contained file for publishing as an artifact.

Inlines assets/course.css and assets/quiz.js, and swaps links between course pages for their
published artifact URLs (kept in assets/links.json). Repo copies stay as normal linked pages
for reading on a computer.

Usage: python3 assets/publish.py lessons/0001-x.html OUT_DIR
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / sys.argv[1]).resolve()
out_dir = Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
html = src.read_text()
links = json.loads((ROOT / "assets/links.json").read_text()) if (ROOT / "assets/links.json").exists() else {}

head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)
title = re.search(r"<title>.*?</title>", head, re.S).group(0)
fonts = "\n".join(re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)[^>]*>', head))

def inline(match):
    path = (src.parent / match.group(1)).resolve()
    return f"<style>\n{path.read_text()}\n</style>"
body_css = re.sub(r'<link rel="stylesheet" href="([^"]*assets/[^"]+\.css)">', inline, head)
css = "\n".join(re.findall(r"<style>.*?</style>", body_css, re.S))

def inline_js(match):
    path = (src.parent / match.group(1)).resolve()
    return f"<script>\n{path.read_text()}\n</script>"
body = re.sub(r'<script src="([^"]*assets/[^"]+\.js)"></script>', inline_js, body)

def relink(match):
    target = (src.parent / match.group(1)).resolve().relative_to(ROOT).as_posix()
    return f'href="{links[target]}"' if target in links else match.group(0)
body = re.sub(r'href="(\.\./(?:lessons|reference)/[^"#]+)"', relink, body)

out = out_dir / src.name
out.write_text(f"{title}\n{fonts}\n{css}\n{body}")
print(out)
