#!/usr/bin/env python3
"""Bundle every quizzes/*.json file into one self-contained quiz.html (works offline, from file:// too)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build() -> Path:
    bank = {}
    for path in sorted((ROOT / "quizzes").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        bank[doc["topic"]] = doc
    total = sum(len(d["questions"]) for d in bank.values())
    # Escape "</" so question text can never close the <script> tag.
    payload = json.dumps(bank, ensure_ascii=False).replace("</", "<\\/")
    html = (ROOT / "tools" / "web_template.html").read_text(encoding="utf-8")
    html = (html.replace("__BANK__", payload)
                .replace("__TOTAL__", str(total)))
    out = ROOT / "quiz.html"
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    print(f"wrote {build()}")
