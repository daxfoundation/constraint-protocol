# CP-SPEC v0.5 — Decision Log (Phase A Deliverable)

**Date:** 2026-09-10
**Status:** Phase A complete. 47 decisions ratified. Phase B (verification) pending.
**Scope:** This log carries every architectural decision from v0.4 reconciliation (D-001–D-012), the v0.4.1 identity point release (D-013), and the v0.5 upgrade (D-014–D-047). It is the traceability record: every primitive in CP-SPEC v0.5 resolves to a numbered decision here.

**Reading rule:** D-001–D-013 are summarized; their full rationale lives in CP-SPEC v0.4 §25 and the v0.4.1 Change Document. D-014–D-047 are recorded in full. Where a v0.5 decision amends or reverses an earlier one, both are cross-referenced.

---

## 0. ARCHITECTURAL COMMITMENTS (LOCKED, CARRIED FORWARD)

- **North Star** — the substrate's purpose is not to prevent harm at T₀ but to preserve fidelity sufficient for retrospective re-evaluation at T₁..Tₙ. (v0.4 §0.3; grows into the threat model per D-045.)
- **Multi-Level Queryability** — surface render → semantic traversal → pattern detection → retrospective re-evaluation; no level privileged. (v0.4 §0.4.)
- **Two-Tier Core** — Tier 1 structural-rigid (meaning IS structure); Tier 2 skeleton in CP, semantics in extensions. (D-003.)
- **Entity-Neutral Principal** — every delegation chain terminates at a principal: an entity not itself acting under delegation, of unrestricted kind. (D-014; formalizes Δ-39.)
- **Adopt / Substitute / Build discipline** — if a mature standard exists, CP adopts or profiles it; CP builds only what is uncovered. (Governs D-015–D-024.)

---

## 1. v0.4 RECONCILIATION — D-001 THROUGH D-012 (SUMMARY)

| ID | Decision | Status in v0.5 |
|---|---|---|
| D-001 | Path C — per-primitive reconciliation, no baseline doc | Stands |
| D-002 | Three artifacts: CP substrate / extensions / master strategy | Stands |
| D-003 | R4-composite: two-tier core + DAG extension composition (lens) | Stands |
| D-004 | AdherenceClaim distinct from WitnessAttestation; .a probabilistic verdict canonical; .b floor time-indexed; .c Snapshot Tier 1 | Stands; D-004.c mechanism amended by D-019 |
| D-005 | Cross-org witnesses independent | Stands |
| D-006 | Tombstone Tier 2 scope-dependent, never removes from queryability; .a scope non-narrowable; .b Contestation open to any DID; .c Adjudication Tier 2; .d IMPORTS_REASONING structural; .e constraints govern adherence not epistemic access | Stands; D-006.b gains engagement checking (D-037) |
| D-007 | Namespaced artifact kinds; CP-native bare; promotion path | Stands |
| D-008 | Walker contract Position β — six substrate-integrity rules in CP | Stands |
| D-009 | Envelope Position γ — CP-native + normative VC transform; .a quantum-grade ID normative; .b Primitives Registry reinforced; .c multi-sig via verification methods | **Conditionally reversed by D-016** (⚑ B) |
| D-010 | Patch as CP-native Tier 2 kind | Stands |
| D-011 | Relationship separate first-class Tier 2; self-asserted may inline; third-party MUST be standalone | Stands; predicate vocabulary amended by D-017 |
| D-012 | Structured event-kind family; conservative top-level; namespaced sub-kinds | Stands; pattern reused by D-025, D-036 |

## 2. v0.4.1 IDENTITY POINT RELEASE — D-013 (SUMMARY)

| ID | Decision | Status in v0.5 |
|---|---|---|
| D-013 | Identity custody: frozen genesis on permanent content-addressed substrate (Arweave); fingerprint = hash of frozen genesis only; append-only rotation log; operator pays and publishes but is never required custodian (§1.11); independent publishing path always open; friendly-name registry is convenience, not root | Stands; vocabulary re-expressed in DID/VC terms by D-021 |

---

## 3. v0.5 UPGRADE — D-014 THROUGH D-047 (FULL)

### 3.0 Foundational correction

**D-014 · Entity-neutral principal**
- **Decision:** Every delegation chain MUST terminate at a *principal* — an entity not itself acting under delegation. Principal kind is unrestricted. "Agent" is a chain role (delegate), not an entity kind.
- **Rationale:** CP-SPEC text already said "non-agent entity"; conversational and comparative-analysis language had drifted to "human." Δ-39 (no special treatment for AGI, Tier 1) already committed to neutrality. Every other surveyed system (KYA-OS, AP2, ERC-8004) binds accountability to a human or legal person; CP records accountability in its own terms — whose anchor key, whose claims accumulate, who is contested — independent of legal personhood. This is future-proof and opens a present-day gap the spec must name: substrate accountability and legal accountability are different things; CP guarantees only the first. "Humanity" lives in the DAX constraint (§1.4 layering), not in the substrate.
- **Cascades:** (i) Schema fix — split `kind: human|agent|system` into `kind: biological|nonbiological|institutional|composite` and `chain_role: principal|delegate`. (ii) D-022 becomes a profile, not adoption. (iii) Wording pass on §1.9 Sacred Boundary and §1.10 Episodicity — they apply to any entity's expression. (iv) Comparative analysis §5.10 and decoder "Humans as principals" corrected.
- **Touches:** §4.5, §5.1.4, §7.3, §9, §1.9, §1.10, Appendix D, Δ-2, Δ-39.

### 3.1 Group 1 — Substitutions

**D-015 · Ledger substrate → SCITT / Rekor profile**
- **Decision:** Re-express the hash-chained append-only ledger (§4.1–4.3) as IETF SCITT Signed Statements persisted on a Rekor/Trillian-class transparency log. Transparency Service instances are **scoped per CP scope** (private / org / public). Witness remains a first-class CP entity distinct from the log operator.
- **Rationale:** SCITT is the IETF standard for exactly this — Signed Statements to an append-only log with hash-referenced detached payloads. Rekor runs the pattern at internet scale with inclusion proofs, split-view protection, and external witnessing (tree heads anchored to an Ethereum L2 — direct precedent for §1.11 anti-chokepoint custody). Building it bespoke is the largest avoidable cost in the project. A public log cannot hold private-scope records, so scoped instances are forced by §4.12, not optional. This is a *profile*: SCITT supplies the format and log; CP supplies the witness-as-entity role SCITT lacks.
- **Cascades:** Tombstone becomes a statement, never a deletion (§4.13 preserved). Snapshot mechanism → D-019. Referrers (D-024) may themselves be SCITT statements. Event/attestation collapse → D-031.
- **Touches:** §4.1, §4.2, §4.3, §4.13, §17, Δ-4, Δ-28. Re-expresses; reverses nothing.
- **⚑ B:** SCITT statement model can carry a no-adherence-claim attestation type; scoped-instance deployment pattern.

**D-016 · Envelope — reopens D-009** ⚑ B
- **Decision (conditional):** Move to W3C VC 2.0 native envelope **only if** Phase B confirms a usable path for ML-DSA / SLH-DSA cryptosuites under VC Data Integrity. Otherwise retain Position γ (CP-native + deterministic VC transform) and register a CP post-quantum cryptosuite with W3C as a contribution.
- **Rationale:** D-009 chose γ because the VC ecosystem's post-quantum story was immature. VC 2.0 reaching Recommendation (15 May 2025) does not by itself change that — the standardized Data Integrity cryptosuites are EdDSA and ECDSA. Going native without PQ suites would reintroduce the coupling D-009 was built to avoid.
- **Cascades:** If yes — D-009 reversed; §10, §11, §19, §20 re-expressed in VC terms; Primitives Registry maps to cryptosuite identifiers. If no — D-009 stands; §20 gains a "contributed cryptosuite" entry.
- **Touches:** D-009, §10, §11, §19, §20.

**D-017 · Relationship predicates → PROV-O / PROV-AGENT — amends D-011**
- **Decision:** Adopt W3C PROV-O (extended per PROV-AGENT) as the predicate vocabulary for Relationship. PROV-O predicates live *inside* CP's signed Relationship wrapper. D-011's property — third-party relationships are standalone, signed, independently contestable — is unchanged.
- **Rationale:** PROV-DM/PROV-O has modelled attribution and derivation since 2013; PROV-AGENT (IEEE e-Science 2025) already extends it via MCP for agent prompts, responses and decisions, with working code. PROV-O is a vocabulary, not a signing model — it fills the predicate slot, not the artifact.
- **Cascades:** §6.5 baseline predicates map to PROV terms (`DERIVED_FROM` → `prov:wasDerivedFrom`, etc.). `DEFERS_TO` (D-034) needs a PROV mapping — ⚑ B under D-034.
- **Touches:** §15, §6.5, D-011, Δ-58.

**D-018 · RoleGrant → VC-based delegation**
- **Decision:** RoleGrant is expressed as a Verifiable Credential issued by the granting principal (KYA-OS / AP2-mandate shape). Revocation via Bitstring Status List. Issuer is any principal (D-014). Issuance MUST check `blocks_roles` on BLOCKING constraints in scope (D-029).
- **Rationale:** Scoped, revocable, auditable authority as a credential is exactly what VC provides, with a standardized revocation mechanism.
- **Touches:** §16, §5.3, Δ-1, D-014, D-029.

**D-019 · Snapshot mechanism — amends D-004.c**
- **Decision:** Snapshot is a signed statement binding `{tree_head_ref, filter_ref, signer, ts}`. Its Tier 1 role as AdherenceClaim's temporal anchor (D-004.c) is unchanged; only the mechanism changes.
- **Rationale:** A tree head snapshots the *log*; the compounding floor is a *validated subset*. Neither alone is the object D-004.c needs. The bridge is a signed statement binding the two.
- **Touches:** §17.1, §11.4, D-004.c, D-015.

**D-020 · Validator executable spec → standard policy language**
- **Decision:** `executable_spec` SHOULD be expressed in a standard policy language — Cedar preferred, OPA/Rego accepted. Free-form remains permitted. The content-addressed executable requirement (§10.7) is unchanged.
- **Rationale:** The forkable-constraint-with-lineage idea stays CP's; the policy language beneath is solved (AWS AgentCore already compiles to Cedar). MUST would over-constrain probabilistic and ML validators that don't fit a policy language.
- **Touches:** §10.7, §5 ConstraintDecl.

### 3.2 Group 2 — Adoptions

**D-021 · Identity substrate → W3C DID + VC 2.0 + Data Integrity** ⚑ B
- **Decision:** Express §7 verbatim in DID/VC terms: fingerprint as a self-certifying identifier (did:key-class / KERI SAID-class); genesis + rotation log as the DID document lifecycle; provider array as verification methods and service endpoints. §1.11, frozen-genesis/growing-log, and Arweave custody are unchanged — they are policy on top of DID.
- **Rationale:** DID and seven VC 2.0 documents are Recommendations; IANA registered `urn:said` (KERI) in 2026. Nothing in §7's structure is novel except custody policy. Standard vocabulary makes every CP identity resolvable by every DID resolver.
- **Touches:** §4.5, §7.2–7.5, §7.10, D-009.a, D-013.
- **⚑ B:** did:key multicodec support for ML-DSA / SLH-DSA public keys (same root question as D-016).

**D-022 · Delegation → DIF KYA-OS profile** ⚑ B
- **Decision:** Align CP's delegation chain with DIF KYA-OS (formerly MCP-I) as a *profile*. Adopt its four questions — who is the agent, who authorized it, what may it do, what scope. Generalize "human authorizer" to "principal of any kind" (D-014) and state the delta explicitly.
- **Rationale:** Actively developed at DIF, VC-based, answers CP's questions. The single divergence is CP's contribution, not grounds to diverge wholesale.
- **Touches:** §5.1.4, §9, D-014, D-018.
- **⚑ B:** KYA-OS current spec state at DIF.

**D-023 · Transport, discovery, coordination — out of scope; composition named**
- **Decision:** Declare transport (MCP, A2A, SLIM), discovery (OASF, ADS), and coordination (L9-class protocols) out of CP scope. New §2.x "Composition Surfaces": CP records interactions over any transport; CP entities publish OASF records to ADS; CP witnesses L9-class coordination without participating. New §26 item: coordination unaddressed by design.
- **Rationale:** CP was never in these businesses. Naming the seams prevents the "CP competes with X" misreading and gives implementers integration points.
- **Touches:** §2 (new), §26 (new), Δ-13 partially resolved.

**D-024 · Attachment model → `agntcy/dir` RecordReferrer pattern** ⚑ B
- **Decision:** Adopt RecordReferrer — typed, content-addressed objects attached to an immutable record without modifying it — as the mechanism by which WitnessAttestation, AdherenceClaim, Contestation, Adjudication, Tombstone and Patch attach to targets. CP defines referrer types in its namespace (`cp.witness.v1`, `cp.adherence.v1`, `cp.contestation.v1`, …).
- **Rationale:** Shipping, maintained, Go/Python/JS SDKs, Sigstore already wired in. It is the append-only-attachment plumbing for D-004 (accumulating claims), D-006.b (open contestation), D-010 (Patch), D-011 (third-party Relationship) in one move. CP defines types, not plumbing.
- **Touches:** §4.2, §5.4–5.5, §11.3, §12, §15.3, Appendix A, D-015.
- **⚑ B:** (i) referrer type registration mechanism; (ii) **can a party other than the record owner attach a referrer?** If not, D-006.b fails and D-024 becomes "borrow the shape, not the server."

### 3.3 Group 3 — Operational findings (Skippy↔CTO cross-node run, 2026-05-04)

**D-025 · WitnessAttestation polymorphism**
- **Decision:** One WitnessAttestation kind with a mandatory `claim_type` discriminator. CP defines a conservative top-level family — `delegation · artifact · constraint-lifecycle · peer-validation` — with sub-types namespaced per D-012. Under D-024, each `claim_type` is a referrer subtype under `cp.witness.v1`.
- **Rationale:** The witness does one thing — "I observed this." What varies is what was observed. One kind keeps the walker contract to a single verification path and matches what the implementation converged on (8+ claim types observed). Eight kinds would fragment the witness role.
- **Touches:** §10.2, §8.1, D-012, Appendix A.

**D-026 · SubAgentArtifact**
- **Decision:** New Tier 2 CP-native kind. Shape: `role` (extension-interpreted string), `produced_via {method, model_used, provider}`, output or output-ref, `tokens`, `latency_ms`, standard provenance. A sub-agent is a delegate; its chain terminates at a principal (D-014).
- **Rationale:** The unit of nonbiological work; every LLM invocation in the run produced one. Cross-model attestability is North-Star load-bearing — a future validator asking whether one model's outputs diverged systematically from another's needs this recorded.
- **Touches:** §5 (new), Appendix A, D-014.

**D-027 · The promotion rule**
- **Decision:** A SubAgentArtifact carrying a verdict is *evidence*, never directly an AdherenceClaim. It becomes an AdherenceClaim only when a validator identity (distinct DID, §4.8) signs an AdherenceClaim referencing it as `evaluation_trace` input. **Tier 1: no artifact is an AdherenceClaim unless signed by a validator DID.**
- **Rationale:** A compliance-checker sub-agent is one party's delegate; its output is that party's evidence, not independent judgment. Letting it count directly lets a party self-certify and collapses D-004. The run's inconsistency — proper AdherenceClaim only cross-org, in-loop compliance routed through SubAgentArtifact → WitnessAttestation — was the symptom. This does not ban the pattern; a validator countersigns.
- **Consequence:** the cto01 vault's constraint-reopen events are non-conforming under v0.5 until a validator countersign step is added.
- **Touches:** §4.8, §10.5–10.8, §11.1, D-004, D-026.

**D-028 · Constraint lifecycle**
- **Decision:** Constraint is a first-class artifact with lifecycle `RAISED → RESOLVED → BLOCKING → REOPENED` and a `compliance_failure {verdict, score, reopened_ts, evidence_ref}` block. Transitions are append-only WitnessAttestations (`claim_type: constraint-lifecycle`). Current state is derived by walkers, never stored authoritatively (§4.15). `compliance_failure.evidence_ref` points at the AdherenceClaim that triggered reopening (D-027).
- **Rationale:** The run showed RAISED→RESOLVED→REOPENED in minutes — the North Star at short timescale — and the spec had no lifecycle. Events plus derived state keeps §1.2 intact.
- **Touches:** §5 ConstraintDecl, §4.15, §11, D-025, D-027.

**D-029 · Role-binding — `blocks_roles`**
- **Decision:** A Constraint MAY carry `blocks_roles[]` (extension-defined role strings). While BLOCKING, those roles MUST NOT be spawned or granted within the constraint's scope. A refused spawn produces a WitnessAttestation (`claim_type: delegation-refused`).
- **Rationale:** This is what made the run work — three bypass attempts, all refused, all permanently recorded. It is T₀ gating, but *declared* gating: the constraint says what it blocks; the substrate doesn't decide. §0.3 holds, and refusals become evidence.
- **Touches:** §5.3, §5 ConstraintDecl, D-028, D-018.

**D-030 · Session envelope optional**
- **Decision:** SessionOpen / SessionMessage / SessionClose are optional. Minimal Context = `context_id` + first event (`previous_hash: null`) + per-context hash chain. SessionOpen/Close remain the *recommended* form. Tier 1 unchanged: scope and witness MUST be determinable for every context — from SessionOpen or from the first event's fields.
- **Rationale:** The run ran without the envelope; the hash chain carries integrity. §4.12 requires scope fixed at context start, so the first event carries it if SessionOpen doesn't.
- **Touches:** §9.1, §9.3, §9.5, §4.12, Δ-7.

**D-031 · Witness-is-the-event-stream** ⚑ B
- **Decision:** Every log entry *is* a WitnessAttestation; there is no separate raw-event layer. **Tier 1 rule:** the attested body MUST include the participant's own signature over the event content. Two signatures per entry — participant (authorship) + witness (observation).
- **Rationale:** The raw-event/attestation split was conceptual, never structural. Collapsing it matches SCITT exactly — a Signed Statement countersigned by the Transparency Service (D-015). The dual-signature rule preserves "witness records, does not author."
- **Touches:** §8, §10.2, §4.7, D-015, D-025.
- **⚑ B:** SCITT countersignature model supports two distinct verifiable signatures.

**D-032 · Inline synchronous validation**
- **Decision:** Inline validation — receiver's validator runs on receipt, returns `receiver_ack.validator_score`, sender records it — is a permitted mode. An inline claim is a proper AdherenceClaim (validator-DID-signed, D-027) marked `mode: inline` with its own `floor_state_ref`. It carries no more authority than any other claim; later claims stack beside it (§11.3).
- **Rationale:** How cross-org worked in the run; immediate signal is useful. The risk was inline claims being treated as final. The marker plus §11.3 keeps them as the first of many.
- **Touches:** §10.5, §11.1, §11.3, §9.4, D-004, D-027.

### 3.4 Group 4 — Deliberation and influence recording (borrowed from Outshift IoC / Mycelium)

**Framing rule for all of Group 4:** CP defines the recording slot; extensions define the metric; what CP adds is that the inputs are witnessed (D-031 dual-signed). Outshift's versions are self-reported; a bloc can lie about its own deferrals. CP's cannot.

**D-033 · `deliberation_quality` on AdherenceClaim** ⚑ B
- **Decision:** Optional Tier 2 block `deliberation_quality {metric_id, value, inputs_ref}`. `inputs_ref` MUST resolve to witnessed records. Metric is extension-defined; SCR and GAR named as the reference example. The `W = (1−SCR)×GAR` formula is **not** written into the spec — unverified in primary sources.
- **Rationale:** The floor currently compounds capitulation as fast as reasoning. A future validator needs how robustly a conclusion was reached, not just what it was.
- **Touches:** §11.1, §11.5, §5, D-004, D-031.

**D-034 · Deferral and influence recording** ⚑ B
- **Decision:** `deferred_to` (principal-ref or null) and `revision_cause` on position-bearing artifacts; `DEFERS_TO` added to baseline Relationship predicates. `null` = position held on own evaluation; non-null = adopted from a named participant. Lives in the witnessed event body.
- **Rationale:** The Sybil substrate. A coordinated bloc's fake independence has a signature in the deferral graph — concentration toward one node, influence flowing one way — visible only across many interactions. Outshift built the field and can't trust it. CP can, for exactly the reason CP exists.
- **Touches:** §8, §15, §6.5, D-011, D-017, D-031.
- **⚑ B:** PROV-O `wasInfluencedBy` / `wasInformedBy` as mapping target.

**D-035 · Immutable prior**
- **Decision:** Optional `prior_ref` at context start (SessionOpen or first event, D-030); `prior` / `posterior` on position-bearing artifacts. Prior is declared before peer contact, hash-referenced, witnessed, immutable for the context. Posterior is the participant's current position. **Both are distinct from the validator's `verdict`** — participant position and validator judgment never merge.
- **Rationale:** Without a baseline, influence is unmeasurable. For a substrate that exists to judge whether interactions were legitimate, that is a blind spot.
- **Touches:** §9.1, §8, §11, D-030, D-034.

**D-036 · Revision-cause taxonomy**
- **Decision:** `grounded_argument | social_compliance | semantic_memory | new_evidence | repair_resolution` as a CP-suggested, extension-extensible enum for `revision_cause`. Attributed to Outshift.
- **Touches:** §6.4–6.5, D-012, D-034.

**D-037 · Engagement checking on Contestation**
- **Decision:** `addresses[]` (hashes of the specific claims engaged) and optional `engagement_verified` / `engagement_score` on Contestation, filled by adjudicator or contested party. A Contestation with empty `addresses[]` is structurally a parallel assertion, not a reply; walkers MAY render it as such.
- **Rationale:** §12.4 had no mechanism to test whether a contestation engages its target. This is CIP's contingency check applied to CP's dispute layer, and the structural defence against contestation-spam under §1.7.
- **Touches:** §12.1, §12.4, §12.7, D-006.b, D-006.d.

**D-038 · Participant stance vocabulary**
- **Decision:** `asserted | deferred | retracted | revised | challenged | unresolved` as a Tier 2 stance vocabulary — a participant's epistemic position, distinct from artifact kinds. `retracted` may trigger Tombstone, `revised` Patch, `challenged` Contestation — but a stance does not require an artifact. **`unresolved` is first-class:** structured impasse is a valid, recordable outcome.
- **Rationale:** CP could record a shift only by minting an artifact and had no way to record honest failure to converge. Aligns with §1.10 — exit is a success state.
- **Touches:** §5, §8, §13, §1.10, D-006, D-010.

**D-039 · Cross-episode stores — stays in open research**
- **Decision:** Per-participant belief history and per-pair directional interaction models remain in §26.1. The *inputs* are now specified (D-033–D-036); the aggregation is not. §26.1 amended to say so.
- **Rationale:** A store is a derived index — §4.15, non-authoritative and regenerable. Making it a primitive would put intelligence into the substrate (§3). CP guarantees the inputs exist, are witnessed, and are queryable across lineages (walker rule 6). Aggregation is a validator's job.
- **Touches:** §26.1, §4.15, §21.

### 3.5 Group 5 — Publication posture

**D-040 · Version** — v0.5, "Public Working Draft." One operational run, no external adversarial review; 1.0 would overclaim.

**D-041 · License** — Apache-2.0 for schemas, JSON, reference code, test vectors (patent grant); CC-BY-4.0 for specification prose (permits the forks §24 requires).

**D-042 · Appendix D — genericize**
- **Decision:** Keep four levels — individual principal ↔ companion; companion ↔ companion cross-org; delegate ↔ delegate; individual ↔ institutional system — with abstract names only. No real names, topology, or run data.
- **Touches:** Appendix D, D-014, D-047.

**D-043 · Watch list and conditions for revision** ⚑ B
- **Decision:** New appendix "Adjacent Work and Conditions for Revision." Watch: Cisco Outshift IoC / L9 / Mycelium · Mesh Memory Protocol · ERC-8004 v2 · IETF SCITT · DIF Trusted AI Agents WG (KYA-OS) · W3C VC 2.1 · PROV-AGENT. Per entry: what they have, what CP watches for, and the condition that moves CP from *build* to *contribute a profile*. Posture: CP composes with these; it does not compete.
- **Known revision triggers:** SCITT adding a native contestation or no-claim-attestation statement type; ERC-8004 v2 adding re-issuable validation against later state; DIF Trusted AI Agents WG scoping in retrospective re-evaluation.
- **Touches:** new appendix, §24, §26.

**D-044 · Third-party claims policy (publication rule P-1)** ⚑ B
- **Decision:** Every claim about a named external project is re-verified against primary source in Phase B, dated in the text ("as of <date>, schema v<x>"), and phrased as observation, not characterization. Specifically: re-check `"Provenance": {}` / `"Epistemic": {}` against current `l9_schema.json`; drop or mark unverified MPC and the W formula; correct SIEP/CIP/SAB expansions to current repo wording.
- **Rationale:** CP's pitch is fidelity; the document must model it.

**D-045 · Threat-model framing**
- **Decision:** §0.3 grows into the threat model. (1) CP makes meaning-formulation attributable, witnessed, and re-judgeable — never "prevents." (2) The threat is **capability asymmetry plus opacity**, not nonbiological-ness; a witnessed, attributable principal of any kind under a declared constraint is what CP wants to exist (reconciles D-014). (3) Verification is structural — who, what, when, witnessed by whom, under which constraint — never semantic truth (§0.2; guards FM-DO). (4) The gradient shifts toward **legibility, not goodness** — the constraint you serve becomes a matter of record; values live in the constraint (§1.4). (5) The gradient depends on re-evaluation actually occurring — CP provides capacity, not exercise; §26.1 and §26.4 named as dependencies. §1.9 Sacred Boundary grows from a data-capture rule into the seed of the threat model. "Prevent," "AGI," "ASI" appear nowhere as claims.
- **Touches:** §0.2, §0.3, §1.4, §1.9, §26.

**D-046 · Validation posture**
- **Decision:** New section "Evidence and Validation." (a) What exists: one cross-node run (2026-05-04) demonstrating refusal under a declared constraint, permanent recording of three bypass attempts, and constraint reopening on a compliance verdict. (b) What it is not: a controlled study; no external adversarial review has occurred. (c) Committed design: A/B modeled on Mycelium's — same participants and goals, with and without witnessing + attestation + contestation, ground truth withheld — dependent variable *detection of manufactured consensus*. (d) Invitation per Appendix E.
- **Touches:** new section, §26, Appendix E.

**D-047 · Vocabulary alignment with IoC / Mycelium** ⚑ B
- **Decision:** Three rules. **(1) Align where semantics match** — prior, posterior, revision_cause, stance, deferred_to (Group 4); "Episode" as preferred name for a bounded Context; "Actor" as recognized synonym for participating Entity; concept URIs; event-kind taxonomies mapped. **(2) Keep CP terms where CP has a concept they lack** — witness, constraint, principal, contestation, adjudication, compounding floor, scope, Tier 1/2, AdherenceClaim, Tombstone, Patch, lineage. **(3) Never adopt a term whose meaning diverges** — `posterior` ≠ `verdict`; `PolicyLabel` ≠ `scope`; L9 `Message` ≠ CP `Event`. Publish a bidirectional vocabulary map as an appendix, pinned to their schema version and dated. "Extension" stays but maps to "subprotocol."
- **Rationale:** Alignment buys interop and makes composition concrete. They are at v0.0.6 and have renamed twice; pinning to a version and holding load-bearing terms prevents churn and keeps the contribution legible.
- **Touches:** Appendix C (becomes bidirectional), §6.4, §9, D-012, D-014, D-035, Appendix D.

---

## 4. PHASE B — VERIFICATION LIST

Eleven items. Each resolves a conditional or validates a claim before Phase C writes it.

| # | Decision | What to verify | Consequence if fails |
|---|---|---|---|
| B-1 | D-016, D-021 | ML-DSA / SLH-DSA cryptosuites for VC Data Integrity; did:key multicodec for PQ keys | Keep Position γ; register CP cryptosuite as W3C contribution |
| B-2 | D-024(ii) | Can a non-owner attach a RecordReferrer in `agntcy/dir`? | D-024 → "borrow the shape, not the server"; open contestation needs own attachment service |
| B-3 | D-044 | Current `l9_schema.json` — are `Epistemic` and `Provenance` still `{}`? | Rewrite the finding as historical, dated; or drop |
| B-4 | D-015 | SCITT statement model supports a no-adherence-claim attestation type; scoped-instance pattern | Profile gains a CP-defined statement type; contribute to SCITT WG |
| B-5 | D-031 | SCITT countersignature yields two distinct verifiable signatures | Fall back to CP-native dual-signature envelope |
| B-6 | D-022 | KYA-OS current spec state at DIF | Profile against whatever is current; date it |
| B-7 | D-024(i) | Referrer type registration mechanism | Define CP namespace registration |
| B-8 | D-033 | SCR / GAR current definitions in Mycelium source; W formula presence | Cite exactly; drop W if absent |
| B-9 | D-034 | PROV-O mapping for `DEFERS_TO` | Define CP predicate with PROV superproperty |
| B-10 | D-043 | Current status of each watched project | Update appendix entries |
| B-11 | D-047 | Current L9 and Mycelium vocabulary | Pin map to current schema version |

**Order:** B-1, B-2, B-3, B-4 first — each can reverse a decision or damage credibility. B-5–B-11 are confirmations.

---

## 5. PHASE C — SECTION CHANGE MAP (PREVIEW)

| v0.4.1 section | v0.5 change | Driven by |
|---|---|---|
| §0.2, §0.3 | Threat model; structural-not-semantic verification | D-045 |
| §1.9, §1.10 | Entity-neutral wording; §1.9 becomes threat-model seed | D-014, D-045 |
| §2 | New "Composition Surfaces" | D-023 |
| §4.1–4.3 | Re-expressed as SCITT profile | D-015 |
| §4.5, §7 | DID/VC vocabulary; `kind`/`chain_role` split | D-014, D-021 |
| §4.8 | Promotion rule added | D-027 |
| §5 | New Tier 2: SubAgentArtifact, Constraint lifecycle, stance vocabulary | D-026, D-028, D-038 |
| §5.3, §16 | RoleGrant → VC; `blocks_roles` check | D-018, D-029 |
| §6.4–6.5 | Revision-cause enum; PROV-O predicates; `DEFERS_TO` | D-017, D-034, D-036 |
| §8 | Dual signature; `deferred_to`, `prior`/`posterior`, stance | D-031, D-034, D-035, D-038 |
| §9 | Envelope optional; "Episode" naming; `prior_ref` | D-030, D-035, D-047 |
| §10 | `claim_type` family; validator exec spec SHOULD; inline mode | D-025, D-020, D-032 |
| §11 | `deliberation_quality`; `mode: inline`; verdict ≠ posterior | D-033, D-032, D-035 |
| §12 | `addresses[]`, engagement fields | D-037 |
| §15 | PROV-O inside signed wrapper | D-017 |
| §17 | Snapshot as tree-head-binding statement | D-019 |
| §26 | Coordination out of scope; §26.1 inputs specified | D-023, D-039 |
| §25 | This log | — |
| New | Evidence and Validation | D-046 |
| Appendix A | New kinds; referrer types | D-024–D-026 |
| Appendix C | Bidirectional vocabulary map | D-047 |
| Appendix D | Genericized | D-042 |
| New appendix | Adjacent Work and Conditions for Revision | D-043 |
| Throughout | Dated, verified third-party claims | D-044 |

---

*Phase A complete. This log is the traceability record for CP-SPEC v0.5. Every decision is revisable through the process it specifies.*
