#!/usr/bin/env python3
"""Validate Index entry and proposal files.

The format data in format.json is the single source for the field list,
the media list, the check fields, and the six states.
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMAT_PATH = ROOT / "format.json"
FORMAT = json.loads(FORMAT_PATH.read_text(encoding="utf-8"))
ENTRY_FIELDS = FORMAT["entry_fields"]
CHECK_FIELDS = FORMAT["check_fields"]
LINK_FIELDS = FORMAT["link_fields"]
PROPOSER_FIELDS = FORMAT["proposer_fields"]
PROPOSER_KINDS = set(FORMAT["proposer_kinds"])
MEDIA = set(FORMAT["media"])
STATES = {state["name"]: state for state in FORMAT["states"]}
STATE_NAMES = [state["name"] for state in FORMAT["states"]]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MONTH_FILE = re.compile(r"^\d{4}-\d{2}\.json$")


def canonical_bytes(entry):
    content = {key: entry[key] for key in ENTRY_FIELDS}
    text = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("utf-8")


def seal_for(entry):
    return hashlib.sha256(canonical_bytes(entry)).hexdigest()


def parse_time(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        if value.endswith("Z"):
            parsed = datetime.fromisoformat(value[:-1] + "+00:00")
        else:
            parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def sentence_count(claim):
    masked = re.sub(r"(?<=\d)\.(?=\d)", "", claim)
    return sum(masked.count(mark) for mark in ".!?")


def complete_check(check):
    if not isinstance(check, dict):
        return False
    if set(check.keys()) != set(CHECK_FIELDS):
        return False
    return all(isinstance(check[key], str) and check[key].strip() for key in CHECK_FIELDS)


def load_file(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        return None, [f"{path}: cannot read JSON: {error}"]
    errors = []
    if not isinstance(data, dict):
        return None, [f"{path}: file must contain one JSON object"]
    if set(data.keys()) != {"format_version", "month", "entries"}:
        errors.append(f"{path}: file fields must be format_version, month, and entries")
    if data.get("format_version") != FORMAT["format_version"]:
        errors.append(f"{path}: format_version must be {FORMAT['format_version']}")
    if not isinstance(data.get("entries"), list):
        errors.append(f"{path}: entries must be a list")
        return data, errors
    if MONTH_FILE.match(path.name) and data.get("month") != path.stem:
        errors.append(f"{path}: month must match the file name {path.stem}")
    return data, errors


def validate_entry(path, entry, seen_ids, all_ids):
    label = f"{path}: {entry.get('id', 'entry without id')}"
    errors = []
    if not isinstance(entry, dict):
        return [f"{path}: each entry must be one JSON object"]
    expected = set(ENTRY_FIELDS) | {"seal"}
    if set(entry.keys()) != expected:
        missing = sorted(expected - set(entry.keys()))
        extra = sorted(set(entry.keys()) - expected)
        if missing:
            errors.append(f"{label}: missing required fields: {', '.join(missing)}")
        if extra:
            errors.append(f"{label}: unknown fields: {', '.join(extra)}")
        return errors

    entry_id = entry["id"]
    if not isinstance(entry_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", entry_id):
        errors.append(f"{label}: id must use lowercase letters, numbers, and hyphens")
    elif entry_id in seen_ids:
        errors.append(f"{label}: duplicate id {entry_id}")
    seen_ids.add(entry_id)

    claimed = parse_time(entry["time_claimed"])
    received = parse_time(entry["time_received"])
    if claimed is None:
        errors.append(f"{label}: time_claimed must be an ISO 8601 date or datetime")
    if received is None:
        errors.append(f"{label}: time_received must be an ISO 8601 date or datetime")
    if MONTH_FILE.match(path.name):
        for field in ("time_claimed", "time_received"):
            value = entry[field]
            if not isinstance(value, str) or not value.startswith(path.stem):
                errors.append(f"{label}: {field} must fall in {path.stem}")

    if entry["place"] is not None and not isinstance(entry["place"], str):
        errors.append(f"{label}: place must be a string or null")
    if entry["medium"] not in MEDIA:
        errors.append(f"{label}: medium must be one of {', '.join(sorted(MEDIA))}")

    claim = entry["claim"]
    if not isinstance(claim, str) or not claim.strip():
        errors.append(f"{label}: claim is required and must be one string")
    elif "\n" in claim or sentence_count(claim) != 1 or claim[-1] not in ".!?":
        errors.append(f"{label}: claim must carry exactly one claim in one sentence")

    original_url = entry["original_url"]
    if not isinstance(original_url, str) or not original_url.startswith(("http://", "https://")):
        errors.append(f"{label}: original_url is required as the ground link")
    original_hash = entry["original_hash"]
    if not isinstance(original_hash, dict) or set(original_hash.keys()) != {"algorithm", "value"}:
        errors.append(f"{label}: original_hash must carry algorithm and value as its ground fingerprint")
    else:
        if original_hash["algorithm"] != FORMAT["original_hash"]["algorithm"]:
            errors.append(f"{label}: original_hash algorithm must be {FORMAT['original_hash']['algorithm']}")
        if not isinstance(original_hash["value"], str) or not HEX64.match(original_hash["value"]):
            errors.append(f"{label}: original_hash value must be 64 lowercase hexadecimal characters")

    proposer = entry["proposed_by"]
    if not isinstance(proposer, dict) or set(proposer.keys()) != set(PROPOSER_FIELDS):
        errors.append(f"{label}: proposed_by must carry kind, name, and operator")
    else:
        if proposer["kind"] not in PROPOSER_KINDS:
            errors.append(f"{label}: proposer kind must be human or agent")
        if not isinstance(proposer["name"], str) or not proposer["name"].strip():
            errors.append(f"{label}: proposer name is required")
        if proposer["kind"] == "agent":
            if not isinstance(proposer["operator"], str) or not proposer["operator"].strip():
                errors.append(f"{label}: an agent proposer must name its operator")
        elif proposer["operator"] is not None:
            errors.append(f"{label}: a human proposer must carry operator as null")

    state = entry["state"]
    if state not in STATES:
        errors.append(f"{label}: state must be one of {', '.join(STATE_NAMES)}")
    if "proposals" in path.parts and state != "proposed":
        errors.append(f"{label}: proposal files may carry only the proposed state")
    if "entries" in path.parts and state == "proposed":
        errors.append(f"{label}: proposed entries belong in the proposals queue, not the entries file")

    hand = entry["hand"]
    if hand is not None and (not isinstance(hand, str) or not hand.strip()):
        errors.append(f"{label}: hand must be a named human or null")
    if state in {"witnessed", "verified"}:
        if not isinstance(hand, str) or not hand.strip():
            errors.append(f"{label}: a {state} entry requires a named human hand")
        if not complete_check(entry["check"]):
            errors.append(
                f"{label}: a {state} entry requires a complete check with "
                + ", ".join(CHECK_FIELDS)
            )
    if entry["check"] is not None and not complete_check(entry["check"]):
        errors.append(f"{label}: check must be null or complete with {', '.join(CHECK_FIELDS)}")
    if isinstance(entry["check"], dict) and complete_check(entry["check"]):
        if parse_time(entry["check"]["date"]) is None:
            errors.append(f"{label}: check date must be an ISO 8601 date or datetime")

    links = entry["links"]
    if not isinstance(links, dict) or set(links.keys()) != set(LINK_FIELDS):
        errors.append(f"{label}: links must carry {', '.join(LINK_FIELDS)}")
    else:
        for field in LINK_FIELDS:
            values = links[field]
            if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                errors.append(f"{label}: links.{field} must be a list of entry ids")
            else:
                for target in values:
                    if target not in all_ids:
                        errors.append(f"{label}: links.{field} names unknown entry id {target}")

    seal = entry["seal"]
    if not isinstance(seal, str) or not HEX64.match(seal):
        errors.append(f"{label}: seal must be 64 lowercase hexadecimal characters")
    elif seal != seal_for(entry):
        errors.append(f"{label}: seal mismatch")
    return errors


def collect_paths(arguments):
    paths = []
    if not arguments:
        candidates = [ROOT / "entries", ROOT / "proposals"]
    else:
        candidates = [Path(argument) for argument in arguments]
    for candidate in candidates:
        if candidate.is_dir():
            paths.extend(sorted(candidate.glob("*.json")))
        elif candidate.is_file():
            paths.append(candidate)
        else:
            print(f"FAIL {candidate}: path does not exist")
            return None
    return sorted(set(paths))


def main(argv):
    paths = collect_paths(argv[1:])
    if paths is None:
        return 2
    if not paths:
        print("FAIL: no JSON files found")
        return 2

    loaded = []
    all_errors = []
    all_ids = set()
    for path in paths:
        data, errors = load_file(path)
        all_errors.extend(errors)
        if data and isinstance(data.get("entries"), list):
            loaded.append((path, data))
            for entry in data["entries"]:
                if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                    all_ids.add(entry["id"])

    seen_ids = set()
    total = 0
    for path, data in loaded:
        errors = []
        previous = None
        for entry in data["entries"]:
            total += 1
            errors.extend(validate_entry(path, entry, seen_ids, all_ids))
            if isinstance(entry, dict):
                current = parse_time(entry.get("time_claimed"))
                if previous is not None and current is not None and current < previous:
                    errors.append(f"{path}: entries must be in chronological order by time_claimed")
                if current is not None:
                    previous = current
        if errors:
            all_errors.extend(errors)
            print(f"FAIL {path}: {len(errors)} error(s) across {len(data['entries'])} entries")
        else:
            print(f"PASS {path}: {len(data['entries'])} entries checked")

    if all_errors:
        for error in all_errors:
            print(f"ERROR {error}")
        print(f"FAIL: {len(all_errors)} error(s) across {total} entries in {len(paths)} files")
        return 1
    print(f"PASS: {total} entries checked across {len(paths)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
