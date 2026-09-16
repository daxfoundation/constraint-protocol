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
| Phase C — specification body | `spec/CP-SPEC-v0_5.md` — **pending upload** (see below) |

## Contents

| File | What it is | Bytes | git blob sha1 | sha256 |
|---|---|---|---|---|
| [`spec/CP-SPEC-v0_5-DECISION-LOG.md`](spec/CP-SPEC-v0_5-DECISION-LOG.md) | The traceability record. Every primitive in v0.5 resolves to a numbered decision here | 31,898 | `68f3ba3a5cff626a85c3644d3723828ecca7f183` | `4cf8a947c85d4b78f866f9ff7700aa878d50101b5fbfba3a815be3931fd161f3` |
| [`spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md`](spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md) | Primary-source verification of the decisions that could have reversed | 17,281 | `235d6d3aa10e707add60c23418d543487d2ae2c3` | `96f27617815e2bedc0c60c16afd023acaff156b5eab17e7c85deddf700217729` |
| `spec/CP-SPEC-v0_5.md` | The specification body | 225,820 | `c7062b60d3b1ae60f80bf24479bbb2dc5f49191c` | `d371e2ee80951a1c5945b8004e69049a95f6fb5a4448fdfba74d519ac0d6f4a0` |

**Reading order.** Start with §0 and §3.5 of the decision log (the architectural commitments and
the publication posture), then the Phase B summary table, then the specification body.

**Integrity.** The digests above are the authority for whether a copy is intact. Verify any copy
before citing it:

```bash
sha256sum spec/*.md
git hash-object spec/*.md
```

A file whose digest does not match its row is not the v0.5 text, whatever its header says.

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
