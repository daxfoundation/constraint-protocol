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
