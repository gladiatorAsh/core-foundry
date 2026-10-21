#!/usr/bin/env python3
"""Validate every question file. Run before committing new questions (CI runs it too)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {"id", "type", "question", "difficulty", "tags", "ref"}


def validate() -> list[str]:
    errors, ids = [], set()
    files = sorted((ROOT / "quizzes").glob("*.json"))
    if not files:
        return ["no quiz files found"]
    for path in files:
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}: invalid JSON ({e})"); continue
        if path.stem != doc.get("topic"):
            errors.append(f"{path.name}: topic '{doc.get('topic')}' doesn't match file name")
        for q in doc.get("questions", []):
            where = f"{path.name}:{q.get('id', '?')}"
            missing = REQUIRED - q.keys()
            if missing:
                errors.append(f"{where}: missing {sorted(missing)}")
            if q.get("id") in ids:
                errors.append(f"{where}: duplicate id")
            ids.add(q.get("id"))
            if q.get("difficulty") not in (1, 2, 3):
                errors.append(f"{where}: difficulty must be 1, 2 or 3")
            if q.get("type") == "mcq":
                opts = q.get("options", [])
                if not 2 <= len(opts) <= 6:
                    errors.append(f"{where}: needs 2–6 options")
                if len(set(opts)) != len(opts):
                    errors.append(f"{where}: duplicate options")
                if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(opts):
                    errors.append(f"{where}: answer must index into options")
                if not q.get("explanation"):
                    errors.append(f"{where}: MCQ needs an explanation")
            elif q.get("type") == "card":
                if not isinstance(q.get("answer"), str) or not q["answer"].strip():
                    errors.append(f"{where}: card needs a text answer")
            else:
                errors.append(f"{where}: type must be 'mcq' or 'card'")
            ref = (q.get("ref") or "").split("#")[0]
            if ref and not (ROOT / ref).exists():
                errors.append(f"{where}: ref '{ref}' does not exist")
    return errors


if __name__ == "__main__":
    errs = validate()
    for e in errs:
        print("ERROR", e)
    total = sum(len(json.loads(p.read_text())["questions"]) for p in (ROOT / "quizzes").glob("*.json"))
    print(f"{total} questions checked, {len(errs)} problems")
    sys.exit(1 if errs else 0)
