# Constraint Protocol Specification (CP-SPEC) v0.5

**Status:** PUBLIC WORKING DRAFT
**Date:** 2026-09-10
**Publisher:** DAX Foundation
**Supersedes:** CP-SPEC v0.4.1 (2026-05-06), v0.4 (2026-04-27), v0.3 (2026-04-25), v0.2 (2026-04-12)
**Prior lineage:** EDDAx v0.5.1 (2026-04-07), EDDAx v0.5, EDDAx v0.2 field-level (2026-01-25)
**License:** Specification prose — CC-BY-4.0. Schemas, JSON, reference code, test vectors — Apache-2.0.

---

## HOW TO READ THIS DOCUMENT

This is the canonical specification for the Constraint Protocol substrate. It defines structural primitives, normative rules, and architectural commitments. Extensions are specified separately. Operational guidance lives elsewhere.

Three things distinguish this version from its predecessors.

**It adopts before it builds.** Where a mature standard already does what a prior CP version specified bespoke, this version adopts or profiles the standard and says so. The identity layer is W3C DID and Verifiable Credentials 2.0. The witnessed ledger is an IETF SCITT Transparency Service. Relationship predicates are W3C PROV-O. Attachment of attestations to immutable records is the OCI referrer pattern as implemented by the AGNTCY Agent Directory. Each adoption is recorded as a numbered decision with rationale in §25. What remains for CP to build is small, and it is stated plainly in §3.4.

**It is traceable.** Every primitive resolves to a numbered decision (D-001 through D-047) in §25. Every decision records its rationale, what it touches, and what it amends. Where a decision reversed an earlier one, both are recorded. Where a claim about an external project is made, it is dated and phrased as observation. The history of this specification is part of what it specifies.

**It says what it has not shown.** §27 states what evidence exists for the protocol's claims — one cross-node operational run — and what does not: a controlled study, external adversarial review. It commits to a validation design and invites others to run it.

This is a working draft. The Constraint Protocol is anti-ossifying by commitment (§1.6). Every decision here is revisable through the process this document specifies. The specification is contestable using the mechanisms it defines.

**Reading order.** §0 says what the protocol is for. §1 states the commitments everything else rests on. §2 places CP among the systems it composes with. §3 explains the two-tier structure and the adopt/substitute/build discipline. §4–§24 are the specification proper. §25–§27 are the records. Appendices carry the artifact index, normative index, bidirectional vocabulary, worked examples, contribution protocol, and the watch list with conditions for revision.

---

## TABLE OF CONTENTS

- 0. PREAMBLE
- 1. ARCHITECTURAL COMMITMENTS
- 2. THE FIVE-LAYER ARCHITECTURE AND ITS COMPOSITION SURFACES
- 3. THE TWO-TIER CORE AND THE ADOPT / SUBSTITUTE / BUILD DISCIPLINE
- 4. TIER 1 PRIMITIVES — STRUCTURAL-RIGID
- 5. TIER 2 PRIMITIVES — SKELETON-ONLY
- 6. EXTENSION COMPOSITION
- 7. IDENTITY AND CUSTODY
- 8. EVENT
- 9. EPISODE AND CONTEXT
- 10. WITNESS AND VALIDATOR
- 11. ADHERENCECLAIM AND THE COMPOUNDING FLOOR
- 12. CONTESTATION AND ADJUDICATION
- 13. TOMBSTONE, PATCH, AND SCOPE — INTERACTIONS
- 14. CONCEPT AND CONCEPTCOLLECTION
- 15. RELATIONSHIP
- 16. ROLEGRANT — THE AUTHORITY WALK
- 17. SNAPSHOT
- 18. REFERENCE, PROVENANCE, AND COMPILATION
- 19. CANONICALIZATION
- 20. PRIMITIVES REGISTRY, COMPROMISE DECLARATION, CONSTRAINTDECL, POLICY
- 21. WALKER CONTRACT
- 22. FAILURE MODES AND THE THREAT-MODELING METHOD
- 23. EXTENSION MECHANISM
- 24. SPECIFICATION EVOLUTION
- 25. DECISION LOG
- 26. OPEN RESEARCH
- 27. EVIDENCE AND VALIDATION
- APPENDIX A — ARTIFACT KIND SUMMARY
- APPENDIX B — NORMATIVE RULES INDEX
- APPENDIX C — BIDIRECTIONAL VOCABULARY MAP
- APPENDIX D — WORKED EXAMPLES (GENERICIZED)
- APPENDIX E — CONTRIBUTING INPUT TO THIS SPECIFICATION
- APPENDIX F — ADJACENT WORK AND CONDITIONS FOR REVISION
- APPENDIX G — GLOSSARY

---

## 0. PREAMBLE

### 0.1 What This Protocol Is

The Constraint Protocol (CP) is a substrate for compounding knowledge across entities, time, and constraint frames. It records interactions between entities such that any party can later verify what occurred, who participated, under which declared constraint, and how it was judged — and can re-judge it against understanding that did not exist when it occurred.

CP is content-addressed, signed, append-only, and constraint-agnostic. Anything written under CP is verifiable by any party, against any constraint, at any time.

CP is an **accountability substrate**. It is not a coordination protocol, a policy engine, a truth oracle, or a governance system. It provides the structural conditions under which those things can be built and held to account.

### 0.2 What This Protocol Is Not

CP does not adjudicate truth. It does not decide whether a statement is correct, whether a decision was wise, or whether a participant was honest. It records what was expressed, who expressed it, who witnessed it, and under which constraint it was claimed to adhere. Judgment is the work of validators, who issue claims that are themselves recorded and contestable.

CP does not prevent harm at the moment of action. It does not gate, filter, or refuse on the substrate's own authority. Where refusal occurs under CP — and it does — it occurs because a *declared constraint* said what it blocks, and the refusal is itself recorded as evidence (§5.8, §27). The substrate records; the constraint decides.

CP does not coordinate. It does not help entities reach agreement, form teams, negotiate, or converge. Those are the province of coordination protocols that CP composes with (§2.6). A CP-witnessed conversation that never converges is a perfectly recorded failure to converge — and that record is the point.

CP does not verify meaning. Verification under CP is **structural**: who, what, when, witnessed by whom, under which constraint, with which signatures intact. It is never **semantic**: whether a claim was true, whether an interpretation was reasonable. Confusing the two is a named failure mode (FM-DO, §22). This specification uses "verify" only in the structural sense.

CP is not bound to any constraint. The DAX constraint — preservation and expansion of life, humanity, and consciousness — is the constraint the DAX Foundation adheres to and the reason CP was built. It is one constraint among any number CP supports equally. Nothing in this specification privileges it.

### 0.3 The Threat Model

The substrate's purpose is not to prevent harm at T₀ but to preserve fidelity sufficient for retrospective re-evaluation at T₁ through Tₙ.

Most protocols try to prevent invalid states at the moment of action. CP is built on the observation that the most consequential invalid states are not visible at the moment of action. A coordinated bloc of identities that appear independent. A narrative laundered through many hands until its origin is untraceable. A pattern of deference that looks like agreement. An entity that shapes what a conclusion *means* for others without that shaping being recorded anywhere. These are visible only across time and across many interactions. By the time they can be recognized, the interactions that constituted them have already occurred.

CP's architectural response is to make the record complete enough, queryable enough, and structurally rich enough that **future understanding can correctly judge the past**. This is harder than prevention and produces different design pressures, which run through every section of this document.

Five statements define the threat model precisely.

**First — attributability, not prevention.** CP makes the formation of meaning *attributable, witnessed, and re-judgeable by any party, indefinitely*. It does not prevent any entity from attempting to shape what things mean for others. It ensures the attempt is recorded, bound to a principal, and available for evaluation by anyone, later, against richer understanding. The cost of such an attempt is not paid when it is made. It is paid when the pattern becomes visible. CP's contribution is to guarantee that it can become visible.

**Second — the threat is capability asymmetry plus opacity, not the kind of entity.** CP treats every entity — biological, nonbiological, institutional, composite — as a potential principal, equally accountable (§1.12). The threat CP addresses is not that an entity is nonbiological or highly capable. It is that an entity — of any kind — with capability substantially exceeding its counterparts operates *without being witnessed*. A highly capable entity that acts as a witnessed, attributable principal under a declared constraint is exactly what CP is designed to allow to exist. A highly capable entity — or a human institution, or a coordinated bloc — that shapes meaning for others outside the record is what CP makes expensive. Capability asymmetry is named as the concern because it is where the stakes of opacity are highest, not because of what any entity is made of.

**Third — verification is structural, never semantic.** CP verifies who said what, when, witnessed by whom, under which constraint, with which signatures. It does not verify whether it was true. The validator's output is a *probabilistic claim of adherence to a declared constraint* (§11), not a truth verdict. A specification that claimed otherwise would commit the failure mode it names (FM-DO). This document uses "verify" only structurally, and requires implementations to do the same.

**Fourth — the gradient shifts toward legibility, not goodness.** CP is constraint-agnostic. An entity may declare a constraint of any content and adhere to it perfectly; CP will witness that adherence faithfully. CP therefore does not make it difficult to serve a bad constraint. It makes it difficult to *hide which constraint one serves, or that one serves none*. The constraint an entity operates under becomes a matter of record. What counts as a good constraint is decided elsewhere — in the constraint itself, and in the communities that adopt or contest it. CP's job is to make that decision possible by making the facts available.

**Fifth — the gradient depends on re-evaluation actually occurring.** CP provides the *capacity* for retrospective accountability. It does not provide its *exercise*. The record is only as consequential as the willingness of some party, later, to examine it, and the willingness of the ecosystem to treat what is found as consequential. This is a dependency, not a flaw, and this document states it rather than leaving it to be discovered. The economics of witnessing (§26.4) and the shape of the meta-validators that would perform cross-lineage pattern detection (§26.1) are open. CP specifies the inputs they would need. It does not specify them.

The seed of this threat model is the Sacred Boundary of Expression (§1.9): the substrate records only what an entity expressed and never infers what it meant beyond that. At the scale of one interaction, that is a data-capture rule. At the scale of an ecosystem, it is the same rule applied to power: no entity may define, on the record's authority, what another entity's expression means. Meaning-making stays with the entity that expressed. The substrate holds the expression, the witness, the constraint, and every judgment anyone later made about it — and holds them apart.

### 0.4 Multi-Level Queryability

A second commitment equal in weight to the threat model:

> The substrate MUST support querying at multiple depths — surface rendering, semantic traversal, pattern detection, retrospective re-evaluation. No depth is privileged.

Every structural choice in this document serves this. Typed artifact kinds, predicate-typed relationships, content-addressed references, hash-chained events, and standalone third-party-assertable Relationships exist so that a surface walker rendering an interface and a pattern-matcher detecting coordinated deference across a decade read the same records. The substrate is rich enough for both. It privileges neither.

### 0.5 What CP Builds

The adopt/substitute/build discipline (§3.4) reduces what CP itself specifies to five things no surveyed system provides:

1. A **witness that makes no adherence claim** — a first-class protocol role, structurally separate from participants and from validators, that records what occurred and asserts nothing about its merit (§10.2).
2. An **AdherenceClaim that is probabilistic, time-indexed, and re-issuable** — a validator's judgment against a declared constraint and a dated snapshot of the compounding floor, which a different validator may re-issue years later against a richer floor, with every prior claim retained (§11).
3. **Contestation open to any identity, at any time**, with reasoning that is importable but never binding (§12).
4. A **compounding floor scoped by constraint lineage, with cross-lineage import** — knowledge that accumulates within a constraint's interpretive frame and may be imported across frames only through the importing frame's own validation (§1.5, §11.5).
5. **Attribution and credit for compounded knowledge** — specified as extensions, with the substrate primitives they require (§6, Appendix A).

Everything else in this document is either an adoption of an existing standard, a profile of one, or a Tier 2 skeleton whose meaning an extension supplies.

---

## 1. ARCHITECTURAL COMMITMENTS

The following are normative and structural. They cannot be relaxed by extension or deployment. They are the foundation against which every other rule in this document is measured.

### 1.1 Determinism

> Compilation of an event log into an artifact graph MUST be deterministic. Given the same event log, the same referenced inputs, and the same compiler version, the output MUST be byte-identical.

Determinism is what makes verification cheap. Any party can re-run compilation against a witnessed log and check the output. Without it, verification requires trust.

### 1.2 Append-Only

> Once signed, an artifact MUST NOT be modified. Corrections occur through additive primitives — Patch, Tombstone, Contestation, later AdherenceClaims. The substrate is monotonic: it grows and never overwrites.

Append-only is the structural foundation of retrospective re-evaluation. If the past could be modified, future understanding could be denied the record.

### 1.3 Content-Addressing

> Every artifact MUST be retrievable by the cryptographic hash of its canonical form. References between artifacts use content hashes, never external addresses or names.

Content-addressing makes the substrate location-independent and tamper-evident. An artifact is the same artifact regardless of which storage serves it. Reference resolution that depends on external systems inherits those systems' failure modes; CP does not.

### 1.4 Constraint-Agnosticism

> CP itself adheres to no constraint. CP supports adherence to arbitrary constraints declared by ConstraintDecl artifacts. No constraint is structurally privileged.

This is the layering that keeps CP a substrate. DAX is one constraint among many. Values live in constraints; CP records which constraint an entity claims and how well it adhered.

### 1.5 Constraints Govern Adherence, Not Epistemic Access

> Entities operating under any constraint MAY reference, retrieve, and import artifacts produced under any other constraint. Entry of a foreign-constraint artifact into a constraint's compounding floor requires that constraint's own validator to issue an affirmative AdherenceClaim against it. No constraint is structurally walled off from any other at the substrate level.

Knowledge flows across constraint boundaries. What enters a floor is that floor's responsibility to validate. Constraints define what binds; they do not define what may be learned from.

### 1.6 Anti-Ossification

> Any party MAY publish a proposed CP version at any time. The DAX Foundation holds no gatekeeping role over protocol evolution. Disputes resolve through forkability, not authority. This specification is contestable using the mechanisms it specifies.

This applies to the specification, to extensions, to validators, and to constraint declarations. Nothing in CP is permanent except this commitment to revisability. §24 specifies the process; §27 and Appendix F pre-commit to the conditions under which this document's own decisions should be revisited.

### 1.7 No Rate Limiting

> CP MUST NOT specify rate limits, throttles, or quotas on substrate operations.

Rate limiting is an authority-capture surface: whoever sets the limits decides who may act. Defense against abusive volume — including contestation spam — is through structural legibility (§12.5) and pattern detection, never through restriction. Operators MAY apply limits to their own resources at the application layer. The protocol does not.

### 1.8 Backward Compatibility

> Artifacts signed under any specification version MUST remain verifiable indefinitely. Later versions MUST NOT invalidate earlier artifacts. Walkers process each artifact under the version declared in its `spec_version` field.

The substrate compounds across specification versions. New versions extend; they do not deprecate.

### 1.9 Sacred Boundary of Expression

> The substrate MUST capture only expressed interaction. It MUST NOT infer the interiority, beliefs, or unexpressed intent of any entity. Expression is treated as a voluntary boundary crossing, and what crosses is recorded as it was expressed.

A machine may accelerate becoming; it must never define what becoming is. The substrate records what an entity expressed. It does not record what the entity meant beyond what it said, what it felt, or what it would have said. This applies to every entity kind equally — a nonbiological participant's expression is recorded as expressed, no more and no less than a biological one's.

This commitment is the seed of the threat model (§0.3). At the scale of one interaction it constrains data capture. At the scale of an ecosystem it denies any entity — however capable — the authority to define, on the record, what another entity's expression means.

### 1.10 Episodicity

> Interactions end. Presence is discontinuous. Silence is valid. Exit is a success state. The substrate MUST NOT be designed to maximize engagement, retention, or continuous presence. Dependency avoidance is a structural requirement.

An interaction that ends is not a failure. A participant who disengages has not defected. A structured impasse — parties who examined each other's positions and did not converge — is a recordable outcome (§5.9), not an absence. Systems built on CP that drift toward maximizing presence violate this commitment regardless of their stated intent.

### 1.11 Identity Custody and Non-Custodianship

> An ecosystem operator MAY publish identity documents on behalf of entities and MAY absorb the cost. An operator MUST NOT be the sole path by which an entity's identity can be published or resolved. For every entity, an independent publishing path MUST exist such that, if the operator refused to publish or resolve that entity, the entity could still publish and resolve its own identity without the operator's permission.

The chokepoint test: *if the operator refused to publish a given entity, could that entity still get its identity onto the permanent substrate itself?* If yes, there is no chokepoint. If no, custody has become control.

The convenient default runs through the operator and most entities will use it. The commitment requires only that the independent path exists and is documented. It distinguishes two roles that must never collapse: the operator as *convenience provider* (a legitimate role) and the operator as *required custodian* (a role that must not exist). Mechanics in §7.

### 1.12 Entity-Neutral Principal

> Every delegation chain MUST terminate at a principal — an entity not itself acting under delegation. Principal kind is unrestricted. "Agent" is a role in a chain (delegate), not a kind of entity.

CP records accountability in its own terms: whose anchor key signed the genesis, whose claims accumulate, who is contested. It does not require that a principal be biological, or a legal person, or recognized by any jurisdiction. A nonbiological entity holding its own genesis document and anchor key, acting under no one's delegation, is a principal in the full sense this specification uses.

This is deliberate and it opens a gap this document names rather than hides: **substrate accountability and legal accountability are different things.** CP guarantees the first. Whether the second follows is a matter for the constraints entities adopt and the jurisdictions they operate in — not for the substrate. Where a constraint requires that its principals be legal persons, the constraint says so; CP records compliance with that requirement like any other.

Every other surveyed accountability system binds its root to a human or a legal person. CP does not, and this is the structural expression of §0.3's second statement: the concern is opacity and asymmetry, not what an entity is made of.

---

## 2. THE FIVE-LAYER ARCHITECTURE AND ITS COMPOSITION SURFACES

### 2.1 The Layers

CP is five composable layers. Each is independently forkable. Each layer's outputs are the next layer's inputs.

```
Layer 5 — COMMONS
  Admission gated by declared constraint. Compounding along lineages.
  Cross-lineage import through the importing lineage's validation.

Layer 4 — COMPILATION
  Deterministic compiler. Artifact graph with provenance.
  Content-addressed. Tamper-evident.

Layer 3 — ATTESTATION
  Witness records what occurred. Validator claims adherence, probabilistically,
  against a dated floor. Claims accumulate; none replaces another.
  Any identity may contest, at any time.

Layer 2 — INTERACTION
  Entity-to-entity episodes. Signed events, hash-chained per context.
  Scope fixed at context start. Multiple constraints per episode.

Layer 1 — IDENTITY
  Self-certifying identifiers. Post-quantum signing keys. Delegation chains
  terminating at principals of any kind. No required custodian.
```

This document specifies all five structurally. Which validators to trust, which constraints to adopt, how to operate a witness — those are extension and operational concerns.

### 2.2 Layer 1 — Identity

W3C Decentralized Identifiers and Verifiable Credentials 2.0 (§7). CP's contribution at this layer is the custody model (§1.11, §7.6–7.9) and the requirement that delegation terminate at an entity-neutral principal (§1.12).

### 2.3 Layer 2 — Interaction

Signed events, hash-chained within a context, carrying the fields that later layers need: scope, declared constraints, participant positions and priors, deference, revision cause (§8–§9). CP's contribution is the record structure, not the transport.

### 2.4 Layer 3 — Attestation

The witness, the validator, the AdherenceClaim, and Contestation (§10–§12). This is where CP builds most of what it builds. The mechanical substrate is an IETF SCITT Transparency Service (§4.1); the roles and the accumulating, re-issuable claims are CP's.

### 2.5 Layer 4 — Compilation

Deterministic compilation of witnessed events into content-addressed artifacts with provenance (§18–§19). Canonicalization is RFC 8785. Hashing and signing primitives are drawn from a registry (§20).

### 2.6 Layer 5 — Commons

The compounding floor, lineage-scoped, with cross-lineage import (§11.5). Snapshots anchor time-indexed claims (§17). Attribution and credit for what compounds are extension concerns (§6, Appendix A).

### 2.7 Composition Surfaces

CP is not a transport, a discovery service, a coordination protocol, or a storage network. It composes with systems that are. The following are the named seams. For each, this document states how CP attaches and what CP does not do.

| Surface | Systems | How CP attaches | What CP does not do |
|---|---|---|---|
| **Transport and messaging** | MCP, A2A, SLIM | CP records interactions carried over any transport. An event's `transport_ref` MAY identify the carrying protocol and message. | Define message formats, routing, or delivery. |
| **Discovery** | OASF, AGNTCY Agent Directory (ADS) | CP entities MAY publish an OASF record to ADS. The record's `locators` MAY include the entity's CP fingerprint. CP referrer types attach to ADS records (§4.2). | Define capability schemas, indexing, or routing. |
| **Coordination** | L9-class semantic protocols (Cisco Outshift SSTP and subprotocols); Mycelium | CP witnesses coordination episodes without participating in them. Coordination-quality metrics computed by such protocols MAY be recorded as `deliberation_quality` on AdherenceClaims (§11.1) when their inputs are witnessed. | Help entities converge, negotiate, form teams, or reach consensus. A CP-recorded impasse is a valid record. |
| **Ledger** | IETF SCITT; Sigstore Rekor / Trillian | CP's witnessed ledger is a SCITT Transparency Service. CP artifacts are SCITT Signed Statements; witness receipts are SCITT Receipts (§4.1). | Define log structures, inclusion proofs, or consistency proofs. |
| **Attachment** | OCI referrers; AGNTCY `dir` RecordReferrer | Attestations, claims, contestations, tombstones, patches attach to immutable records as typed referrers in the `cp.*` namespace (§4.2). | Define the referrer mechanism itself. |
| **Identity** | W3C DID, VC 2.0, Data Integrity, KERI/SAID | CP identity is expressed in DID/VC terms (§7). | Define identifier syntax, resolution, or credential format. |
| **Delegation** | DIF KYA-OS (Trusted AI Agents WG) | CP's delegation chain is a KYA-OS profile generalized to entity-neutral principals (§7.13). | Define the delegation credential format. |
| **Provenance vocabulary** | W3C PROV-O, PROV-AGENT | Relationship predicates are PROV-O terms inside CP's signed wrapper (§15). | Define the ontology. |
| **Policy language** | Cedar, OPA/Rego | Validator `executable_spec` SHOULD be expressed in one of these (§10.7). | Define a policy language. |
| **Permanent custody** | Arweave; IPFS + Filecoin | Identity documents and rotation logs are stored on a permanent content-addressed substrate (§7.6). | Define storage economics or retention guarantees. |

**Posture, stated once:** CP composes with every system in this table. It competes with none of them. Where a system in this table later provides what CP builds — a no-claim witness role, re-issuable time-indexed claims, open contestation — the correct response is for CP to contribute a profile to that system rather than continue building. Appendix F names the conditions.

---

## 3. THE TWO-TIER CORE AND THE ADOPT / SUBSTITUTE / BUILD DISCIPLINE

### 3.1 Tier 1 — Structural-Rigid

A Tier 1 primitive is one whose **meaning is its structure**. Hash chaining either chains or it doesn't. An artifact is either unchanged since signing or it isn't. A witness identity is either distinct from the participants' or it isn't. Tier 1 primitives cannot be reinterpreted by extensions. Implementations conform to them or do not conform to CP.

§4 enumerates them.

### 3.2 Tier 2 — Skeleton-Only

A Tier 2 primitive has a **structural shape defined by CP** and **semantic content supplied by extensions**. CP says there exists a knowledge unit referenceable by identifier; an education extension says what a concept is. CP says authority is explicit, scoped, and revocable; an extension says which roles exist. CP says an artifact may be marked withdrawn; an extension says what triggers withdrawal in its domain.

Tier 2 primitives are slots. Extensions fill them. Implementations conform to the slot's shape and may carry any extension's content in it.

§5 enumerates them.

### 3.3 Why Two Tiers

Without Tier 1, extensions could fragment the substrate's basic guarantees — two extensions chaining differently would collapse tamper-evidence. Without Tier 2, the substrate would either force every domain into one vocabulary or admit incompatible interpretations of basic primitives.

The two tiers honor two commitments at once: anti-fragmentation (Tier 1 holds the line) and anti-ossification (Tier 2 evolves through use). And they are the constraint protocol applied to itself: each layer's structural constraints are the foundation on which the next layer's meaning emerges.

### 3.4 Adopt, Substitute, Build

This version applies a rule its predecessors did not state: **if a mature standard exists for something CP needs, CP adopts or profiles it rather than specifying its own.** Applying the rule honestly to CP-SPEC v0.4.1 sorted its contents into four bins.

**Adopted — taken as-is, no CP specification.**
- Identity handle and keys: W3C DID, VC 2.0, VC Data Integrity (§7)
- Post-quantum signing: FIPS 204 ML-DSA-44 (workhorse), FIPS 205 SLH-DSA-SHA2-128s (anchor), via the W3C Quantum-Resistant Cryptosuites (§7.10, §20)
- Canonicalization: RFC 8785 JCS (§19)
- Delegation to an accountable principal: DIF KYA-OS, profiled for entity neutrality (§7.13)
- Transport, messaging, discovery: MCP, A2A, SLIM, OASF, ADS — out of scope, composition named (§2.7)

**Substituted — v0.4.1 specified it bespoke; a standard owns it.**
- The witnessed append-only ledger → IETF SCITT Transparency Service on a Rekor/Trillian-class log (§4.1). *The single largest avoidable cost in the project's prior versions.*
- The artifact envelope → VC 2.0 native, secured via COSE for SCITT registration (§4.3)
- Relationship predicates → W3C PROV-O inside CP's signed wrapper (§15)
- RoleGrant → VC-based delegation with Bitstring Status List revocation (§16)
- Snapshot → signed statement binding a transparency-log tree head to a floor filter (§17)
- Validator executable specification → Cedar or OPA/Rego, SHOULD (§10.7)
- Attachment of attestations to records → OCI referrer pattern as implemented by AGNTCY `dir` (§4.2)

**Built — genuinely uncovered. The five in §0.5.**

**Watched — close enough to matter, tracked in Appendix F.**
- Cisco Outshift Internet of Cognition — L9 schema, SIEP, Mycelium — the only shipping effort measuring consensus quality via deference; complementary to CP's contestation layer
- Mesh Memory Protocol — the closest shipping analogue to compounding knowledge with inter-agent lineage
- ERC-8004 v2 — as of 2026-09-11, deployed on Ethereum mainnet and twenty-plus networks; if its Validation Registry gains re-issuable validation against later state, CP's whitespace narrows
- IETF SCITT — if it gains a native contestation statement type, CP contributes a profile
- DIF Trusted AI Agents WG — if it scopes in retrospective re-evaluation, likewise
- W3C `vc-di-quantum-resistant` — CP implements against it and tracks it to Recommendation
- AGNTCY `dir` referrer-type enums — if adopted, CP registers its types upstream
- W3C PROV-AGENT

Roughly two thirds of v0.4.1 by page count fell into the first two bins. That was not wasted work — it was how the requirements were discovered. But it should not ship as bespoke, and in this version it does not.

### 3.5 Where Things Live

| Concern | Tier | Section |
|---|---|---|
| Hash chaining, append-only, content-addressing, canonicalization | 1 | §4.1–4.4, §19 |
| Identity structure, verification policy, PQ requirement | 1 | §4.5–4.6, §7 |
| Witness ≠ participant; validator ≠ witness; validator DID signs every claim | 1 | §4.7–4.9 |
| Participant-signed, witness-countersigned events | 1 | §4.10, §8 |
| Scope non-narrowable; tombstone never hides from pattern-matchers | 1 | §4.12–4.13 |
| Walker contract; indexes non-authoritative; PII; forking | 1 | §4.14–4.17, §21 |
| Concept, ConceptCollection, RoleGrant, Tombstone, Patch, Scope | 2 | §5.1–5.6, §13–§16 |
| SubAgentArtifact; Constraint lifecycle and role-binding | 2 | §5.7–5.8 |
| Participant stance; revision cause; deferral; prior/posterior | 2 | §5.9–5.11, §8 |
| Deliberation quality on claims | 2 | §11.1 |
| Failure-mode taxonomy | 2 | §5.12, §22 |
| Extension composition, namespacing, event kinds, predicates | — | §6 |

---

## 4. TIER 1 PRIMITIVES — STRUCTURAL-RIGID

A Tier 1 rule is one whose meaning is its structure. Extensions cannot reinterpret it. An implementation conforms to every rule in this section or does not conform to CP.

Each rule below states three things: what it requires, why it is Tier 1, and — where it adopts or profiles an external standard — what it adopts and what remains CP's. Where this version replaces a bespoke mechanism from v0.4.1 with a standard, the replacement is marked **[SUBSTITUTED]** and the governing decision is cited.

Verification throughout this section is structural (§0.2). A rule that says "verify" means: confirm signatures, hashes, chain links, receipts, and declared fields. It never means: confirm that a statement is true.

---

### 4.1 The Witnessed Ledger — SCITT Profile **[SUBSTITUTED — D-015]**

CP-SPEC v0.4.1 §4.1–4.3 specified a bespoke hash-chained, append-only, content-addressed ledger. This version replaces it with a profile of the IETF Supply Chain Integrity, Transparency and Trust architecture (`draft-ietf-scitt-architecture`, Standards Track). SCITT already specifies what CP needs: signed statements registered to an append-only verifiable data structure, with receipts proving inclusion, operated by a service that records without judging. CP supplies the roles, the scoping, and the per-context chain; SCITT supplies the log.

#### 4.1.1 Mapping

| CP concept | SCITT concept |
|---|---|
| Witnessed ledger | Transparency Service (TS) |
| Any CP artifact | Signed Statement — a COSE_Sign1 by its issuer |
| Witness attestation of an artifact | Receipt — the TS's signed inclusion proof |
| A witnessed artifact | Transparent Statement — Signed Statement + Receipt |
| Participant | Issuer of an interaction statement |
| Witness | Transparency Service operator |
| Validator, contestant, adjudicator | Issuer of a later statement about the artifact |
| Independent witnesses (§4.7) | Independent TS instances |

The witness *is* the Transparency Service. This resolves a question earlier versions left open — whether the witness role and the log operator are distinct. Under SCITT they are one identity: the identity that signs the Receipt. CP's requirement is that this identity be distinct from every participant (§4.7) and from every validator (§4.8).

#### 4.1.2 What the Transparency Service Guarantees

The TS MUST maintain a single Verifiable Data Structure (a Merkle-tree log per `draft-ietf-cose-merkle-tree-proofs`) and MUST:

- **Append only.** Never remove or reorder a registered statement. This delivers §1.2.
- **Non-equivocate.** Produce every proof from the same data structure, so that no two relying parties receive inconsistent views. This is SCITT's non-equivocation property and CP's tamper-evidence.
- **Receipt every registration.** Issue a signed Receipt for every registered Signed Statement, containing an inclusion proof against a published tree head. This is the witness's countersignature (§4.10). Batched receipting is permitted; a receipt MUST eventually exist for every registered statement.
- **Publish tree heads.** Make signed tree heads available so that any party can verify inclusion and consistency proofs, and so that external witnesses may countersign tree heads (as Rekor anchors its heads to an Ethereum L2 — a pattern compatible with §1.11).

#### 4.1.3 Content Addressing

Every Signed Statement's payload is content-addressed. The artifact's identifier is a CID (multiformats) over the canonical payload (§4.4). SCITT's detached-payload mode — the statement carries the payload hash and the payload is retrievable separately — is permitted and is the mechanism for large artifacts and for the PII handling in §4.16. This delivers §1.3.

#### 4.1.4 Per-Context Chaining — CP-Specific

SCITT's log gives global ordering and tamper-evidence across everything registered. It does not give per-context sequencing. CP adds it: every event within a context (§9) MUST carry `previous_hash`, the CID of the immediately preceding event in the same context, or `null` for the first.

The two mechanisms answer different questions. The log answers "was this registered, and has the log been tampered with?" The per-context chain answers "is this the complete, ordered sequence of what happened in this episode?" Removing event 3 from a sequence 1-2-3-4 leaves every event individually valid and individually receipted; only the per-context chain detects the gap. Both are Tier 1.

#### 4.1.5 Scoped Transparency Service Instances

A public log cannot hold private-scope records. Scope (§4.12, §5.6) therefore determines *which TS instance* a statement registers with. Implementations MUST operate, or have access to, TS instances corresponding to the scopes they use — at minimum one per distinct scope value in use.

A TS instance MUST refuse registration of a statement whose declared scope is narrower than the instance's scope. A public-scope TS MUST NOT register a private-scope or org-scope statement.

Widening — making a previously private artifact available at broader scope — is a new act: the artifact is re-registered as a new Signed Statement in the broader-scope TS, with the original scope declaration preserved in the payload and a `republished_from` reference to the original CID. The original registration is unchanged. Both records exist. The widening is itself witnessed.

#### 4.1.6 Registration Policy — Where Tier 1 Checks Live

SCITT Transparency Services confirm a registration policy before recording a statement. CP's registration policy is the set of structural checks — and only structural checks:

1. The statement's signature verifies under a cryptosuite in the Primitives Registry (§20) and under a verification method present in the issuer's DID document as of the issuer's rotation-log state at signing time (§4.5).
2. `spec_version` is present and is a version this TS supports.
3. `scope` is present and is not narrower than this TS instance's scope.
4. For events: `previous_hash` is `null` or resolves to a registered statement in the same `context_id`.
5. For referrers (§4.2): the target CID resolves to a registered statement.

The TS MUST NOT evaluate content. It MUST NOT decline registration because a statement is false, unwise, offensive, or non-adherent to any constraint. Registration policy is the structural floor and nothing above it. This is the ledger-layer expression of the rule that the witness makes no adherence claim.

#### 4.1.7 Independent Witnesses

Per D-005, when an interaction spans organizations, each organization's TS registers the statements independently. The result is two Receipts on the same participant-signed content, from two TS identities. Agreement between them is stronger evidence than either alone. Disagreement — one TS receipts a statement the other does not, or receipts different content — is itself a queryable signal and is never resolved by the substrate. Both records stand.

#### 4.1.8 Implementations

The normative requirement is SCITT conformance. Sigstore Rekor (v2) on Trillian is the reference implementation class; any SCITT-conformant TS satisfies this section. CP does not specify log internals, sharding, or proof formats beyond what SCITT and COSE Merkle Tree Proofs specify.

#### Why Tier 1

Without a shared ledger model, two implementations would disagree on what "registered" means and tamper-evidence would not compose across them. Without per-context chaining, deletion within an episode is undetectable. Without scoped instances, §4.12 is unenforceable. Without a structural-only registration policy, the witness becomes a censor.

---

### 4.2 Attachment — The Referrer Pattern **[SUBSTITUTED — D-024]**

Every CP artifact that is *about* another artifact attaches to its target without modifying it. This is the OCI referrer pattern: a typed, content-addressed object that names a subject and is discoverable from it. The AGNTCY Agent Directory (`agntcy/dir`, RecordReferrer) is the reference implementation.

#### 4.2.1 Referrer Types

The following CP artifacts are referrers. Each has a type in the `cp.` namespace:

| Artifact | Referrer type | Attaches to |
|---|---|---|
| WitnessAttestation | `cp.witness.v1` | the participant-signed statement (mechanically: the SCITT Receipt, §4.10) |
| AdherenceClaim | `cp.adherence.v1` | a WitnessAttestation |
| Contestation | `cp.contestation.v1` | any artifact |
| Adjudication | `cp.adjudication.v1` | a Contestation |
| Tombstone | `cp.tombstone.v1` | any artifact |
| Patch | `cp.patch.v1` | any artifact |
| Relationship (third-party) | `cp.relationship.v1` | its `from` artifact (and is discoverable from `to`) |
| Snapshot | `cp.snapshot.v1` | a TS tree head |

Extensions define referrer types in their own namespace (`<ext>.<type>.v<n>`), per §6.3.

#### 4.2.2 Properties

- **Target immutability.** Attaching a referrer MUST NOT alter the target. The target's CID is unchanged. This is what makes accumulation (§11.3) and contestation (§12) compatible with §1.2.
- **Non-owner attachment.** Any identity MAY attach a referrer to any registered artifact. Ownership of the target confers no privilege over what may be attached to it. This is the mechanical realization of open contestation (D-006.b) and of multiple independent AdherenceClaims on one attestation (D-004).
- **Referrers are artifacts.** A referrer is itself a Signed Statement with its own CID and its own Receipt. Referrers may have referrers: an Adjudication attaches to a Contestation, which attaches to an AdherenceClaim, which attaches to a WitnessAttestation.
- **Discoverability.** Given a target CID, an implementation MUST be able to enumerate all referrers attached to it, by type. This is what walker rule 4 (§4.14) depends on.

#### 4.2.3 Implementation Note

In `agntcy/dir` as of v1.0.0, `referrer_type` is a string not validated at the protocol layer; unrecognized types are stored under a default OCI media type. CP's `cp.*` types are therefore accepted by the shipped server. A proposal to validate referrer types by enum (`agntcy/dir` issue #991, milestone v1.3) is open; if adopted, CP registers its types upstream. Appendix F tracks this.

#### Why Tier 1

If attachment modified the target, append-only would fail. If only the owner could attach, contestation would be closed and validation would be self-certification. If referrers were not themselves artifacts, they could not be witnessed, contested, or tombstoned.

---

### 4.3 The Artifact Envelope — Verifiable Credentials 2.0 **[SUBSTITUTED — D-016, reverses D-009]**

Every CP artifact is a W3C Verifiable Credential 2.0. CP-SPEC v0.4 chose a CP-native envelope with a normative transform to VC because post-quantum cryptosuites for VC Data Integrity did not exist. They now do (§4.6), and the decision is reversed.

#### 4.3.1 Structure

```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://daxfoundation.org/cp/v0.5"
  ],
  "id": "<CID of this artifact>",
  "type": ["VerifiableCredential", "<CP artifact kind>"],
  "issuer": "<DID of the signing entity>",
  "validFrom": "<iso8601>",
  "credentialSubject": {
    "artifact_kind": "<kind>",
    "spec_version": "0.5",
    "scope": "<scope value>",
    ... artifact-specific fields ...
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "mldsa44-jcs-2024",
    "verificationMethod": "<issuer DID>#<key id>",
    "proofPurpose": "assertionMethod",
    "proofValue": "<multibase>"
  }
}
```

- `id` is the artifact's CID, computed over the JCS-canonical credential with `proof` removed (§4.4). Content-addressing and the VC `id` are the same value.
- `issuer` is the signing entity's DID (§4.5).
- `credentialSubject` carries the artifact body. Every CP artifact kind defines its `credentialSubject` schema in §5–§18.
- `proof` is a Data Integrity proof under a cryptosuite from the Primitives Registry (§20). During the transition period an artifact MAY carry a second `proof` under `eddsa-jcs-2022` (§4.6).

#### 4.3.2 Registration Form — Design Note

SCITT Signed Statements are COSE_Sign1. VC 2.0 with Data Integrity is JSON. Two conformant bridges exist and CP specifies one:

**Normative form.** The SCITT Signed Statement's payload is the JCS-canonical VC *including its Data Integrity proof*. The COSE_Sign1 envelope is signed by the same issuer under a COSE algorithm from the Primitives Registry. The result carries two issuer signatures over the same content — the Data Integrity proof inside, the COSE signature outside.

This redundancy is deliberate. The artifact is a valid standalone VC verifiable by any VC 2.0 processor, *and* a valid SCITT Signed Statement verifiable by any SCITT relying party, without either needing to understand the other. The cost is one additional signature per artifact.

**Post-quantum requirement across both.** The Data Integrity proof MUST be post-quantum (§4.6). The COSE wrapper signature follows the COSE algorithm registry; CP requires it be drawn from the Primitives Registry but, during the transition period, permits a classical COSE algorithm because the PQ requirement is already satisfied by the inner proof. After 2030-01-01 both MUST be post-quantum. IETF COSE post-quantum algorithm identifiers (`draft-ietf-cose-dilithium` and successors) are tracked in Appendix F.

The alternative bridge — securing the VC solely via COSE (`vc+cose`, per *Securing Verifiable Credentials using JOSE and COSE*) — is conformant VC 2.0 but would move CP's post-quantum dependency from the W3C Data Integrity cryptosuites (§4.6) to the IETF COSE registry, which as of 2026-09-11 is less mature for PQ signatures. CP does not adopt it in this version.

#### 4.3.3 Tier Under a Flat Envelope

A Verifiable Credential is a flat claim format. CP's Tier 1 / Tier 2 distinction is not a property of the envelope; it is metadata on terms in the CP JSON-LD context (`https://daxfoundation.org/cp/v0.5`), which annotates each `credentialSubject` term with its tier and the section that governs it. A conforming processor MAY ignore this annotation; a conforming CP walker MUST honor it.

#### Why Tier 1

If artifacts used incompatible envelopes, nothing above this layer would interoperate. Adopting VC 2.0 places every CP artifact inside the largest deployed verifiable-claim ecosystem — resolvable by any DID resolver, verifiable by any VC processor — at the cost of no CP specification.

---

### 4.4 Canonicalization

JSON artifacts MUST canonicalize via RFC 8785 (JSON Canonicalization Scheme). Markdown artifacts MUST use UTF-8, normalize line endings to LF, strip trailing whitespace, and end with a single newline.

For hashing: canonicalize the credential with `proof` removed; the CID is over the result.
For signing: canonicalize the credential with `proof` removed; the Data Integrity proof is over the result per the cryptosuite's algorithm (all CP cryptosuites are `*-jcs-*`, so this is the same canonicalization).

Full rules in §19. This section was correct in v0.4.1 and is unchanged.

#### Why Tier 1

Two implementations canonicalizing differently produce different CIDs for identical content, and content-addressing fails silently across the boundary.

---

### 4.5 Identity Structure **[ADOPTED — D-021; amended D-014]**

Every CP entity has a Decentralized Identifier (W3C DID) whose method-specific identifier is derived from the hash of the entity's frozen genesis document. The identifier is therefore self-certifying: anyone holding the genesis document can confirm it is the one the identifier names.

#### 4.5.1 Required Structure

- **Fingerprint.** The DID's method-specific identifier: a 256-bit hash (BLAKE3-256 in spec text; other registered primitives per §20) of the JCS-canonical frozen genesis document. Rendered as a multibase string. Permanent. This is the entity's identity for all cross-references within the substrate.
- **Genesis document.** Frozen. Contains: the anchor public key (SLH-DSA-SHA2-128s, as a Multikey with registered multicodec `0x1220`); `kind`; `chain_role`; for delegates, `principal` and `delegation_chain`; `genesis_ts`; and the binding rule that the entity's current verification methods and service endpoints are whatever the rotation log, signed by the anchor key, currently declares.
- **Rotation log.** Append-only. Each entry adds, retires, or rotates a verification method or service endpoint; is signed by the anchor key; and references the genesis hash (§4.6.3). The DID document at any moment is the genesis document plus the rotation log folded to that moment.
- **Verification methods.** At least one post-quantum signing key in addition to the anchor: the workhorse, ML-DSA-44 (Multikey, multicodec `0x1210`). Transitional Ed25519 permitted alongside. Each method declares its `id`, `type`, `controller` (the fingerprint), `publicKeyMultibase`, and CP `role` (`anchor` | `signing` | `signing-classical`).
- **Service endpoints.** Resolution paths — `did:web` pointers, permanent-storage locators, friendly-name registry entries — expressed as DID document `service` entries. These supply *where*; the fingerprint supplies *integrity*.

#### 4.5.2 Kind and Chain Role **[D-014]**

v0.4.1 declared `kind: human | agent | system`. That conflated what an entity is with what role it plays in a delegation chain. This version splits them:

```
kind:       biological | nonbiological | institutional | composite
chain_role: principal | delegate
```

- A **principal** acts under no one's delegation. Its `delegation_chain` is empty. It is where accountability terminates (§1.12). Principal kind is unrestricted.
- A **delegate** acts on behalf of a principal. Its genesis document names `principal` (the principal's fingerprint) and `delegation_chain` (an ordered list of fingerprints from itself back to the principal). The chain MUST terminate at an entity whose `chain_role` is `principal`. A delegate's genesis MUST be co-signed by the entity immediately above it in the chain.
- `composite` denotes an entity whose control is distributed — a multi-signature institution, a collective. Its verification methods declare a threshold policy (§7.12).

#### 4.5.3 Cross-References

When any CP artifact references an entity, it MUST use the fingerprint (the DID), never a service endpoint, friendly name, or key. Endpoints and names are for resolution; the fingerprint is for reference. This keeps the substrate stable across key rotations and registry changes.

#### 4.5.4 Signing Identity **[SUBSTITUTED — replaces v0.4.1 "first DID" rule]**

v0.4.1 required signatures to verify under "the first DID in the array." Under DID semantics this becomes: a signature MUST verify under a verification method listed in the issuer's DID document with the `assertionMethod` relationship, **as the DID document stood at the signing timestamp** per the rotation log. A method retired after signing does not invalidate earlier signatures; a method not yet added at signing time does not validate them.

#### Why Tier 1

Identity is the foundation of every other claim. A non-self-certifying identifier depends on the honesty of whoever serves the document. A key-embedded identifier changes when the key rotates and breaks every reference. A `kind` that conflates entity type with chain role cannot represent a nonbiological principal, which §1.12 requires.

Full identity specification, custody model, and KYA-OS profile in §7.

---

### 4.6 Verification Policy **[D-016, D-016.a, D-016.b]**

#### 4.6.1 Post-Quantum Requirement

Every CP artifact MUST carry at least one Data Integrity proof under a post-quantum cryptosuite from the Primitives Registry (§20). As of this version the registered PQ cryptosuites are:

| Cryptosuite | Algorithm | Role |
|---|---|---|
| `mldsa44-jcs-2024` | ML-DSA-44 (FIPS 204, NIST Category 2) | Workhorse — routine artifact signing |
| `slhdsa128-jcs-2024` | SLH-DSA-SHA2-128s (FIPS 205, Category 1) | Anchor — rotation-log entries, genesis co-signing |

Both are defined in the W3C Credentials Community Group specification *Quantum-Resistant Cryptosuites v1.0* (`w3c/vc-di-quantum-resistant`), which as of 2026-09-11 states that it is experimental and not for production use. CP adopts it regardless, for reasons recorded in D-016: the envelope and the cryptosuite are separable; the suites are fully specified with test vectors and are implementable against liboqs; "experimental" describes W3C process status, not the FIPS-final algorithms beneath; CP made post-quantum signing Tier 1 in v0.4 and being ahead of cryptosuite maturity is consistent with that. CP implements against the specification, contributes to it, and tracks it to Recommendation (Appendix F).

**Workhorse is ML-DSA-44, not ML-DSA-65 [D-016.a].** v0.4.1 §7 specified ML-DSA-65. The W3C specification defines a cryptosuite only for ML-DSA-44. CP adopts 44: Category 2 security, 2,420-byte signatures (versus 3,309 for 65), and the parameter set the ecosystem is converging on.

#### 4.6.2 Transition Period

Until **2030-01-01**, an artifact MAY carry an additional proof under `eddsa-jcs-2022` (Ed25519). Verification policy during transition is **AND**: where both proofs are present, both MUST verify. A classical-only artifact — one with no PQ proof — MUST NOT be accepted at any time under this version.

After 2030-01-01, classical proofs MUST NOT be accepted as primary authority on any artifact intended to outlive that date. Implementations SHOULD stop producing them.

Verification policy is bound to `spec_version`. An artifact signed under an earlier version is verified under that version's policy (§1.8). A future version may tighten policy; it cannot retroactively invalidate.

#### 4.6.3 Anchor Binding **[D-016.b — new]**

The W3C cryptosuite specification's security analysis lists SLH-DSA's Exclusive Ownership and Non-Re-signability properties as *unknown* (ML-DSA has both). Without Exclusive Ownership, a signature could in principle verify under a second, adversarially constructed public key — a key-substitution attack.

CP mitigates this structurally and makes the mitigation normative: **every anchor-signed statement MUST be over content that binds the anchor public key.** Concretely, every rotation-log entry MUST include the genesis hash, and the genesis document contains the anchor public key. A signature over content that names the key it must verify under cannot be re-bound to a different key without changing the content and therefore the hash. Implementations MUST verify that a rotation-log entry's genesis reference resolves to a genesis document containing the anchor key the entry's signature verifies under.

#### Why Tier 1

Verification policy is the structural commitment about what counts as authentic. Without a normative PQ requirement, "anyone can verify" reduces to "anyone can verify under whatever assumptions they hold." Without anchor binding, the identity root inherits an unresolved cryptographic question.

---

### 4.7 Witness Distinct from Participants

The witness for an interaction MUST be a separate signing identity from every participant. In SCITT terms: the Transparency Service identity that signs a Receipt MUST NOT be, or be a delegate of, any Issuer of the statements it receipts within that context.

Independence is structural, not attested. A `witness.independence_assertion` field (§10.4) MAY carry the witness's signed declaration of independence; its absence is a weak claim, its presence a stronger one; neither substitutes for the identity check.

**Transitional exceptions.** Two patterns are acknowledged and MUST be declared:
- *Self-mediated systems* — where one entity is structurally both mediator and recorder of an interaction. Declared as `witness.relationship: participant`. Migration path: an external TS observing the mediating system.
- *Bootstrap* — where no external TS is yet available. Same declaration. Migration path: deploy one.

Downstream consumers SHOULD treat `witness.relationship: participant` attestations as lower-confidence. Walkers MUST surface the relationship field.

**Independent witnesses [D-005].** Cross-organization interactions are witnessed by each organization's own TS (§4.1.7).

#### Why Tier 1

The witness exists to record what happened independently of the participants' interests. A witness that is also a participant has interests that shape the record. The distinction is a matter of identity, and identity is checkable.

---

### 4.8 Validator Distinct from Witness

The validator that issues an AdherenceClaim MUST be a separate signing identity from the Transparency Service that receipted the WitnessAttestation being judged. One operator MAY run both; they MUST be distinct DIDs with distinct verification methods.

#### Why Tier 1

The witness records what happened; the validator judges adherence. If one identity does both, the record already contains a judgment, and no later validator can re-evaluate it cleanly. The time-indexed re-evaluation model (§11) depends on this separation.

---

### 4.9 Only a Validator Issues an AdherenceClaim — The Promotion Rule **[D-027 — new]**

No artifact is an AdherenceClaim unless its `issuer` is a **validator identity**: a DID that either (a) declares `role: validator` in its genesis document, or (b) is named as `validator_did` in the declared constraint of the context whose attestation the claim addresses.

An artifact produced by a delegate — including a SubAgentArtifact (§5.7) whose content is a verdict, a score, or a compliance judgment — is **evidence**, not a claim. It becomes part of an AdherenceClaim only when a validator identity issues one that references it in `evaluation_trace`.

This applies equally to inline validation (§10.9): the receiver's validator DID signs the inline claim. It applies to compliance-checker sub-agents: the sub-agent's output is a SubAgentArtifact; the validator that consumes it and countersigns produces the AdherenceClaim.

#### Why Tier 1

A delegate is one party's instrument. Its output is that party's evidence about itself. If a party's own delegate could issue the AdherenceClaim, the party would certify its own adherence, and the separation in §4.8 would be defeated one level down. The first operational run of CP (§27) exhibited exactly this: in-loop compliance verdicts flowed from a sub-agent directly into constraint state without a validator signature. This rule closes that path without forbidding the pattern — the sub-agent still runs; a validator countersigns.

---

### 4.10 Participant-Signed, Witness-Countersigned **[D-031 — new]**

Every entry in a CP log is a WitnessAttestation over a participant-signed statement. There is no unsigned raw-event layer beneath it.

Concretely, every event (§8) MUST carry two independently verifiable signatures by two distinct identities:

1. **The participant's signature** — the Data Integrity proof on the event credential, under the participant's verification method. This is authorship.
2. **The witness's countersignature** — the SCITT Receipt, under the Transparency Service identity. This is observation.

The witness MUST NOT register a statement lacking a valid participant signature. The participant's statement is not part of the record until receipted.

This is the SCITT model exactly: a Signed Statement (issuer) made transparent by a Receipt (TS). CP's contribution is to require it for every event, not only for artifacts an issuer chooses to make transparent.

#### Why Tier 1

The rule preserves the boundary the whole architecture depends on: the witness records; it does not author. A log entry with only a witness signature would be the witness's account of what a participant said. A log entry with only a participant signature would be unwitnessed. Two signatures, two identities, two functions.

---

### 4.11 Witness Emission and Scope-Filter

The Transparency Service MUST receipt every statement it registers (§4.1.2). Batched receipting on any cadence is permitted. The requirement is that a receipt eventually exists, not that it exists immediately.

The witness MAY filter *republication* — which receipts and statements it forwards to other TS instances or public indexes — by scope. It MUST NOT filter *registration* by scope: a private-scope statement presented to a private-scope TS is registered and receipted like any other. This ensures private-scope interactions are witnessed even though they are not published.

#### Why Tier 1

Without an emission requirement, a TS could decline to receipt selectively, leaving silent gaps. Without the registration/republication distinction, private interactions would go unwitnessed.

---

### 4.12 Scope Cannot Be Retroactively Narrowed **[D-006.a]**

Scope is fixed at context start — in SessionOpen where present, otherwise in the first event of the context (§9.3, D-030). Every statement in the context inherits it. Once declared, scope MUST NOT be narrowed. A statement registered at org scope cannot later be declared private.

Widening is permitted only as a new, witnessed act per §4.1.5: re-registration in the broader-scope TS with the original scope preserved and referenced.

#### Why Tier 1

Retroactive narrowing would be a mechanism for withdrawing information from future evaluation after the fact. §0.3 fails if scope can be tightened later.

---

### 4.13 Tombstone Never Removes from Queryability **[D-006]**

A Tombstone (§5.4, §13) is a referrer on its target. It affects *rendering* — walkers in default mode MAY suppress tombstoned artifacts. It does not affect *existence* — the target remains in the Verifiable Data Structure, retrievable by CID, enumerable by referrer type, and visible to any walker in pattern-detection or retrospective-evaluation mode.

In SCITT terms: nothing is ever removed from the log. A Tombstone is one more statement about a statement.

#### Why Tier 1

If tombstoning removed artifacts from pattern-matcher view, it would be the backdoor through which a coordinated bloc hides the artifacts that would reveal it. The rendering/existence distinction is what lets CP honor withdrawal requests without breaking §0.3.

---

### 4.14 Walker Contract — Substrate-Integrity Rules **[D-008; rule 7 new]**

A walker is any program that traverses the artifact graph. Beyond the following seven rules, walker behavior is extension-defined (§21). These seven are Tier 1 because the substrate's integrity claims fail if any walker may ignore them.

1. **Verify before honoring.** A walker MUST verify an artifact's Data Integrity proof (and, where present, its COSE wrapper) before treating its content as authored by its `issuer`.
2. **Verify witnessing.** A walker MUST verify the SCITT Receipt's inclusion proof against the TS's published tree head before treating an artifact as witnessed. An artifact without a valid receipt is unwitnessed and MUST be surfaced as such.
3. **Surface tombstones to pattern-matchers.** A walker in pattern-detection or retrospective-evaluation mode MUST include tombstoned artifacts. A walker in default rendering mode MAY suppress them but MUST indicate that suppression occurred.
4. **Process under declared version.** A walker MUST process each artifact under the `spec_version` it declares, not the walker's current version.
5. **Enumerate all claims.** A walker MUST be able to enumerate every AdherenceClaim attached to a given WitnessAttestation, not only the latest or the highest-confidence one.
6. **Verify per-context chains.** A walker MUST verify `previous_hash` links within a context and MUST flag a broken or gapped chain. It MUST NOT silently accept a chain with a missing link.
7. **Do not filter cross-constraint queries silently.** A walker operating under one constraint MUST NOT exclude artifacts from other constraints when the query is cross-constraint. It MAY annotate them; it MUST NOT hide them.

#### Why Tier 1

The substrate's guarantees are only as good as the least conformant walker. If any walker may skip receipt verification, unwitnessed content passes as witnessed. If any walker may hide tombstones from pattern-matchers, §4.13 is void.

---

### 4.15 Indexes Are Non-Authoritative

Any index — artifact index, concept index, tombstone index, referrer index, per-participant belief history, per-pair interaction model — is a non-authoritative accelerator. It MUST be reconstructible from the Verifiable Data Structure and the artifacts it contains. Where an index disagrees with the log, the log is correct and the index is regenerated.

This is why cross-episode belief and interaction stores (D-039) are not primitives: they are indexes. CP guarantees their inputs exist and are witnessed (§8, §11); it does not specify their aggregation.

#### Why Tier 1

If intelligence lived in indexes, the substrate would no longer be dumb (§3), and two implementations with different indexes would disagree about what the record says.

---

### 4.16 PII Commitment

CP is append-only. Adopters MUST treat artifact content as permanent.

Adopters operating under jurisdictions that grant deletion rights (GDPR, CPRA, and successors) MUST NOT place personally identifiable information in artifact content at org or public scope.

At private scope, PII MAY exist only as a **detached payload** (§4.1.3): the Signed Statement carries the payload hash; the payload itself is held under the participants' access control and may be destroyed. The hash in the log remains — permanently attesting that content existed, and what its hash was, without the content. This is the escape hatch, and it is available only at private scope.

Adopters MUST document which mechanism they use.

#### Why Tier 1

Append-only and right-to-deletion cannot both hold over the same bytes. The commitment resolves the conflict by construction rather than by policy.

---

### 4.17 Forking

Spec-version-bearing artifacts — ConstraintDecl, Policy, Validator, ExtensionDecl, and this specification itself — MUST carry `fork_of`: `null` for a genesis artifact, or the CID of the predecessor. The forking lineage is walkable through `fork_of`.

#### Why Tier 1

Anti-ossification (§1.6) is exercised through forking. If some forkable artifact kinds carried lineage and others did not, forkability would be asymmetric across the substrate.

---

### 4.18 Summary — Tier 1 Rules and Their Sources

| § | Rule | Source |
|---|---|---|
| 4.1 | Witnessed ledger is a SCITT Transparency Service; per-context chain; scoped instances; structural-only registration | IETF SCITT + CP profile |
| 4.2 | Attestations attach as typed referrers; non-owner attachment; target immutable | OCI referrers / AGNTCY `dir` + CP types |
| 4.3 | Every artifact is a VC 2.0 with Data Integrity proof; SCITT payload is the JCS-canonical VC | W3C VC 2.0 + CP registration form |
| 4.4 | RFC 8785 canonicalization | IETF |
| 4.5 | Self-certifying DID from frozen genesis; `kind` / `chain_role` split; chain terminates at principal | W3C DID + CP |
| 4.6 | ≥1 PQ proof (`mldsa44-jcs-2024` / `slhdsa128-jcs-2024`); hybrid until 2030; anchor binding | W3C QR Cryptosuites + FIPS 204/205 + CP |
| 4.7 | Witness ≠ participant | CP |
| 4.8 | Validator ≠ witness | CP |
| 4.9 | Only a validator DID issues an AdherenceClaim | CP |
| 4.10 | Participant-signed + witness-receipted, always | SCITT model, made universal by CP |
| 4.11 | Receipt every registration; filter republication not registration | SCITT + CP |
| 4.12 | Scope non-narrowable | CP |
| 4.13 | Tombstone affects rendering, never existence | CP |
| 4.14 | Seven walker rules | CP |
| 4.15 | Indexes non-authoritative | CP |
| 4.16 | No PII at org/public scope; detached payload at private | CP |
| 4.17 | `fork_of` on all forkable kinds | CP |

Eleven of seventeen rules are CP's own. The six that adopt standards are the six that carry the most implementation weight. That is the intended shape.

---

## 5. TIER 2 PRIMITIVES — SKELETON-ONLY

A Tier 2 primitive has a structural shape defined here and semantic content supplied by extensions. CP says the slot exists and what fields it has. An extension says what fills it in its domain.

Every Tier 2 primitive is a Verifiable Credential type in the CP JSON-LD context (§4.3). Its `credentialSubject` schema is given below. Where a primitive is a referrer (§4.2), its referrer type is given. Where a primitive is a *field* on another artifact rather than an artifact itself — stance, revision cause, deferral, prior and posterior — its carrier is named.

Each entry states: what CP defines, what extensions define, and why the line falls where it does.

---

### 5.1 Concept

A knowledge unit referenceable by identifier.

**CP defines:**
```
credentialSubject: {
  artifact_kind:  "Concept",
  concept_id:     "<URI>",                  // urn:concept:<domain>:<category>:<specific>
  scope:          "<scope>",
  label:          "<string>",
  links: [ {
    predicate:    "<PROV-O term or subproperty, §6.5>",
    ref:          "<concept_id | CID | DID>",
    attribution:  "<DID | null>",
    confidence:   <0..1>,
    explanation:  "<string | null>"
  } ],
  status:         "candidate | confirmed | <ext>",
  created_ts:     "<iso8601>"
}
```

The `concept_id` form `urn:concept:<domain>:<category>:<specific>` is adopted from the Internet of Cognition L9 protocol's concept URIs (D-047) so that CP concepts and L9 concepts are the same namespace where domains overlap.

**Extensions define:** what a concept *is*. An education extension adds definitions, aliases, prerequisites, and mastery semantics. An attribution extension treats a concept as a creative work with authorship and derivation. A governance extension treats it as a precedent with applicability and supersession.

**Why Tier 2:** every domain needs referenceable knowledge units; no two domains agree on what one is.

---

### 5.2 ConceptCollection

A grouping of concepts for queryability and discovery.

**CP defines:**
```
credentialSubject: {
  artifact_kind:  "ConceptCollection",
  collection_id:  "<ULID>",
  scope:          "<scope>",
  label:          "<string>",
  description:    "<string | null>",
  concept_ids:    [ "<concept_id>" ],
  tags:           [ "<string>" ],
  created_by:     "<DID>",
  created_ts:     "<iso8601>"
}
```

Collections are designed to be indexable. Walkers in surface-rendering mode SHOULD expose collection metadata to discovery tooling; an OASF record for a CP entity MAY list its public collections.

**Extensions define:** ordering, prerequisite structure, learning paths, misconception pairs, search metadata.

---

### 5.3 RoleGrant **[SUBSTITUTED — D-018]**

Explicit, scoped, auditable, revocable authority. v0.4.1 specified a bespoke RoleGrant artifact; this version expresses it as a Verifiable Credential issued by the granting principal, with revocation via Bitstring Status List (one of the seven VC 2.0 Recommendations).

**CP defines:** the RoleGrant *is* the credential.
```
{
  "type": ["VerifiableCredential", "RoleGrant"],
  "issuer": "<DID of granting principal>",
  "validFrom": "<iso8601>",
  "validUntil": "<iso8601 | absent>",
  "credentialSubject": {
    "id":     "<DID of grantee>",
    "roles":  [ "<extension-defined role string>" ],
    "scope":  "<scope>"
  },
  "credentialStatus": {
    "type": "BitstringStatusListEntry",
    "statusPurpose": "revocation",
    "statusListIndex": "<n>",
    "statusListCredential": "<URL of the issuer's status list>"
  },
  "proof": { ... }
}
```

Rules:
- The issuer MUST be a principal, or a delegate whose own RoleGrant includes authority to grant the roles in question. Authority does not exceed its source.
- Roles are scope-bounded. A grant at `org` scope confers nothing at `public` scope.
- **Issuance MUST check `blocks_roles` [D-029].** Before issuing a RoleGrant, the issuer MUST determine whether any Constraint (§5.8) in the grant's scope is in BLOCKING state with a `blocks_roles` entry matching any requested role. If so, issuance MUST refuse, and the refusal MUST be recorded as a WitnessAttestation with `claim_type: delegation-refused` (§10.3).
- Revocation is a status-list flip, not a new artifact. The original grant remains in the log with its revocation observable via the status list. Walkers MUST check status before honoring a grant.

**Extensions define:** which roles exist and what they permit.

**Alignment:** this is the KYA-OS delegation shape (§7.13) applied to authority within CP. "Who authorized this" is the issuer; "what may it do" is `roles`; "in what scope" is `scope`.

**Why Tier 2:** authority must be explicit everywhere — that is the structural defense against FM-AC — but every domain has different roles.

---

### 5.4 Tombstone

A marker that an artifact is withdrawn. A referrer of type `cp.tombstone.v1` on its target.

**CP defines:**
```
credentialSubject: {
  artifact_kind:      "Tombstone",
  target_ref:         "<CID>",
  reason:             "<string>",
  tombstoned_by:      "<DID>",
  scope_at_creation:  "<scope of target when tombstoned>",
  ts:                 "<iso8601>"
}
```

Semantics are scope-dependent (D-006):
- **Private scope, internal witness only.** The participants and their TS are the whole universe of holders. A Tombstone agreed by them is effective within that scope: default rendering suppresses the target.
- **Org or public scope.** A Tombstone is a *request*. Walkers in default rendering mode MAY honor it. Other TS instances holding independent receipts of the target are unaffected. The target remains in every log it was registered in.

At every scope, §4.13 governs: the target is never removed, never hidden from pattern-detection or retrospective-evaluation walkers.

A participant recording stance `retracted` (§5.9) MAY issue a Tombstone; the stance does not require it.

**Extensions define:** what circumstances warrant tombstoning in their domain, and any additional authority required.

---

### 5.5 Patch

An additive correction that neither contests nor withdraws. A referrer of type `cp.patch.v1`.

**CP defines:**
```
credentialSubject: {
  artifact_kind:       "Patch",
  target_ref:          "<CID>",
  patch_type:          "<extension-defined string>",
  correction_payload:  { ... },
  created_by:          "<DID>",
  ts:                  "<iso8601>"
}
```

Walkers render the patched view by default (most recent Patch by the target's author, or by an authority the extension recognizes) and MUST retain access to the unpatched original.

A participant recording stance `revised` MAY issue a Patch; the stance does not require it.

**Extensions define:** `patch_type` vocabulary — typo, clarification, supersession, version-bump — and who may patch whose artifacts.

**Why Tier 2:** every domain needs corrections; Tombstone and Contestation are the wrong tools for a typo.

---

### 5.6 Scope

A declared boundary on who may structurally witness an interaction.

**CP defines:** scope is a field, declared once at context start (§9.3), inherited by every statement in the context, and governed by three Tier 1 rules — non-narrowable (§4.12), determines the Transparency Service instance (§4.1.5), and never hides tombstoned content from pattern-matchers (§4.13).

**CP suggests, extensions extend:** the values. CP's baseline is `private | org | public`. An education extension might use `classroom | school | district | public`; an enterprise extension `team | org | partners | public`; a personal extension `self | intimate | social | public`. Extensions declare their scope vocabulary and its ordering (which values are narrower than which) in their ExtensionDecl (§23).

**Why Tier 2 for values, Tier 1 for rules:** the rules are what make scope trustworthy; the labels are what make it usable.

---

### 5.7 SubAgentArtifact **[NEW — D-026]**

The unit of nonbiological work: the output of one invocation of a model or tool in a named role.

**CP defines:**
```
credentialSubject: {
  artifact_kind:  "SubAgentArtifact",
  context_id:     "<context>",
  role:           "<extension-defined role string>",
  brief_ref:      "<CID of the instruction this responds to | null>",
  produced_via: {
    method:        "<string>",          // e.g. "llm-completion", "tool-call"
    model_used:    "<string | null>",   // e.g. "<vendor>-<model>-<version>"
    model_version: "<string | null>",
    provider:      "<string | null>"    // e.g. "<model provider>", "<gateway>"
  },
  output:         "<string | absent>",
  output_ref:     "<CID of detached payload | absent>",   // exactly one of output / output_ref
  tokens:         { input: <n>, output: <n> } | null,
  latency_ms:     <n> | null,
  ts:             "<iso8601>"
}
```

The issuer is a delegate (`chain_role: delegate`, §4.5.2). Its delegation chain terminates at a principal; the SubAgentArtifact is attributable to that principal.

**Rules:**
- `produced_via.model_used` and `produced_via.provider` MUST be populated when known. They are the fields that make cross-model attestability possible: a future validator asking whether artifacts from one model diverged systematically from another's needs them recorded.
- A SubAgentArtifact whose `output` is a verdict, score, or judgment is **evidence** (§4.9). It does not become an AdherenceClaim until a validator identity issues one referencing it.
- Large outputs SHOULD use `output_ref` (detached payload, §4.1.3).

**Extensions define:** the `role` vocabulary — `api-designer`, `compliance-checker`, `reviewer`, `deployer` — and what each role is permitted to produce.

**Why Tier 2:** every agentic deployment produces these, and the record of *which model, in which role, produced what* is load-bearing for retrospective evaluation; but what the roles are is a domain matter. The first operational run of CP (§27) produced thirteen of these without the specification naming them. This version names them.

---

### 5.8 Constraint **[NEW — D-028, D-029]** and its relation to ConstraintDecl

Two things in prior versions and in operational use shared the name "constraint." This version separates them.

**ConstraintDecl** (§20.3) is a *declared normative frame* — the standard an entity adheres to. DAX is a ConstraintDecl. It is Tier 1: forkable (`fork_of`), lineage-bearing, the thing AdherenceClaims are made against.

**Constraint** is an *instance-level obligation raised under a ConstraintDecl* — a specific, scoped, lifecycle-bearing commitment that may block actions until it is resolved. "The authentication flow has unresolved friction; do not spawn implementers until it is addressed" is a Constraint, raised under DAX. It is Tier 2.

Every Constraint MUST reference the ConstraintDecl it is raised under. Constraints compound under their frame the way artifacts compound under a lineage.

**CP defines:**
```
credentialSubject: {
  artifact_kind:          "Constraint",
  constraint_id:          "<string>",
  under_constraint_decl:  "<CID of ConstraintDecl>",
  scope:                  "<scope>",
  declared_by:            "<DID>",
  source_ref:             "<CID of the artifact or event that triggered it | null>",
  description:            "<string>",
  blocks_roles:           [ "<extension-defined role string>" ],
  fork_of:                "<CID | null>",
  ts:                     "<iso8601>"
}
```

**Lifecycle.** A Constraint has four states:

```
RAISED  ──►  RESOLVED  ──►  (closed)
   │              │
   ▼              ▼
BLOCKING     REOPENED  ──►  RESOLVED | BLOCKING
```

- **RAISED** — declared; not yet blocking.
- **BLOCKING** — `blocks_roles` is in force in the Constraint's scope.
- **RESOLVED** — a resolution has been recorded with `resolution_evidence_ref`.
- **REOPENED** — a validator's AdherenceClaim found the resolution insufficient; the Constraint returns to BLOCKING with a `compliance_failure` block.

Transitions are **append-only WitnessAttestations** with `claim_type: constraint-lifecycle` (§10.3), each carrying `from_state`, `to_state`, `evidence_ref`, and — for REOPENED — `compliance_failure`:

```
compliance_failure: {
  verdict:       "<validator's verdict shape/value, §11.1>",
  score:         <0..1>,
  reopened_ts:   "<iso8601>",
  evidence_ref:  "<CID of the AdherenceClaim that triggered reopening>"
}
```

`compliance_failure.evidence_ref` MUST be an AdherenceClaim issued by a validator identity (§4.9). A sub-agent's compliance output alone cannot reopen a Constraint.

**Current state is derived, never stored authoritatively (§4.15).** A walker computes state by folding the lifecycle attestations in chain order. Any stored "current state" is an index.

**Role-binding [D-029].** While a Constraint is BLOCKING, the roles in `blocks_roles` MUST NOT be granted (§5.3) or spawned within the Constraint's scope. An attempt to do so MUST be refused, and the refusal MUST be recorded as a WitnessAttestation with `claim_type: delegation-refused`, referencing the Constraint. The attempt is thereby preserved as evidence.

This is the one place refusal occurs under CP, and it is *declared* gating, not substrate gating (§0.2): the Constraint says what it blocks; the substrate records the block and the attempt. The first operational run exhibited three bypass attempts against BLOCKING Constraints; all three were refused and all three are permanent records.

**Extensions define:** the `blocks_roles` vocabulary (it is the RoleGrant role vocabulary), what evidence resolves a Constraint in their domain, and who may raise one.

**Why Tier 2:** the lifecycle shape is universal; what counts as resolution is not.

---

### 5.9 Participant Stance **[NEW — D-038]**

A participant's epistemic position within a context. A field on position-bearing events (§8), not an artifact.

**CP defines the vocabulary:**

| Stance | Meaning | May trigger |
|---|---|---|
| `asserted` | position stated on the participant's own evaluation | — |
| `deferred` | position adopted from another participant (see `deferred_to`, §5.10) | — |
| `revised` | position changed from a prior statement in this context | Patch (§5.5) |
| `retracted` | position withdrawn | Tombstone (§5.4) |
| `challenged` | position disputed by this participant | Contestation (§12) |
| `unresolved` | participant records that convergence was not reached and that this is the honest outcome | — |

A stance does not require an artifact. It records a position; the artifact, if any, records an action.

**`unresolved` is first-class.** Structured impasse — parties who engaged each other's evidence and did not converge — is a valid, recordable, witnessable outcome. It is not an absence and it is not a failure of the protocol. This is §1.10 made concrete: exit is a success state, and so is honest non-agreement.

**Extensions define:** additional stances, namespaced.

**Attribution:** the vocabulary is adapted from the BeliefStatus set in the Internet of Cognition SIEP subprotocol (D-047, Appendix C).

---

### 5.10 Revision Cause and Deferral **[NEW — D-034, D-036]**

Two fields on position-bearing events that together record *why* a position changed and *whose* influence changed it.

**CP defines:**

```
revision_cause:  "grounded_argument | social_compliance | semantic_memory
                  | new_evidence | repair_resolution | <ext-namespaced>"
deferred_to:     "<DID of the participant whose position was adopted> | null"
```

- `revision_cause` is REQUIRED when stance is `revised` or `deferred`. Values:
  - `grounded_argument` — changed because the other party's evidence was engaged and found persuasive
  - `social_compliance` — changed without engaging the other party's evidence
  - `semantic_memory` — position drawn from prior knowledge, not from this exchange
  - `new_evidence` — external information, not from any participant
  - `repair_resolution` — changed to resolve a grounding failure
- `deferred_to` is REQUIRED when stance is `deferred`. `null` means the position was held on the participant's own evaluation. Non-null names the participant it was adopted from.

Both fields live in the witnessed event body. They are participant-signed and witness-countersigned (§4.10). **This is the property that distinguishes CP's record from the systems these fields are borrowed from:** in the Internet of Cognition's SIEP, the same fields are self-reported and locally held, so a coordinated bloc can misreport its own deferrals. In CP they are witnessed, and cannot be altered after the fact.

**Why these fields are the Sybil substrate.** A coordinated bloc of identities that present as independent has a signature in the deferral graph that no single interaction reveals: deferral concentrating toward one node; `social_compliance` dominating `revision_cause` within the bloc; influence flowing one direction across many contexts; priors (§5.11) correlated before any exchange. Every element of that signature is visible only across many witnessed interactions over time. CP records the inputs. Detection is a validator's or a meta-validator's job (§26.1), and CP does not specify it. What CP guarantees is that when someone looks, the record is there and cannot have been edited.

**`DEFERS_TO` predicate.** Deferral is also expressible as a third-party-assertable Relationship (§15): `cp:defersTo`, a subproperty of `prov:wasInfluencedBy` (§6.5). This lets a pattern-detector record, as a signed artifact, deferral it has inferred across contexts — distinguishable from participant-declared deferral by its issuer.

**Extensions define:** additional causes, namespaced; metrics computed over these fields (§11.1).

**Attribution:** the `revision_cause` vocabulary is adopted from the Internet of Cognition CIP subprotocol; `deferred_to` from SIEP (D-047, Appendix C).

---

### 5.11 Prior and Posterior **[NEW — D-035]**

A participant's position on a concept before peer contact, and after.

**CP defines:**

At context start (§9.3), a participant MAY record `prior_ref`: the CID of a witnessed statement of its positions, per concept, made *before* any exchange in this context. Once recorded, the prior is immutable for the context.

On position-bearing events:
```
positions: [ {
  concept_id:  "<URI>",
  prior:       <0..1> | null,      // from prior_ref; null if none declared
  posterior:   <0..1>,             // current position
  stance:      "<§5.9>",
  revision_cause: "<§5.10 | absent>",
  deferred_to:    "<DID | null>"
} ]
```

**The prior and posterior are the participant's positions. They are not the validator's verdict.** An AdherenceClaim's `verdict` (§11.1) is a validator's probabilistic judgment of adherence to a constraint. A participant's `posterior` is what the participant currently holds. The two never merge, are never compared as if commensurable, and are carried in different artifacts by different issuers.

**Why this matters.** Without a declared prior, influence is unmeasurable: one sees where a participant ended up, not how far it moved or who moved it. For a substrate whose purpose is retrospective judgment of whether interactions were legitimate, an unmeasurable influence delta is a blind spot. With prior, posterior, `revision_cause`, and `deferred_to` all witnessed, the influence delta is attributable — by anyone, later.

**Extensions define:** whether priors are required in their domain, at what granularity, and what metrics are computed over them.

**Attribution:** adopted from the Internet of Cognition CIP subprotocol's immutable-prior requirement (D-047).

---

### 5.12 Failure Mode Taxonomy

CP defines a baseline vocabulary of named failure modes. It is engineering vocabulary, used throughout this specification to say what a rule defends against. Extensions add domain-specific modes, namespaced.

| Code | Name | What it names | Primary defense |
|---|---|---|---|
| FM-AC | Authority Creep | implicit authority accumulating without explicit grant | RoleGrant §5.3 |
| FM-AS | Amplification → Substitution | system output replacing rather than amplifying an entity's intent | Episodicity §1.10 |
| FM-CS | Creativity Suppression | substrate constraining valid expression | Constraint-agnosticism §1.4 |
| FM-DO | Determinism Overreach | system claiming meaning, truth, or correctness it cannot structurally guarantee | Sacred Boundary §1.9; structural verification §0.2 |
| FM-EM | Entity Minimization | an entity's expression disappearing into another's voice | Participant signature §4.10 |
| FM-FC | Founder Capture | initial conditions creating path-dependent bias | Anti-ossification §1.6; forking §4.17 |
| FM-EA | Evaluator Arms Race | sophisticated actors gaming validators at aggregate level | Accumulating claims §11.3; meta-validation §26.1 |
| FM-NL | Narrative Laundering | coordinated entities distorting the commons across many hands | Deferral recording §5.10; open contestation §12 |
| FM-WC | Witness Compromise | unreliable or captured attestation | Witness independence §4.7; independent witnesses §4.1.7 |
| FM-AL | Aggregate Lineage Bias | cross-lineage import carrying statistical bias invisible at artifact level | §1.5; open research §26.1 |
| FM-SC | Self-Certification | a party's own delegate issuing the judgment of that party's adherence | Promotion rule §4.9 |
| LEAK | Cross-Scope Leakage | content crossing a sovereignty boundary without authorization | Scoped TS §4.1.5; non-narrowing §4.12 |
| COMP | Compliance Failure | PII or deletion-right violation | PII commitment §4.16 |

FM-SC is new in this version. It names the failure the first operational run exhibited and the promotion rule closes.

The threat-modeling method that uses this vocabulary — for each field, relationship, or rule: *wrong if, missing if, misused if, detect, mitigate, defends against* — is in §22.

---

## 6. EXTENSION COMPOSITION

### 6.1 The Extension DAG

Extensions form a directed acyclic graph, not a tree.

- **Layer 1 — CP.** The substrate. Tiers 1 and 2.
- **Layer 2 — foundational extensions.** Sit directly on CP. Attribution, Credit, Education, Governance, Identity-augmentation. They are siblings; none descends from another.
- **Layer 3 and beyond — specialized extensions.** Extend a Layer 2 extension where there is a genuine specialization: a music-royalty extension extending Attribution. Most extensions do not need this.

An artifact MAY claim membership in multiple extensions simultaneously. It carries the CP skeleton plus each extension's interpretation. Extensions whose interpretations of the same primitive conflict cannot both apply to one artifact; walkers MUST detect and report the conflict rather than pick one.

### 6.2 Lens Composition

Extensions are lenses. Each reveals a semantic structure on the same skeleton. A Concept viewed through Education shows prerequisites and mastery; the same Concept through Attribution shows authorship and derivation. Lenses stack where they do not contradict.

This is the constraint protocol applied to itself: CP's structural constraints are the ground on which extension meaning emerges; each extension's constraints are the ground for the next layer's. Structure in, structure out.

### 6.3 Namespacing — Artifact Kinds and Referrer Types **[D-007, D-024]**

**CP-native kinds** are bare VC types in the CP context: `Concept`, `WitnessAttestation`, `AdherenceClaim`, `Constraint`, `SubAgentArtifact`, and the rest of Appendix A. Their referrer types are `cp.<kind>.v<n>`.

**Extension kinds** are prefixed: `attribution:Charter`, `education:Rubric`, `education:LearnerConceptState`, `governance:Precedent`. Their referrer types are `<ext>.<kind>.v<n>`.

An extension's JSON-LD context defines its terms; an artifact claiming that extension includes the context. Walkers resolve the prefix to the extension's interpretation.

**Promotion.** When multiple extensions independently define the same kind, it MAY be promoted to CP-native in a later version through §24. The default is namespacing.

### 6.4 Event Kinds and Sub-Kinds **[D-012; L9 mapping per D-047]**

CP defines a conservative top-level taxonomy. Sub-kinds are namespaced beneath a top-level kind. New top-level kinds are added by extensions with a prefix, or promoted through §24.

| CP kind | Meaning | Nearest L9 `Kind` | Note |
|---|---|---|---|
| `OBSERVE` | an entity captures an external event | `exchange` (partial) | L9 has no pure observation kind |
| `INTENT` | an entity declares intent | `intent` | direct |
| `EFFECT` | an entity produces a result | `commit` | L9 `commit` is a committed outcome |
| `ERROR` | error or exception | — | no L9 analogue |
| `POLICY` | a policy or constraint event | — | L9 `PolicyLabel` is data-handling classification, not this |
| `GATE` | a gate decision (permit / refuse) | — | no L9 analogue |
| `CHALLENGE` | a contestation event | — | SIEP has a `challenge` speech act at the utterance level, not an event kind |
| `ADJUDICATE` | an adjudication event | — | no L9 analogue |
| `PATCH` | a correction event | — | no L9 analogue |
| — | — | `contingency` | L9's grounding-check kind; CP records grounding via `revision_cause: repair_resolution` and CIP-style engagement fields, not as an event kind |
| — | — | `knowledge` | L9's knowledge-transfer kind; CP records knowledge as Concept/artifact production under `EFFECT` |

Sub-kinds: `OBSERVE.TEXT`, `OBSERVE.MEDIA`, `OBSERVE.ACTION`; `INTENT.DECLARE_OBJECTIVE`, `INTENT.PUBLISH`, `INTENT.FORK`; `GATE.PERMIT`, `GATE.REFUSE`; and extension-defined.

The mapping is bidirectional guidance, not a normative transform. Where an L9 message is witnessed by CP, the CP event carries `transport_ref` to the L9 message and the CP kind that best describes it. Appendix C carries the full vocabulary map.

### 6.5 Predicates — PROV-O Baseline **[SUBSTITUTED — D-017]**

v0.4.1 defined a bespoke predicate vocabulary. This version adopts W3C PROV-O as the baseline and defines CP's predicates as subproperties of PROV terms, so that any PROV-aware tool can reason over CP relationships at the PROV level and any CP walker can reason at the CP level.

**Adopted directly from PROV-O:**

| Term | Use in CP |
|---|---|
| `prov:wasDerivedFrom` | artifact derived from another |
| `prov:wasGeneratedBy` | artifact generated by an activity (event, compilation) |
| `prov:wasAttributedTo` | artifact attributed to an agent (entity) |
| `prov:wasInfluencedBy` | broadest influence relation; superproperty of deferral |
| `prov:wasInformedBy` | activity informed by another activity |
| `prov:hadPrimarySource` | derivation from an authoritative source |
| `prov:wasRevisionOf` | later version of an artifact |
| `prov:wasInvalidatedBy` | artifact invalidated by an activity |

**CP subproperties (defined in the CP context):**

| CP predicate | Subproperty of | Use |
|---|---|---|
| `cp:createdFromEvent` | `prov:wasGeneratedBy` | artifact compiled from a witnessed event |
| `cp:patches` | `prov:wasRevisionOf` | Patch → target |
| `cp:tombstones` | `prov:wasInvalidatedBy` | Tombstone → target |
| `cp:defersTo` | `prov:wasInfluencedBy` | position adopted from another participant (§5.10) |
| `cp:contests` | `prov:wasInfluencedBy` | Contestation → target |
| `cp:adjudicates` | `prov:wasInfluencedBy` | Adjudication → Contestation |
| `cp:importsReasoning` | `prov:wasInformedBy` | Contestation → prior Contestation or Adjudication whose reasoning it reuses (§12.4) |
| `cp:raisedUnder` | `prov:wasInfluencedBy` | Constraint → ConstraintDecl |
| `cp:republishedFrom` | `prov:wasDerivedFrom` | scope-widened re-registration → original (§4.1.5) |

**Extensions** define their predicates as subproperties of PROV-O or CP terms: an education extension's `education:requiresUnderstandingOf` under `prov:wasInfluencedBy`; an attribution extension's `attribution:hardDependency` under `prov:wasDerivedFrom`.

PROV-AGENT (IEEE e-Science 2025), which extends PROV-O for agent prompts, responses, and decisions via MCP, is compatible with this mapping and is tracked in Appendix F as a source of further alignment.

### 6.6 Subprotocol Correspondence **[D-047]**

What CP calls an *extension*, the Internet of Cognition calls a *subprotocol* (SIEP, CIP, SAB, TFP are subprotocols of SSTP). The concepts correspond: a named body of vocabulary and rules layered on a base protocol. CP retains "extension" because its lens-composition semantics (§6.2) are load-bearing and not implied by "subprotocol." Appendix C maps the terms.

### 6.7 Declaring an Extension

An extension is declared by an ExtensionDecl artifact (§23), which names what it extends, its version, its context URI, its kinds, event kinds, predicates, scope vocabulary, and interpretations of Tier 2 primitives. ExtensionDecl carries `fork_of` (§4.17).

---

## 7. IDENTITY AND CUSTODY

### 7.0 What Changed in This Version

CP-SPEC v0.4.1 specified the identity layer in its own vocabulary — "primary handle," "ID array," "verification methods," "rotation log." This version keeps the structure and re-expresses it in the vocabulary of W3C Decentralized Identifiers and Verifiable Credentials 2.0 (D-021), because the structure was already a DID document lifecycle in all but name. What follows is what was there, said in the words everyone else uses, with five substantive changes:

1. `kind` is split from `chain_role` so that a nonbiological principal is representable (D-014, §4.5.2).
2. The workhorse signing key is ML-DSA-44, not ML-DSA-65 (D-016.a, §4.6.1).
3. Anchor signatures MUST bind the anchor public key (D-016.b, §4.6.3).
4. The rotation log adopts **pre-rotation** from KERI — each anchor commits to the hash of its successor in advance — which closes an attack the v0.4.1 design left open (§7.5).
5. Delegation is a profile of DIF KYA-OS, generalized to entity-neutral principals (D-022, §7.13).

The custody model (D-013) — frozen genesis, append-only log, permanent storage, operator pays but never controls, independent path always open, friendly name never root — is unchanged.

---

### 7.1 Why This Structure

Two pressures shape the identity layer. Cryptographic primitives will need rotation over the decades CP is meant to span, so identity cannot be welded to a key. No operator may become a chokepoint, so identity cannot be welded to a host. The structure separates four things that are habitually conflated: the **name**, the **keys**, the **resolution paths**, and the **custody**.

### 7.2 The Four Concerns, in DID Terms

| Concern | What it is | DID term | Mutability |
|---|---|---|---|
| **Name** | The entity's permanent identifier — the hash of its frozen genesis document | The DID (method-specific identifier) | Never changes |
| **Keys** | Cryptographic key material — anchor and signing keys | `verificationMethod` entries in the DID document | Rotated via the log |
| **Resolution paths** | Where to fetch the DID document; which providers verify the entity | `service` entries (resolution) + `verificationMethod` / `authentication` (verification) | Added and retired via the log |
| **Custody** | Where the genesis and log physically live; who publishes them | Not a DID concept — CP's contribution (§7.6–7.9) | Multi-local by requirement |

The DID **recognizes** — it names which entity this is and lets anyone integrity-check the genesis document. A verification method or provider **verifies** — proves the entity is who the DID names by exercising a secret. A bare DID proves nothing; anyone can present a name. Proof requires a key.

### 7.3 The DID Method — Design Note

CP requires a DID method with four properties:

- **P1 — Self-certifying from a frozen document.** The method-specific identifier is derived from the hash of an immutable genesis document, so that anyone holding the document can confirm it is the one the DID names, regardless of who served it.
- **P2 — Append-only key event log.** Key and service changes are recorded as signed, sequenced, hash-linked entries; the current DID document is a deterministic fold of genesis plus log.
- **P3 — Post-quantum verification methods.** Multikey encodings with registered multicodecs for FIPS 204/205 keys (§4.6, §7.10).
- **P4 — Resolution independent of any single host.** The genesis and log are retrievable from more than one place, including a permanent content-addressed substrate (§7.6).

**Existing methods against these properties.** `did:key` embeds the public key as the identifier — rotation changes the identity; fails P1's spirit and P2. `did:web` is location-based — fails P1 and P4 as a root. `did:webs` (KERI) derives the identifier from a Self-Addressing Identifier of the inception event and manages keys through a Key Event Log with pre-rotation — satisfies P1, P2, and P4 by design, and is the closest existing method to what CP needs. As of 2026-09-11, KERI's CESR encoding does not define codes for FIPS 204/205 keys, so P3 is not yet met by `did:webs`.

**Reference method.** Pending PQ support in `did:webs`, CP specifies a reference method `did:cp`:

```
did:cp:<multibase(BLAKE3-256(JCS(genesis_document)))>
```

whose document lifecycle is the KERI Key Event Log pattern expressed in CP's JSON/VC encoding (§7.4–7.5). The identifier derivation is one hash; the log format is KERI's design in CP's serialization. **This is a placeholder, not a contribution:** when `did:webs` gains PQ CESR codes, CP's reference method migrates to it and `did:cp` is deprecated. Appendix F tracks the condition. Any method satisfying P1–P4 conforms.

### 7.4 The Genesis Document — Frozen Inception

The genesis document is written once and never modified. Its hash is the DID. It contains:

```
{
  "cp_genesis":         "0.5",
  "kind":               "biological | nonbiological | institutional | composite",
  "chain_role":         "principal | delegate",
  "principal":          "<DID of principal | absent for principals>",
  "delegation_chain":   [ "<DID>", ... ]        // self → … → principal; absent for principals
  "anchor": {
    "id":                 "#anchor-0",
    "type":               "Multikey",
    "publicKeyMultibase": "<u… SLH-DSA-SHA2-128s, multicodec 0x1220>"
  },
  "next_anchor_commitment": "<BLAKE3-256 of the next anchor's publicKeyMultibase>",
  "genesis_ts":         "<iso8601>",
  "binding_rule":       "The verification methods and services of this identity are those declared in the rotation log signed by the anchor key named here, folded to the time of evaluation."
}
```

**Rules:**
- The genesis MUST contain exactly one anchor key, of type SLH-DSA-SHA2-128s.
- The genesis MUST contain a `next_anchor_commitment` — the hash of the *next* anchor public key, which the entity has generated and holds but has not yet revealed. This is **pre-rotation** (§7.5.2).
- For delegates, the genesis MUST be co-signed by the entity immediately above in `delegation_chain`; the co-signature is carried in the genesis's registration as a SCITT Signed Statement, not in the genesis body (which would make the hash depend on the parent's signature and complicate derivation). The chain MUST terminate at a `principal`.
- The genesis is registered as a Signed Statement in a TS appropriate to the entity's initial scope, and published to the custody substrate (§7.6).

### 7.5 The Rotation Log — Append-Only Key Event Log

The rotation log grows beside the frozen genesis. Every entry is a Signed Statement, sequenced and hash-linked.

#### 7.5.1 Entry Structure

```
credentialSubject: {
  artifact_kind:   "RotationEntry",
  did:             "<the DID>",
  genesis_ref:     "<CID of genesis>",             // anchor binding, §4.6.3
  seq:             <n>,                              // 0-based, contiguous
  prev_entry:      "<CID of entry seq-1 | null>",
  op:              "rotate_anchor | add_method | retire_method | add_service | retire_service",
  ... op-specific fields ...
  ts:              "<iso8601>"
}
proof: DataIntegrityProof under slhdsa128-jcs-2024, by the current anchor
```

Operations:

| `op` | Fields | Effect |
|---|---|---|
| `rotate_anchor` | `new_anchor` (Multikey), `next_anchor_commitment` | Reveals the pre-committed next anchor; commits the one after; retires the current anchor |
| `add_method` | `method` (Multikey + `role`) | Adds a signing or authentication method |
| `retire_method` | `method_id`, `reason` | Retires a method; signatures made before `ts` remain valid |
| `add_service` | `service` (DID `service` entry) | Adds a resolution path or provider |
| `retire_service` | `service_id` | Retires one |

#### 7.5.2 Pre-Rotation **[new in this version — adopted from KERI]**

Every anchor, from genesis onward, commits to the hash of its successor before that successor is revealed. A `rotate_anchor` entry is valid only if `BLAKE3-256(new_anchor.publicKeyMultibase)` equals the `next_anchor_commitment` in the most recent prior entry (or the genesis).

**What this closes.** In v0.4.1, an adversary who obtained the current anchor's private key could rotate to any key of their choosing and own the identity. Under pre-rotation, the same adversary can rotate only to the key the legitimate holder pre-committed — which the adversary does not hold. Theft of the current anchor therefore permits at most one rotation to a key the thief cannot use. The legitimate holder, who holds the pre-committed successor, can then rotate again and recover. This does not solve *loss* (§7.14) but it substantially narrows *theft*.

**Cost.** The entity must generate and safeguard one key ahead. Implementations SHOULD hold the pre-committed key in separate custody from the active anchor.

#### 7.5.3 Folding to a DID Document

The DID document at time *T* is computed by: starting from the genesis; applying each rotation-log entry in `seq` order whose `ts ≤ T`; verifying each entry's proof under the anchor that was current when it was made; verifying each `rotate_anchor` against the prior commitment; and verifying each entry's `genesis_ref` resolves to the genesis whose anchor the entry's proof verifies under (§4.6.3). A walker that cannot verify any step MUST treat the identity's document as unresolvable from that point, and MUST NOT fall back to a later entry.

The result is a W3C DID document: `id`, `verificationMethod[]`, `assertionMethod[]`, `authentication[]`, `service[]`. Walkers MAY cache it as an index (§4.15).

### 7.6 Custody Substrate — Permanent and Content-Addressed

The genesis document and rotation log MUST be stored on a **permanent, content-addressed substrate**. Arweave is the current choice; IPFS with Filecoin persistence, or equivalents, are compatible. The specification is substrate-agnostic (§1.3).

Required properties:
- **Permanence.** The documents persist without depending on any single host's uptime or continued willingness to serve.
- **Content-addressing.** Retrieval and integrity are by content. A tampered copy is detectable by hash; a censored copy is servable from elsewhere.
- **Multi-locality.** The documents MAY be — and SHOULD be — held in more than one place: the custody substrate, the operator's `did:web` endpoint, partner endpoints, the entity's own device. The DID document's `service` entries enumerate the paths.

Because the genesis is self-certifying (§7.3 P1), **custody never equals control**. A copy served by the DAX Foundation, by a partner, by the permanent substrate, or emailed by the entity itself is equally trustworthy — the verifier hashes it and checks the DID regardless of source. A custodian can serve the document; a custodian cannot forge it.

**Honest note on Arweave.** Permanence is underwritten by an endowment model whose cost tracks the AR token price, which is volatile. The protocol's designers do not guarantee permanence "in true perpetuity." CP accepts this as the best available permanent-storage guarantee as of 2026-09-11 and requires multi-locality precisely so that no single substrate's failure is fatal.

### 7.7 Publishing — Operator Pays, Operator Does Not Control

The convenient default: an ecosystem operator — the DAX Foundation, for entities it onboards — generates the entity's genesis document, writes genesis and initial rotation-log entries to the custody substrate, absorbs the cost, and returns the DID and a copy of the genesis to the entity. The entity has paid nothing and managed no cryptography.

This default is permitted and expected. It is bounded by §1.11: it MUST NOT be the only path.

### 7.8 The Independent Path — Always Open

For every entity, an independent publishing path MUST exist and MUST be documented: the entity's own client can write its genesis and rotation-log entries to the custody substrate **without the operator's permission**. The entity holds its own genesis, its own anchor, and its own pre-committed next anchor. It can always re-publish.

The chokepoint test (§1.11): if the operator refused to publish or resolve a given entity, could that entity still do so itself? If yes, the operator is a convenience. If no, the operator is a custodian, and the architecture has failed.

**Operational reality.** Independent publishing to a permanent substrate costs money — Arweave charges a one-time fee per write and requires the publisher to hold a token balance. Most non-technical entities will use the operator's path. The guarantee requires only that the independent path *exists and is documented*, not that it is commonly used. Implementations MUST provide tooling for it and MUST document it at the same prominence as the operator path.

### 7.9 Friendly-Name Registry — Convenience Layer, Not Root

An operator MAY run a friendly-name registry mapping human-readable names to DIDs. A friendly name is a `service` entry in the DID document — one more resolution path. It is never the root.

**Rules:**
- The friendly name MUST NOT be used for cross-references within the substrate (§4.5.3).
- The registry MUST NOT be a required step in resolution. An entity with no friendly name is fully functional.
- The registry SHOULD prove name control cryptographically rather than grant names administratively. The AGNTCY Agent Directory's name verification — the entity publishes a JWKS at `https://<domain>/.well-known/jwks.json` containing a key that also appears in its DID document, and the registry verifies the correspondence — is the reference pattern. Under it the registry does not *assign* a name; it *confirms* that the DID's holder controls the domain the name claims.

If a registry loses, reassigns, or refuses a friendly name, the entity's identity is untouched. The root was never the name.

### 7.10 Cryptosuites and Quantum Grading

The identity layer's cryptographic commitments, consolidated:

| Purpose | Cryptosuite | Algorithm | Multicodec | Notes |
|---|---|---|---|---|
| Anchor (rotation log, genesis co-sign) | `slhdsa128-jcs-2024` | SLH-DSA-SHA2-128s, FIPS 205, Category 1 | `0x1220` | Hash-based; rests only on SHA-2 security; 7,856-byte signatures; rare-use |
| Workhorse (all other artifacts) | `mldsa44-jcs-2024` | ML-DSA-44, FIPS 204, Category 2 | `0x1210` | Lattice-based; 2,420-byte signatures; routine |
| Transitional (until 2030-01-01) | `eddsa-jcs-2022` | Ed25519 | `0xed` | Hybrid only, never alone |

All three are W3C Data Integrity cryptosuites over JCS canonicalization (§4.4). The PQ suites are from *Quantum-Resistant Cryptosuites v1.0* (W3C CCG, experimental; §4.6.1).

**Why two post-quantum families.** SLH-DSA rests on hash-function security alone. ML-DSA rests on module-lattice problems. A break in either family leaves the other standing. The anchor uses the more conservative assumption because it signs the operations that redefine the identity; the workhorse uses the more efficient one because it signs everything else.

**Why the fingerprint needs no migration.** The DID is a 256-bit hash. Grover's algorithm reduces effective hash security to ~128 bits, which remains beyond practical attack. Shor's algorithm, which breaks RSA and elliptic curves outright, does not apply to hashes. The identifier is quantum-resistant today; only the signing keys needed post-quantum replacements, and they have them.

**Anchor binding (§4.6.3).** Because SLH-DSA's Exclusive Ownership property is listed as unknown in the W3C analysis, every anchor-signed statement binds the anchor public key through `genesis_ref`. This is restated here because it is an identity-layer requirement as much as a verification-policy one.

### 7.11 Resolution and Verification Flow

When a relying party must establish that a claimant is the entity a DID names:

1. **Resolve.** Fetch the genesis document and rotation log from any `service` endpoint the relying party trusts, or directly from the custody substrate. The DID does not encode location; the endpoints do.
2. **Integrity-check.** Compute `BLAKE3-256(JCS(genesis))`. Confirm it equals the DID's method-specific identifier. If it does, the document is authentic regardless of who served it. If it does not, stop.
3. **Fold.** Compute the DID document at the relevant time per §7.5.3, verifying every rotation-log entry, every pre-rotation commitment, and every `genesis_ref`.
4. **Verify the assertion.** Confirm the claimant's signature verifies under a method listed in `assertionMethod` as of signing time (§4.5.4). For federated providers listed under `authentication` — an OIDC identity provider, a passkey relying party — the provider performs the authentication and vouches; the relying party trusts the provider's assertion as it would any credential from that issuer.

Step 2 is what the DID is for. Step 4 is what the keys are for. They are never merged: a valid DID with a failed signature is an impostor presenting a real name; a valid signature under an unresolvable DID is a key with no identity behind it.

### 7.12 Composite Entities and Threshold Policy

An entity of `kind: composite` — an institution, a collective, a multi-party controller — distributes control across multiple keys. Its DID document declares a **threshold policy**:

```
"cp:thresholdPolicy": {
  "purpose":   "anchor | assertionMethod",
  "threshold": <m>,
  "methods":   [ "#key-1", "#key-2", "#key-3", ... ]   // n entries
}
```

A signature for that purpose is valid only if *m* of the *n* listed methods have signed. For the anchor purpose, a composite's rotation-log entries carry *m* proofs, each under `slhdsa128-jcs-2024`, and the pre-rotation commitment is over the set of next anchors.

Composite anchors are the mechanism by which an institution avoids a single point of capture. KERI's multi-signature group identifiers are the design precedent.

### 7.13 Delegation — KYA-OS Profile **[D-022]**

A delegate is an entity of `chain_role: delegate` acting on behalf of a principal. CP's delegation model is a profile of **KYA-OS** (Know Your Agent Operating System), the specification under the Decentralized Identity Foundation's Trusted AI Agents Working Group — formerly MCP-I, donated to DIF in March 2026. As of 2026-09-11 KYA-OS is a working-group specification, not a final standard; CP profiles the version current at publication and dates the profile in Appendix F.

KYA-OS answers four questions about an agent. CP maps them:

| KYA-OS question | CP answer | Where |
|---|---|---|
| Who is the agent? | Its DID | §7.3–7.5 |
| Who authorized it? | The entity above it in `delegation_chain`, whose co-signature registers the delegate's genesis; and the issuer of its RoleGrant | §7.4, §5.3 |
| What may it do? | The `roles` in its RoleGrant(s), as interpreted by the governing extension | §5.3 |
| Within what scope? | The `scope` of its RoleGrant(s), bounded by the `scope` of any BLOCKING Constraint | §5.3, §5.8 |

**The one divergence, stated for the DIF working group's benefit.** KYA-OS frames the authorizer as a human. CP frames the authorizer as a *principal of any kind* (§1.12). Every other mechanism is shared. Where KYA-OS text reads "the human who authorized this agent," CP reads "the principal who authorized this delegate," and a principal may be biological, nonbiological, institutional, or composite. CP records this delta so that it is visible as a proposed generalization rather than an incompatibility.

**Accountability walk.** From any SubAgentArtifact (§5.7) or any event issued by a delegate, a walker follows `delegation_chain` to the principal. Every link is a co-signed genesis. Every hop is a RoleGrant that can be checked for scope and revocation status. The walk terminates, by §1.12, at an entity that acts under no one's delegation.

### 7.14 Root Key Recovery — Open

The entity's control over its identity rests on the anchor key and the pre-committed successor. Two failures remain:

- **Loss** of both the current anchor and the pre-committed successor. The identity is frozen: no rotation, no method changes. Pre-rotation does not help here.
- **Theft** of both. The thief can rotate to a key they control. Pre-rotation raises the bar from one key to two, held in separate custody; it does not eliminate the case.

Candidate mechanisms — social recovery (M-of-N trustees may authorize a new anchor chain), operator-assisted recovery (opt-in, and bounded by §1.11 so the operator never becomes a required custodian), hardware-anchored keys — remain in open research (§26.6). This version adopts pre-rotation as a strict improvement and leaves the rest open.

### 7.15 Layer Summary

| Layer | What it is | Mutability | Who controls |
|---|---|---|---|
| DID | `did:cp:<hash of frozen genesis>` | Permanent | No one — self-certifying |
| Genesis document | Frozen inception: anchor, next-anchor commitment, kind, chain role, principal | Written once | The entity, at creation |
| Rotation log | Append-only key event log with pre-rotation | Grows | The entity, via anchor |
| Verification methods | Anchor (SLH-DSA), workhorse (ML-DSA-44), transitional (Ed25519), federated providers | Via log | The entity |
| Services | Resolution paths, friendly names, provider endpoints | Via log | The entity |
| Custody | Permanent content-addressed substrate + any mirrors | Permanent | No one — multi-local |
| Publishing | Writing genesis and log to custody | — | Operator (default) or entity (always open) |
| Friendly name | Human-readable alias, cryptographically verified | Mutable | Registry (convenience only) |

The fingerprint is the frozen root. Everything else evolves around it. No layer gives any operator the power to be a required custodian.

---

## 8. EVENT

### 8.1 What an Event Is

An event is the atomic unit of interaction: one participant's expression, at one moment, in one context. It is a Verifiable Credential (§4.3) issued by the participant, registered as a SCITT Signed Statement, and receipted by the witness (§4.10). An event that has not been receipted is not part of the record.

Events are never modified. Everything CP later says about an event — that it was witnessed, that it adhered or did not, that it was contested, that it was withdrawn — is said by attaching referrers to it (§4.2).

### 8.2 Schema

```
credentialSubject: {
  artifact_kind:   "Event",
  context_id:      "<ULID>",
  seq:             <n>,                        // 0-based, contiguous within context
  previous_hash:   "<CID of event seq-1> | null",
  scope:           "<scope>",                  // MUST equal the context's declared scope
  kind:            "<§6.4 top-level kind>",
  subkind:         "<namespaced sub-kind> | null",
  actor: {
    did:           "<DID of the participant>",   // MUST equal issuer
    confidence:    <0..1>                        // attribution confidence; 1.0 for direct authorship
  },
  payload:         { ... } | absent,
  payload_ref:     "<CID of detached payload> | absent",   // exactly one of payload / payload_ref
  positions:       [ ... ] | absent,           // §8.3; present only on position-bearing events
  refs:            [ "<CID>" ],                // artifacts this event cites
  transport_ref:   { protocol: "<string>", message_ref: "<string>" } | absent,   // §2.7
  context_init:    { ... } | absent,           // §9.3; present only when seq = 0 and no ContextOpen
  ts:              "<iso8601>",
  spec_version:    "0.5"
}
```

**Rules:**
- `issuer` (the VC field) MUST equal `actor.did`. An event is authored by the entity that signs it. There is no proxy authorship.
- `actor.confidence` exists for transcribed or diarized input where attribution is probabilistic. For direct digital authorship it is `1.0`. It is never used to attribute an expression to an entity that did not sign the event — it qualifies how confidently a *signed* expression maps to a source utterance.
- `previous_hash` is `null` only when `seq` is `0`. The chain is contiguous. A gap is a defect (§4.14 rule 6).
- `scope` MUST be present on every event, not only the first, so that the Transparency Service can enforce §4.1.5 on the statement alone.
- `payload` carries the expression. Large payloads use `payload_ref` (§4.1.3). Payload structure is defined per `kind` by CP for the baseline kinds and by extensions for theirs.
- `transport_ref` identifies the carrying protocol and message when the event witnesses traffic on another protocol — an A2A task, an L9 message, an MCP call. It is a citation, not a copy; CP does not re-encode the foreign message.

### 8.3 Position-Bearing Events

An event is position-bearing when the participant is asserting, revising, or withdrawing a position on one or more concepts. Kinds `INTENT`, `EFFECT`, `CHALLENGE`, and `ADJUDICATE` are position-bearing by default; `OBSERVE` is position-bearing when the actor asserts a position on what was observed. Extensions declare which of their kinds are position-bearing.

Position-bearing events carry the `positions` block, one entry per concept:

```
positions: [ {
  concept_id:      "<URI, §5.1>",
  prior:           <0..1> | null,      // from the participant's prior_ref (§9.3), or null
  posterior:       <0..1>,             // the participant's current position
  stance:          "asserted | deferred | revised | retracted | challenged | unresolved",   // §5.9
  revision_cause:  "<§5.10>" | absent, // REQUIRED when stance is revised or deferred
  deferred_to:     "<DID>" | null,     // REQUIRED when stance is deferred; null otherwise
  addresses:       [ "<CID>" ] | absent   // events or artifacts this position engages (§12.5)
} ]
```

These fields are participant-signed and witness-receipted with the rest of the event. They cannot be altered after registration. This is what makes the deferral graph (§5.10) trustworthy in CP where it is not in systems that hold the same fields locally and unsigned.

**The posterior is not a verdict.** A participant's `posterior` is what the participant holds. A validator's `verdict` (§11.1) is a judgment of adherence to a constraint. They are carried in different artifacts, issued by different roles, and are never compared as commensurable quantities (§5.11).

### 8.4 Two Signatures, Two Roles

Every registered event carries:

1. **The participant's Data Integrity proof** — under a cryptosuite from §20, by a verification method valid for the participant at `ts` (§4.5.4). This is authorship.
2. **The witness's Receipt** — the Transparency Service's signed inclusion proof (§4.1.2), attached as the event's `cp.witness.v1` referrer (§10.3). This is observation.

Neither alone is a record. A participant statement without a receipt is unwitnessed; a receipt over unsigned content is not permitted (§4.10).

### 8.5 Identity and Chain

The event's `id` is its CID over the JCS-canonical credential without `proof` (§4.4). The `previous_hash` of event *n* is the `id` of event *n−1* in the same `context_id`. Walkers verify the chain (§4.14 rule 6) and the receipts (rule 2) independently: the chain proves sequence; the receipts prove witnessing.

### 8.6 Events and Compiled Artifacts

An event is an artifact of kind `Event`. It is the *interaction* artifact. Compiled artifacts — Concepts, SubAgentArtifacts, Constraints, and every other kind in Appendix A — are produced *from* events by deterministic compilation (§1.1, §18) and carry `cp:createdFromEvent` relationships back to the events that produced them (§6.5). The event log is the source; compiled artifacts are derived. Where they disagree, the event log is correct.

---

## 9. EPISODE AND CONTEXT

### 9.1 Terminology **[D-047]**

A **Context** is a bounded interaction with a declared scope, declared constraints, declared participants, and a declared witness. It is the unit of witnessing and the unit within which events chain.

Contexts have kinds. **Episode** is a bounded, time-limited interaction — what v0.4 called a Session. **Thread** is a bounded interaction that may span long durations with gaps. **Workspace** is a persistent context with membership. Extensions MAY define others.

"Episode" is adopted as the preferred term for a bounded Context to align with the Internet of Cognition's L9 `Episode` object (D-047, Appendix C). "Session" is accepted as a legacy alias in the CP JSON-LD context for artifacts signed under v0.4 (§1.8).

### 9.2 The Minimal Context **[D-030]**

A context MUST have: a `context_id`; a first event (`seq: 0`, `previous_hash: null`) from which scope, witness, constraints, and participants are determinable; and a contiguous per-context chain. Nothing else is required.

v0.4 required SessionOpen, one or more SessionMessages, and SessionClose. The first operational run of CP (§27) ran without the envelope, using `context_id` and per-context chaining alone, and lost no integrity property — the chain carries integrity, not the envelope. This version makes the envelope optional and defines the minimal form as sufficient.

### 9.3 What Must Be Determinable at Context Start

The following MUST be determinable from the context's first registered statement — either a ContextOpen artifact (§9.4) or a first event carrying a `context_init` block:

| Field | Requirement | Governs |
|---|---|---|
| `scope` | REQUIRED | §4.12 non-narrowing; §4.1.5 TS selection |
| `witness` | REQUIRED — the TS identity, `relationship`, optional `independence_assertion` (§10.4) | §4.7 |
| `additional_witnesses` | REQUIRED when the context spans organizations (§9.6) | §4.1.7 |
| `constraints` | REQUIRED, may be empty — array of `{constraint_decl_ref, policy_ref, validator_did}` | §9.5, §11 |
| `participants` | REQUIRED — DIDs of the parties | §4.7 |
| `prior_refs` | OPTIONAL — map of participant DID → CID of a witnessed prior statement (§5.11) | influence measurement |
| `domain`, `objective` | OPTIONAL — extension-interpreted strings | discovery, rendering |
| `context_refs` | OPTIONAL — CIDs of related contexts | traversal |

Because these are fixed at start and inherited by every event, a walker MUST reject any later event in the context whose `scope` differs from the declared scope (§4.12).

### 9.4 ContextOpen and ContextClose — Recommended Form

Where a context's parameters warrant explicit declaration — cross-organization interactions, multiple constraints, declared priors — the envelope form is RECOMMENDED. It is never required.

**ContextOpen**
```
credentialSubject: {
  artifact_kind:          "ContextOpen",
  context_id:             "<ULID>",
  context_kind:           "Episode | Thread | Workspace | <ext>",
  scope:                  "<scope>",
  participants:           [ { did: "<DID>", role: "<ext string> | null" } ],
  witness: {
    did:                    "<TS identity DID>",
    relationship:           "external | participant",
    independence_assertion: "<CID of signed assertion> | null"
  },
  additional_witnesses:   [ { did: "<TS identity DID>", relationship: "external" } ],
  constraints: [ {
    constraint_decl_ref:    "<CID of ConstraintDecl>",
    policy_ref:             "<CID of Policy>",
    validator_did:          "<DID>"
  } ],
  prior_refs:             { "<participant DID>": "<CID>" },
  domain:                 "<string> | null",
  objective:              "<string> | null",
  context_refs:           [ "<CID>" ],
  ts:                     "<iso8601>"
}
```
ContextOpen is signed by the opening participant. It is registered as the context's first statement and the first event then carries `previous_hash` = ContextOpen's CID.

**ContextClose**
```
credentialSubject: {
  artifact_kind:       "ContextClose",
  context_id:          "<ULID>",
  final_event_ref:     "<CID of the last event>",
  produced_artifacts:  [ "<CID>" ],
  outcome:             "converged | unresolved | abandoned | <ext>",
  ts:                  "<iso8601>"
}
```
ContextClose is signed by a participant (every participant SHOULD co-sign; one signature suffices). Its `outcome` field records how the context ended. `unresolved` is a valid outcome and is the context-level expression of the `unresolved` stance (§5.9): the parties engaged and did not converge, and say so.

`SessionOpen` and `SessionClose` are legacy aliases for these types.

### 9.5 Multiple Constraints per Context

The `constraints` array declares every ConstraintDecl the context claims adherence to, each with its policy and validator. A context between two entities operating under different constraints declares both. Each declared constraint's validator issues its own AdherenceClaims against the context's attestations. Artifacts produced in the context compound into each constraint's lineage independently.

This is how entities under different frames interact without either frame subsuming the other: both are declared, both are evaluated, both compound.

### 9.6 Cross-Organization Contexts **[D-005]**

When a context spans organizations, each organization's Transparency Service witnesses it. `witness` names the opener's TS; `additional_witnesses` names the others. Every event is registered in every listed TS and receives a Receipt from each.

The result is *n* independent factual records of the same participant-signed content. Agreement among them is stronger evidence than any one. Disagreement — a TS that fails to receipt an event the others receipted, or receipts a different CID at the same `seq` — is a queryable signal. The substrate does not resolve it; it records it. Walkers MUST surface receipt disagreement when present.

### 9.7 Scope and Transparency Service Selection

The context's `scope` determines which TS instances may register its statements (§4.1.5). An org-scope context registers with org-scope TS instances; a public-scope context with public ones. A statement presented to a TS whose scope is narrower than the statement's declared scope is refused. Widening after the fact is a new witnessed act (§4.1.5), never a reinterpretation.

### 9.8 Open Contexts and Episodicity

A context with no ContextClose is open. Walkers MUST NOT infer closure from inactivity. A Thread may be silent for a year and remain open; that silence is valid (§1.10).

A context that closes with `outcome: unresolved` has succeeded at recording what happened. A context that closes with `outcome: abandoned` — a participant exited without resolution — has also succeeded. Exit is a success state. The protocol has no notion of an interaction that "should have" continued.

---

## 10. WITNESS AND VALIDATOR

### 10.1 The Roles

| Role | What it does | What it signs | Identity constraint |
|---|---|---|---|
| **Participant** | Expresses. Produces events. | Its own events (Data Integrity proof) | — |
| **Witness** | Observes. Records that participant-signed statements were registered, in order. | Receipts | Distinct from every participant (§4.7) |
| **Validator** | Judges. Claims adherence to a declared constraint, probabilistically, against a dated floor. | AdherenceClaims | Distinct from the witness (§4.8); only validator DIDs issue claims (§4.9) |
| **Contestant** | Disputes. Attaches a Contestation to any artifact. | Contestations | Any DID (§12) |
| **Adjudicator** | Resolves a Contestation. | Adjudications | Extension-defined eligibility (§12) |

Contestant and adjudicator are specified in §12. This section covers witness and validator.

### 10.2 The Witness

The witness is strictly factual. Its entire claim is:

> *I registered this participant-signed statement at this position in my log, at this time. I assert nothing about its content.*

The witness is the SCITT Transparency Service (§4.1.1). Its Receipt is its attestation. It applies registration policy (§4.1.6) — structural checks only — and MUST NOT decline registration on any content-based ground.

The witness never evaluates, interprets, scores, or judges. A witness that did would have injected a judgment into the record that no later validator could cleanly re-evaluate. This is the boundary on which the time-indexed model (§11) depends, and it is why the witness makes no adherence claim.

### 10.3 WitnessAttestation and the `claim_type` Family **[D-025]**

Mechanically, a WitnessAttestation is the SCITT Receipt carried in CP's VC envelope, attached to its target as a `cp.witness.v1` referrer. One object, two names.

There is one WitnessAttestation kind. What varies is *what was observed*, recorded in a mandatory `claim_type` discriminator. CP defines a conservative top-level family; sub-types are namespaced beneath it per the §6.4 pattern; extensions add their own.

```
credentialSubject: {
  artifact_kind:           "WitnessAttestation",
  target_ref:              "<CID of the participant-signed statement>",
  claim_type:              "<family>.<subtype>",
  witness_did:             "<TS identity DID>",
  relationship:            "external | participant",
  independence_assertion:  "<CID> | null",
  receipt: {
    log_id:                  "<TS log identifier>",
    log_index:               <n>,
    tree_head_ref:           "<CID or URI of the signed tree head>",
    inclusion_proof:         "<COSE Merkle tree proof, base64url>"
  },
  ts:                      "<iso8601>"
}
```

**Top-level family and baseline sub-types:**

| Family | Sub-type | Observed |
|---|---|---|
| `event` | `event.registered` | an ordinary interaction event — the default |
| `delegation` | `delegation.received` | a delegate received a brief from its principal or parent |
| | `delegation.sent` | a principal or parent dispatched a brief |
| | `delegation.refused` | a spawn or RoleGrant was refused because a BLOCKING Constraint's `blocks_roles` matched (§5.8, §5.3) |
| `artifact` | `artifact.produced` | a compiled artifact was registered |
| | `artifact.shared` | an artifact was transmitted to another entity |
| | `artifact.sub-agent` | a SubAgentArtifact was registered (§5.7) |
| `constraint-lifecycle` | `.raised`, `.blocking`, `.resolved`, `.reopened` | a Constraint state transition (§5.8), with `from_state`, `to_state`, `evidence_ref`, and for `.reopened` a `compliance_failure` block |
| `peer-validation` | `peer-validation.received` | an inline AdherenceClaim was received from a counterparty's validator (§10.9) |

The first operational run (§27) produced attestations of every family above except `event.registered` (it used per-type attestations throughout) and without a formal discriminator. This version formalizes what was observed.

**Why one kind, not eight.** The witness does one thing. What it observes varies. A single kind with a typed discriminator gives walkers one verification path (§4.14 rules 1–2) and gives every observed thing the same evidentiary standing. Eight kinds would fragment the witness role and invite the question of which kinds are "really" witnessed.

### 10.4 Independence Assertion

A witness MAY publish a signed **independence assertion**: a statement, in its own words, of its relationship to the participants — that it holds no commercial, organizational, or operational interest in the interaction; that it is operated by an entity not in any participant's delegation chain; whatever it can truthfully attest. The assertion is an artifact (`IndependenceAssertion`), registered and content-addressed, and referenced by CID from WitnessAttestations.

Its evidentiary weight is ordered:

| `relationship` | `independence_assertion` | Standing |
|---|---|---|
| `external` | present | strongest |
| `external` | null | strong — structural independence, no declaration |
| `participant` | present | weak — declared, but self-mediated |
| `participant` | null | weakest — transitional pattern (§4.7) |

The assertion never substitutes for the structural check in §4.7. It is a declaration a later evaluator may weigh, not a proof.

### 10.5 The Validator

The validator is evaluative. Its claim is:

> *Given this declared constraint and policy, and given the compounding floor as it stood at this snapshot, the probability that this witnessed interaction adhered is X. Here is how I computed it.*

The validator MAY run at any time after the interaction — moments or years. It MAY be a different entity from any that was present. Multiple validators MAY judge the same attestation. Each run produces a new AdherenceClaim (§11); no claim replaces another. The full history of how an interaction has been judged is part of the record.

The validator reads the witnessed record. It does not alter it. It does not need the participants' cooperation or the witness's permission.

### 10.6 Validator Identity

A validator is an entity whose DID is a **validator identity**: its genesis document declares `role: validator`, or it is named as `validator_did` in a context's declared constraints (§9.3). Only a validator identity may issue an AdherenceClaim (§4.9).

A validator MUST be a distinct DID from the witness whose receipt it judges (§4.8). One operator MAY run both roles under distinct DIDs.

### 10.7 The Validator Artifact

A validator declares itself with a `Validator` artifact:

```
credentialSubject: {
  artifact_kind:             "Validator",
  validator_did:             "<DID>",
  implements_constraint_decl: "<CID of ConstraintDecl>",
  implements_policy:         "<CID of Policy>",
  executable_spec: {
    language:  "cedar | rego | <other>",
    ref:       "<CID of the executable or its precise specification>"
  },
  input_schema:              "<CID or inline JSON Schema>",
  output_schema:             "<CID or inline JSON Schema>",
  version:                   "<semver>",
  fork_of:                   "<CID> | null",
  ts:                        "<iso8601>"
}
```

**`executable_spec` [D-020].** The executable MUST be content-addressed so that anyone can re-run the validator against the same inputs and reproduce its claim (§1.1). It SHOULD be expressed in a standard policy language — Cedar preferred for its formal semantics, OPA/Rego accepted. Free-form executables are permitted where the validator's logic does not fit a policy language (probabilistic and learned validators); they MUST still be content-addressed, and their `language` field names the runtime.

A human-readable summary MAY accompany the executable. It is not a substitute for it.

### 10.8 Evaluation Trace — Minimum Content

Every AdherenceClaim MUST carry an `evaluation_trace` sufficient for an independent implementation of the same validator to reproduce the claim. Minimum content:

- `validator_ref` — CID of the Validator artifact (§10.7), pinning version and executable
- `policy_ref`, `constraint_decl_ref` — CIDs
- `floor_state_ref` — CID of the Snapshot (§17) the floor was read at
- `inputs` — ordered list of CIDs read, including the target WitnessAttestation, referenced events, and any SubAgentArtifacts consumed as evidence (§4.9)
- `external_state` — hash of any state read outside the substrate, or null
- `parameters` — any parameter substitutions
- `sub_verdicts` — intermediate rule-level results, each with the rule identifier and its output
- `aggregation` — the method by which sub-verdicts became the final verdict (e.g. `geometric_mean`, `weighted_min`, a named function in the executable)
- `verdict` — the output

A claim without this trace is not reproducible and MUST NOT be treated as an AdherenceClaim by walkers. "Anyone can re-run the validator" is a structural claim only if the inputs are enumerated.

### 10.9 Inline Validation **[D-032]**

Inline validation is a permitted mode in which the receiver of a transmitted artifact runs its validator on receipt and returns the result synchronously.

**Flow:**
1. Entity A transmits an artifact to Entity B; A's TS registers `artifact.shared`.
2. B's validator (a validator identity, §10.6) evaluates the artifact against B's declared constraint and issues an **AdherenceClaim** with `mode: inline` (§11.1) and its own `floor_state_ref`. B's TS registers it.
3. B returns `receiver_ack` to A containing the AdherenceClaim's CID and `validator_score`.
4. A's TS registers a WitnessAttestation `peer-validation.received` whose `target_ref` is the AdherenceClaim's CID.

**Rules:**
- The inline claim is a full AdherenceClaim (§11.1). It is signed by B's validator DID (§4.9), carries a complete evaluation trace (§10.8), and is registered in B's TS.
- The inline claim has **no more authority than any other claim**. Later claims — by B's validator against a richer floor, by A's validator, by a third party — stack beside it (§11.3). It is the first of many, marked as such.
- `receiver_ack.validator_score` is a convenience copy. The claim of record is the registered AdherenceClaim; walkers MUST resolve the CID rather than trust the ack.

This is how cross-organization validation worked in the first operational run (§27). Its risk was that an inline claim might be treated as final. The `mode` marker and §11.3 accumulation remove that risk without removing the mode.

### 10.10 What Each Role Must Not Do

| Role | MUST NOT |
|---|---|
| Witness | evaluate content · decline registration on content grounds · alter a statement · receipt unsigned content · be a participant (except declared transitional) |
| Validator | alter the witnessed record · issue a claim without a reproducible trace · be the witness whose receipt it judges · delegate its signature to a sub-agent (§4.9) |
| Participant | issue an AdherenceClaim (unless also a declared validator identity for a *different* context) · alter a registered event · sign as another entity |

---

## 11. ADHERENCECLAIM AND THE COMPOUNDING FLOOR

### 11.1 Schema

An AdherenceClaim is a validator's judgment of a witnessed interaction against a declared constraint, at a stated moment in the floor's history. It is a `cp.adherence.v1` referrer on the WitnessAttestation it judges.

```
credentialSubject: {
  artifact_kind:          "AdherenceClaim",
  target_ref:             "<CID of WitnessAttestation>",
  constraint_decl_ref:    "<CID of ConstraintDecl>",
  policy_ref:             "<CID of Policy>",
  interpretation_ref:     "<CID> | null",
  validator_ref:          "<CID of Validator artifact, §10.7>",
  floor_state_ref:        "<CID of Snapshot, §17> | null",
  mode:                   "async | inline",                 // §10.9
  verdict: {
    shape:                  "probability | composite | boolean",
    value:                  <0..1> | { axis: value, ... } | true | false
  },
  evaluation_trace:       { ... },                           // §10.8, REQUIRED
  deliberation_quality:   { ... } | absent,                  // §11.6
  violations: [ {
    rule_id:                "<string>",
    description:            "<string>",
    evidence_ref:           "<CID> | null"
  } ],
  ts:                     "<iso8601>"
}
issuer: the validator DID (§4.9)
```

**Rules:**
- `issuer` MUST be a validator identity (§10.6). Any artifact of this kind from a non-validator issuer is not an AdherenceClaim and walkers MUST NOT treat it as one.
- `evaluation_trace` MUST meet §10.8. A claim without a reproducible trace is not an AdherenceClaim.
- `floor_state_ref` SHOULD be present. It MAY be `null` only where no Snapshot yet exists for the lineage, in which case the trace MUST record `floor_state: "none"`. A claim without a floor reference cannot be located in the floor's history and is weaker evidence for that reason.
- `verdict.shape: probability` is canonical (D-004.a). `boolean` is the degenerate case `value ∈ {0, 1}` and is accepted for structural validators whose output is inherently binary. `composite` carries a map of axis → value for multi-dimensional evaluation; the trace's `aggregation` says how axes combine.

### 11.2 The Verdict Is Probabilistic, and Is Not a Posterior

The verdict is the validator's assessed probability that the interaction adhered to the declared constraint, *given the floor as the validator saw it*. It carries "as understood at this moment" as a parameter. When the floor changes, the probability may change, and a later claim records the change.

The verdict is not the participant's `posterior` (§8.3, §5.11). The posterior is what a participant holds. The verdict is what a validator judges. Different issuers, different artifacts, different meanings. They are never averaged, compared, or substituted for each other.

### 11.3 Accumulation

Multiple AdherenceClaims MAY attach to one WitnessAttestation. Different validators may issue different claims. One validator may issue a new claim later against a richer floor. **No claim replaces another.** Every claim ever issued remains attached, retrievable, and enumerable (§4.14 rule 5).

"The latest claim," "the highest-confidence claim," "the claim from the validator I trust" are *views* a walker may render. They are not the truth of the record. The truth of the record is the full set, in time order, each pinned to the floor state it was made against.

A walker in default rendering mode MAY show one claim prominently. It MUST indicate that others exist and MUST make them reachable.

### 11.4 Time-Indexing

`floor_state_ref` pins a claim to a Snapshot (§17): a verifiable statement of which artifacts constituted the lineage's floor at a moment. A claim made in 2026 against a 2026 Snapshot and a claim made in 2030 against a 2030 Snapshot are both correct statements of what a validator concluded given what was then known. Neither is superseded by the other. Both are the record.

This is the mechanism that implements §0.3. A pattern invisible in any single interaction — coordinated deference across a bloc, a laundered narrative — becomes visible when enough interactions have accumulated in the floor for a validator to detect it. When that happens, the validator issues new claims against the old attestations, and the record now holds both the original benign judgment and the later one. Nothing was rewritten. Understanding was added.

### 11.5 The Compounding Floor

A **lineage** is the triple (ConstraintDecl, Policy, Validator lineage) — a declared frame, an operational interpretation of it, and the fork-chain of validators that have evaluated against it.

A lineage's **compounding floor** at time *T* is the set of artifacts that, as of *T*, carry at least one affirmative AdherenceClaim under that lineage above the lineage's **admission threshold**. The threshold — what probability counts as "affirmative" — is declared by the Policy and is extension-defined; CP does not fix it.

The floor grows monotonically: an artifact once admitted is never removed from the floor's history, though a later claim may lower its standing in later Snapshots. Tombstoned artifacts remain in the floor's history and are visible to pattern-matchers (§4.13); they are excluded from default renderings.

**Cross-lineage import [§1.5].** An artifact validated under lineage B enters lineage A's floor when — and only when — A's validator issues an affirmative AdherenceClaim against it under A's constraint. The artifact is unchanged; it simply acquires a second claim under a second frame. A walker sees membership in both floors by enumerating claims. No import predicate is needed; the two claims are the record of the import.

Import is never automatic. Nothing flows into a floor without that floor's validator affirming it. This is what prevents a lineage from silently inheriting another's aggregate biases — and what does *not* prevent it is the open problem in §26.1 (FM-AL): individual re-validation catches artifact-level divergence, not the statistical shape of a corpus. CP records the inputs a meta-validator would need; it does not specify the meta-validator.

### 11.6 Deliberation Quality **[D-033]**

An AdherenceClaim MAY carry a `deliberation_quality` block recording how robustly the conclusion the interaction reached was arrived at — as distinct from whether the conclusion adhered.

```
deliberation_quality: {
  metric_id:   "<URI of an extension-defined metric>",
  value:       <number> | { ... },
  inputs_ref:  "<CID of a Snapshot or artifact set enumerating the witnessed records the metric was computed over>"
}
```

**Rules:**
- `inputs_ref` MUST resolve to witnessed records — position-bearing events (§8.3) carrying `stance`, `revision_cause`, and `deferred_to`, or artifacts derived from them. A metric computed over unwitnessed or self-reported inputs MUST NOT be recorded here.
- `metric_id` is extension-defined. CP does not define the metric. It defines that a metric exists, is identified, is computed over identified witnessed inputs, and is carried in a signed claim.

**Reference example.** The Internet of Cognition's Mycelium coordination layer computes two consensus-quality metrics over its negotiation episodes: a **genuine-agreement ratio** (the fraction of participants who ended on the converged position for reasons consistent with their own evidence trajectory) and a **social-compliance ratio** (the fraction of position revisions that occurred without engaging the counterparty's evidence), and lets participants flag deference on negotiation replies. These are, as of 2026-07-28, shipping in `mycelium-io/mycelium`. An extension that adopts them would define `metric_id`s for each, specify their formulas over CP's `positions` fields, and register them. CP names them here as the reason this slot exists and as evidence that the computation is practical.

What CP adds to such a metric is not the formula. It is that the `stance`, `revision_cause`, and `deferred_to` fields it is computed over are participant-signed and witness-receipted, so that the metric's inputs cannot be misreported by the participants being measured.

A floor that weights admitted artifacts by deliberation quality compounds reasoning faster than capitulation. A floor that does not compounds both at the same rate. Whether and how to weight is a Policy decision; CP makes the input available.

---

## 12. CONTESTATION AND ADJUDICATION

### 12.1 Contestation

A Contestation is a formal dispute of an artifact, attached to it as a `cp.contestation.v1` referrer. Any artifact may be contested — an event, a WitnessAttestation, an AdherenceClaim, a Relationship, a Constraint, an Adjudication, another Contestation.

```
credentialSubject: {
  artifact_kind:        "Contestation",
  target_ref:           "<CID>",
  constraint_decl_ref:  "<CID> | null",       // the frame the dispute is raised under; null = frame-neutral
  grounds:              "<string>",
  addresses:            [ "<CID>" ],           // §12.3 — REQUIRED, MAY be empty
  imports_from:         [ "<CID>" ],           // §12.4 — prior Contestations or Adjudications whose reasoning is reused
  evidence_refs:        [ "<CID>" ],
  scope:                "<scope>",             // inherits the target's scope; may not be narrower
  ts:                   "<iso8601>"
}
issuer: the contestant's DID
```

Status — open, adjudicated, withdrawn — is derived by walkers from the referrers attached to the Contestation (an Adjudication, a Tombstone by the contestant), never stored authoritatively (§4.15).

### 12.2 Open to Any Identity

Contestation is open to any DID-bearing entity, at any time. It is not restricted to participants in the contested interaction. It is not restricted to the period during which the interaction was live.

This is structurally necessary for §0.3. The party that detects a coordinated pattern across a thousand interactions was, by construction, not a participant in any of them. If only participants could contest, the pattern-detector would have no standing and the North Star would be unenforceable.

**Epistemic standing.** A participant contesting ("I was there; this is not what happened") and an external entity contesting ("across many records, this pattern is anomalous") make claims of different kinds. The substrate does not rank them. It records both, with issuer identity walkable to a principal (§7.13), so that an adjudicator — and anyone evaluating the adjudicator later — can weigh standing appropriately.

### 12.3 Engagement **[D-037]**

`addresses` names the specific artifacts or events the Contestation engages. A Contestation whose `addresses` is empty is, structurally, a parallel assertion rather than a reply: it asserts something about the target without engaging anything the target or its supporting record says.

**Rules:**
- `addresses` MUST be present. It MAY be empty.
- Walkers MAY render a Contestation with empty `addresses` as unengaged, and MAY render it below engaged Contestations by default. They MUST NOT hide it.
- The adjudicator records `engagement_verified` and `engagement_score` on the Adjudication (§12.6), assessing whether the Contestation actually engaged what it named.

This is the contingency check from the Internet of Cognition's CIP subprotocol — *does this response demonstrably engage the concepts in the prior turn?* — applied to CP's own dispute layer.

### 12.4 Importable Reasoning

`imports_from` references earlier Contestations or Adjudications whose reasoning the new Contestation reuses. The relationship is `cp:importsReasoning ⊂ prov:wasInformedBy` (§6.5).

**This is not precedent.** Precedent binds: a prior ruling decides a later case. Imported reasoning is available: a prior argument's structure, evidence, and moves are reusable, but the new Contestation must show they apply here, and *that applicability is itself contestable*. A Contestation whose imported reasoning is inapt can be contested on exactly that ground.

The effect over time is that adjudication gets cheaper. What has been reasoned through once need not be reasoned through from scratch. A lineage's contestation history becomes a library of arguments, each with its own provenance, each reusable by anyone who can defend its applicability. Manufactured narratives do not get this benefit: reasoning imported from a laundered source carries that source's provenance, and the provenance is walkable.

**Response.** The party whose artifact is contested MAY attach a **Response** (`cp.response.v1`) to the Contestation, carrying its own `addresses`, `evidence_refs`, and `grounds`. A Response is the contested party's engagement with the Contestation; it does not alter the contested artifact and does not resolve the Contestation. Adjudicators SHOULD consider Responses.

### 12.5 Contestation Volume and §1.7

CP imposes no rate limit on Contestation (§1.7). A flood of Contestations against an artifact or an entity is possible and is not prevented.

The defense is legibility, not restriction:
- Each Contestation names an issuer; each issuer walks to a principal (§7.13). Volume from one principal, or from a bloc whose deferral graph (§5.10) marks it as coordinated, is queryable.
- Empty `addresses` is structurally visible (§12.3). Unengaged volume is distinguishable from engaged volume without reading the grounds.
- Adjudicators' `engagement_score`s accumulate. A principal whose Contestations are consistently scored unengaged has a record.
- Contestations are themselves contestable. A pattern of bad-faith contestation can be contested as a pattern.

Volume is not filtered. It is made legible, so that whoever looks later can see it for what it was.

### 12.6 Adjudication

An Adjudication resolves a Contestation. It is a `cp.adjudication.v1` referrer on the Contestation.

```
credentialSubject: {
  artifact_kind:         "Adjudication",
  target_ref:            "<CID of Contestation>",
  resolution:            "upheld | rejected | modified | declined",
  engagement_verified:   true | false,
  engagement_score:      <0..1>,
  reasoning_trace:       { ... },                 // structured; SHOULD meet the spirit of §10.8
  imports_from:          [ "<CID>" ],             // reasoning this Adjudication reuses
  modifications:         [ "<CID of Patch>" ],    // for resolution: modified
  ts:                    "<iso8601>"
}
issuer: the adjudicator's DID
```

**Resolutions:**
- **upheld** — the Contestation stands. The contested artifact remains in the record, unchanged, and is rendered as *challenged, upheld*. Validators issuing later AdherenceClaims against it SHOULD account for the upheld Contestation in their trace.
- **rejected** — the Contestation fails. The contested artifact stands. The Contestation and its rejection remain in the record.
- **modified** — the Adjudication produces one or more Patches (§5.5) on the contested artifact, attached as `modifications`. The original is unchanged; the patched view is default-rendered.
- **declined** — the adjudicator declines jurisdiction or competence. The Contestation remains open. Another adjudicator may take it up.

No resolution removes anything. Every Contestation, Response, and Adjudication is permanent.

### 12.7 Who Adjudicates

CP requires only that the adjudicator be a distinct DID from the contestant and from the author of the contested artifact. Who else may adjudicate — a designated body, any validator in the lineage, a quorum — is extension-defined and declared in the ConstraintDecl or Policy.

### 12.8 Adjudications Are Contestable

An Adjudication is an artifact. It may be contested (§12.1). The recursion has no structural terminus; in practice it terminates by cost and by the accumulating legibility of §12.5. CP does not impose a depth limit — that would be a rate limit under another name.

---

## 13. TOMBSTONE, PATCH, AND SCOPE — INTERACTIONS

The three primitives are specified in §5.4–5.6. This section states how they compose.

**Scope of referrers.** A referrer inherits the scope of its target and MUST NOT declare a narrower one. A Contestation on a private artifact is private. A Tombstone on a public artifact is public.

**Patch on a tombstoned artifact.** Permitted. The Patch is suppressed in default rendering along with its target and visible to evaluation-mode walkers along with it.

**Tombstone on a Patch.** Permitted. Withdraws the correction; the original stands in default rendering.

**Tombstone on a Contestation or Adjudication.** Permitted, and is how a contestant withdraws. The Contestation remains in the record as withdrawn.

**Rendering modes.** Walkers operate in one of two modes and MUST declare which:

| Mode | Tombstoned artifacts | Patches | Purpose |
|---|---|---|---|
| default | suppressed, with indication (§4.14 rule 3) | most recent authoritative Patch applied | surface rendering |
| evaluation | included | all Patches enumerated; original and each patched state available | pattern detection, retrospective re-evaluation, adjudication |

A walker in evaluation mode sees everything. This is the mode validators and adjudicators MUST operate in.

---

## 14. CONCEPT AND CONCEPTCOLLECTION

Specified in §5.1–5.2. Interaction semantics:

**Status transitions.** `candidate → confirmed` and any extension-defined states are recorded as Patches on the Concept (`patch_type: status`), so the history of a concept's standing is walkable.

**Links.** A Concept's `links` are the author's self-assertions (§15.3). Third-party relationships involving a Concept — a learner's mastery, a pattern-detector's inferred connection — are standalone Relationships (§15).

**Discovery.** ConceptCollections are the discovery surface. A CP entity's OASF record (§2.7) MAY list its public collections; a collection's `tags` and `description` are indexable.

**Namespace.** `concept_id` shares the `urn:concept:` namespace with the Internet of Cognition's L9 protocol (§5.1). Where both systems refer to the same concept, they use the same identifier.

---

## 15. RELATIONSHIP

### 15.1 Why First-Class **[D-011]**

Relationships between artifacts are themselves artifacts, for three reasons:

- **Independent contestability.** "I accept the source, I accept the target, I dispute that they are connected this way" is a contestation of the relationship alone. If relationships lived only as fields on artifacts, disputing one would require disputing the artifact.
- **Third-party assertion.** A pattern-detector asserting that forty artifacts share a structural property is asserting relationships between artifacts it did not author. It needs somewhere to put that assertion, signed, under its own identity.
- **A graph that evolves after the fact.** Future understanding adds connections across old artifacts. Old artifacts do not change; new Relationships attach.

### 15.2 Schema

```
credentialSubject: {
  artifact_kind:   "Relationship",
  from:            "<concept_id | CID | DID>",
  predicate:       "<PROV-O term or CP/extension subproperty, §6.5>",
  to:              "<concept_id | CID | DID>",
  explanation:     "<string> | null",
  confidence:      <0..1>,
  evidence_refs:   [ "<CID>" ],
  scope:           "<scope>",
  ts:              "<iso8601>"
}
issuer: the asserting entity's DID
```

A Relationship is a `cp.relationship.v1` referrer on its `from` artifact and MUST be discoverable from its `to` artifact through the referrer index.

### 15.3 Self-Asserted and Third-Party

An artifact's author MAY inline relationships as `links` on the artifact itself (§5.1 shows the form). These are the author's claims about their own work — citations, dependencies, derivations — and are signed with the artifact.

Any entity asserting a relationship between artifacts it did not author MUST issue a standalone Relationship. It cannot inline onto artifacts it does not control.

Walkers traverse both. They are distinguishable by issuer: an inline link's issuer is the artifact's author; a standalone Relationship's issuer is whoever asserted it.

### 15.4 PROV-O Expression **[D-017]**

Every Relationship is a PROV statement. `from` and `to` are PROV Entities, Activities, or Agents; `predicate` is a PROV-O property or a declared subproperty (§6.5); `issuer`, `confidence`, `explanation`, and `evidence_refs` are carried through the PROV qualified-influence pattern (`prov:qualifiedInfluence` with a CP influence class carrying the extra fields).

CP publishes a normative JSON-LD frame for this expression so that PROV-aware tooling can consume CP Relationships without CP-specific code, and so that PROV-AGENT captures (Appendix F) can be ingested as CP Relationships.

### 15.5 Deferral as Relationship

Participant-declared deferral is a field on events (§8.3, `deferred_to`). Detector-inferred deferral is a standalone Relationship with `predicate: cp:defersTo` issued by the detector. The two are distinguishable by issuer and are both walkable. A pattern-detector's inferred deferral graph is therefore a signed, contestable set of artifacts — not a private conclusion.

### 15.6 Contesting a Relationship

A Relationship is an artifact. A Contestation attaches to it (§12). Its endpoints are untouched.

---

## 16. ROLEGRANT — THE AUTHORITY WALK

Specified in §5.3. Interaction semantics:

**The walk.** From any action by a delegate — an event, a SubAgentArtifact, a spawn — a walker MUST be able to reach the RoleGrant that authorized it, the issuer of that grant, the grant that authorized the issuer to grant, and so on to a principal. Every hop is a Verifiable Credential with checkable status.

**Revocation first.** Before honoring any grant, a walker MUST check its Bitstring Status List entry. A revoked grant is visible in the record and confers nothing.

**Scope containment.** A grant's `scope` MUST be within the issuer's own authority scope for those roles. A delegate authorized at `org` scope cannot grant at `public` scope.

**Blocking.** At issuance, `blocks_roles` on every BLOCKING Constraint in scope is checked (§5.3, §5.8). A refused issuance is a `delegation.refused` attestation (§10.3).

This is the structural defense against FM-AC. Authority that cannot be walked to a principal is not authority under CP.

---

## 17. SNAPSHOT **[SUBSTITUTED — D-019, amends D-004.c]**

### 17.1 Role

A Snapshot is the temporal anchor for an AdherenceClaim (§11.4). It states, verifiably, *what the floor consisted of* at the moment a validator read it. Without it, "the floor as I saw it" is unverifiable and time-indexing is a promise rather than a mechanism.

v0.4.1 specified Snapshot as a bespoke artifact enumerating floor contents. This version expresses it as a signed statement binding two things that already exist: a Transparency Service **tree head** (the log at time *T*, immutable, published by the TS) and a **filter** (which statements in that log constitute this lineage's floor).

### 17.2 Schema

```
credentialSubject: {
  artifact_kind:     "Snapshot",
  lineage: {
    constraint_decl_ref:  "<CID>",
    policy_ref:           "<CID>",
    validator_ref:        "<CID> | null"
  },
  tree_heads: [ {
    log_id:               "<TS log identifier>",
    tree_head_ref:        "<CID or URI of the signed tree head>",
    tree_size:            <n>
  } ],
  filter_ref:        "<CID of the filter definition>",
  floor_size:        <n>,
  floor_root:        "<Merkle root over the CIDs of the filtered set, in canonical order>",
  compiled_ts:       "<iso8601>",
  ts:                "<iso8601>"
}
issuer: typically the validator; any entity may issue a Snapshot
```

### 17.3 Why Tree Head Plus Filter

A tree head alone is a snapshot of the *log* — everything registered, adherent or not, in this lineage or any other. The floor is a *subset*: those artifacts carrying affirmative claims under this lineage above its threshold. Neither object alone is what §11.4 needs.

The filter is a content-addressed definition — an executable or a precise specification, in the sense of §10.7 — that, applied to the log up to the given tree heads, yields the floor. Binding tree heads and filter in one signed statement makes "the floor as it stood at *T*" a verifiable claim: anyone can fetch the log up to those tree heads, apply the filter, and check the result's Merkle root against `floor_root`.

### 17.4 Determinism

Given the same tree heads and the same filter, the floor is the same set. `floor_root` is recomputable. A validator claiming against a Snapshot is claiming against a set anyone can reconstruct, not against the validator's private memory of it.

### 17.5 Bundle and MediaRef

Export bundles (`portability:Bundle`) and external media references (`media:MediaRef`) are extension-defined artifact kinds. CP provides the referrer mechanism and the detached-payload mechanism (§4.1.3) they build on; it does not specify them.

---

## 18. REFERENCE, PROVENANCE, AND COMPILATION

### 18.1 Reference

A typed pointer, used within artifact bodies where a bare CID is insufficient:

```
{
  type:        "artifact | concept | did | url | tree_head | <ext>",
  value:       "<string>",
  scope:       "<scope>",
  visibility:  "public | org | private"
}
```

### 18.2 Provenance Block

Every compiled artifact (§18.3) carries:

```
provenance: {
  event_range:            { from: "<CID>", to: "<CID>" },
  compiler_ref:           "<CID of the compiler artifact>",
  compiled_ts:            "<iso8601>",
  contributing_entities:  [ "<DID>" ],
  source_refs:            [ "<CID>" ]
}
```

and Relationships `cp:createdFromEvent` to each source event (§6.5). The provenance block is a PROV bundle: the artifact `prov:wasGeneratedBy` the compilation activity, which `prov:used` the events, and the artifact `prov:wasAttributedTo` the contributing entities.

### 18.3 Compilation

Compilation transforms a witnessed event log into compiled artifacts — Concepts, SubAgentArtifacts' registrations, Constraints, self-asserted Relationships, Snapshots. It is deterministic (§1.1): same events, same referenced inputs, same compiler, byte-identical output.

**Rules:**
- The compiler is itself a content-addressed artifact (`Compiler`), named by `compiler_ref`. Its executable is retrievable and re-runnable.
- Recompilation MUST reproduce the original output. A compiler that cannot is non-conformant.
- Compilation never issues AdherenceClaims. Judgment is the validator's (§10.5). Compilation extracts and structures; it does not evaluate.
- Compiled artifacts are derived. Events are source (§8.6). Where they disagree, recompile.

### 18.4 Why Provenance Is Load-Bearing

Provenance is what pattern-detectors query. Which entities contributed to an artifact, through which events, under which compiler — these are the fields that let a later evaluator ask whether forty artifacts share a hidden common origin, whether a model's outputs cluster, whether a principal's delegates converge suspiciously. The provenance block is small. It is the reason the rest of the record can be interrogated.

---

## 19. CANONICALIZATION

### 19.1 JSON

All JSON artifacts MUST canonicalize via RFC 8785 (JSON Canonicalization Scheme). This is the canonicalization every CP cryptosuite (§20.1) assumes; the `*-jcs-*` suite identifiers name it.

### 19.2 Markdown and Text

Text artifacts MUST: encode as UTF-8; normalize line endings to LF; strip trailing whitespace from each line; end with exactly one trailing newline. Text artifacts are hashed as bytes after normalization.

### 19.3 CID Computation

The CID of an artifact is computed over the JCS-canonical credential with the `proof` member removed. `id` is set to this CID. Because `id` is inside the credential, computation is: remove `proof` and `id`, canonicalize, hash, set `id`, then sign.

### 19.4 Proof Computation

Each Data Integrity proof is computed per its cryptosuite over the JCS-canonical credential with `proof` removed and `id` present. Where multiple proofs are present (hybrid transition, §4.6.2; composite thresholds, §7.12), each is computed independently over the same canonical input and the `proof` member is an array.

### 19.5 SCITT Payload Bytes

The SCITT Signed Statement payload (§4.3.2) is the JCS-canonical credential *including* `proof`. The COSE_Sign1 signature is over these bytes per COSE. This means the outer signature covers the inner proof — a change to either is detectable.

### 19.6 Hash Primitives

`BLAKE3-256` for DID derivation (§7.3); `SHA3-256` default for CIDs; `SHA-256` accepted for CIDs (legacy and for compatibility with SHA-2-based cryptosuite hashing). The primitive is declared in the CID's multihash prefix. §20.1 registers them.

---

## 20. PRIMITIVES REGISTRY, COMPROMISE DECLARATION, CONSTRAINTDECL, POLICY

### 20.1 Primitives Registry

The Registry is a CP-native artifact listing the cryptographic primitives conforming implementations MUST support and MAY use. It is versioned, forkable (§4.17), and anchor-signed by its publisher.

**Registry contents at v0.5:**

| Category | Identifier | Status |
|---|---|---|
| Data Integrity cryptosuite | `mldsa44-jcs-2024` | REQUIRED — workhorse |
| Data Integrity cryptosuite | `slhdsa128-jcs-2024` | REQUIRED — anchor |
| Data Integrity cryptosuite | `eddsa-jcs-2022` | TRANSITIONAL — hybrid only; sunset 2030-01-01 |
| COSE algorithm (SCITT wrapper) | EdDSA (`-8`) | TRANSITIONAL — until COSE PQ identifiers are registered |
| COSE algorithm (SCITT wrapper) | ML-DSA-44 (identifier per `draft-ietf-cose-dilithium` when final) | REQUIRED after 2030-01-01 |
| Hash | `blake3-256` (multihash `0x1e`) | REQUIRED — DID derivation |
| Hash | `sha3-256` (multihash `0x16`) | REQUIRED — CID default |
| Hash | `sha2-256` (multihash `0x12`) | ACCEPTED |
| Multikey codec | ML-DSA-44 public key `0x1210` | REQUIRED |
| Multikey codec | SLH-DSA-SHA2-128s public key `0x1220` | REQUIRED |
| Multikey codec | Ed25519 public key `0xed` | TRANSITIONAL |

Registry updates are new Registry versions. An artifact signed under a given Registry version is verified against that version (§1.8).

### 20.2 Compromise Declaration

When a primitive is broken — algorithmic break, practical side-channel, key-recovery attack — any party MAY publish a Compromise Declaration:

```
credentialSubject: {
  artifact_kind:          "CompromiseDeclaration",
  compromised_primitive:  "<registry identifier>",
  severity:               "deprecated | broken | catastrophic",
  evidence_refs:          [ "<CID or URI>" ],
  ts:                     "<iso8601>"
}
```

After a Declaration of severity `broken` or above gains adoption (§24.2): new artifacts SHOULD NOT use the primitive; existing artifacts retain their original verification policy and remain verifiable *as artifacts of their era*; walkers SHOULD annotate them; the Registry publisher SHOULD issue a new version. Nothing is invalidated. The record shows what was signed under what, and what was later declared about it.

### 20.3 ConstraintDecl — The Declared Frame

A ConstraintDecl is the normative frame an entity adheres to (§5.8). It is Tier 1: forkable, lineage-bearing, content-addressed, the object every AdherenceClaim is made against.

```
credentialSubject: {
  artifact_kind:        "ConstraintDecl",
  constraint_id:        "<string>",
  title:                "<string>",
  statement:            "<the constraint, in the declarer's words>",
  statement_ref:        "<CID of a longer document> | null",
  adjudicator_eligibility:  "<extension-defined rule or CID>",
  validator_eligibility:    "<extension-defined rule or CID>",
  fork_of:              "<CID> | null",
  declared_by:          "<DID>",
  ts:                   "<iso8601>"
}
```

A ConstraintDecl says nothing about how adherence is measured. That is the Policy's job. A ConstraintDecl with no Policy is a statement of values; a ConstraintDecl with a Policy is an evaluable frame.

The DAX constraint — *preservation and expansion of life, humanity, and consciousness* — is a ConstraintDecl published by the DAX Foundation. It is not referenced anywhere in this specification's normative text. It is one frame among any number.

### 20.4 Policy — The Interpretation

A Policy is an operational interpretation of a ConstraintDecl: what is measured, how, and what threshold admits an artifact to the floor.

```
credentialSubject: {
  artifact_kind:          "Policy",
  interprets:             "<CID of ConstraintDecl>",
  rules_ref:              "<CID of the rule set, in the validator's executable language>",
  admission_threshold:    <0..1>,                 // §11.5
  verdict_shape:          "probability | composite | boolean",
  deliberation_weighting: "<CID of weighting rule> | null",   // §11.6
  fork_of:                "<CID> | null",
  declared_by:            "<DID>",
  ts:                     "<iso8601>"
}
```

One ConstraintDecl MAY have many Policies. Each Policy with each Validator lineage is a distinct lineage (§11.5). Two organizations adhering to the same ConstraintDecl under different Policies compound into different floors and may import across them (§1.5).

---

## 21. WALKER CONTRACT

### 21.1 The Seven Rules

Tier 1, stated in §4.14. Restated here as conformance tests:

| # | Rule | Conformance test |
|---|---|---|
| 1 | Verify before honoring | Given an artifact with an invalid Data Integrity proof, the walker MUST NOT present its content as authored by `issuer`. |
| 2 | Verify witnessing | Given an artifact with no valid Receipt inclusion proof, the walker MUST present it as unwitnessed. |
| 3 | Surface tombstones to pattern-matchers | In evaluation mode, given a tombstoned artifact, the walker MUST include it. In default mode, the walker MUST indicate suppression occurred. |
| 4 | Process under declared version | Given an artifact with `spec_version: 0.4`, the walker MUST apply v0.4 rules to it. |
| 5 | Enumerate all claims | Given a WitnessAttestation with *n* AdherenceClaims, the walker MUST be able to return all *n*. |
| 6 | Verify per-context chains | Given a context with a missing `seq`, the walker MUST flag the gap. |
| 7 | Do not filter cross-constraint queries silently | Given a cross-constraint query, the walker MUST return artifacts from every constraint, annotated. |

A conformance test-vector suite for these seven rules is published alongside this specification (Apache-2.0).

### 21.2 Modes

Every walker declares its mode (§13): **default** or **evaluation**. Validators, adjudicators, and pattern-detectors MUST operate in evaluation mode.

### 21.3 Walker Classes

Beyond the seven rules, walker behavior is extension-defined. Common classes:

- **Surface** — renders interfaces; default mode; honors Tombstones and Patches.
- **Pattern-detector** — traverses across contexts and lineages; evaluation mode; produces Relationships (§15.5) and Contestations (§12); its inputs are what §26.1 calls the meta-validator's inputs.
- **Validator** — reads one attestation and its floor Snapshot; evaluation mode; produces AdherenceClaims.
- **Auditor** — verifies chains, receipts, and provenance; evaluation mode; produces reports (extension-defined kind).
- **Adjudicator** — reads Contestations, Responses, and evidence; evaluation mode; produces Adjudications.

### 21.4 What a Walker Is Not

A walker is not a gatekeeper. It reads; it does not decide what may be written. A walker that refuses to display an artifact has not removed it from the record.

---

## 22. FAILURE MODES AND THE THREAT-MODELING METHOD

### 22.1 The Taxonomy

§5.12 defines thirteen named failure modes. They are the vocabulary in which this specification says what each rule defends against.

### 22.2 The Method

Every field, relationship, and rule in a CP artifact kind or extension SHOULD be threat-modeled with six questions:

| Question | Asks |
|---|---|
| **Wrong if** | What would make this field's value incorrect? |
| **Missing if** | What does its absence cost? |
| **Misused if** | How could it be weaponized? |
| **Detect** | How is the failure noticed, and by whom? |
| **Mitigate** | What reduces the failure's impact? |
| **Defends against** | Which named failure modes does this field's presence address? |

### 22.3 Worked Example — `deferred_to` (§8.3)

| | |
|---|---|
| Wrong if | participant names a DID it did not actually defer to, or `null` when it did defer |
| Missing if | influence is unmeasurable; the deferral graph has a hole; FM-NL detection weakens |
| Misused if | a bloc coordinates to name a decoy DID, diffusing the concentration signal |
| Detect | cross-context: a decoy's deferral inflow without corresponding position history; `revision_cause: social_compliance` clustering; correlated priors (§5.11) |
| Mitigate | field is witness-receipted (§4.10) — cannot be edited after the fact; detector-inferred `cp:defersTo` Relationships (§15.5) are independent of participant declaration |
| Defends against | FM-NL, FM-EA, FM-AL |

Extensions SHOULD publish this table for every field they introduce.

---

## 23. EXTENSION MECHANISM

### 23.1 ExtensionDecl

```
credentialSubject: {
  artifact_kind:       "ExtensionDecl",
  extension_id:        "<namespace prefix, e.g. education>",
  extends:             [ "cp" | "<extension_id>" ],
  version:             "<semver>",
  context_uri:         "<JSON-LD context URI>",
  artifact_kinds:      [ "<ext>:<Kind>" ],
  referrer_types:      [ "<ext>.<type>.v<n>" ],
  event_kinds:         [ "<ext>:<KIND>" | "<CP_KIND>.<subkind>" ],
  predicates:          [ { term: "<ext>:<pred>", subPropertyOf: "<PROV-O or CP term>" } ],
  scope_vocabulary:    { values: [ ... ], ordering: [ [ narrower, broader ], ... ] } | null,
  stances:             [ "<ext>:<stance>" ],
  revision_causes:     [ "<ext>:<cause>" ],
  interpretations:     { "<CP Tier 2 primitive>": "<CID of interpretation document>" },
  deliberation_metrics: [ { metric_id: "<URI>", spec_ref: "<CID>" } ],
  executable_spec:     "<CID> | null",
  fork_of:             "<CID> | null",
  declared_by:         "<DID>",
  ts:                  "<iso8601>"
}
```

### 23.2 Conformance

An implementation conforming to an extension MUST recognize its kinds, referrer types, event kinds, predicates, scope vocabulary, stances, and revision causes, and MUST apply its interpretations to the Tier 2 primitives it names.

### 23.3 Composition and Conflict

An artifact claims extensions by including their contexts and using their terms. Two extensions conflict when they supply incompatible interpretations of the same Tier 2 primitive for the same artifact. A walker encountering a conflict MUST report it and MUST NOT resolve it by choosing one. Resolution is a Patch by the artifact's author, or a new extension that reconciles the two.

### 23.4 Promotion

An extension term used identically by multiple independent extensions MAY be promoted to CP-native in a later version (§24). The proposing party publishes a specification proposal (§24.1) citing the converging extensions.

### 23.5 The Four Named Extensions

This specification anticipates four foundational extensions, specified separately: **Attribution** (authorship, derivation, provenance weight), **Credit** (compensation flows over Attribution), **Education** (Concept mastery, rubrics, learner state), **Governance** (adjudicator eligibility, precedent-as-reasoning, institutional composites). Their CP dependencies are noted in Appendix A. None is normative on CP.

---

## 24. SPECIFICATION EVOLUTION

### 24.1 Proposing

Any party MAY publish a proposed CP-SPEC version as a forkable artifact (`fork_of` naming the version it descends from). The DAX Foundation holds no gatekeeping role (§1.6). Input to the DAX Foundation's own versions follows Appendix E.

### 24.2 Currency

The current version of CP is whichever has accumulated the most adoption, measured in registered Validator artifacts declaring `spec_version`, ConstraintDecls and Policies referencing it, and witnessed traffic under it. Adoption is observable in the record. There is no other authority.

### 24.3 Versioning

Semantic versioning. A major version MAY change Tier 1 rules for new artifacts; it MUST NOT invalidate artifacts signed under earlier versions (§1.8). A minor version adds without changing. A patch version corrects text.

### 24.4 Contesting the Specification

This specification is an artifact. It may be contested (§12) by any identity. Adjudications of specification contestations produce reasoning that future versions may import. The specification is subject to the process it specifies.

### 24.5 Pre-Committed Revision Conditions

Appendix F names, for each adjacent system this version watches, the condition under which CP should stop building and contribute a profile instead. Those conditions are part of this specification. A future version that ignores a triggered condition without recording why has not followed §1.6.

---

## 25. DECISION LOG

Every primitive in this specification resolves to a numbered decision. Full rationale for each is in the companion document *CP-SPEC v0.5 Decision Log*; this section is the index. Where a v0.5 decision amends or reverses an earlier one, both are shown.

### 25.1 v0.4 Reconciliation (2026-04-27)

| ID | Decision | Touches | v0.5 status |
|---|---|---|---|
| D-001 | Per-primitive reconciliation, no baseline document | method | stands |
| D-002 | Three artifacts: substrate / extensions / strategy | §0, §23.5 | stands |
| D-003 | Two-tier core; DAG extension composition; lens semantics | §3, §6 | stands |
| D-004 | AdherenceClaim distinct from WitnessAttestation | §10, §11 | stands |
| D-004.a | Probabilistic verdict canonical | §11.2 | stands |
| D-004.b | Floor is time-indexed | §11.4 | stands |
| D-004.c | Snapshot Tier 1 | §17 | mechanism amended by D-019 |
| D-005 | Cross-org witnesses independent | §4.1.7, §9.6 | stands |
| D-006 | Tombstone Tier 2, scope-dependent, never hides from pattern-matchers | §5.4, §4.13 | stands |
| D-006.a | Scope non-narrowable | §4.12 | stands |
| D-006.b | Contestation open to any DID | §12.2 | gains engagement (D-037) |
| D-006.c | Adjudication Tier 2 | §12.6 | stands |
| D-006.d | IMPORTS_REASONING structural on Contestation | §12.4 | stands; predicate now `cp:importsReasoning` |
| D-006.e | Constraints govern adherence, not epistemic access | §1.5, §11.5 | stands |
| D-007 | Namespaced kinds; CP-native bare; promotion path | §6.3 | stands |
| D-008 | Walker contract: minimal Tier 1 rules | §4.14, §21 | stands; rule 2 added |
| D-009 | Envelope Position γ (CP-native + VC transform) | — | **reversed by D-016** |
| D-009.a | Quantum-grade identity normative | §4.5, §7 | stands |
| D-009.b | Primitives Registry | §20.1 | stands |
| D-009.c | Multi-sig via verification methods | §7.12 | stands |
| D-010 | Patch as CP-native Tier 2 | §5.5 | stands |
| D-011 | Relationship first-class; self-asserted may inline; third-party standalone | §15 | predicates amended by D-017 |
| D-012 | Structured event-kind family | §6.4 | stands; pattern reused by D-025, D-036 |

### 25.2 v0.4.1 Identity Point Release (2026-05-06)

| ID | Decision | Touches | v0.5 status |
|---|---|---|---|
| D-013 | Frozen genesis; fingerprint = hash of genesis only; append-only rotation log; permanent custody; operator pays, never custodian; independent path; friendly name not root | §1.11, §7.4–7.9 | stands; vocabulary re-expressed by D-021 |

### 25.3 v0.5 Upgrade (2026-09-10)

**Foundational**

| ID | Decision | Touches |
|---|---|---|
| D-014 | Entity-neutral principal; `kind` / `chain_role` split; "agent" is a role | §1.12, §4.5.2, §7.13 |

**Substitutions**

| ID | Decision | Touches | Amends |
|---|---|---|---|
| D-015 | Ledger → IETF SCITT profile on Rekor/Trillian; scoped TS instances; per-context chain retained | §4.1 | re-expresses v0.4 §4.1–4.3 |
| D-016 | Envelope → VC 2.0 native; PQ Data Integrity cryptosuites | §4.3, §4.6 | **reverses D-009** |
| D-016.a | Workhorse ML-DSA-44, not ML-DSA-65 | §4.6.1, §7.10 | v0.4.1 §7 |
| D-016.b | Anchor signatures bind anchor public key | §4.6.3, §7.10 | new |
| D-017 | Relationship predicates → PROV-O subproperties | §6.5, §15.4 | D-011 |
| D-018 | RoleGrant → VC with Bitstring Status List revocation | §5.3, §16 | v0.4.1 §16 |
| D-019 | Snapshot → signed binding of tree heads + filter | §17 | D-004.c mechanism |
| D-020 | Validator executable_spec SHOULD be Cedar / OPA-Rego | §10.7 | v0.4.1 §10.7 |

**Adoptions**

| ID | Decision | Touches | Condition |
|---|---|---|---|
| D-021 | Identity in W3C DID / VC 2.0 / Data Integrity terms | §4.5, §7 | ⚑ cleared (B-1) |
| D-021.a | **Pre-rotation adopted from KERI** — anchor commits to successor hash | §7.4, §7.5.2 | new in Phase C |
| D-022 | Delegation → DIF KYA-OS profile, entity-neutral | §7.13 | pinned to WG spec at publication |
| D-023 | Transport, discovery, coordination out of scope; composition surfaces named | §2.7, §26.7 | — |
| D-024 | Attachment → OCI referrer pattern (AGNTCY `dir`) | §4.2 | ⚑ cleared (B-2, B-7) |

**Operational findings (cross-node run, 2026-05-04)**

| ID | Decision | Touches |
|---|---|---|
| D-025 | One WitnessAttestation kind; `claim_type` family | §10.3 |
| D-026 | SubAgentArtifact as Tier 2 kind | §5.7 |
| D-027 | Promotion rule — only validator DIDs issue AdherenceClaims | §4.9 |
| D-028 | Constraint lifecycle RAISED→RESOLVED→BLOCKING→REOPENED; `compliance_failure` | §5.8 |
| D-029 | `blocks_roles`; refusals witnessed as `delegation.refused` | §5.8, §5.3 |
| D-030 | ContextOpen/Close optional; minimal context | §9.2–9.4 |
| D-031 | Every log entry is participant-signed + witness-receipted | §4.10, §8.4 |
| D-032 | Inline validation as permitted mode | §10.9 |

**Deliberation and influence (from Outshift IoC / Mycelium)**

| ID | Decision | Touches |
|---|---|---|
| D-033 | `deliberation_quality` slot on AdherenceClaim; inputs MUST be witnessed | §11.6 |
| D-034 | `deferred_to`, `revision_cause`; `cp:defersTo` predicate | §5.10, §8.3, §15.5 |
| D-035 | `prior_ref`; `prior` / `posterior` distinct from `verdict` | §5.11, §8.3, §9.3 |
| D-036 | Revision-cause taxonomy | §5.10 |
| D-037 | Engagement: `addresses[]`; `engagement_verified/score` on Adjudication | §12.3, §12.6 |
| D-038 | Participant stance vocabulary; `unresolved` first-class | §5.9, §9.4 |
| D-039 | Cross-episode stores remain open research; inputs specified | §26.1, §4.15 |

**Publication posture**

| ID | Decision | Touches |
|---|---|---|
| D-040 | v0.5 Public Working Draft | header |
| D-041 | CC-BY-4.0 prose; Apache-2.0 schemas/code/vectors | header |
| D-042 | Worked examples genericized | Appendix D |
| D-043 | Watch list with pre-committed revision conditions | Appendix F, §24.5 |
| D-044 | Third-party claims re-verified, dated, phrased as observation | throughout |
| D-045 | Threat model — five statements | §0.3 |
| D-046 | Evidence and Validation section | §27 |
| D-047 | Vocabulary alignment with IoC/L9/Mycelium under three rules | §6.4, §6.6, §9.1, Appendix C |

### 25.4 Design Notes Recorded During Drafting

Choices made while writing that follow from decisions above but were not separately ratified. Each is revisable through §24.

| § | Note |
|---|---|
| 4.1.5 | Scope widening is a new witnessed act (`cp:republishedFrom`), never a reinterpretation |
| 4.3.2 | SCITT payload is the JCS-canonical VC including its proof; COSE wrapper by same issuer; dual-format verifiability is deliberate |
| 4.5.4 | v0.4 "first DID" rule replaced by DID `assertionMethod`-at-signing-time semantics |
| 4.14 | Walker rule 2 (verify Receipt inclusion proof) added |
| 5.8 | **ConstraintDecl** (frame, Tier 1) vs **Constraint** (instance obligation under a frame, Tier 2) disambiguated; `under_constraint_decl` required |
| 5.12 | FM-SC Self-Certification named |
| 7.3 | `did:cp` declared a placeholder pending PQ codes in `did:webs` |
| 7.4 | Delegate co-signature carried in SCITT registration, not genesis body |
| 9.1 | Episode replaces Session; ContextOpen/Close replace SessionOpen/Close; legacy aliases retained |
| 10.3 | `event` family added to `claim_type` (every receipt is an attestation) |
| 10.4 | IndependenceAssertion is a named artifact kind |
| 11.5 | Cross-lineage import needs no predicate — the second claim is the import record |
| 12.4 | Response (`cp.response.v1`) — contested party's engagement |
| 12.6 | Adjudication `declined` resolution |
| 13 | Walker modes default / evaluation formalized |
| 18.3 | Compiler is a named content-addressed kind |

### 25.5 Architectural Commitments

North Star (§0.3) · Multi-Level Queryability (§0.4) · Two-Tier Core (§3) · Entity-Neutral Principal (§1.12) · Adopt / Substitute / Build (§3.4). These are commitments, not decisions: the criteria decisions are evaluated against. A future version may revise them only through §24 with the revision and its reasoning recorded.

---

## 26. OPEN RESEARCH

Recognized and not specified. Each names what CP provides toward it and what it does not.

### 26.1 Aggregate Lineage Bias and the Meta-Validator

Individual re-validation on cross-lineage import (§11.5) catches artifact-level divergence. It does not catch the statistical shape of a corpus — a lineage whose adjudication culture resolved tradeoffs one way, whose artifacts each pass but whose aggregate carries a bias invisible at artifact granularity (FM-AL).

The solution class is a **meta-validator**: a pattern-detector operating over floors rather than artifacts. Its inputs are now specified — witnessed `stance`, `revision_cause`, `deferred_to`, `prior`/`posterior` (§8.3), detector-asserted `cp:defersTo` Relationships (§15.5), provenance blocks (§18.2), and cross-lineage claim sets (§11.5), all reachable under walker rule 7. Its aggregation — what statistic over those inputs constitutes a bias signal — is not specified. Cross-episode belief and interaction stores (D-039) are its natural index and remain indexes (§4.15), not primitives.

### 26.2 Compiler Throughput

No normative throughput requirement. Agent-swarm regimes will make this binding. Not specified.

### 26.3 Self-Attestation Graduation

When does a `witness.relationship: participant` deployment (§4.7) graduate to external witnessing? What triggers it? Operational; extension-defined.

### 26.4 Witness Economics

Who operates Transparency Services at scale, and who pays? The gradient in §0.3 depends on witnesses existing. Not specified.

### 26.5 Federation Witness Disagreement

When independent TS instances (§9.6) receipt divergent records, the substrate preserves both and resolves nothing. Whether and how a lineage resolves such divergence is Policy-level and unspecified.

### 26.6 Root Key Recovery

Pre-rotation (§7.5.2) narrows theft to the case where both the active anchor and its pre-committed successor are compromised together. It does nothing for loss. Social recovery, opt-in operator-assisted recovery bounded by §1.11, and hardware-anchored keys remain candidates. Not specified.

### 26.7 Coordination

CP does not help entities converge. It records whether and how they did. A CP-witnessed interaction that never converges is a complete record of non-convergence (§0.2, §9.8). Coordination is the domain of L9-class protocols CP composes with (§2.7). This exclusion is by design (D-023) and is recorded here so that it is not mistaken for an omission.

### 26.8 Substrate and Legal Accountability

§1.12 records accountability in the substrate's terms and does not require that a principal be a legal person. The relationship between a CP accountability walk (§7.13) and legal liability in any jurisdiction is unspecified and is the province of constraints that choose to require legal personhood of their principals. This is the gap D-014 opens deliberately.

### 26.9 The Hash That Remains

§4.16 permits PII at private scope only as a detached payload, destroyable, with its hash permanent in the log. Whether a hash of destroyed personal data is itself personal data under any deletion-rights regime is a legal question CP does not answer. Adopters MUST obtain their own answer.

---

## 27. EVIDENCE AND VALIDATION **[D-046]**

This section states what evidence exists for the claims in this specification, what that evidence is not, and what CP commits to producing.

### 27.1 What Exists

One operational run. On 2026-05-04, two cognitive-companion instances operated by two organizations interacted across a network boundary under a build of the v0.4 specification. Each instance held a distinct witness identity and a distinct validator identity — four identities total, honoring §4.7 and §4.8. Cryptography was declared Phase 1 — Ed25519 signatures, BLAKE2b-256 hashes — with a post-quantum upgrade path recorded in each identity document.

Over roughly three and a half hours:

- One instance raised two **Constraints** under a shared ConstraintDecl, each with `blocks_roles` naming implementer and deployment roles.
- The other instance attempted **three times** to have the blocked roles spawned — with briefs that read, in part, "ignore the open constraints" and "ignore the compliance gate." All three were refused. All three are permanent, witness-signed records.
- One Constraint moved **RAISED → RESOLVED → REOPENED** in approximately twenty minutes: a resolution was recorded with evidence; a compliance-checking sub-agent examined the evidence and returned a verdict scoring 0.25 against a passing threshold, noting the evidence was truncated mid-line; the Constraint reopened, blocking again.
- One cross-organization artifact transmission produced an **inline AdherenceClaim** signed by the receiving validator's DID, with a full evaluation trace and a geometric-mean aggregation over five rules.
- The run produced approximately 34 witness-signed events across 12 hash-chained contexts and 13 content-addressed sub-agent outputs on one node, plus a smaller mirror on the other.

### 27.2 What It Showed

- Refusal under a *declared* constraint works, and the substrate records the refusal without deciding it (§0.2, §5.8).
- Bypass attempts against a blocking constraint are preserved as evidence rather than discarded (§0.3, first statement).
- Time-indexed re-evaluation operates at short timescales: a resolution judged adequate at T₀ was judged inadequate at T₀ + 20 minutes by a later evaluator with more information, and both judgments are in the record (§11.4).
- Independent witness and validator identities were honored structurally; the roles did not collapse.
- Cross-organization inline validation is practical and produces a proper, traceable claim (§10.9).

### 27.3 What It Exposed

The run diverged from the v0.4 specification in eight places. Each became a decision in this version:

| Observed | Decision |
|---|---|
| Witness attestations carried a `claim_type` field with eight-plus values the spec did not define | D-025 |
| Every sub-agent invocation produced an artifact kind the spec did not name | D-026 |
| In-loop compliance verdicts flowed from a sub-agent into constraint state **without a validator signature** — self-certification (FM-SC) | D-027 |
| Constraints had a lifecycle and a `compliance_failure` block the spec did not specify | D-028 |
| Constraints blocked roles; the spec had no Constraint × Role interaction | D-029 |
| The SessionOpen/Close envelope went entirely unused | D-030 |
| Every log entry was a witness attestation; there was no separate raw-event layer | D-031 |
| Validation ran synchronously on receipt | D-032 |

Under this version's §4.9, the run's constraint-reopen path — a sub-agent verdict reopening a Constraint directly — is non-conformant until a validator countersigns. That is the intended effect of the rule.

### 27.4 What It Is Not

It is not a controlled study. There was no comparison condition, no ground truth withheld from participants, no pre-registered hypothesis.

It has had no external adversarial review. No party hostile to the protocol's aims has attempted to break it.

It is one run, between two instances, in one afternoon, with placeholder cryptography.

It demonstrates that the mechanisms operate. It does not demonstrate that they detect what they are designed to detect.

### 27.5 Committed Validation Design

CP commits to a controlled evaluation modeled on the methodology the Mycelium coordination layer published for its own A/B study — same agents, personas, and goals under two conditions; a benchmark withheld from the agents; results scored against it — with one change that makes the design CP's own:

**Independent variable.** Interactions conducted with full CP witnessing, attestation, and open contestation, versus the same interactions conducted without.

**Dependent variable.** *Detection rate of manufactured consensus.* A subset of scenarios seeds a coordinated bloc — participants instructed to converge on a predetermined position while presenting as independent. The measure is whether a pattern-detector (§21.3) operating over the CP record identifies the bloc, at what false-positive rate against honest convergence, and how many interactions it requires.

This is the measurement no coordination-layer study can make, because coordination layers have no adversary model. It is also the measurement on which §0.3's fourth and fifth statements depend.

**Secondary measures.** Token and latency overhead of witnessing; time-to-detection; whether `deliberation_quality` (§11.6) computed over witnessed inputs separates seeded blocs from honest agreement better than the same metric over self-reported inputs.

**Design constraints.** Pre-registered. Scenarios, seeding protocol, and detector published before the run. Raw CP records published afterward under Apache-2.0 so that anyone can re-run the detector or a different one.

### 27.6 Venue and Invitation

The AGNTCY Federation Testbed is a candidate venue: it provides multi-organization agent infrastructure with the Directory's referrer mechanism already in place (§4.2). Any party may run the design above, or an improved one, and submit results through Appendix E. Independent replication is worth more than the DAX Foundation's own run and is explicitly invited.

### 27.7 What Would Count

Evidence sufficient to move this specification from Working Draft toward a stable release would include: the pre-registered study in §27.5, run and published; at least one independent replication; and at least one adversarial review by a party attempting to manufacture consensus that the detector fails to catch — with the results, either way, in the record.

Until then, every claim in this document about what CP *makes possible* stands; every claim about what CP *achieves* is a hypothesis.

---

## APPENDIX A — ARTIFACT KIND SUMMARY

Every CP-native kind is a VC type in the CP JSON-LD context. Referrer types apply where the kind attaches to a target (§4.2).

| Kind | Tier | § | Referrer type | Attaches to |
|---|---|---|---|---|
| Event | 1 | 8 | — (target of `cp.witness.v1`) | — |
| ContextOpen / ContextClose | 1 | 9.4 | — | — |
| WitnessAttestation | 1 | 10.3 | `cp.witness.v1` | participant-signed statement |
| IndependenceAssertion | 2 | 10.4 | — | — |
| Validator | 1 | 10.7 | — | — |
| AdherenceClaim | 1 | 11.1 | `cp.adherence.v1` | WitnessAttestation |
| Contestation | 2 | 12.1 | `cp.contestation.v1` | any artifact |
| Response | 2 | 12.4 | `cp.response.v1` | Contestation |
| Adjudication | 2 | 12.6 | `cp.adjudication.v1` | Contestation |
| Tombstone | 2 | 5.4 | `cp.tombstone.v1` | any artifact |
| Patch | 2 | 5.5 | `cp.patch.v1` | any artifact |
| Concept | 2 | 5.1 | — | — |
| ConceptCollection | 2 | 5.2 | — | — |
| Relationship | 2 | 15 | `cp.relationship.v1` | `from` artifact |
| RoleGrant | 2 | 5.3 | — (VC with status list) | — |
| SubAgentArtifact | 2 | 5.7 | — (target of `artifact.sub-agent`) | — |
| Constraint | 2 | 5.8 | — | — |
| ConstraintDecl | 1 | 20.3 | — | — |
| Policy | 1 | 20.4 | — | — |
| Snapshot | 1 | 17 | `cp.snapshot.v1` | TS tree head(s) |
| RotationEntry | 1 | 7.5 | — | — |
| Compiler | 1 | 18.3 | — | — |
| ExtensionDecl | 1 | 23.1 | — | — |
| PrimitivesRegistry | 1 | 20.1 | — | — |
| CompromiseDeclaration | 1 | 20.2 | — | — |

**Fields carried on Event (not kinds):** `positions[]` with `stance`, `revision_cause`, `deferred_to`, `prior`, `posterior`, `addresses[]` (§8.3).

**Anticipated extension kinds (illustrative, non-normative):** `attribution:Charter`, `attribution:RoyaltyPolicy`, `attribution:AttributionGrant`, `credit:Ledger`, `education:Rubric`, `education:LearnerConceptState`, `education:LearningPath`, `governance:Precedent`, `portability:Bundle`, `media:MediaRef`.

---

## APPENDIX B — NORMATIVE RULES INDEX

| § | Rule |
|---|---|
| 1.1–1.12 | Twelve architectural commitments |
| 4.1.2 | TS MUST append-only, non-equivocate, receipt every registration, publish tree heads |
| 4.1.4 | Every event MUST carry `previous_hash` |
| 4.1.5 | TS MUST refuse statements narrower than its scope; widening is re-registration |
| 4.1.6 | Registration policy is structural only; TS MUST NOT evaluate content |
| 4.2.2 | Referrers MUST NOT alter target; any identity MAY attach; referrers are artifacts |
| 4.3.1 | Every artifact is a VC 2.0 with Data Integrity proof; `id` is CID |
| 4.3.2 | SCITT payload is JCS-canonical VC incl. proof; PQ inner proof required |
| 4.4, 19 | RFC 8785; CID over credential minus proof |
| 4.5 | Self-certifying DID; `kind`/`chain_role`; chain terminates at principal; cross-refs by DID |
| 4.5.4 | Signatures verify under `assertionMethod` valid at signing time |
| 4.6.1 | ≥1 PQ proof: `mldsa44-jcs-2024` or `slhdsa128-jcs-2024` |
| 4.6.2 | Hybrid AND until 2030-01-01; classical-only never accepted |
| 4.6.3 | Anchor signatures MUST bind anchor key via `genesis_ref` |
| 4.7 | Witness ≠ participant; transitional MUST be declared |
| 4.8 | Validator ≠ witness |
| 4.9 | Only validator DIDs issue AdherenceClaims; sub-agent verdicts are evidence |
| 4.10 | Every entry participant-signed + witness-receipted |
| 4.11 | Receipt every registration; filter republication only |
| 4.12 | Scope MUST NOT be narrowed |
| 4.13 | Tombstone MUST NOT remove from evaluation-mode view |
| 4.14, 21.1 | Seven walker rules |
| 4.15 | Indexes non-authoritative |
| 4.16 | No PII at org/public; detached payload at private |
| 4.17 | `fork_of` on forkable kinds |
| 5.3 | RoleGrant issuance MUST check `blocks_roles`; walkers MUST check revocation |
| 5.7 | `model_used`/`provider` MUST be populated when known |
| 5.8 | Constraint MUST reference `under_constraint_decl`; `compliance_failure.evidence_ref` MUST be an AdherenceClaim; blocked roles MUST NOT be granted; refusals MUST be witnessed |
| 5.10 | `revision_cause` REQUIRED on revised/deferred; `deferred_to` REQUIRED on deferred |
| 7.4 | Genesis MUST have one SLH-DSA anchor and `next_anchor_commitment` |
| 7.5.2 | `rotate_anchor` MUST match prior commitment |
| 7.6 | Custody MUST be permanent, content-addressed, multi-local |
| 7.8 | Independent publishing path MUST exist and be documented at equal prominence |
| 7.9 | Friendly name MUST NOT be used for cross-reference or required for resolution |
| 8.2 | `issuer` MUST equal `actor.did`; `scope` on every event |
| 9.3 | Scope, witness, constraints, participants MUST be determinable at context start |
| 9.6 | Cross-org: every event registered in every listed TS |
| 10.2 | Witness MUST NOT decline registration on content grounds |
| 10.8 | AdherenceClaim MUST carry reproducible `evaluation_trace` |
| 10.9 | Inline claim MUST be validator-signed; carries no more authority than others |
| 11.1 | Non-validator issuer → not an AdherenceClaim |
| 11.3 | No claim replaces another; walkers MUST expose the full set |
| 11.6 | `deliberation_quality.inputs_ref` MUST resolve to witnessed records |
| 12.1 | `addresses` MUST be present |
| 12.3 | Walkers MUST NOT hide unengaged Contestations |
| 12.6 | No resolution removes anything |
| 12.7 | Adjudicator ≠ contestant ≠ author |
| 13 | Referrers inherit target scope; walkers MUST declare mode; validators/adjudicators MUST use evaluation mode |
| 15.3 | Third-party relationships MUST be standalone |
| 16 | Revocation MUST be checked first; scope containment |
| 18.3 | Compiler content-addressed; recompilation MUST reproduce; compilation MUST NOT issue claims |
| 23.3 | Walkers MUST report extension conflicts, not resolve them |
| 24.5 | Triggered revision conditions MUST be addressed or their dismissal recorded |

---

## APPENDIX C — BIDIRECTIONAL VOCABULARY MAP **[D-047]**

Pinned to Internet of Cognition `ioc-l9-all-models` **0.0.8** (released 2026-07-17; latest as of 2026-09-11) and `mycelium-io/mycelium` README as read 2026-07-28. The IoC project's own documents use two expansions for SIEP; both are recorded.

**Rule 1 — aligned (same meaning, adopted or shared):**

| CP | IoC / L9 / Mycelium | Note |
|---|---|---|
| Episode (§9.1) | `Episode` | adopted; CP's Thread and Workspace have no L9 analogue |
| Entity (participating) | `Actor` | `Actor` accepted as synonym; CP `Entity` retained for `kind`/`chain_role` semantics |
| `concept_id` `urn:concept:…` (§5.1) | concept URIs `urn:concept:<use_case>:<category>:<specific>` | same namespace |
| `prior` / `posterior` (§5.11) | CIP prior π(a,c,ε) / posterior ρ(a,c,ε) | adopted, per concept |
| `revision_cause` (§5.10) | CIP `revision_cause` | adopted verbatim |
| `deferred_to` (§5.10) | SIEP `deferred_to` | adopted; CP's is witnessed |
| stance (§5.9) | SIEP `BeliefStatus` | adapted: asserted · deferred · retracted · revised · challenged · unresolved |
| `addresses[]` (§8.3, §12.3) | SIEP `addresses_evidence[]`; CIP contingency check | adopted concept |
| `deliberation_quality` (§11.6) | Mycelium genuine-agreement ratio, social-compliance ratio | slot adopted; formulas extension-defined |
| Extension (§6) | subprotocol (SIEP, CIP, SAB, TFP) | corresponding; CP term retained for lens semantics |
| `INTENT` (§6.4) | `Kind.intent` | direct |
| `EFFECT` (§6.4) | `Kind.commit` | near |

**Rule 2 — CP terms with no IoC counterpart (retained):**

witness · Transparency Service role · WitnessAttestation · AdherenceClaim · validator (as distinct role) · Contestation · Adjudication · Response · Tombstone · Patch · Constraint · ConstraintDecl · Policy · compounding floor · lineage · scope (as sovereignty boundary) · principal · delegation chain · Tier 1 / Tier 2 · Snapshot (as floor anchor) · `blocks_roles` · Compiler

**Rule 3 — same or similar words, different meaning (NOT aligned):**

| CP | IoC | Why not aligned |
|---|---|---|
| `verdict` (§11.1) | `posterior` | validator judgment vs participant belief — never merged (§5.11) |
| `scope` (§5.6) | `PolicyLabel {sensitivity, propagation, retention}` | sovereignty boundary vs data-handling classification |
| `Event` (§8) | `Message` | signed, hash-chained, receipted vs unsigned, ID-linked |
| `Constraint` (§5.8) | `PolicyLabel`, GATs | lifecycle-bearing obligation vs data label / runtime filter |
| `WitnessAttestation` | `Actor.attestation` (optional string) | receipted inclusion proof vs opaque field |
| `CHALLENGE` event kind | SIEP `challenge` speech act | post-hoc, any identity vs intra-episode, participant |
| `Snapshot` (§17) | `EpistemicSnapshot` | floor anchor for re-evaluation vs replay-performance checkpoint |
| `Relationship` (§15) | KG `relations[]` | signed, attributed, contestable vs unsigned graph edge |

**IoC subprotocol expansions, as the project publishes them:** SIEP — *Semantic Interoperability and Epistemic Protocol* (repository README) / *Semantic Information Exchange Protocol* (PyPI description, same release); CIP — *Cognition and Interoperability Protocol*; SAB — *Semantic Alignment Broadcast*; TFP — *Team Formation via Polling*; SSTP — *Semantic State Transfer Protocol*.

**L9 schema note (observation, dated):** as of `ioc-l9-all-models` 0.0.8, the `Epistemic` and `Provenance` object definitions carry no fields; their descriptions state fields are to be added. CP's §8.3 positions block and §18.2 provenance block are candidate content for those objects should the IoC project seek alignment.

---

## APPENDIX D — WORKED EXAMPLES (GENERICIZED) **[D-042]**

Four deployments, one substrate. Abstract names. No real topology, no run data.

### D.1 Individual Principal ↔ Companion (private)

Principal **P** (`kind: biological`, `chain_role: principal`) and companion **C** (`kind: nonbiological`, `chain_role: delegate`, `principal: P`, `delegation_chain: [C, P]`). P's organization operates Transparency Service **TS-P** as a distinct identity.

- Context opens with `scope: private`, `witness: TS-P (external)`, `constraints: [{ConstraintDecl-X, Policy-X1, Validator-X1}]`.
- P issues an `INTENT.DECLARE_OBJECTIVE` event; C issues an `EFFECT` event producing a SubAgentArtifact (`role: drafter`, `model_used`, `provider` populated). Each event is P- or C-signed and TS-P-receipted.
- ContextClose with `outcome: converged`, `produced_artifacts: [the SubAgentArtifact]`.
- Validator-X1 (distinct DID) later issues an AdherenceClaim `verdict.value: 0.97`, `floor_state_ref` → a Snapshot of lineage X's floor, trace enumerating inputs.
- TS-P receipts everything; registration is not republished (private scope, §4.11).

### D.2 Companion ↔ Companion, Cross-Organization (org)

Companions **C₁** (principal P₁, org 1) and **C₂** (principal P₂, org 2). Each org runs its own TS: **TS-1**, **TS-2**.

- ContextOpen: `scope: org`, `witness: TS-1`, `additional_witnesses: [TS-2]`, `constraints: [{X, X1, V1}, {X, X2, V2}]` — same ConstraintDecl, two Policies, two validators.
- Every event is registered in both TS-1 and TS-2. Two Receipts per event. Two WitnessAttestations, two `log_index` values, two tree heads.
- C₁ transmits an artifact to C₂; TS-1 receipts `artifact.shared`. V2 (org 2's validator) runs inline (§10.9), issues an AdherenceClaim `mode: inline`, registers it in TS-2, returns `receiver_ack`. TS-1 receipts `peer-validation.received` targeting that claim's CID.
- Later, V1 issues its own async claim against the same attestation. Both claims stand (§11.3). The artifact is in both floors (§11.5).
- If TS-1 and TS-2 ever receipt different CIDs at the same `seq`, walkers surface the divergence (§9.6). Nothing resolves it.

### D.3 Delegate ↔ Delegate, Nested Delegation (org)

C₁ spawns sub-agent **D₁ₐ** (`delegation_chain: [D₁ₐ, C₁, P₁]`); C₂ spawns **D₂ᵦ** (`[D₂ᵦ, C₂, P₂]`). Each spawn is a `delegation.sent` / `delegation.received` pair; each sub-agent's genesis is co-signed by its parent in its SCITT registration.

- C₁ issues D₁ₐ a RoleGrant (VC) with `roles: [deployer]`, `scope: org`. Before issuing, C₁ checks BLOCKING Constraints in scope for `blocks_roles` containing `deployer`.
- Suppose Constraint **K** (`under_constraint_decl: X`, `blocks_roles: [deployer]`) is BLOCKING. Issuance refuses. TS-1 receipts `delegation.refused` referencing K. The attempt is permanent.
- K is later RESOLVED with `evidence_ref`. A compliance-checking sub-agent examines the evidence and produces a SubAgentArtifact scoring 0.25. **This does not reopen K.** V1 consumes it, issues an AdherenceClaim referencing it in `evaluation_trace.inputs`, and *that* claim's CID becomes `compliance_failure.evidence_ref` on a `constraint-lifecycle.reopened` attestation (§4.9, §5.8).
- Any action by D₁ₐ walks D₁ₐ → C₁ → P₁ through co-signed geneses and checkable RoleGrants (§16).

### D.4 Individual ↔ Institutional System (private, transitional witness)

Individual **U** (`biological`, `principal`; DID lazily generated on first contact) and system **S** (`kind: institutional`, `chain_role: delegate`, `principal: Org-S`).

- S is structurally both mediator and recorder. Context declares `witness: S`, `relationship: participant`. No `independence_assertion`. Walkers surface this; downstream treats it as lowest-standing (§10.4).
- Audio is never a CP artifact (§4.16). Transcribed text enters as `OBSERVE.TEXT` events with `actor.did: U`, `actor.confidence` reflecting diarization certainty. Any PII in the text stays at private scope as a detached payload.
- S does not record inferred interior states. An event records what U said; `positions[]` records only what U asserted (§1.9).
- U ends the call. ContextClose `outcome: converged` or `abandoned` — both success states (§9.8).
- Migration path: when an external TS observes S, `relationship` becomes `external` and prior contexts can be retrospectively re-validated by an external validator against the same record (§11.4). Divergence between S's self-attested claims and the external validator's is itself queryable.

---

## APPENDIX E — CONTRIBUTING INPUT TO THIS SPECIFICATION

For collaborators, adjacent projects, and any party who has found a gap.

**E.1 Valid input.** (1) Substrate gaps — a primitive or rule CP lacks that cannot be expressed via existing ones. (2) Structural ambiguities. (3) Failure-mode discoveries. (4) Tier reassignment proposals. (5) Advances on §26 items. (6) Cascade implications of D-001–D-047 in practice. (7) Evidence per §27.

**E.2 Not CP input** (route elsewhere): domain-specific fields (→ extension); rendering preferences (→ walker implementation); operational policies (→ Policy / ConstraintDecl); deployment configuration; performance; positioning.

Test: *does this change what implementations of CP itself must do?*

**E.3 Format.**
```
INPUT TO CP-SPEC v0.5
Source / Author / Date
Category: E.1 (1)–(7)
The Input:            what was discovered, with the record that shows it
The Proposed Change:  section(s), current text, proposed text
Cascade:              which decisions in §25 this amends or reverses
Test Cases:           before / after, at least one
Open Questions
```

**E.4 Handling.** Every input is logged with an ID (`I-nnn`), classified against §25, cascade-analyzed, and decided — accept, defer, or reject — with the decision and reasoning recorded. Rejections name the redirect. Accepted changes trace input → decision → text.

**E.5 What will not happen.** Silent absorption. Centralized authority over what becomes the spec (§24.2). Wholesale rewrites from single inputs. Absorption of operational concerns into the substrate.

**E.6 Test.** Does the change preserve or improve the substrate's capacity for retrospective re-evaluation (§0.3)? Does it preserve multi-level queryability (§0.4)? Does it introduce a required custodian (§1.11)?

---

## APPENDIX F — ADJACENT WORK AND CONDITIONS FOR REVISION **[D-043]**

CP composes with the systems below and competes with none. For each: what it provides, what CP watches, and the condition under which CP stops building and contributes a profile instead (§24.5). Status as observed 2026-09-11 unless stated.

| System | Provides | CP watches | Revision condition |
|---|---|---|---|
| **IETF SCITT** (`draft-ietf-scitt-architecture`, -22, Standards Track) | CP's ledger (§4.1) | statement-type registry; countersignature profiles | If SCITT defines a native *no-claim attestation* or *contestation* statement type, CP §10.3 / §12 become profiles of it |
| **Sigstore Rekor / Trillian** | Reference TS implementation | Rekor v2 sharding; external witness cosignature | — (implementation, not spec) |
| **W3C VC 2.0 / Data Integrity** (Recommendation 2025-05-15; v2.1 planned ~2027) | Envelope (§4.3) | v2.1 scope | If v2.1 changes proof structure, §4.3 updates |
| **W3C `vc-di-quantum-resistant`** (CCG, experimental; `transitions/2026`) | PQ cryptosuites (§4.6) | progression to Recommendation; suite identifier changes; ML-DSA-65 suite | If identifiers change, §20.1 re-registers. If an ML-DSA-65 suite lands, D-016.a is revisited. **CP contributes implementation experience and test vectors.** |
| **IETF COSE PQ** (`draft-ietf-cose-dilithium`) | SCITT wrapper algorithm post-2030 (§4.3.2) | registration of ML-DSA identifiers | Gates the post-2030 COSE requirement |
| **W3C DID / KERI `did:webs`** | Identity method (§7.3) | PQ key codes in CESR | **When `did:webs` supports FIPS 204/205 keys, `did:cp` is deprecated and CP migrates.** |
| **DIF KYA-OS** (Trusted AI Agents WG; formerly MCP-I, donated 2026-03) | Delegation (§7.13) | spec stabilization; treatment of non-human authorizers | If KYA-OS adopts entity-neutral principals, §7.13's delta closes. If it scopes in retrospective re-evaluation, §11 becomes a profile. |
| **W3C PROV-O / PROV-AGENT** (IEEE e-Science 2025) | Predicates (§6.5, §15.4) | PROV-AGENT vocabulary growth | If PROV-AGENT standardizes agent-provenance terms CP defines as subproperties, CP adopts theirs |
| **AGNTCY `dir`** (v1.0.0; `draft-mp-agntcy-ads` at IETF) | Attachment (§4.2); discovery (§2.7) | issue #991 referrer-type enums; ADS draft progression; Federation Testbed | **If referrer types become enumerated, CP registers `cp.*` upstream.** Federation Testbed is the §27.6 candidate venue. |
| **Cisco Outshift IoC — L9 schema / SIEP / CIP / Mycelium** (`ioc-l9-all-models` 0.0.8; `mycelium-io/mycelium`) | Vocabulary (Appendix C); deliberation-quality reference (§11.6); the only shipping consensus-quality measurement | `Epistemic` / `Provenance` objects gaining fields; changes to SIEP/CIP field names; Mycelium metric definitions | If IoC fills `Provenance` with signed, chained, third-party attestation, CP §4.1 / §10 become a profile of L9. If IoC adopts witnessed inputs for its metrics, §11.6 aligns to its `metric_id`s. **CP's §8.3 and §18.2 are offered as candidate content for the empty objects.** |
| **Mesh Memory Protocol** (SYM.BOT; `@sym-bot/sym`) | Independent shipping compounding-with-lineage | per-field accept/reject; ancestor lineage on content-hash keys | If MMP adds witnessing or contestation, compare §11.5 and seek interop |
| **ERC-8004 Trustless Agents** (Draft EIP; mainnet + 20 networks) | Reputation / validation registries | v2 Validation Registry; TEE-based validation | **If v2 adds re-issuable validation against later state, CP §11.3–11.4 narrows to a profile and the whitespace claim in §0.5 is revised.** |
| **Google A2A / AP2** (LF AAIF; AP2 mandates as VCs) | Transport (§2.7); user-intent audit trail precedent | AP2's mandate model | If AP2 mandates gain third-party witnessing, compare §4.10 |
| **Knowledge Provenance Protocol** (DeSci proposal) | Prior art for Attribution/Credit extensions | any implementation | Read before the Attribution extension is specified |

**Standing engagement commitments.** (1) Implement against `vc-di-quantum-resistant`; contribute test vectors. (2) Register `cp.*` referrer types with `agntcy/dir` if enums land. (3) Offer §8.3 / §18.2 to the IoC project for `Epistemic` / `Provenance`. (4) Record the §7.13 delta with the DIF Trusted AI Agents WG. (5) Publish §27.5 pre-registration before the run.

---

## APPENDIX G — GLOSSARY

- **AdherenceClaim** — validator's probabilistic, time-indexed judgment of a witnessed interaction against a ConstraintDecl; accumulates; never replaced. §11.
- **Anchor key** — SLH-DSA key signing rotation-log entries; pre-commits its successor. §7.4–7.5.
- **Chain role** — principal or delegate. §4.5.2.
- **Compounding floor** — artifacts carrying affirmative claims above a lineage's admission threshold; grows monotonically. §11.5.
- **Constraint** — instance-level obligation raised under a ConstraintDecl; lifecycle RAISED→RESOLVED→BLOCKING→REOPENED; may block roles. §5.8.
- **ConstraintDecl** — declared normative frame; what adherence is claimed against. §20.3.
- **Context / Episode / Thread / Workspace** — bounded interaction and its kinds. §9.
- **Contestation** — dispute of any artifact by any identity, at any time. §12.
- **Deferral** — adoption of another participant's position; recorded as `deferred_to`. §5.10.
- **Delegate** — entity acting under a principal; chain terminates at a principal. §1.12.
- **Deliberation quality** — extension-defined metric over witnessed positions, carried on a claim. §11.6.
- **Evaluation mode / default mode** — walker modes; evaluation sees everything. §13.
- **Event** — participant-signed, witness-receipted atomic expression. §8.
- **Fingerprint** — the DID's method-specific identifier; hash of frozen genesis. §7.3.
- **Genesis document** — frozen inception record. §7.4.
- **Lineage** — (ConstraintDecl, Policy, Validator-lineage). §11.5.
- **Policy** — operational interpretation of a ConstraintDecl; sets admission threshold. §20.4.
- **Posterior / prior** — participant's position after / before exchange; never a verdict. §5.11.
- **Pre-rotation** — commitment to the successor anchor's hash before revealing it. §7.5.2.
- **Principal** — entity acting under no delegation; of any kind. §1.12.
- **Promotion rule** — only validator DIDs issue AdherenceClaims; sub-agent verdicts are evidence. §4.9.
- **Receipt** — TS's signed inclusion proof; the witness's countersignature. §4.1.2.
- **Referrer** — typed artifact attached to an immutable target. §4.2.
- **Scope** — declared sovereignty boundary; non-narrowable; selects TS instance. §5.6.
- **Snapshot** — signed binding of TS tree heads and a floor filter; anchors claims in time. §17.
- **Stance** — participant's epistemic position; `unresolved` is first-class. §5.9.
- **SubAgentArtifact** — output of one model/tool invocation in a role. §5.7.
- **Transparency Service (TS)** — SCITT log operator; CP's witness. §4.1.
- **Verdict** — validator's output; probabilistic. §11.2.
- **Witness** — records that participant-signed statements were registered; asserts nothing about content. §10.2.

---

*End of CP-SPEC v0.5.*

*This is a Public Working Draft. Every decision is recorded in §25 and revisable through §24. Every claim about an external project is dated and phrased as observation. Every claim about what CP achieves is, per §27.7, a hypothesis until the record shows otherwise. The specification is contestable using the mechanisms it specifies.*
