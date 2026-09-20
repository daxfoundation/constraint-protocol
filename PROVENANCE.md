# Provenance

**Version.** Constraint Protocol **v0.5**. The version was **not** incremented for publication.

**What these copies are.** A sanitised publication copy, prepared 2026-09-19, of the v0.5 source documents. Sanitising was name-level only: nothing was restructured, no argument rewritten, no technical claim softened, no decision removed, and no normative MUST/SHOULD/MAY language touched.

**Categories of change, in full:**

1. **Context IRI.** The CP JSON-LD context IRI now reads `https://daxfoundation.org/cp/v0.5`, at both sites where it appears.
2. **Date-stamped observations.** Seven statements about third-party systems that were undated or written relative to publication ("as of this writing", "today") now carry the date the observation was made, as the specification's own D-044 requires.
3. **Internal identifiers.** Two internal identifiers — a cross-node run label and a record-store name — were replaced with neutral descriptions. No finding or consequence was changed.
4. **Illustrative vendor names.** Example model and provider names in one schema sketch were generalised to placeholders, so the text neither dates itself nor reads as endorsement.
5. **Wording.** One clarity fix: "Human alias" to "Human-readable alias".

**Source digests (sha256)** of the documents these copies derive from:

- Specification body — `d371e2ee80951a1c5945b8004e69049a95f6fb5a4448fdfba74d519ac0d6f4a0`
- Decision log — `4cf8a947c85d4b78f866f9ff7700aa878d50101b5fbfba3a815be3931fd161f3`
- Phase B verification — `96f27617815e2bedc0c60c16afd023acaff156b5eab17e7c85deddf700217729`

**Publication digests (sha256)** of the sanitised copies:

- Specification body — `816b5f4798a71a83ff4e2c3c36695144a45928d9a03fb1f94c759820891b37c9`
- Decision log — `d5247ebbfe33f533f16752457eeddfb6f905bd2a51e64108988db7386f556dfc`
- Phase B verification — `4a077e01e201fbbb47e6e781aa519d3b0a1dc420c778193f82a8f45ebce2d7d0`

**Publication state.** All three sanitised copies are present in this repository under `spec/`, and each was verified against its publication digest above on 2026-09-20:

| File | Bytes | git blob sha1 |
|---|---|---|
| `spec/CP-SPEC-v0_5.md` | 225,851 | `b63a3ee7f5b75b5e10f6eb1868b220c876b42b5a` |
| `spec/CP-SPEC-v0_5-DECISION-LOG.md` | 31,891 | `835e5862fd0aee53ef3ebea438ed0c602b6389f1` |
| `spec/CP-SPEC-v0_5-PHASE-B-VERIFICATION.md` | 17,290 | `209e50278e7fe8b412963d9f25207b41c0fc5757` |

The specification body was assembled inside this repository from six byte-exact, line-aligned parts that had been staged under `spec/_staging/`. The staging directory was removed once the assembled file matched the publication digest for the body. The bytes served here are the sanitised copy — not the private original.

The byte-exact originals are retained privately, unmodified, as the archive of record.
