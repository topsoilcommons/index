#!/usr/bin/env python3
"""Run the Index validator against the fixture corpus."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate.py"
FIXTURES = ROOT / "tests" / "fixtures"
CASES = [
    ("valid", 0, "PASS: 2 entries checked across 2 files"),
    ("missing-ground", 1, "original_url is required"),
    ("ungrounded-verified", 1, "original_hash value must be"),
    ("forged-seal", 1, "seal mismatch"),
    ("agent-proposal-without-operator", 1, "an agent proposer must name its operator"),
    ("verified-without-a-hand", 1, "requires a named human hand"),
]


def run_case(name):
    base = FIXTURES / name
    command = [
        sys.executable,
        str(VALIDATOR),
        str(base / "entries"),
        str(base / "proposals"),
    ]
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    failures = []
    for name, expected_code, expected_text in CASES:
        result = run_case(name)
        if result.returncode != expected_code:
            failures.append(
                f"{name}: expected exit {expected_code}, got {result.returncode}\n{result.stdout}"
            )
        elif expected_text not in result.stdout:
            failures.append(f"{name}: expected text not found: {expected_text}\n{result.stdout}")
        else:
            print(f"PASS {name}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS: {len(CASES)} fixture cases behaved as expected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
