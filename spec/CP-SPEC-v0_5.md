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
@@CP_PART_2@@

**Extensions define:** the `role` vocabulary — `api-designer`, `compliance-checker`, `reviewer`, `deployer` — and what each role is permitted to produce.

**Why Tier 2:** every agentic deployment produces these, and the record of *which model, in which role, produced what* is load-bearing for retrospective evaluation; but what the roles are is a domain matter. The first operational run of CP (§27) produced thirteen of these without the specification naming them. This version names them.

---

### 5.8 Constraint **[NEW — D-028, D-029]** and its relation to ConstraintDecl

Two things in prior versions and in operational use shared the name "constraint." This version separates them.

**ConstraintDecl** (§20.3) is a *declared normative frame* — the standard an entity adheres to. DAX is a ConstraintDecl. It is Tier 1: forkable (`fork_of`), lineage-bearing, the thing AdherenceClaims are made against.
@@CP_PART_3@@
| Rotation log | Append-only key event log with pre-rotation | Grows | The entity, via anchor |
| Verification methods | Anchor (SLH-DSA), workhorse (ML-DSA-44), transitional (Ed25519), federated providers | Via log | The entity |
| Services | Resolution paths, friendly names, provider endpoints | Via log | The entity |
| Custody | Permanent content-addressed substrate + any mirrors | Permanent | No one — multi-local |
| Publishing | Writing genesis and log to custody | — | Operator (default) or entity (always open) |
| Friendly name | Human-readable alias, cryptographically verified | Mutable | Registry (convenience only) |

The fingerprint is the frozen root. Everything else evolves around it. No layer gives any operator the power to be a required custodian.

---

## 8. EVENT
@@CP_PART_4@@
- Adjudicators' `engagement_score`s accumulate. A principal whose Contestations are consistently scored unengaged has a record.
- Contestations are themselves contestable. A pattern of bad-faith contestation can be contested as a pattern.

Volume is not filtered. It is made legible, so that whoever looks later can see it for what it was.

### 12.6 Adjudication

An Adjudication resolves a Contestation. It is a `cp.adjudication.v1` referrer on the Contestation.

```
credentialSubject: {
  artifact_kind:         "Adjudication",
@@CP_PART_5@@
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

@@CP_PART_6@@
