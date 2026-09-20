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
