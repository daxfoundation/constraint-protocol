# Verifying this record

## Run it

```
pip install cryptography          # or: pip install pynacl
python3 verify.py                 # checks the folder that holds verify.py
python3 verify.py path/to/folder  # or any copy of it
```

You need Python 3.8+ and one Ed25519 library. The script reads only the files in the folder and makes no network calls. Exit status 0 means every required check passed. Expected result (abridged):

```
identities            4 documents, primary_handle 4/4, did matches key 4/4
events                44 in 21 hash-chained contexts (cto01 34, test01 10)
  content_hash        44/44
  signature           44/44  (signed by witness 42, validator 2)
  chain genesis       21/21  (prev_hash null)
  chain links         23/23  (prev_hash = previous content_hash)
artifacts             14
  name = hash         14/14  (filename = content_hash = recomputed)
  signature           14/14  (13 against published keys; 1 only against a self-asserted key)
constraint records    2
  content_hash        2/2
  signature           2/2
SHA256SUMS            46/46 entries match; unlisted files: 0
RESULT: PASS
```

`sha256sum -c SHA256SUMS` also checks the file list on Linux or macOS.

## The rules the run used

These are the rules of the v0.4 build that produced the record. They were recovered from the files and confirmed against every object. They are **not** the canonicalisation that CP v0.5 specifies (RFC 8785); see the section on RFC 8785 below.

### Canonical bytes

`C(x)` = the UTF-8 encoding of Python's `json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`:
- object keys sorted (every key in the record is ASCII, so code-point and UTF-16 order agree);
- no whitespace;
- non-ASCII characters written as themselves, not as `\u` escapes;
- strings escaped as Python's `json` does: `\"`, `\\`, `\n`, `\r`, `\t`, `\b`, `\f`, and other control characters as lowercase `\u00xx`;
- numbers as Python writes them: integers plain, floats by `repr`, so `0.25` is `0.25` and `1.0` is `1.0`.

### Hash

`H(b)` = `"blake2b-256:"` + lowercase hex of BLAKE2b with a 32-byte digest. No key, salt or personalisation is used.

### What each hash and signature covers

| Object | `content_hash` | The Ed25519 signature is over | Signature hex in |
|---|---|---|---|
| Event (one line of `events/<vault>/<context_id>.jsonl`) | `H(C(event without content_hash, signatures))` | `C(event without signatures)`, which **includes** `content_hash` | `signatures[0].value` |
| Artifact (`artifacts/<vault>/blake2b-256_<hex>.json`) | `H(C(artifact without content_hash, signatures))`; the file name is the same hash with `_` for `:` | `C(artifact without content_hash, signatures)`, the same bytes as the hash input, so it **excludes** `content_hash` | `signatures[0].value_hex` |
| Constraint record (`constraints/cto01/*.json`) | `H(C(record without content_hash, signatures))` | `C(record without signatures)` | `signatures[0].value_hex` |
| Identity document (`identities/<vault>/*.json`) | `primary_handle` = `H(C(doc without primary_handle, also_known_as, rotation_log))` | not signed | n/a |

Artifacts are signed differently from events and constraint records. Both conventions are in the record exactly as the build produced them.

Artifact files are pretty-printed. A hash of the raw file bytes therefore does not equal the file name: parse the file, then hash `C(...)` as above.

### Chains

Each context is one file, with one event per line in order. The first event has `prev_hash: null`, and every later event's `prev_hash` equals the previous event's `content_hash`. Each event's `context_id` equals its file name.

### Public keys and signers

In each identity document, `verification_method[0].public_key_multibase` is `z` followed by 64 hex characters, and those hex characters are the raw 32-byte Ed25519 public key. This is **not** multibase base58btc. Likewise the DID `did:key:z<hex>` is not standard did:key encoding, which would be base58btc of the multicodec-prefixed key. Use the hex directly.

To find an object's key, take the handle before `#` in `signatures[0].verification_method`. It equals an identity's `primary_handle`. For events it also equals `issuer`, and `issuer_did` equals that identity's DID.

One artifact, `blake2b-256:6828d930…`, is signed by a key that has no identity document here; it belongs to the third instance, which was not captured. verify.py checks it against the key stated in that artifact's own `produced_by_did`. That shows the artifact is internally consistent, not who held the key.

### Artifact file names

Names have the form `blake2b-256_<hex>.json`: the artifact's `content_hash` with its `:` written as `_`, because Windows does not allow `:` in file names. Read the `_` back as `:` and the name must equal `content_hash`; verify.py checks this. Only the file names were changed. The file contents are byte-for-byte as captured, so references inside signed bytes (such as `stored_path` and `artifact_path`) keep the form the vaults used, `artifacts/blake2b-256:<hex>.json`.

## Why RFC 8785 reproduces only 36 of the 44 events

CP v0.5 (§4.4, §19) requires RFC 8785, the JSON Canonicalization Scheme (JCS). JCS writes numbers the way JavaScript does, so `1.0` becomes `1`. The v0.4 build wrote `1.0`.

Eight published events contain such a value: `validator_score: 1.0` in the receipts for artifacts sent to the third instance, and scores of `1.0` in the two AdherenceClaims. They are:
- cto01 `loop2-step1-design` #3, #4;
- cto01 `loop2-step2-implement` #3–#6;
- cto01 `loop2-step4-simulate` #1;
- test01 `meta-analysis-001` #1.

Their hashes and signatures reproduce only under the run's rule. Every other event, all 14 artifacts and both constraint records come out identical under either rule. verify.py prints the JCS count for information; the run's rule is the one that must pass.

If you implement verification in another language, keep `1.0` as `1.0`, for example by preserving each number's original text when parsing. Otherwise those eight events will fail.

## What verification establishes and what it does not

**It establishes** three things:
- each published object is unchanged since it was signed;
- each chain is complete and in order;
- each signature was made with the private half of the stated key.

**It does not establish:**
- **When objects were signed.** Timestamps are written by the signer, and nothing anchors them externally.
- **That no other objects exist under these keys.** The private keys were exposed on 2026-10-20, so the record is exactly the set listed in `SHA256SUMS` (see KEYS-RETIRED.md).
- **What the third instance held.** See WITHHELD.md.
- **Anything about the content.** It does not show that the instructions given to the models, or their outputs, were sound.
