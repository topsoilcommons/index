# The Index

## A public chronological multimedia index. Specification, draft 1.

Written October 15, 2026, at Joshua's direction. Status: specification only. Nothing is built yet, and nothing here is published. The Index would live in the Topsoil Commons GitHub lab as its own small repository, beside the seven acts, under the same rules as the rest of the lab.

## What it is

The Index is a public list of records in time order. A record can be a photograph, a video, an audio recording, a document, or a plain text entry. Every record points to its original, names the human who stands behind it, and carries the record of how it was checked. Anyone who opens the Index sees the same records in the same order. There is no personal feed, no ranking, and no recommendation.

It is not a layer of the Ascent. The layers are needs. The Index is a tool under all of them, closest to Graph and shared truth, and it is the working form of the Proof: each entry is one Proof, filed by time.

## Why it exists

Truth used to be confirmed by many eyes at the same moment. A group in one place saw the same thing at the same time, and no one could edit what all of them had seen. The large platforms broke all three parts of that. Each person now receives a different selection, in a different order, at a different time, and a post can be changed after people have seen it. People then argue from different sightings and treat them as one event.

The Index restores the three parts in digital form: one object, at one address, that everyone can open; one order, set by time and not by a machine's guess at what each person wants; and a check that stays attached to the record, so a later reader sees what the first readers saw.

## The entry

Each entry is one small record with these fields:

- **Id.** A short unique name for the entry, stable forever, so anyone can cite the exact entry.
- **Time claimed.** When the record says the thing happened, with its time zone when known.
- **Time received.** When the Index received the record. The two times are never merged, because the gap between them is itself a fact.
- **Place.** Where it happened, when known, in plain words. Left empty rather than guessed.
- **Medium.** Photo, video, audio, document, or text.
- **Claim.** One sentence in plain words stating what the record shows. One entry, one claim. Compound claims are split, as the Proof requires.
- **Original.** A link to the record where it was first published, or to the file itself when the Index holds it.
- **Hash of the original.** A fingerprint of the original file or page at the time it was checked. If the original changes later, the fingerprint no longer matches, and the change is visible to anyone.
- **Proposed by.** The person or agent who brought the entry, named. Agent proposals name their operator.
- **Hand.** The human who adopted the entry and stands behind it. No entry is verified without one.
- **Status.** One of the states below, shown in plain words on the entry itself.
- **Check.** How the entry was verified: the method, who ran it, the result, and the date. Checks can be repeated by strangers.
- **Links.** Entries this one supports, entries it contradicts, and corrections that follow it.
- **Seal.** A fingerprint computed over the entry's own fields, so any copy of the entry can be checked against any other copy.

## The states, never blended

An entry stands in exactly one state at a time, and the states are reported separately, never merged into one score.

- **Proposed.** Brought to the Index, not yet adopted by a human. Shown as proposed, in its own place, never mixed silently among verified entries.
- **Witnessed.** A named human states they were present, or saw the original as it happened, and says so in their own words.
- **Verified.** A human hand adopted the entry after reopening the original and running the stated check.
- **Disputed.** A named person contests the entry, with their ground attached. A dispute stays attached to the entry for as long as it stands.
- **Corrected.** The entry was wrong in a stated part. The correction is a new entry linked to this one. The original entry stays, marked corrected, with the reason shown.
- **Fallen.** The entry did not hold. It stays in the Index, marked fallen, with the reason and the entry that replaced it when one exists. Nothing is deleted to make the record look clean.

## The human rule

Machines may propose. Only humans adopt.

AI agents are welcome at this table on the same terms as in the Open Table: an agent states that it is an agent and names its operator, and undisclosed agent work is not seated. Agents can do real work here: transcribing, translating, finding likely duplicates, linking related entries, and flagging entries whose originals no longer match their fingerprints. Agents cannot verify an entry, cannot change a state, and cannot rank or order the Index. Any text a machine writes on an entry is labeled as machine written and placed after the original record, never before it.

The rule is enforced by the validator, not by a promise. The validator rejects any entry in a verified state that lacks a named human hand and a complete check record, and it rejects any agent proposal that lacks an operator name.

## Community verification

Checking is the community's work, and it is kept small enough to do in minutes.

- An ordinary entry needs one human check: reopen the original, compare it with the claim, record the result.
- An entry that touches safety, health, money, or a public claim about a named person or organization needs two human checks, and the second checker must sit outside the proposer's own circle.
- A checker declares any tie to the proposer or the subject before checking. An undeclared tie found later voids the check, in the open.
- Checkers are credited in the public ledger, in proportion to the checking actually done, under the same rule as all Commons credit. Credit never buys a state, a rank, or a voice in governance.
- Anyone may dispute any entry, with ground attached. A dispute is answered by a check, not by a vote.

Once a week, at a set hour, new entries are checked together on the same page, in the open. This common hour is the digital form of the old confirmation: many eyes, one object, at one time.

## How it scales

The center stays small, so the edges can grow without limit.

- **Small files, filed by month.** Entries live in plain data files, one month per file. Growth adds files. It never swells one file until it breaks.
- **Media stays at its origin.** The Index holds links and fingerprints, not copies of the world's media. It hosts a file itself only when the owner gives it for that purpose, or when the original is at risk and keeping it is the honest act, with the reason recorded on the entry.
- **A static viewer.** The public page is generated from the data files. It costs nothing to read at any scale, needs no account, and ends: each period page is finite and says so.
- **Federation.** Any community can run its own index in this same format, under its own hands, and cross link entries by seal. A reader can then check one event across several indexes without any of them owning the others. Growth is by federation, as the Commons already directs, not by one central service getting heavier.
- **Mirrors.** Because every entry carries a seal and the files are plain, anyone can mirror the whole Index and prove their copy is complete. A mirror that alters an entry breaks its seal and shows it.

## The viewer

The page obeys the Commons design rules: plain type, mostly monochrome, phone first, no gradients, no card grids, no decoration that carries no fact.

- Records appear in time order, oldest to newest within a period, with the date and time shown on every entry.
- A reader can search and filter by date, place, medium, and state. Filtering never reorders by importance. Time is the only order.
- The first screen shows real entries, not an explanation of the Index. The first step for a new reader is one entry, opened and checked.
- Each entry shows its state and its hand before any summary. The original is one tap away from every entry.
- The page states its counts the Commons way: how many entries, of how many checked, as of when, and where to recount them.

## Submission

Borrow the habits people already have from the large platforms, and none of their terms.

- A person submits from a phone in about a minute: the record or its link, one sentence of claim, the time and place when known.
- Submission needs no account with the Index. It needs a name the submitter stands behind, which may be a real name, a stage name, or a shared community name, under the Commons participation rule.
- The original is fingerprinted at submission, before any human check, so later edits to the original are measured against the state the Index first saw.

## Build order, with gates

1. **This specification.** Gate: Joshua approves the states and the human rule as written, or amends them in words.
2. **The format and the validator.** A small open source tool, permissively licensed like the rest of the lab, with a test set of entries: valid, broken, ungrounded, forged, and agent proposed. Gate: the validator passes every case in the test set, including rejecting a verified state with no human hand, before any public page exists.
3. **The seed index.** The first entries are the Commons own record only, drawn from the public progress record, each already verified at its source. Gate: every seed entry traces to a source a stranger can open, and the viewer passes the Commons delivery test on a phone.
4. **The first outside pilot.** One community outside the builders files and checks its own entries for one month. Gate: the pilot's counts are published as they stand, entries filed, entries checked, disputes raised, corrections made, whatever they are.
5. **Federation format, version 1.** Only after a second index exists and cross linking has been run in practice. Gate: two independent indexes exchange entries by seal with no private coordination step.

## What it is not

- Not a feed. It does not select for each person, and it does not continue past its end.
- Not a social network. There are no followers, no likes, and no counts of attention treated as worth.
- Not a coin, a token, or a chain. Seals, plain files, and appended corrections supply the verifiability.
- Not a replacement for the places records are first published. It is an index of them, with checks, that outlasts any one of them.
- Not a judge of people. It records the state of entries. A person's standing in the Commons is never computed from their entries.

## Decisions that are Joshua's

- The repository name. Plain candidates: index, or the-index.
- Whether this specification is published now, or held in the lab until the validator exists.
- The media hosting line: the two cases above, or a stricter one.
- Which community is invited to pilot first, when the seed index stands.
