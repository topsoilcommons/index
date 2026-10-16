# Security of the Index

What protects this record, what each protection proves, and what none of them can prove. Written in plain words so any reader, including the newsrooms and historians this Index is built to serve, can judge the design without trusting it.

## Who might tamper

- **A compromised account.** The GitHub account that holds this repository could be taken over, and entries could be edited, removed, or reordered under a name readers trust.
- **A malicious contributor.** A person with write access, or a person whose pull request is merged without a real check, could file a false entry or alter a true one.
- **A coerced host.** The platform that serves the repository and the page could be ordered, hacked, or bought, and could serve a changed copy to some or all readers.
- **A future agent.** A machine acting for the Commons, in this generation or a later one, could rewrite data at a speed and scale no human reviewer would catch by eye. The rules in AGENTS.md bind agents, and this design assumes a rule can fail.

## What each measure proves, and what it does not

**The fingerprint of the original.** Each entry stores a SHA-256 hash of its original at the time of the check. It proves the original a reader opens today is the same bytes the check saw, or that it changed. It does not prove the original was true when it was checked.

**The seal.** Each entry carries a SHA-256 seal over its own fields. It proves a copy of the entry matches the entry as sealed, field for field. It does not stop a person who can edit the entry from sealing it again.

**The chain.** Each entry also carries a chain record that binds it to the entry before it, and the published root in chain.json holds the head hash and the entry count of each queue. It proves that an entry was edited, removed, or moved, because the chain breaks at that point, and that a copy is complete, because a complete copy recomputes to the same head hash. It does not stop a person who holds the only copy from computing a whole new chain over false entries. That is why the root has to live in more than one place, held by more than one party, as the witnessing design below states.

**The states and the human gate.** Truth in this Index is carried by the six states and by the rule that only a named human can adopt an entry, after reopening the original and running the stated check. A chained false claim is still false. The chain carries integrity: it shows the record was not quietly changed. The states and the gate carry truth: they show what a named person checked, and what they found.

## The witnessing design

When newsrooms, historians, and other outside keepers contribute, the record stops depending on any one account, including this one.

- **Independent mirrors.** Each contributing organization keeps its own full copy of the data files, on its own systems, under its own control. A mirror is not a backup of this repository. It is a second standing copy whose keeper can compare it against any other copy at any time.
- **Signatures by the adopting hand.** When an outside human adopts an entry, that human signs the entry chain head with their own private key, and the signature is published beside the root. The signature says one thing only: this named person, holding this key, stood behind the record as it stood at that head hash. Design note: signatures arrive with the first outside adopters. The measures standing today are the seal, the chain, and the published root.
- **Periodic root comparison.** Mirror keepers recompute the chain over their own copies on a shared schedule and compare head hashes and entry counts against the published root. A mismatch is itself news. It is published, with the differing copies named, and it is answered by showing the copies, not by voting.
- **Disagreement in the open.** A keeper who finds an entry false does not edit it and does not delete it. They file a dispute, which stands attached to the entry, or a correction, which is a new entry linked to the old one. Nothing in this record is ever resolved silently.
- **Recovery from mirrors.** If this repository is altered or lost, the record is rebuilt from a mirror whose chain recomputes clean, and the alteration is filed as an entry in the rebuilt record, so the tamper attempt itself stays on the timeline.

## Key handling for contributors

- Each person signs with a key that belongs to them alone. A shared key signs nothing here, because a signature must name one hand.
- Private keys never enter this repository, any Commons repository, or any shared document. A private key found in the record is treated as burned, and every signature under it is rechecked.
- A public key is published with the name it stands for, in the contributor's own place first, so the name and the key can be checked against each other in two places.
- A lost key is announced in the open, in an entry, on the day it is known. Signatures made before the announcement stand as they were. Signatures after it do not.
- Losing a key loses the power to sign. It never loses a place in the record, and it never rewrites what the person signed before.

## The honest limit

No system is beyond tampering, so this design makes tampering visible, attributable, and recoverable from mirrors instead.
