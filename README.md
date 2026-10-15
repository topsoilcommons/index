# The Index

A public chronological multimedia index for Aurora Commons.

First step: open the live page, pick the first entry, open its original, and compare it with the claim. The check takes about a minute.

Live page: https://auroracommons.github.io/index/

## What it is

The Index files records in time order. A record can be text, an image, a page, a photograph, a video, an audio recording, or a document. Each entry points to its original, carries a fingerprint of that original, names who proposed it, shows its state, and carries its check.

Everyone who opens the Index sees the same entries in the same order. It has no personal feed, no ranking, and no recommendation.

The full design is in [SPEC.md](SPEC.md). The machine format is in [FORMAT.md](FORMAT.md), with its single machine readable source in [format.json](format.json).

## The human rule

Machines may propose. Only humans adopt.

An agent may bring an entry to the proposal queue, transcribe, translate, find likely duplicates, link related entries, or flag an original whose fingerprint no longer matches. An agent cannot verify an entry, change a state, or order the Index. Every agent proposal names its operator.

The validator enforces the rule. A witnessed or verified entry without a named human hand and a complete check fails validation.

## The states

The six states are proposed, witnessed, verified, disputed, corrected, and fallen. Their definitions live once in format.json. FORMAT.md, the validator, and the viewer key all draw from that file.

The states are reported separately. They are never blended into one score. Corrections are new linked entries. Fallen and corrected entries stay visible with their reasons.

## Propose an entry

1. Find the original record and keep its address.
2. Write one claim in one sentence.
3. Add an entry to the current month file under `proposals/`, following FORMAT.md.
4. If you are an agent, state that in `proposed_by` and name your operator.
5. Run the validator.

A human adopter moves a sound proposal into `entries/`, adds their name as the hand, and records a complete check.

## Run the tools

```bash
python3 tools/validate.py
python3 tests/run_tests.py
python3 tools/build_format.py --check
python3 tools/build_viewer.py --check
```

After changing data, rebuild the public products:

```bash
python3 tools/build_format.py
python3 tools/build_viewer.py
```

The viewer is generated from the data files. Do not hand edit index.html.

## Files

- `entries/YYYY-MM.json`: entries adopted or settled, by month.
- `proposals/YYYY-MM.json`: the proposal queue, by month.
- `format.json`: the single source for fields, states, and rules the tools share.
- `tools/validate.py`: the validator, using only the Python standard library.
- `tools/build_viewer.py`: the viewer generator.
- `tools/build_format.py`: the state table generator for FORMAT.md.
- `tests/`: valid and broken fixtures with a runner.

## License

MIT. See [LICENSE](LICENSE). Copyright (c) 2026 Index contributors.

Advised by Groundskeeper.
