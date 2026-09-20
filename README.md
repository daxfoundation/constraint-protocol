# The Constraint Protocol (CP-SPEC)

**A substrate for recording who did what, under which declared constraint, witnessed by whom —
so that any interaction between principals of any kind can be re-judged later.**

> *The substrate's purpose is not to prevent harm at T₀ but to preserve fidelity sufficient for
> retrospective re-evaluation at T₁..Tₙ.*
> — North Star, CP-SPEC v0.5 Decision Log §0

Stewarded by the [DAX Foundation](https://daxfoundation.org).

## Status

| | |
|---|---|
| Version | **v0.5** |
| Status | **Public Working Draft** (D-040) — one operational run, no external adversarial review; 1.0 would overclaim |
| Dated | 2026-09-10 |
| Phase A — decisions | Complete. 47 decisions (D-001 – D-047) |
| Phase B — verification | Decision-affecting checks complete (B-1 – B-5, B-7). Phase A holds; one conditional resolved |
| Phase C — specification body | Staged byte-exact, not yet assembled. See **Publication state** |

## Contents

| File | What it is | Bytes | git blob sha1 | sha256 |
|---|---|---|---|---|
| [`spec/CP-SPEC-v0_5-DECISION-LOG.md`](spec/CP-SPEC-v0_5-DECISION-LOG.md) | The traceability record. Every primitive in v0.5 resolves to a numbered decision here | 31,891 | `835e5862fd0aee53ef3ebea438ed0c602b6389f1` | `d5247ebbfe33f533f16752457eeddfb6f905bd2a51e64108988db7386f556dfc` |
| [`spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md`](spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md) | Primary-source verification of the decisions that could have reversed | 17,290 | `209e50278e7fe8b412963d9f25207b41c0fc5757` | `4a077e01e201fbbb47e6e781aa519d3b0a1dc420c778193f82a8f45ebce2d7d0` |
| `spec/CP-SPEC-v0_5.md` | The specification body — **not yet in this repository**; staged, see below | 225,851 | `b63a3ee7f5b75b5e10f6eb1868b220c876b42b5a` | `816b5f4798a71a83ff4e2c3c36695144a45928d9a03fb1f94c759820891b37c9` |

**Reading order.** Start with §0 and §3.5 of the decision log (the architectural commitments and
the publication posture), then the Phase B summary table, then the specification body.

**Integrity.** The digests above are the authority for whether a copy is intact. Verify any copy
before citing it:

```bash
sha256sum spec/*.md
git hash-object spec/*.md
```

A file whose digest does not match its row is not the v0.5 text, whatever its header says.

**Which digests these are.** The rows above are the digests of the *sanitised publication copies*
— the bytes this repository serves. They match the publication digests in
[`PROVENANCE.md`](PROVENANCE.md), and they are deliberately **not** the source digests of the
private originals those copies derive from. PROVENANCE.md lists both sets; do not verify a file
here against a source digest.

## Publication state

The two linked files above are present, and their rows were verified against this repository on
2026-09-20. The specification body is **not** yet here as a single file.

It is staged byte-exact as six line-aligned parts under `spec/_staging/`:

| Part | Bytes | git blob sha1 |
|---|---|---|
| `part-01` | 44,701 | `1413c4ccdb074faf76bfa5f23aeca2840cbaed59` |
| `part-02` | 44,973 | `ead018f2c08509d7ef396d194869e1c669bad7a3` |
| `part-03` | 44,969 | `8882a8297ae04a81687db445ebb6187da6e40ba2` |
| `part-04` | 44,951 | `0362d3430c0e0846db6d4f12138d4318c0f2d119` |
| `part-05` | 44,928 | `7b1b20b119a8a64303f576bf06a5bde76fa3119c` |
| `part-06` | 1,329 | `19165d3c0fbae4d8dfb2ea70a4a428646b1d051c` |

Concatenated in sorted order they reproduce the body exactly — 225,851 bytes:

```bash
cat spec/_staging/part-* > spec/CP-SPEC-v0_5.md
sha256sum spec/CP-SPEC-v0_5.md        # 816b5f47…891b37c9
git hash-object spec/CP-SPEC-v0_5.md  # b63a3ee7…76b42b5a
```

Until that join is committed and `spec/_staging/` is removed, the body is staged, not published.
This section is the repository's own statement of that, so that no row above is read as a claim
that the file is here.

## What CP is — and is not

Per D-045 (threat-model framing) and D-014 (entity-neutral principal):

- CP makes meaning-formulation **attributable, witnessed, and re-judgeable**. It never claims to
  *prevent* anything.
- The threat it addresses is **capability asymmetry plus opacity** — not nonbiological-ness. A
  witnessed, attributable principal of *any* kind, acting under a declared constraint, is what CP
  wants to exist.
- Every delegation chain terminates at a **principal**: an entity not itself acting under
  delegation, of unrestricted kind — biological, nonbiological, institutional or composite.
- Verification is **structural** — who, what, when, witnessed by whom, under which constraint —
  never semantic truth.
- Substrate accountability and legal accountability are different things. CP guarantees only the
  first.

## Composition, not competition

CP adopts or profiles mature standards and builds only what is uncovered (the Adopt / Substitute /
Build discipline):

| Concern | CP uses | Decision |
|---|---|---|
| Append-only ledger | IETF SCITT Signed Statements on a Rekor/Trillian-class log, scoped per CP scope | D-015 |
| Envelope | W3C VC 2.0 native, post-quantum cryptosuites (`mldsa44-jcs-2024`, `slhdsa128-jcs-2024`) | D-016, Phase B B-1 |
| Identity | W3C DID + VC 2.0 + Data Integrity | D-021 |
| Relationship predicates | W3C PROV-O / PROV-AGENT | D-017 |
| Delegation | DIF KYA-OS, as a profile | D-018, D-022 |
| Attachments | `agntcy/dir` RecordReferrer pattern | D-024 |
| Transport, discovery, coordination | Out of scope; composition surfaces named | D-023 |

The watch list of adjacent work, and the conditions under which CP moves from *build* to
*contribute a profile*, are D-043.

## Evidence

Per D-046: one cross-node operational run (2026-05-04) demonstrated refusal under a declared
constraint, permanent recording of three bypass attempts, and constraint reopening on a
compliance verdict. **It is not a controlled study, and no external adversarial review has
occurred.** A controlled A/B design — dependent variable: detection of manufactured consensus —
is committed. Review and adversarial testing are invited.

## Licence

Per D-041:

- **Specification prose:** CC BY 4.0 — see [`LICENSE`](LICENSE). Chosen because it permits the
  forks the specification requires.
- **Schemas, JSON, reference code, test vectors:** Apache-2.0 — see
  [`LICENSE-CODE`](LICENSE-CODE). Chosen for its patent grant.

Attribution is required on redistribution and on derivative works.

## Lineage

v0.3 (complete synthesis) → v0.4 (reconciliation, D-001 – D-012) → v0.4.1 (identity point
release, D-013) → **v0.5 (2026-09-10, D-014 – D-047)**.

---

*Every decision is revisable through the process it specifies.*
