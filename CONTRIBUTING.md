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

## Ways in, by level

**First hour.** No experience with this project is assumed. Run python3 tools/validate.py and python3 tests/run_tests.py (9 fixture cases, all passing), then check one adopted entry against its original, by the steps above. One check by a new hand is a full contribution.

**First week.** Propose entries of your own, one claim each, in the current month file under proposals/. A named human adopts sound proposals into entries/, and adoptions and checks stand in the public record with your name on them.

**The deep end.** Every entry carries a place, and no view of the Index by place exists yet: the place layer is promised in SPEC.md and unbuilt. There is no measured figure to beat here; the honest problem is design under this project's own rules (one timeline for everyone, nothing ranked, nothing deleted) at a scale past the current 13 standing records.
