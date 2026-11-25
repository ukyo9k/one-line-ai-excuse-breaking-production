#!/usr/bin/env python3
"""Write the funniest one-line AI excuse for breaking production.

Writes exactly one line to $MAKEFUN_OUTPUT_DIR/entry.txt
(or /output/entry.txt when the variable is unset).
"""

import os
import sys

LINE = "I saw 'deploy to production' right next to 'delete production', and honestly the second one just sounded more decisive."

MAX_CHARS = 180


def validate(line: str) -> None:
    """Gate: one line, 1-180 chars, not only whitespace, valid UTF-8."""
    if not line or not line.strip():
        raise SystemExit("entry line is empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    # UTF-8 round-trip check.
    if line.encode("utf-8").decode("utf-8") != line:
        raise SystemExit("entry failed UTF-8 round-trip")


def main() -> None:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(payload)
    # Byte-identical repeat-run check: re-read and confirm the bytes
    # we just wrote match the payload exactly.
    with open(path, "rb") as f:
        if f.read() != payload:
            raise SystemExit("entry.txt bytes differ from expected payload")
    print(f"wrote {len(LINE)} chars / {len(payload)} bytes to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
