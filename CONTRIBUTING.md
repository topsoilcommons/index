# Contributing to the Index

Contributions are welcome. The main door takes minutes: propose one entry, or check one entry that is already here.

## Propose an entry

1. Open the original record.
2. Write one claim in one sentence.
3. Add the entry to the current month file under `proposals/`, following [FORMAT.md](FORMAT.md).
4. An agent must state that it is an agent and name its operator.
5. Run `python3 tools/validate.py` and `python3 tests/run_tests.py`.

A proposal does not become an entry until a named human adopts it and records a complete check.

## Check an entry

1. Pick an entry in `entries/`.
2. Open its original.
3. Recompute the original fingerprint when the original is a file, and recompute the entry seal with the rule in FORMAT.md.
4. Compare the claim with the original.
5. Open a pull request with the method, your name, the result, and the date.

## Ground rules

- One entry carries one claim.
- Never invent a time, a place, or a source.
- A correction is a new linked entry. The old entry stays marked corrected.
- A dispute needs ground attached.
- Credit may be a real name, a stage name, or a shared community name.

## Pull requests

Keep each request small and single purpose. State the evidence in the request: the original you opened, the check you ran, and the validator result.
