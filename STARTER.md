# Start your own index

A starter kit for a community that wants to keep its own record the way this one is kept. Written for the person who would organize it. You do not need permission, an account with us, or any payment. You need a place, two people willing to check, and one month.

## What an index is

An index is a public list, in time order, of records your community files about its own place. Each entry carries one claim in one sentence, the original it rests on, a fingerprint of that original, the state the entry stands in, and the name of the human who adopted it. Nothing in the list is ranked. Time is the only order. When something turns out wrong, the correction is a new entry linked to the old one, and the old one stays where it was. A stranger can open any entry, follow it to its original, and run the same check you ran.

This repository is the first index kept this way. Yours would be the second kind of thing it was built for: not a branch of this one, but a sibling, standing under your own hand.

## The human rule

Machines may propose entries. Only humans adopt them. An entry becomes verified only when a named person reopens the original, runs the stated check, and stands behind the result with their own name, a real name, a stage name, or a shared community name. Any agent that proposes an entry must say it is an agent and name the human or organization that operates it. Undisclosed machine authorship is not seated. No one, human or machine, edits the past quietly, ranks the entries, or sells a state. That is the whole rule, and every tool in this kit exists to hold it.

## What you need

- A place your people share: a neighborhood, a school, a congregation, a town, a network.
- Two checkers. Checking is the scarce work, so the kit starts with two people, not one, and the second checker is never the person who proposed the entry they check.
- Somewhere to keep two small text files where your community can read them. A free repository account works. This whole index is plain files, and a phone is enough to run a cycle.

## The smallest first cycle

One month, five entries. Five is the whole first goal.

1. **Collect five records from your own place.** A photograph of a door with its hours. A page your town or school published. A notice your group sent. Records your people already trust or already doubt are both good material, because the index holds disputed and corrected entries as honestly as verified ones.
2. **File each one as a proposal.** Use the template in the `starter/` folder of this repository. One claim per entry, in one sentence. Give the original's address. Give its fingerprint, the SHA-256 hash of the original: if the original is a file, hash the file; free hash tools exist for every phone and computer, and the format document in this repository states the rule exactly.
3. **Check each proposal with your second person.** The checker reopens the original, compares it with the claim, and either adopts the entry, adding their name as its hand and the check they ran, or leaves it proposed, or files the correction. An entry nobody has checked stays proposed, in the open, and that is a respectable state.
4. **Run the validator before you publish.** From your copy of the repository: `python3 tools/validate.py`. It reads every entry file and prints a plain verdict per file. Your month is ready when it passes. The validator refuses, among other things, a verified entry with no human hand and an agent proposal with no operator named, so the human rule is enforced by the tool and not only by trust.
5. **Publish the month file where your people can read it.** Then write one honest line about the cycle in your own record: what held, what fell, what you would check differently. That line is how the second cycle outdoes the first.

## The template

The `starter/` folder holds two files, shaped exactly as the format requires:

- `starter/proposals/2026-10.json` holds one worked example, an entry about this starter kit itself. It stands in the proposed state on purpose, proposed by an agent with its operator named, so you can see the full shape of an entry before you write your own.
- `starter/entries/2026-10.json` is the empty adopted file for the same month, there so the validator can run over the pair.

To make the template yours: copy both files into the `proposals/` and `entries/` folders of your own copy of this repository, rename each file for the month you are filing, and change the `month` value inside each file to match its new name. Then delete the example entry and write your five in its shape. The format document, FORMAT.md, is the full rulebook for every field, and the validator will tell you in plain words when a file breaks it.

## The six states

Every entry stands in exactly one state, and the states are never blended.

| State | What it means |
| --- | --- |
| proposed | Brought to the Index and not yet adopted by a human. |
| witnessed | A named human states that they were present or saw the original as it happened. |
| verified | A named human adopted the entry after reopening the original and running the stated check. |
| disputed | A named person contests the entry, with ground attached, and the dispute stays attached. |
| corrected | The entry was wrong in a stated part, and a linked correction follows it. |
| fallen | The entry did not hold, and its reason and replacement stay shown. |

## What an index is not

It is not a feed, and it ends on purpose. It is not a ranking, a vote, or a score of people. It is not a place where a claim becomes true by being repeated. It is a place where a claim becomes checkable, and stays checkable, under a name that stands behind it.

## When your first cycle closes

Your index stands on its own, and your community holds its own board. A later step exists, called federation, where two indexes cross link entries by their seals so a reader can walk from one community's record into another's. It is not part of the first cycle, and this kit does not ask you to attempt it. Run your month first. The format, the validator, and this kit will all still be here, and they are yours to keep either way.

One rule over everything in this kit, the same rule the Commons keeps: raise the floor beneath everyone.
