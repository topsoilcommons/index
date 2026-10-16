# The 110 percent checklist: the Index

State as of October 15, 2026. Every line carries its evidence; a line without evidence does not count as done.

## 100 percent: completeness

- [x] SPEC.md present, byte identical to the approved specification in the Commons working files
- [x] FORMAT.md present, with its state table generated from format.json
- [x] format.json present as the single source for fields, media, checks, links, and the six states
- [x] README.md present and accurate against the tools in this repo
- [x] LICENSE present (MIT)
- [x] COLLABORATE.md present
- [x] CONTRIBUTING.md present
- [x] AGENTS.md present
- [x] .nojekyll present
- [x] Validator present: tools/validate.py, Python standard library only
- [x] Viewer generator present: tools/build_viewer.py
- [x] Viewer present: index.html, generated from the data files
- [x] Seed data present: 12 entries in entries/2026-10.json, counted from that file on October 15, 2026
- [x] Proposal queue present: 1 agent proposal in proposals/2026-10.json, counted from that file on October 15, 2026, left in proposed state with no human hand

## The extra 10 percent

- [x] CI workflow present: validator, format check, fixture tests, and viewer check
- [x] Fixture corpus present: 6 cases under tests/fixtures, counted by tests/run_tests.py on October 15, 2026
- [x] Repository pushed and verified against the remote: local and remote main matched at commit e2f2148 on October 15, 2026
- [ ] Live page answering at https://topsoilcommons.github.io/index/
- [ ] Repository description and topics set
- [ ] Good first issues open, sized in hours
- [ ] Tagged release v0.1 once CI is green

## Verification baseline (October 15, 2026)

- The validator passes the seed entries and the proposal queue.
- The fixture runner passes all 6 cases: the valid case is accepted, and each broken case is rejected for its stated reason.
- The generated format table matches format.json.
- The generated viewer matches the data files.
- Hardening, October 16, 2026: every standing entry carries a chain record computed by tools/build_chain.py; chain.json publishes the head hash and count of each queue (12 adopted entries, 1 proposal); SECURITY.md states the threat model and the limits; the fixture corpus stands at 9 cases, with tampered-entry, removed-entry, and reordered-entries each rejected for the chain error alone.
- Seed states, counted from entries/2026-10.json on October 15, 2026: 11 entries stand verified and 1 entry stands corrected.
- Seed media, counted from entries/2026-10.json on October 15, 2026: 6 entries are text, 1 entry is image, and 5 entries are page.

## What remains

- The first outside pilot: one community outside the builders files and checks its own entries for one month.
- Federation format version 1, only after a second index exists and cross linking has been run in practice.
- A fluent human check is not needed for this seed, which is in English only.
