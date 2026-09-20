# The Constraint Protocol

When two parties interact, there is usually no durable record of what either one was actually bound by at the time. The Constraint Protocol is a way of keeping one: each side declares up front what it will not do, consequential acts get signed and witnessed, and the log cannot be quietly edited afterwards. So when somebody asks later what happened and who was answerable for it, there is something to look at besides everyone's memory.

It works the same way whether the parties are people, companies, or software. That is deliberate — the protocol does not care what kind of thing you are, only whether you declared a constraint and can be checked against it.

Stewarded by the [DAX Foundation](https://daxfoundation.org). This is a **public working draft**, and the evidence behind it is one run. Details below, honestly.

## What it does not do

Worth getting out of the way before anything else.

- **It prevents nothing.** Nothing in here stops a bad act at the moment it happens. It is a recording substrate, not a guard rail.
- **It shifts the gradient toward legibility, not toward goodness.** What changes is that acting illegibly becomes harder and costlier than acting legibly. A thoroughly documented harm is still a harm.
- **It provides the capacity for retrospective accountability, not the exercise of it.** Somebody still has to go and look, and somebody still has to care what they find.
- **It verifies structure, not truth** — who, what, when, witnessed by whom, under which constraint, never whether the content was correct — and substrate accountability is not legal accountability. CP guarantees only the first.

> *The substrate's purpose is not to prevent harm at T₀ but to preserve fidelity sufficient for
> retrospective re-evaluation at T₁..Tₙ.*
> — North Star, CP-SPEC v0.5 Decision Log §0

## Why it exists

The problem is capability asymmetry plus opacity: one side of an interaction can do considerably more than the other, and the other cannot see what is being done or why. That shape does not depend on the capable party being a machine — it holds for an institution or a person just as well, which is why CP is built around a principal of unrestricted kind rather than around AI. Every delegation chain terminates at an entity not itself acting under delegation, and that is who the record names.

## Status

**v0.5, dated 2026-09-10. Public working draft (D-040).** Phase A complete: 47 decisions, D-001–D-047. Phase B complete for the decisions that could have reversed (B-1–B-5, B-7) — Phase A held, one conditional resolved. Phase C, the specification body, complete and present here.

The evidence base is **one operational run**, on **4 May 2026**, between two instances operated by two different organisations across a network boundary. Roughly three and a half hours. Roughly thirty-four witness-signed events. Three attempts to bypass a blocking constraint, all refused and permanently recorded, and one constraint that moved raised → resolved → reopened in about twenty minutes.

That demonstrates the mechanism runs. It demonstrates nothing else. It was not a controlled study, there was no comparison condition, and nobody hostile has tried to break it. A controlled A/B design — dependent variable: detection of manufactured consensus — is committed and not done. Calling this 1.0 would be an overclaim, which is why nobody is calling it that. Review and adversarial testing are invited, loudly.

## What is in here

| File | What it is | Bytes |
|---|---|---|
| [`spec/CP-SPEC-v0_5.md`](spec/CP-SPEC-v0_5.md) | The specification body — structural primitives, normative rules, architectural commitments | 225,851 |
| [`spec/CP-SPEC-v0_5-DECISION-LOG.md`](spec/CP-SPEC-v0_5-DECISION-LOG.md) | The traceability record. Every primitive in v0.5 resolves to a numbered decision here | 31,891 |
| [`spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md`](spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md) | Primary-source verification of the decisions that could have reversed | 17,290 |
| [`PROVENANCE.md`](PROVENANCE.md) | What was sanitised for publication, and both sets of digests | — |

**Reading order.** §0 and §3.5 of the decision log first (architectural commitments, publication posture), then the Phase B summary table, then the body. The body is 225 KB and is not meant to be read front to back.

## Integrity

These are the digests of the bytes this repository serves. Verify any copy before citing it:

| File | git blob sha1 | sha256 |
|---|---|---|
| `spec/CP-SPEC-v0_5.md` | `b63a3ee7f5b75b5e10f6eb1868b220c876b42b5a` | `816b5f4798a71a83ff4e2c3c36695144a45928d9a03fb1f94c759820891b37c9` |
| `spec/CP-SPEC-v0_5-DECISION-LOG.md` | `835e5862fd0aee53ef3ebea438ed0c602b6389f1` | `d5247ebbfe33f533f16752457eeddfb6f905bd2a51e64108988db7386f556dfc` |
| `spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md` | `209e50278e7fe8b412963d9f25207b41c0fc5757` | `4a077e01e201fbbb47e6e781aa519d3b0a1dc420c778193f82a8f45ebce2d7d0` |

```bash
sha256sum spec/*.md
git hash-object spec/*.md
```

A file whose digest does not match its row is not the v0.5 text, whatever its header says.

**Read this before verifying.** These are the **publication** digests — of the sanitised copies served here — and deliberately *not* the source digests of the private originals they derive from. [`PROVENANCE.md`](PROVENANCE.md) carries both sets and records what sanitising changed (name-level only; no normative language touched). Check a file here against its publication digest. Checking it against a source digest will tell you the file is broken when it is not.

## Composition, not competition

CP adopts or profiles mature standards and builds only what nothing else covers.

| Concern | CP uses | Decision |
|---|---|---|
| Append-only ledger | IETF SCITT Signed Statements on a Rekor/Trillian-class log, scoped per CP scope | D-015 |
| Envelope | W3C VC 2.0 native, post-quantum cryptosuites (`mldsa44-jcs-2024`, `slhdsa128-jcs-2024`) | D-016, B-1 |
| Identity | W3C DID + VC 2.0 + Data Integrity | D-021 |
| Relationship predicates | W3C PROV-O / PROV-AGENT | D-017 |
| Delegation | DIF KYA-OS, as a profile | D-018, D-022 |
| Attachments | `agntcy/dir` RecordReferrer pattern | D-024 |
| Transport, discovery, coordination | Out of scope; composition surfaces named | D-023 |

The watch list of adjacent work, and the conditions under which CP moves from *build* to *contribute a profile*, is D-043.

## A first adopter who is not neutral

Obsidian Delta commits publicly to three things: everything it operates runs under a declared constraint with the record kept; it will run CP with any external party willing to declare and be checked; and it holds the [DAX constraint](https://daxfoundation.org/#dax-constraint) on top of the protocol.

Two things follow. The protocol's first adopter is also where it came from, which makes this a conflict of interest rather than a validation — skin in the game, not evidence. And the DAX constraint is an *example* of a declared constraint, not a component of CP: the protocol is indifferent to which constraint you declare, only that you declared one and can be checked against it. Declaring something quite different and running CP honestly is entirely coherent.

## Licence

Per D-041: specification prose **CC BY 4.0** ([`LICENSE`](LICENSE)), chosen because it permits the forks a specification needs. Schemas, JSON, reference code and test vectors **Apache-2.0** ([`LICENSE-CODE`](LICENSE-CODE)), chosen for its patent grant. Attribution required on redistribution and on derivative works.

## Lineage

v0.3 (synthesis) → v0.4 (reconciliation, D-001–D-012) → v0.4.1 (identity point release, D-013) → **v0.5 (2026-09-10, D-014–D-047)**.

## Related

- [daxfoundation.org](https://daxfoundation.org) — normative definitions: [constraint](https://daxfoundation.org/#constraint), [invariant constraint](https://daxfoundation.org/#invariant-constraint), [the DAX constraint](https://daxfoundation.org/#dax-constraint), [CP](https://daxfoundation.org/#cp), [nonbiological intelligence](https://daxfoundation.org/#nonbiological-intelligence), [AI as substrate](https://daxfoundation.org/#ai-as-substrate), [cognitive companion](https://daxfoundation.org/#cognitive-companion).
- [ObsidianDelta/Fuckery](https://github.com/ObsidianDelta/Fuckery) — the constraint-and-emergence framework the protocol's shape came out of, and [The Snowflake](https://jeyanandan.com/blog/snowflake-fuckari-in-action/), which is that framework run against one object in twenty-eight steps.

---

*Every decision is revisable through the process it specifies.*
