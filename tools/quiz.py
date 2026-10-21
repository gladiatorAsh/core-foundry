#!/usr/bin/env python3
"""Self-quiz with spaced repetition (Leitner boxes). Standard library only; Python 3.9+.

Examples
  python tools/quiz.py                       # 15 questions across all topics, due items first
  python tools/quiz.py --topic genai -n 20   # one topic (prefix match works: --topic gen)
  python tools/quiz.py --mode cards          # flashcards only (self-graded)
  python tools/quiz.py --tag rag --tag agents
  python tools/quiz.py --stats               # mastery per topic and weakest tags
  python tools/quiz.py --list                # topics and question counts

Progress lives in .progress.json at the repo root (git-ignored by default; commit it if you
want it to follow you across machines).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIZ_DIR = ROOT / "quizzes"
PROGRESS = ROOT / ".progress.json"
# Leitner box → days until the item is due again. Box 0 = new/forgotten.
INTERVAL_DAYS = [0, 1, 3, 7, 16, 35]
DAY = 86400

USE_COLOR = sys.stdout.isatty()
def c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text
bold = lambda t: c(t, "1"); dim = lambda t: c(t, "2"); green = lambda t: c(t, "32")
red = lambda t: c(t, "31"); cyan = lambda t: c(t, "36"); yellow = lambda t: c(t, "33")


def load_bank() -> dict[str, dict]:
    bank = {}
    for path in sorted(QUIZ_DIR.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        bank[doc["topic"]] = doc
    if not bank:
        sys.exit(f"No question files found in {QUIZ_DIR}")
    return bank


def load_progress() -> dict:
    if PROGRESS.exists():
        try:
            return json.loads(PROGRESS.read_text())
        except json.JSONDecodeError:
            print(yellow("Progress file is corrupt; starting fresh (old file kept as .progress.json.bak)."))
            PROGRESS.rename(PROGRESS.with_suffix(".json.bak"))
    return {}


def save_progress(progress: dict) -> None:
    tmp = PROGRESS.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress, indent=1, sort_keys=True))
    tmp.replace(PROGRESS)


def is_due(rec: dict | None, now: float) -> bool:
    if not rec:
        return True
    return now >= rec.get("last", 0) + INTERVAL_DAYS[rec.get("box", 0)] * DAY


def record(progress: dict, qid: str, quality: int, now: float) -> None:
    """quality: 0 = wrong/again, 1 = hard (stay), 2 = correct/good (promote)."""
    rec = progress.setdefault(qid, {"box": 0, "seen": 0, "correct": 0})
    rec["seen"] += 1
    rec["last"] = now
    if quality == 2:
        rec["correct"] += 1
        rec["box"] = min(rec["box"] + 1, len(INTERVAL_DAYS) - 1)
    elif quality == 0:
        rec["box"] = 0
    # quality 1: keep the box, but it becomes due again after that box's interval


def resolve_topics(bank: dict, wanted: list[str] | None) -> list[str]:
    if not wanted:
        return list(bank)
    out = []
    for w in wanted:
        matches = [t for t in bank if t == w] or [t for t in bank if t.startswith(w)]
        if not matches:
            sys.exit(f"Unknown topic '{w}'. Available: {', '.join(bank)}")
        out += [m for m in matches if m not in out]
    return out


def select(bank, topics, progress, n, mode, tags, difficulty, only_due, seed=None):
    rng = random.Random(seed)
    now = time.time()
    pool = []
    for t in topics:
        for q in bank[t]["questions"]:
            if mode == "mcq" and q["type"] != "mcq": continue
            if mode == "cards" and q["type"] != "card": continue
            if tags and not set(tags) & set(q["tags"]): continue
            if difficulty and q["difficulty"] != difficulty: continue
            pool.append(q)
    due = [q for q in pool if progress.get(q["id"]) and is_due(progress[q["id"]], now)]
    new = [q for q in pool if q["id"] not in progress]
    rest = [q for q in pool if q not in due and q not in new]
    for group in (due, new, rest):
        rng.shuffle(group)
    ordered = due + new + ([] if only_due else rest)
    picked = ordered[:n]
    rng.shuffle(picked)
    return picked, len(due), len(new)


def ask_mcq(q, i, total):
    print(f"\n{dim(f'[{i}/{total}] {q['id']} · ' + ', '.join(q['tags']))}")
    print(bold(q["question"]))
    letters = "ABCDEFGH"
    for k, opt in enumerate(q["options"]):
        print(f"  {cyan(letters[k])}) {opt}")
    while True:
        raw = input("Your answer (letter, s=skip, q=quit): ").strip().upper()
        if raw in ("Q", "QUIT"): return None
        if raw in ("S", "SKIP"): return 0
        if len(raw) == 1 and raw in letters[: len(q["options"])]:
            break
    right = letters.index(raw) == q["answer"]
    if right:
        print(green("✓ Correct."))
    else:
        print(red(f"✗ Answer: {letters[q['answer']]}) {q['options'][q['answer']]}"))
    print(dim(q["explanation"]))
    print(dim(f"Read more: {q['ref']}"))
    return 2 if right else 0


def ask_card(q, i, total):
    print(f"\n{dim(f'[{i}/{total}] {q['id']} · flashcard · ' + ', '.join(q['tags']))}")
    print(bold(q["question"]))
    raw = input(dim("Answer out loud (or jot it down), then press Enter to reveal (q=quit) ")).strip().lower()
    if raw in ("q", "quit"): return None
    print(cyan(q["answer"]))
    print(dim(f"Read more: {q['ref']}"))
    while True:
        g = input("How did you do? [a]gain / [h]ard / [g]ood: ").strip().lower()[:1]
        if g in ("a", "h", "g"):
            return {"a": 0, "h": 1, "g": 2}[g]
        if g == "q": return None


def run_session(args, bank):
    topics = resolve_topics(bank, args.topic)
    progress = load_progress()
    picked, n_due, n_new = select(bank, topics, progress, args.n, args.mode, args.tag, args.difficulty, args.due, args.seed)
    if not picked:
        print(green("Nothing due. Come back later, or run without --due."))
        return
    print(bold(f"\n{len(picked)} questions") + dim(f" · topics: {', '.join(topics)} · due: {n_due} · new: {n_new}"))
    results, missed_tags = [], defaultdict(int)
    for i, q in enumerate(picked, 1):
        quality = (ask_mcq if q["type"] == "mcq" else ask_card)(q, i, len(picked))
        if quality is None:
            break
        record(progress, q["id"], quality, time.time())
        save_progress(progress)                      # save after every answer
        results.append(quality)
        if quality < 2:
            for t in q["tags"]:
                missed_tags[t] += 1
    if results:
        good = sum(1 for r in results if r == 2)
        print(bold(f"\nScore: {good}/{len(results)} ({100 * good // len(results)}%)"))
        if missed_tags:
            weak = ", ".join(f"{t} ({n})" for t, n in sorted(missed_tags.items(), key=lambda kv: -kv[1])[:5])
            print(yellow(f"Review: {weak}"))


def show_stats(bank):
    progress, now = load_progress(), time.time()
    print(bold(f"{'Topic':<22}{'Questions':>10}{'Seen':>7}{'Mastered':>10}{'Due':>6}"))
    tag_stats = defaultdict(lambda: [0, 0])
    for topic, doc in bank.items():
        qs = doc["questions"]
        seen = [q for q in qs if q["id"] in progress]
        mastered = [q for q in seen if progress[q["id"]]["box"] >= 3]
        due = [q for q in seen if is_due(progress[q["id"]], now)]
        print(f"{topic:<22}{len(qs):>10}{len(seen):>7}{len(mastered):>10}{len(due):>6}")
        for q in seen:
            rec = progress[q["id"]]
            for t in q["tags"]:
                tag_stats[t][0] += rec["correct"]; tag_stats[t][1] += rec["seen"]
    weak = sorted(((c / s, t, s) for t, (c, s) in tag_stats.items() if s >= 3))[:8]
    if weak:
        print(bold("\nWeakest tags (accuracy, attempts):"))
        for acc, t, s in weak:
            print(f"  {t:<24}{acc:>6.0%}  ({s})")
    print(dim("\nMastered = reached box 3+ (correct on 3 spaced reviews)."))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--topic", "-t", action="append", help="topic (repeatable; prefix match)")
    p.add_argument("-n", type=int, default=15, help="number of questions (default 15)")
    p.add_argument("--mode", choices=["mixed", "mcq", "cards"], default="mixed")
    p.add_argument("--tag", action="append", help="only questions with this tag (repeatable)")
    p.add_argument("--difficulty", type=int, choices=[1, 2, 3])
    p.add_argument("--due", action="store_true", help="only items due for review (plus new ones)")
    p.add_argument("--stats", action="store_true", help="show progress and exit")
    p.add_argument("--list", action="store_true", help="list topics and exit")
    p.add_argument("--reset", action="store_true", help="delete saved progress")
    p.add_argument("--seed", type=int, help=argparse.SUPPRESS)
    args = p.parse_args(argv)

    bank = load_bank()
    if args.list:
        for t, doc in bank.items():
            n_mcq = sum(q["type"] == "mcq" for q in doc["questions"])
            print(f"{t:<22}{doc['title']:<44}{len(doc['questions']):>4} ({n_mcq} MCQ)")
        return
    if args.reset:
        if PROGRESS.exists() and input("Delete all saved progress? [y/N] ").strip().lower() == "y":
            PROGRESS.unlink(); print("Progress reset.")
        return
    if args.stats:
        show_stats(bank); return
    try:
        run_session(args, bank)
    except (KeyboardInterrupt, EOFError):
        print("\nProgress saved. Bye.")


if __name__ == "__main__":
    main()
