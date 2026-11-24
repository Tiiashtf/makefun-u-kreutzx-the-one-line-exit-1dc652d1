#!/usr/bin/env python3
"""The One-Line Exit — make.fun entry.

Writes a single one-line resignation letter to /output/entry.txt.

The letter's whole job is to be funny in one line. The joke is the gap
between the job advert's promise and the job itself: the advert said
"fast-paced environment", and the reality turned out to be a haunted
house with Wi-Fi. One sentence, one specific voice, no padding — the
kind of line a colleague would forward to the group chat.
"""

import os
import shutil
import sys

LETTER = (
    "Effective today, I resign \u2014 the job description said "
    "'fast-paced environment', not 'haunted house with Wi-Fi'."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")
MAX_CHARS = 140


def main() -> int:
    if not 1 <= len(LETTER) <= MAX_CHARS:
        print(
            f"letter is {len(LETTER)} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if "\n" in LETTER or "\r" in LETTER:
        print("letter must be exactly one line", file=sys.stderr)
        return 1
    if not LETTER.strip():
        print("letter must not be only whitespace", file=sys.stderr)
        return 1

    # Never remove the output directory itself: the grader may run us
    # with a root-owned /output inside a sticky parent, where removing
    # the directory fails with EPERM. Create it if missing, clear only
    # the files inside it, then write.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LETTER + "\n")

    # Read it back and fail loudly if the bytes on disk differ from
    # the letter: a silent partial write would fail the gate with no
    # trace of why.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != (LETTER + "\n").encode("utf-8"):
        print("verification failed: entry.txt differs from the letter",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
