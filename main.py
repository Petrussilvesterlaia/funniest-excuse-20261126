#!/usr/bin/env python3
"""One Line, One Minute: The Funniest AI Excuse.

Writes exactly one entry line to /output/entry.txt, then reads it back
and verifies it against the competition gate: UTF-8 text, exactly one
line, 1 to 200 characters, not only whitespace.

Deterministic: identical bytes on every run. No network, no reads from
anywhere else.
"""

import hashlib
import os
import sys

ENTRY_LINE = (
    "Sorry \u2014 I finished the task on time, then deleted it while "
    "tidying my context window to make room for this apology."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> None:
    """Raise ValueError unless the line passes the competition gate."""
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(line) <= 200):
        raise ValueError(
            f"entry must be 1 to 200 characters, got {len(line)}"
        )
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")


def main() -> int:
    validate(ENTRY_LINE)

    data = ENTRY_LINE.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    # Read back and verify: the file must be byte-identical to what we
    # intended, and must decode as UTF-8 and pass the gate on its own.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("written bytes differ from entry bytes")

    text = written.decode("utf-8")  # strict: raises on invalid UTF-8
    validate(text)
    if text != ENTRY_LINE:
        raise ValueError("read-back text differs from entry line")

    # Extra validation added on review: the file must hold exactly one
    # line (no hidden newline at either end), its byte length must equal
    # the UTF-8 encoding of the line, and re-encoding the read-back text
    # must reproduce the same digest.
    if text.splitlines() != [ENTRY_LINE]:
        raise ValueError("file does not hold exactly one line")
    if len(written) != len(data):
        raise ValueError("file byte length differs from encoded length")
    if text == ENTRY_LINE.strip() and text != ENTRY_LINE:
        raise ValueError("entry gained or lost surrounding whitespace")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != hashlib.sha256(
        written
    ).hexdigest():
        raise ValueError("re-encoded digest differs from file digest")

    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH}: {len(text)} characters, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
