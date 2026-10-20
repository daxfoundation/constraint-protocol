# Retired signing keys

**Status as of 2026-10-20: RETIRED.** The five Ed25519 keys below are every key that signed an object in this folder. All five are retired as of 2026-10-20 and will never be reused for any purpose.

## Why

The private halves of the four keys held by `cto01` and `test01` were held only on the run's machines and in a local forensic copy of the two captured vaults. On 2026-10-20 they were exposed in a working-session transcript while this publication was being prepared. Anyone who holds them can produce new objects that verify against the public keys below.

The fifth key belongs to the third instance, whose vault and identity document were not captured. Its private half was not in the captured material and was not exposed. It is retired with the others so that the whole run is closed under one rule.

Signatures in this record carry no external timestamp, so a signature alone cannot show when an object was made.

## Rule

The record is exactly the set of files listed in `SHA256SUMS` in this folder. **Any object signed by one of these five keys that is not listed in `SHA256SUMS` is not part of the record**, whatever its timestamps say.

## The five retired keys

Public key = the raw 32-byte Ed25519 key, hex. The DID is the run's own `did:key:z<hex>` form, not standard did:key encoding (see VERIFY.md). Handle = the identity's `primary_handle`, which is what `verification_method` refers to.

### cto01 witness

- Public key (hex): `757782d2d494162ab4c17fbc14ee3c293ce1da06ca7f31217a62d0ec5290e794`
- DID: `did:key:z757782d2d494162ab4c17fbc14ee3c293ce1da06ca7f31217a62d0ec5290e794`
- Handle: `blake2b-256:5b6ccc4485321727e1400b160ebf4a097dd57a508080d18eba95ddc3461d31ac`
- Identity document: `identities/cto01/witness.json` (created 2026-05-04T11:53:25.297611Z)

### cto01 validator

- Public key (hex): `c6e67a51705d5cc199932d557c4533db4e11017233674df94876f4b0322763bb`
- DID: `did:key:zc6e67a51705d5cc199932d557c4533db4e11017233674df94876f4b0322763bb`
- Handle: `blake2b-256:3790ddf887ae98f5e976254b9f39afd019c351319d61621d35c93fd5e9133d69`
- Identity document: `identities/cto01/validator.json` (created 2026-05-04T11:53:25.398161Z)

### test01 witness

- Public key (hex): `255f4cd154a42ddb1bbe0895f5dedb1c54a7820b3f0cd2dfe26ce01dcf2f74ae`
- DID: `did:key:z255f4cd154a42ddb1bbe0895f5dedb1c54a7820b3f0cd2dfe26ce01dcf2f74ae`
- Handle: `blake2b-256:4115fdfb91eefd8a111a593f0ff7e14034cce6e7e1e92f78ebea4612c97291f9`
- Identity document: `identities/test01/witness.json` (created 2026-05-04T11:45:07.059582Z)

### test01 validator

- Public key (hex): `455424192f4ec3cd7bfe66fe10c1732aa49f30a9a0d64482fbfee9dccea5f9db`
- DID: `did:key:z455424192f4ec3cd7bfe66fe10c1732aa49f30a9a0d64482fbfee9dccea5f9db`
- Handle: `blake2b-256:3a8cd910b0433ac91526c6fb0d1ee670cd3d638c76b52580bae8e99eb8661da9`
- Identity document: `identities/test01/validator.json` (created 2026-05-04T11:45:07.158134Z)

### third instance

- Public key (hex): `c22fa743e903ddcc4190210ac5ca5c9b7d923e61efe8db103c5d52841c8d381a`
- DID: `did:key:zc22fa743e903ddcc4190210ac5ca5c9b7d923e61efe8db103c5d52841c8d381a`
- Handle: `blake2b-256:ca93be991517ca8a076a286894a19322b8a349184877940a01ad957a5511d581`
- Identity document: none published; the key is self-asserted in `artifacts/cto01/blake2b-256_6828d93087faacd48fcc2a166350f33dbf29eb7863b8ada6fcfe57653ea16e00.json` (`produced_by_did`)
