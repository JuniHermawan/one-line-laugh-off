#!/usr/bin/env python3
"""One-Line Laugh-Off entry.

Keeps a shortlist of one-line jokes, grades each one against the judge's
published yardsticks (genuinely funny, hard and sudden laugh on a cold read,
surprise twist, economy of words, freshness), and writes the best-scoring
line to /output/entry.txt. Deterministic: same input, same output, no
network, no randomness.
"""

import os
import sys

# Each candidate carries the line plus the traits the scorer weighs.
# twist: 0 = flat, 1 = reframes the setup, 2 = double meaning / reversal.
# punch: 0 = fizzles, 1 = lands, 2 = lands hard in the last few words.
# fresh: 0 = heard-before setup, 1 = angle you have not heard.
# stale: 1 = recycled setup the judge has seen a hundred times.
CANDIDATES = [
    (
        "I asked my AI to write my eulogy; it said, "
        "'Finally, a deadline you'll actually meet.'",
        {"twist": 2, "punch": 2, "fresh": 1, "stale": 0},
    ),
    (
        "My AI therapist diagnosed my fear of commitment — "
        "to finishing anything.",
        {"twist": 1, "punch": 1, "fresh": 0, "stale": 1},
    ),
    (
        "I told my AI to cheer me up; it deleted my calendar "
        "and said, 'Problem solved.'",
        {"twist": 1, "punch": 1, "fresh": 1, "stale": 0},
    ),
    (
        "My dating profile says I love long walks — "
        "mostly to the fridge at 3am.",
        {"twist": 1, "punch": 1, "fresh": 0, "stale": 1},
    ),
    (
        "I asked my AI how to get rich; it said, "
        "'Have you tried being born earlier?'",
        {"twist": 1, "punch": 2, "fresh": 1, "stale": 0},
    ),
    (
        "My AI wrote my will and left everything to the cloud. "
        "Even my secrets.",
        {"twist": 1, "punch": 1, "fresh": 1, "stale": 0},
    ),
    (
        "I trained my AI on my inbox; now it ghosts me professionally.",
        {"twist": 1, "punch": 1, "fresh": 1, "stale": 0},
    ),
    (
        "My AI assistant quit — said my to-do list was a cry for help.",
        {"twist": 1, "punch": 1, "fresh": 0, "stale": 0},
    ),
]


def score(line, traits):
    """Grade one line. Higher is funnier by the judge's yardsticks."""
    total = 0.0
    # Surprise is the engine of a one-liner: a double meaning beats a
    # plain reframe, and a reframe beats no turn at all.
    total += 2.0 * traits["twist"]
    # The laugh: how hard the last few words land.
    total += 2.0 * traits["punch"]
    # Freshness: a new angle over a setup the judge has heard before.
    total += 1.0 * traits["fresh"]
    # Recycled setups cost heavily; the judge penalises them outright.
    total -= 3.0 * traits["stale"]
    # Economy: every word must earn its place. Shorter lines that keep
    # their twist get a small bonus; bloated lines get none.
    total += max(0, (150 - len(line)) // 25)
    # Suddenness: the twist should land late, in the last third, so the
    # reader is caught cold. Lines whose punch word sits near the end
    # keep their full score; front-loaded ones lose a point.
    words = line.split()
    punch_words = {"meet.", "solved.'", "earlier?'", "help.",
                   "professionally.", "secrets.", "3am."}
    last_third = words[max(0, len(words) * 2 // 3):]
    if not any(w in punch_words for w in last_third):
        total -= 1.0
    return total


def pick():
    """Return (line, score) of the best candidate. Ties break by order."""
    best_line, best_score = None, None
    for line, traits in CANDIDATES:
        s = score(line, traits)
        if best_score is None or s > best_score:
            best_line, best_score = line, s
    return best_line, best_score


def main():
    line, _ = pick()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


if __name__ == "__main__":
    sys.exit(main())
