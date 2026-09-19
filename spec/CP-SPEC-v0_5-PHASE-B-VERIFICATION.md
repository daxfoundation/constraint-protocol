# CP-SPEC v0.5 — Phase B Verification Results

**Date:** 2026-09-10
**Status:** Decision-affecting checks complete (B-1, B-2, B-3, B-4, B-5, B-7). Confirmation checks (B-6, B-8, B-9, B-10, B-11) deferred to inline verification during Phase C — none can reverse a decision.
**Method:** Primary sources only — published artifacts (PyPI wheel), rendered specs, IETF datatracker, project documentation. No inference where a source was reachable.

---

## SUMMARY OF OUTCOMES

| Check | Decision | Result | Consequence |
|---|---|---|---|
| **B-1** | D-016, D-021 | PQ cryptosuites exist as W3C CCG experimental spec with JCS variants and registered multicodecs | **D-016 resolves: reverse D-009, go VC 2.0 native.** Workhorse → ML-DSA-44. Anchor EO note added. |
| **B-2** | D-024(ii) | Non-owner referrer attachment is how `agntcy/dir`'s own reconciler works | **D-024 holds.** Open contestation via referrers is viable on the server. |
| **B-3** | D-044 | `Epistemic` and `Provenance` are `pass` in published 0.0.8 (2026-07-17), latest release | Finding stands; dated as observation. |
| **B-4** | D-015 | SCITT is content-agnostic; third-party issuers and new-statements-over-time are explicit; per-domain TS instances are the design | **D-015 holds.** Format bridge via VC-COSE noted for Phase C. |
| **B-5** | D-031 | Issuer signature + Transparency Service receipt = two distinct verifiable signatures | **D-031 holds** and is standardized. |
| **B-7** | D-024(i) | `referrer_type` not validated; unknown types accepted via default OCI media type (issue #991) | `cp.*.v1` types work today; enum proposal is a watch item. |

**Net effect on the decision log:** one conditional resolves (D-016 → reverse D-009), one §7 parameter changes (ML-DSA-65 → ML-DSA-44), one §7 security note is added, zero decisions reversed by evidence. Phase A holds.

---

## B-1 — POST-QUANTUM CRYPTOSUITES FOR VC DATA INTEGRITY

**Source:** `https://w3c.github.io/vc-di-quantum-resistant/` — *Quantum-Resistant Cryptosuites v1.0*, W3C Credentials Community Group; repo `w3c/vc-di-quantum-resistant` (54 commits, 6 stars, 15 watchers, `transitions/2026` folder present). Corroborating: Data Integrity call transcript 2025-02-28 (incubation → standards track via next VC charter).

**Status line, verbatim:** *"This specification is experimental, do not use it in any production setting."*

**What it defines that CP needs:**

| Cryptosuite | Algorithm | Canonicalization | Signature bytes |
|---|---|---|---|
| `mldsa44-jcs-2024` | ML-DSA-44 (FIPS 204, Cat. 2) | **JCS / RFC 8785** — CP §4.4 | 2,420 |
| `slhdsa128-jcs-2024` | SLH-DSA-SHA2-128s (FIPS 205, Cat. 1) | JCS | 7,856 |
| `mldsa44-rdfc-2024`, `slhdsa128-rdfc-2024` | same | RDF Canonicalization | same |

Also defined: `falcon512-*` (FN-DSA, pending FIPS 206) and `sqisign1-*` (not yet NIST-selected) — both with **unregistered** multicodec codes. CP does not adopt these.

**Multikey / multicodec prefixes (registered):**
- ML-DSA-44 public key: varint `0x1210`, prefix `0x9024`, 1,312 bytes
- SLH-DSA-SHA2-128s public key: varint `0x1220`, prefix `0xa024`, 32 bytes

This answers **D-021's condition**: `did:key` with a PQ public key is representable using registered multicodec prefixes.

**Gap:** no cryptosuite is defined for **ML-DSA-65** (Cat. 3). It is tabulated but has no suite identifier. CP §7 specified ML-DSA-65 as the workhorse.

**Security-properties table in the spec (BUFF properties):**

| Scheme | EUF-CMA | SUF-CMA | Exclusive Ownership | Message-Bound | Non-Re-signability |
|---|---|---|---|---|---|
| ML-DSA | Yes | Yes | Yes | Yes | Yes |
| SLH-DSA | Yes | **No** | **Unknown** | Yes | **Unknown** |

**Resolution of D-016:** **Reverse D-009. Adopt VC 2.0 native envelope.**

Rationale:
1. The envelope decision and the cryptosuite decision are separable. VC 2.0 Data Integrity is a W3C Recommendation; the cryptosuite is a plug-in identified by string.
2. `mldsa44-jcs-2024` and `slhdsa128-jcs-2024` are fully specified with algorithms, encodings, and test vectors. They are implementable today against liboqs.
3. "Experimental" is a W3C process status. The underlying algorithms are FIPS 204 and FIPS 205 — final NIST standards since August 2024. The cryptographic risk is not what the label describes.
4. CP made post-quantum signing Tier 1 normative in April 2026 (D-009.a). Being ahead of W3C cryptosuite maturity is consistent with a commitment CP already made.
5. Retaining Position γ means maintaining a bespoke envelope indefinitely pending W3C process — the reinvention the adopt/substitute/build rule exists to prevent.

**Cascades from the resolution:**
- **§7 workhorse: ML-DSA-65 → ML-DSA-44.** The only defined ML-DSA cryptosuite. Category 2 (~NIST Level 2). Smaller signatures (2,420 vs 3,309 bytes). Ecosystem is converging here. Anchor remains SLH-DSA-SHA2-128s. Hybrid Ed25519 transition unchanged; `eddsa-jcs-2022` is the transitional cryptosuite identifier.
- **§7 anchor Exclusive-Ownership note (new).** SLH-DSA's EO and NR properties are listed as Unknown. Without Exclusive Ownership, a key-substitution attack is theoretically possible — a signature verifying under a second, adversarial public key. CP mitigates structurally: anchor signatures over rotation-log entries are over content that binds the anchor public key (the frozen genesis document contains it, and every rotation-log entry references the genesis hash). This must be stated as a normative requirement in §7, not left implicit.
- **§20 Primitives Registry** keys become cryptosuite identifiers: `mldsa44-jcs-2024` (workhorse), `slhdsa128-jcs-2024` (anchor), `eddsa-jcs-2022` (transitional, sunset 2030-01-01).
- **§19 canonicalization** unchanged — JCS is what the PQ suites use.
- **D-043 appendix engagement item:** CP implements against `vc-di-quantum-resistant`, contributes test vectors and implementation experience, and tracks the spec to Recommendation. Condition for revision: if the spec reaches Recommendation with different suite identifiers, CP re-registers.

**D-021 resolves:** identity substrate in DID/VC terms with PQ keys is viable now.

---

## B-2 — NON-OWNER REFERRER ATTACHMENT IN `agntcy/dir`

**Sources:** `https://dir.agntcy.org/latest/dir/dir-features-scenarios/` (Usage Guide, v1.0.0); arXiv 2509.18787 (ADS architecture); `agntcy/dir` issue #991.

**Findings:**
1. **The reconciler attaches referrers to records it did not publish.** From the Usage Guide, Security Scanning: *"The Directory reconciler automatically scans records… Scan results are stored as OCI referrers and indexed in the local database."* The reconciler is a separate service. This is non-owner attachment as a first-class operational pattern.
2. **Self-managed-key signing has no ownership check.** `dirctl sign $RECORD_CID --key cosign.key` signs any CID with any key. Signing is a referrer push (Signature referrer type), decoupled from the original record push.
3. **The architecture names third-party referrers explicitly.** ADS paper: *"Optional referrers (signatures, evaluations) are attached."* An evaluation attached by a third party is the AdherenceClaim shape.
4. **Storage is OCI/ORAS referrers.** The OCI referrers API exists so that signers, scanners and attesters who are not the artifact publisher can attach to it. Non-owner attachment is the mechanism's design intent.

**Access control** is at the server/registry layer (SPIFFE per the repo's `utils/`), not in the protocol. Whoever has push credentials to a dir node can attach referrers. This is the right layer for it — CP scope semantics map to node-level access policy.

**Resolution:** **D-024 holds.** WitnessAttestation, AdherenceClaim, Contestation, Adjudication, Tombstone, Patch as CP-namespaced referrer types on immutable records is viable on the shipped server, not just as a borrowed shape.

**Additional findings from the same source:**
- **ADS is now an IETF draft:** `draft-mp-agntcy-ads` on the datatracker. New since the July analysis. With SCITT at IETF, CP's two substitution targets converge on one standards body. → D-043 appendix.
- **Federation Testbed** is live (`agntcy/dir` discussions #455). → D-046 validation venue.
- **Name verification uses JWKS at `.well-known`** — domain proves key control; the registry does not grant names. This is §7.9's friendly-name-not-root principle, implemented. → D-021 vocabulary.
- `dir` is at **v1.0.0**, ~174 stars, 51 forks, active issues and milestones (v1.3). Maintained.
- `dirctl export --format=a2a` and `--format=agent-skill` — dir already bridges to A2A AgentCards and SKILL.md. → D-023 composition.

---

## B-3 — L9 SCHEMA `Epistemic` AND `Provenance` PLACEHOLDERS

**Sources:** PyPI `ioc-l9-all-models` 0.0.8; the published wheel `ioc_l9_all_models-0.0.8-py3-none-any.whl` (14.2 kB, uploaded 2026-07-17, Sigstore-attested, from commit `b6b4dc25`, tag `v0.0.8`); GitHub `outshift-open/ioc-protocols-models` (60 commits, 1 star, 2 PRs — unchanged since late July).

**From the published artifact, `ai/outshift/data_model.py`, generated by datamodel-codegen from `l9_schema.json`:**

```python
class Epistemic(BaseModel):
    pass


class Provenance(BaseModel):
    pass
```

**Status:** the finding is current, not stale. 0.0.8 is the latest release; the repo has had no commits since it was cut. The schema `version` field lags the package version (schema said 0.0.6 when the package was 0.0.8) — irrelevant to the finding.

**Publication wording under D-044:** *"As of `ioc-l9-all-models` 0.0.8 (released 2026-07-17; the latest release as of 2026-09-10), the L9 schema's `Epistemic` and `Provenance` objects are defined without fields. Their descriptions state fields are to be added."* Observation, dated, no characterization.

**Additional D-044 findings — expansion inconsistencies are the project's own:**
- GitHub README: **SIEP = Semantic Interoperability and Epistemic Protocol**; PyPI description (same release): **SIEP = Semantic Information Exchange Protocol**. Both are the project's text. CP cites the GitHub README as canonical (the repo is their declared single source of truth) and notes the PyPI variant.
- **CIP = Cognition and Interoperability Protocol** (README). The "Contingency Interaction Protocol" expansion recorded in earlier drafts is not in current project text; dropped.
- **SAB = Semantic Alignment Broadcast** (README). "Semantic Alignment via Bargaining"; dropped.
- **TFP = Team Formation via Polling** — consistent.

---

## B-4 — SCITT STATEMENT MODEL AND SCOPED INSTANCES

**Source:** `draft-ietf-scitt-architecture-22` (October 2025, Standards Track, authors Fraunhofer SIT / Microsoft Research / ARM), datatracker and WG GitHub.

**Findings:**
1. **Content-agnostic.** *"This 'content-agnostic' approach allows SCITT transparency services to be either integrated in existing solutions or to be an initial part of new emerging systems."* The document *"only specifies the format of Signed Statements… and a very thin wrapper format for Receipts."* A CP WitnessAttestation payload is a Statement type; SCITT imposes nothing on it.
2. **Third-party issuers are explicit.** *"An Issuer may be the owner or author of Artifacts, or an independent third party such as an Auditor, reviewer or an endorser."* CP validators and contestants are Issuers.
3. **Statements about an artifact accumulate over time.** *"Over time, an Issuer may register new Signed Statements about an Artifact in a Transparency Service with new information."* This is D-004's accumulating AdherenceClaims and D-006.b's post-hoc contestation, in IETF text.
4. **Per-domain Transparency Services with interoperability.** *"The SCITT architecture enables Transparency Services in a given application domain to implement a collective baseline… interoperability between different transparency services."* Per-scope TS instances (D-015) and per-org independent witnesses (D-005) are the design, not a workaround.
5. **Registration policy.** *"Transparency services confirm a policy is met before recording the statement on the ledger."* This is where CP's Tier 1 structural checks (signature validity, chain integrity, scope) sit — as TS registration policy, not as content judgment.
6. **Non-equivocation.** *"All proofs provided by the Transparency Service to Relying Parties are produced from a Single Verifiable Data Structure."* The append-only, tamper-evident property.

**Role mapping (resolves the "witness vs log operator" question raised in Phase A):**

| CP role | SCITT role |
|---|---|
| Participant | Issuer of the interaction Statement |
| Witness | Transparency Service (records, receipts, asserts nothing about content) |
| Validator | Issuer of a later Statement about the artifact |
| Contestant | Issuer of a later Statement about the artifact |

The witness *is* the TS operator in SCITT terms. D-005 (independent witnesses per org) maps to: each org runs its own TS; cross-org interactions register in both; two Receipts = two independent witness records.

**Format bridge (Phase C design item, not a decision):** SCITT is COSE/CBOR (COSE_Sign1). D-016 is VC 2.0 JSON. *Securing Verifiable Credentials using JOSE and COSE* is one of the seven VC 2.0 Recommendations. A CP artifact is: VC 2.0 data model → COSE_Sign1-secured (`vc+cose`) → registered as a SCITT Signed Statement. Alternatively the SCITT payload carries the JCS-canonical VC JSON directly; SCITT permits either. Choose in Phase C; both are conformant.

**Resolution:** **D-015 holds.** No CP-defined statement type needs to be contributed to SCITT — the content-agnostic payload carries it. The "no adherence claim" property is not a statement *type*; it is what the Transparency Service role already means.

---

## B-5 — TWO DISTINCT VERIFIABLE SIGNATURES

**Source:** same draft.

*"Transparent Statement: a Signed Statement that is augmented with a Receipt created via Registration in a Transparency Service. The Receipt is stored in the unprotected header of COSE Envelope of the Signed Statement."*

Signature 1: Issuer, over the Statement (protected header + payload), COSE_Sign1.
Signature 2: Transparency Service, in the Receipt — a signed inclusion proof per `draft-ietf-cose-merkle-tree-proofs`.

Both independently verifiable; both identities distinct (`iss` CWT claim in the Statement; TS identity in the Receipt wrapper).

**Resolution:** **D-031 holds** — the participant-signs / witness-countersigns rule is the SCITT model. CP's Tier 1 rule becomes a citation, not an invention.

---

## B-7 — REFERRER TYPE REGISTRATION

**Source:** `agntcy/dir` issue #991 (opened 2026-03-02, milestone DIR v1.3), `server/store/oci/types.go`.

`referrer_type` is a string, not validated at the proto layer. Server mapping: `SignatureReferrerType` and `PublicKeyReferrerType` map to specific OCI artifact types; **everything else maps to `DefaultReferrerArtifactMediaType`**. So `cp.witness.v1`, `cp.adherence.v1`, `cp.contestation.v1` are accepted today and stored as generic referrers.

**Watch item:** the issue proposes proto-level enums, which would close open registration. If adopted, CP needs its types registered upstream. → D-043 appendix, with the dir repo as engagement venue.

---

## DEFERRED TO PHASE C (INLINE CONFIRMATION)

None of these can reverse a decision. Each is verified at the point of writing the section it affects.

| Check | Decision | Where verified | Fallback |
|---|---|---|---|
| B-6 KYA-OS current state | D-022 | §5.1.4 / §9 | Profile against current draft; date it |
| B-8 SCR / GAR definitions; W formula | D-033 | §11.1 | Cite exactly; W is already excluded |
| B-9 PROV-O mapping for `DEFERS_TO` | D-034 | §15 / §6.5 | `prov:wasInfluencedBy` superproperty |
| B-10 Watched-project status | D-043 | new appendix | Update per entry |
| B-11 L9 / Mycelium vocabulary | D-047 | Appendix C | Pin to 0.0.8 |

---

## DECISION LOG AMENDMENTS FROM PHASE B

- **D-016:** conditional → **DECIDED. Reverse D-009. VC 2.0 native envelope.** Cryptosuites `mldsa44-jcs-2024` (workhorse), `slhdsa128-jcs-2024` (anchor), `eddsa-jcs-2022` (transitional). CP cites W3C CCG *Quantum-Resistant Cryptosuites v1.0* as experimental, implements against it, tracks to Recommendation.
- **D-016.a (new cascade):** §7 workhorse ML-DSA-65 → ML-DSA-44.
- **D-016.b (new cascade):** §7 normative requirement that anchor (SLH-DSA) signatures are over content binding the anchor public key, mitigating SLH-DSA's unknown Exclusive-Ownership property.
- **D-021:** conditional → **DECIDED.** Registered multicodecs `0x1210` / `0x1220` make PQ `did:key` representable.
- **D-024:** conditional → **DECIDED.** Non-owner attachment confirmed on the shipped server.
- **D-015, D-031:** conditions cleared. Role mapping to SCITT recorded.
- **D-044:** expansion corrections recorded (CIP, SAB); SIEP dual-expansion noted as the project's own.
- **D-043:** four new watch entries — `draft-mp-agntcy-ads` (IETF), `agntcy/dir` issue #991 (referrer enums), `w3c/vc-di-quantum-resistant` (track to Rec), agntcy Federation Testbed (validation venue).

---

*Phase B decision-affecting verification complete. Phase A holds with one conditional resolved and two §7 cascades. Phase C may begin.*
