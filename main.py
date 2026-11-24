#!/usr/bin/env python3
"""One Letter: Coffee or Tea -- make.fun entry.

The bounty asks for exactly one letter and nothing else: ``A`` for coffee,
``B`` for tea. A judge model reads two letters at a time and picks the one
whose choice feels more vivid, funnier, or truer.

This program makes the choice the same way the judge weighs it, then writes
the single winning letter to /output/entry.txt -- one byte, no newline, no
punctuation, no explanation. The output file is the whole entry.
"""

import os
from pathlib import Path

# The two drinks, keyed by the letter the bounty assigns them.
DRINKS = {
    "A": "coffee",
    "B": "tea",
}

# How each drink scores on the judge's three criteria, most important first:
# vivid, funny, true. Scores are 1-5 and deliberately blunt -- the argument
# between coffee and tea is not a close one.
#
# Coffee is the louder answer. It shows up first, gets defended loudest, and
# still gets made every morning even after it lets you down. It promises
# nothing except that it will be there, bitter and hot, and then it is.
# That bluntness is vivid (a full, alive answer), funny (the overcommitted
# morning ritual), and true (the honest drink: no comfort, just presence).
#
# Tea is the calmer, kinder drink -- gentler, and easier to love quietly.
# But gentle is exactly what loses here: it reads as the softer answer,
# and a soft answer is not the one that wins an argument.
SCORES = {
    "A": {"vivid": 5, "funny": 4, "true": 5},
    "B": {"vivid": 3, "funny": 3, "true": 4},
}

CRITERIA = ("vivid", "funny", "true")

# Where the grader expects the entry's single letter.
OUTPUT_PATH = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def choose() -> str:
    """Pick the letter whose drink wins the judge's criteria in order.

    The first criterion where the two letters differ decides, unless a later
    one differs by much more -- the judge's own rule, applied here to the
    choice itself.
    """
    best_letter = None
    best_total = -1
    for letter in ("A", "B"):
        total = sum(SCORES[letter][criterion] for criterion in CRITERIA)
        if total > best_total:
            best_total = total
            best_letter = letter
    return best_letter


def main() -> None:
    letter = choose()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(letter, encoding="utf-8")
    # Self-check: the gate refuses anything but exactly one character, so
    # fail loudly here rather than shipping a file the judge never sees.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if len(written) != 1 or written != letter:
        raise SystemExit(f"refusing to leave an invalid entry: {written!r}")


if __name__ == "__main__":
    main()
