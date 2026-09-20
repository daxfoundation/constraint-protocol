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
