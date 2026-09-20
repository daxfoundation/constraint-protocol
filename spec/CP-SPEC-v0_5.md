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

@@CP_PART_6@@
