#!/usr/bin/env python3
"""Build the state table in FORMAT.md from format.json."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- states:begin -->"
END = "<!-- states:end -->"


def state_table():
    data = json.loads((ROOT / "format.json").read_text(encoding="utf-8"))
    lines = [
        "| State | What it means |",
        "| --- | --- |",
    ]
    for state in data["states"]:
        lines.append(f"| {state['name']} | {state['definition']} |")
    return "\n".join(lines)


def render():
    path = ROOT / "FORMAT.md"
    text = path.read_text(encoding="utf-8")
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END)
    return text[:start] + "\n\n" + state_table() + "\n\n" + text[end:]


def main(argv):
    rendered = render()
    path = ROOT / "FORMAT.md"
    if "--check" in argv:
        if path.read_text(encoding="utf-8") != rendered:
            print("FAIL FORMAT.md: the state table differs from format.json")
            return 1
        print("PASS FORMAT.md: the state table matches format.json")
        return 0
    path.write_text(rendered, encoding="utf-8")
    print("Wrote FORMAT.md from format.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
