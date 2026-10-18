"""Convert the deck (presentation/deck_EN/project) into a readable Markdown file with slide text and speaker notes.

python tools/deck_to_md.py  ->  presentation/deck_EN.md
"""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "presentation" / "deck_EN" / "project"


class Slide(HTMLParser):
    """Collects headings, paragraphs, list items, tables and the <aside> speaker notes in reading order."""

    def __init__(self):
        super().__init__()
        self.out, self.notes, self.buf, self.stack = [], "", "", []
        self.table, self.row, self.skip = None, None, 0

    def handle_starttag(self, tag, attrs):
        if tag in ("svg", "x-embed"):
            self.skip += 1
        if self.skip:
            return
        if tag == "br":
            self.buf += " "
        if tag == "table":
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag in ("h1", "h2", "h3", "p", "li", "td", "th", "aside"):
            self.flush()
            self.stack.append(tag)
        elif tag == "img":
            alt = dict(attrs).get("alt")
            if alt:
                self.out.append(f"*[Image: {alt}]*")

    def handle_endtag(self, tag):
        if tag in ("svg", "x-embed"):
            self.skip -= 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "p", "li", "td", "th", "aside") and self.stack and self.stack[-1] == tag:
            self.stack.pop()
            text = re.sub(r"\s+", " ", self.buf).strip()
            self.buf = ""
            if not text:
                return
            if tag in ("td", "th") and self.row is not None:
                self.row.append(text)
            elif tag == "aside":
                self.notes = text
            elif tag == "h1":
                self.out.append(f"# {text}")
            elif tag == "h2":
                self.out.append(f"## {text}")
            elif tag == "h3":
                self.out.append(f"**{text}**")
            elif tag == "li":
                self.out.append(f"- {text}")
            else:
                self.out.append(text)
        elif tag == "tr" and self.table is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table:
            head, *rows = self.table
            self.out.append("| " + " | ".join(head) + " |\n|" + "---|" * len(head))
            self.out[-1] += "".join("\n| " + " | ".join(r) + " |" for r in rows)
            self.table = None

    def handle_data(self, data):
        if not self.skip and self.stack:
            self.buf += data

    def flush(self):
        self.buf = ""


deck = json.loads((DECK / "deck.json").read_text(encoding="utf-8"))
starts = {v["start"]: v["description"] for v in deck["sections"].values()}
lines = [f"# {deck['title']} — slide text and speaker notes", "",
         f"{len(deck['order'])} slides. Source: `presentation/deck_EN/project/`. Live deck: https://claude.ai/artifact/FJ9M2YcumqxRwVyPRG1sF1", ""]
for n, sid in enumerate(deck["order"], 1):
    if sid in starts:
        lines += ["---", "", f"## Part: {starts[sid]}", ""]
    p = Slide()
    p.feed((DECK / "slides" / f"{sid}.html").read_text(encoding="utf-8"))
    lines += [f"### Slide {n} · `{sid}`", ""] + [x + "\n" for x in p.out]
    if p.notes:
        lines += [f"> **Speaker notes:** {p.notes}", ""]
out = ROOT / "presentation" / "deck_EN.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out}")
