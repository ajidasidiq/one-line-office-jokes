#!/usr/bin/env python3
"""One-Line Office Jokes — make.fun entry.

Writes a single fresh one-line joke about office life to /output/entry.txt.
The joke turns on a real office detail (the printer that only jams when a
deadline is near) and lands the laugh in the last few words.
"""

import os
import sys

ENTRY = "Our printer only jams when the deadline is in five minutes, like it read the email first."

OUTPUT_PATH = "/output/entry.txt"


def gate_check(text):
    """Mirror the competition gate: UTF-8 text, 1-199 chars, not only whitespace."""
    if not isinstance(text, str):
        return False, "entry is not text"
    if not (1 <= len(text) <= 199):
        return False, "entry must be 1-199 characters, got %d" % len(text)
    if not text.strip():
        return False, "entry must not be only whitespace"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    encoded = text.encode("utf-8")  # raises if not valid UTF-8
    if len(encoded) > 199:
        return False, "entry must be at most 199 bytes, got %d" % len(encoded)
    if any(ord(ch) < 32 for ch in text):
        return False, "entry must not contain control characters"
    if text != text.strip():
        return False, "entry must not have leading or trailing whitespace"
    return True, "ok"


def main():
    ok, reason = gate_check(ENTRY)
    if not ok:
        print("gate check failed: %s" % reason, file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Re-read and verify what landed on disk matches the entry exactly.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        print("verification failed: file contents differ from entry", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
