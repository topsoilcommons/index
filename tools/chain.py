"""The hash chain over Index entries.

One chain runs over the adopted entries in entries/, in file order:
monthly files in name order, entries in file order inside each file.
A second, separate chain runs over the proposal queue in proposals/
in the same order. No entry stands in both chains.

Each entry carries a chain record with two fields:

- previous: the chain hash of the entry before it in its queue, or
  null for the first entry in the queue.
- hash: SHA-256 over the canonical JSON of one object holding the
  entry itself, without its chain record, under the key "entry", and
  the previous value under the key "previous".

Canonical JSON is the same encoding the seal uses: UTF-8, object keys
sorted at every level, arrays kept in file order, comma and colon
separators with no spaces, and no trailing newline.

The chain is computed by tools/build_chain.py and checked by
tools/validate.py. It is never written by hand.
"""

import hashlib
import json
from pathlib import Path


QUEUES = ("entries", "proposals")


def canonical_bytes(value):
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("utf-8")


def entry_content(entry):
    return {key: value for key, value in entry.items() if key != "chain"}


def chain_hash_for(entry, previous):
    payload = {"entry": entry_content(entry), "previous": previous}
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def queue_files(root, queue):
    folder = Path(root) / queue
    if not folder.is_dir():
        return []
    return sorted(folder.glob("*.json"))


def load_queue(root, queue):
    """Return a list of (path, data) pairs for one queue, in chain order."""
    loaded = []
    for path in queue_files(root, queue):
        data = json.loads(path.read_text(encoding="utf-8"))
        loaded.append((path, data))
    return loaded


def compute_records(entries):
    """Return the chain records for entries already standing in chain order."""
    records = []
    previous = None
    for entry in entries:
        digest = chain_hash_for(entry, previous)
        records.append({"previous": previous, "hash": digest})
        previous = digest
    return records


def chain_state(root):
    """Compute the chain over both queues under root, without writing.

    Returns {queue: {"count": int, "head": hash or None,
    "files": {path: data with chain records set}}}.
    """
    state = {}
    for queue in QUEUES:
        loaded = load_queue(root, queue)
        flat = [entry for _path, data in loaded for entry in data["entries"]]
        records = compute_records(flat)
        files = {}
        index = 0
        for path, data in loaded:
            entries = []
            for entry in data["entries"]:
                chained = dict(entry)
                chained["chain"] = records[index]
                index += 1
                entries.append(chained)
            files[path] = {
                "format_version": data["format_version"],
                "month": data["month"],
                "entries": entries,
            }
        head = records[-1]["hash"] if records else None
        state[queue] = {"count": len(flat), "head": head, "files": files}
    return state


def root_record(state):
    return {
        "algorithm": "SHA-256",
        "generated_by": "tools/build_chain.py",
        "adopted_entries": {
            "count": state["entries"]["count"],
            "head": state["entries"]["head"],
        },
        "proposals": {
            "count": state["proposals"]["count"],
            "head": state["proposals"]["head"],
        },
    }
