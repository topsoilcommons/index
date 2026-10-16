#!/usr/bin/env python3
"""Build or check the hash chain over the Index data files.

With no arguments, this writes the chain record into every entry under
entries/ and proposals/, and writes chain.json at the repository root
with each queue's head hash and entry count.

With --root PATH, it chains the entries/ and proposals/ folders under
PATH instead, and writes no root file. The fixture corpus and the
starter kit are chained this way.

With --check, it writes nothing and fails if any stored chain record,
or chain.json on a default run, differs from a fresh computation.
"""

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from chain import chain_state, root_record  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def dump(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def run(root, check):
    state = chain_state(root)
    problems = []
    for queue_state in state.values():
        for path, data in queue_state["files"].items():
            rendered = dump(data)
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != rendered:
                if check:
                    problems.append(f"{path}: chain records differ from a fresh computation")
                else:
                    path.write_text(rendered, encoding="utf-8")
                    print(f"Chained {path}")
    return state, problems


def main(argv):
    check = "--check" in argv
    roots = [Path(arg) for arg in argv[1:] if arg != "--check"]
    default_run = not roots
    if default_run:
        roots = [ROOT]
    problems = []
    for root in roots:
        state, found = run(root, check)
        problems.extend(found)
        if default_run:
            record_path = root / "chain.json"
            rendered = dump(root_record(state))
            current = (
                record_path.read_text(encoding="utf-8") if record_path.exists() else None
            )
            if current != rendered:
                if check:
                    problems.append(f"{record_path}: the published root differs from a fresh computation")
                else:
                    record_path.write_text(rendered, encoding="utf-8")
                    print(f"Wrote {record_path}")
    if problems:
        for problem in problems:
            print(f"FAIL {problem}")
        return 1
    if check:
        print("PASS: every chain record matches a fresh computation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
