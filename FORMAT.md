# The Index entry format

This file states the format in machine terms. The machine readable source is [format.json](format.json). The field list, media list, check fields, link fields, and six states are defined there once. This document explains them, [tools/validate.py](tools/validate.py) enforces them, and the viewer key is generated from the same file.

## File layout

- `entries/YYYY-MM.json` holds adopted and settled entries for one month.
- `proposals/YYYY-MM.json` holds the agent and human proposal queue for one month.
- A proposal file may carry only entries in the proposed state.
- An entries file may not carry entries in the proposed state.
- Each file is one JSON object with `format_version`, `month`, and `entries`.
- The `month` value must match the file name.
- Entries inside a monthly file stand in chronological order by `time_claimed`.

## Entry fields

An entry is one JSON object with every field below, plus `seal` and the `chain` record defined under The chain below. No other fields are allowed.

| Field | Machine rule |
| --- | --- |
| `id` | A string of lowercase letters, numbers, and hyphens. It is unique across entries and proposals. |
| `time_claimed` | An ISO 8601 date or datetime stating when the record says the thing happened. |
| `time_received` | An ISO 8601 date or datetime stating when the Index received the record. |
| `place` | A string in plain words, or null when the place is not known. |
| `medium` | One of the media values in format.json: text, image, page, photo, video, audio, or document. |
| `claim` | One string carrying exactly one claim in one sentence. Decimal points inside numbers do not count as sentence endings. |
| `original_url` | An HTTP or HTTPS address for the original record or the repository file that serves it. |
| `original_hash` | An object with `algorithm` and `value`, as defined below. |
| `proposed_by` | An object with `kind`, `name`, and `operator`, as defined below. |
| `hand` | The named human who adopted the entry, or null when no human has adopted it. |
| `state` | One of the six states in format.json. |
| `check` | A complete check object, or null. |
| `links` | An object with `supports`, `contradicts`, `corrects`, and `corrections`, each a list of entry ids. |
| `seal` | The SHA-256 seal defined below. |
| `chain` | An object with `previous` and `hash`, as defined below. |

## Proposer

`proposed_by.kind` is `human` or `agent`.

- A human proposer carries `operator` as null.
- An agent proposer must carry a nonempty `operator` string.
- A verified entry proposed by an agent still needs a named human `hand` and a complete `check`.

## Check

A check object has exactly four nonempty string fields from format.json: `method`, `checked_by`, `result`, and `date`. The date is an ISO 8601 date or datetime.

An entry in the witnessed or verified state must have a named human hand and a complete check. Other states may carry a complete check when one has been run.

## The six states

<!-- states:begin -->

| State | What it means |
| --- | --- |
| proposed | Brought to the Index and not yet adopted by a human. |
| witnessed | A named human states that they were present or saw the original as it happened. |
| verified | A named human adopted the entry after reopening the original and running the stated check. |
| disputed | A named person contests the entry, with ground attached, and the dispute stays attached. |
| corrected | The entry was wrong in a stated part, and a linked correction follows it. |
| fallen | The entry did not hold, and its reason and replacement stay shown. |

<!-- states:end -->

The state names in this table, the validator messages, and the viewer key all come from format.json.

## Hash of the original

`original_hash.algorithm` is `SHA-256`. `original_hash.value` is 64 lowercase hexadecimal characters.

The input is the byte sequence of the original at the time of the check:

- For a file in a repository, the input is that file's bytes.
- For a page served from a repository, the input is the serving file's bytes in that repository.
- For another web page, the input is the response body bytes received at the check.

A later change to the original changes the hash. The stored hash is the state the check saw.

## The seal

The seal is SHA-256 over the canonical JSON of every entry field except `seal`.

Canonical JSON means:

1. Build one object with the entry fields listed in format.json, in their stored values.
2. Encode it as JSON in UTF-8.
3. Sort object keys at every level.
4. Keep arrays in file order.
5. Use comma and colon separators with no spaces.
6. Add no trailing newline.
7. Hash those bytes with SHA-256 and write the result as 64 lowercase hexadecimal characters.

Changing any content field without changing the seal makes validation fail.

## The chain

Every entry also carries a `chain` record with two fields, `previous` and `hash`. The chain is defined in format.json and computed by [tools/build_chain.py](tools/build_chain.py). It is never written by hand.

- One chain runs over the entries queue and a second, separate chain runs over the proposals queue.
- Inside a queue, the order is the file order of the Index itself: monthly files in name order, entries in file order inside each file.
- `previous` is the chain hash of the entry before this one in its queue, or null for the first entry in the queue.
- `hash` is SHA-256 over the canonical JSON of one object holding the entry without its chain record under the key `entry`, and the previous value under the key `previous`. Canonical JSON means the same encoding the seal uses.

The seal binds one entry to its own fields. The chain binds each entry to its place in the order, so an entry that is edited, removed, or moved breaks the chain at that point and at every point after it, unless the whole chain after it is computed again. The published root, [chain.json](chain.json) at the repository root, holds the head hash and the entry count of each queue, regenerated by the same tool. A mirror holder compares that root with a fresh computation over their own copy. What the chain proves, and what it does not, is stated in [SECURITY.md](SECURITY.md).

## Validation

Run:

```bash
python3 tools/validate.py
```

The validator reads format.json, checks every file under `entries/` and `proposals/`, prints one plain verdict per file, and exits nonzero on any failure. It checks required fields, one claim per entry, state membership, human hands and complete checks where a state requires them, agent operators, original ground, seals, chain records, unique ids, link targets, file months, and chronological order.

Run `python3 tools/build_chain.py` after any change to the data files to write the chain records and the published root, and `python3 tools/build_chain.py --check` to confirm the stored chain matches a fresh computation without writing.
