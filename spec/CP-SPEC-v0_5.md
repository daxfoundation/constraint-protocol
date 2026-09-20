@@CP_PART_1@@
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
