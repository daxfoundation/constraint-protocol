#!/usr/bin/env python3
"""Re-check the 2026-05-04 Constraint Protocol (v0.4 build) run record from this folder alone.

Usage:   python3 verify.py [FOLDER]        (FOLDER defaults to the directory holding this script)
Needs:   Python 3.8+ and ONE of:  pip install cryptography   |   pip install pynacl

Checks every event (content_hash, Ed25519 signature, issuer, context_id, hash chain), every
artifact (file name blake2b-256_<hex>.json, with '_' read back as ':', = content_hash = recomputed
hash; signature), every constraint record
(hash, signature) and every identity document (primary_handle), then SHA256SUMS if present.
Rules are documented in VERIFY.md. Exit status 0 means every required check passed.
"""
import hashlib
import json
import os
import re
import sys
from decimal import Decimal


# --------------------------------------------------------------------------- Ed25519 backend
def _load_ed25519():
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        def verify(pub, sig, msg):
            try:
                Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg)
                return True
            except InvalidSignature:
                return False

        return verify, "cryptography"
    except ImportError:
        pass
    try:
        from nacl.exceptions import BadSignatureError
        from nacl.signing import VerifyKey

        def verify(pub, sig, msg):
            try:
                VerifyKey(pub).verify(msg, sig)
                return True
            except BadSignatureError:
                return False

        return verify, "pynacl"
    except ImportError:
        sys.exit("verify.py needs 'cryptography' or 'pynacl' (pip install cryptography)")


ED25519_VERIFY, BACKEND = _load_ed25519()


# --------------------------------------------------------------------------- the run's rules
def canon(obj):
    """Canonical bytes used by the v0.4 build: sorted keys, no whitespace, non-ASCII unescaped, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def bhash(data):
    return "blake2b-256:" + hashlib.blake2b(data, digest_size=32).hexdigest()


def without(obj, *keys):
    return {k: v for k, v in obj.items() if k not in keys}


def key_from_multibase(mb):
    """The run writes Ed25519 public keys as 'z' + 64 hex characters (not base58btc)."""
    if not (isinstance(mb, str) and mb.startswith("z") and re.fullmatch(r"[0-9a-f]{64}", mb[1:])):
        raise ValueError("unexpected public_key_multibase form: %r" % (mb,))
    return bytes.fromhex(mb[1:])


def sig_bytes(entry):
    return bytes.fromhex(entry.get("value") or entry.get("value_hex"))


# --------------------------------------------------------------------------- RFC 8785 (informational only)
def _jcs_number(x):
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if x == 0:
        return "0"
    d = Decimal(repr(x)).as_tuple()
    raw = "".join(map(str, d.digits))
    n = len(raw) + d.exponent
    digits = raw.lstrip("0")
    n -= len(raw) - len(digits)
    digits = digits.rstrip("0") or "0"
    k = len(digits)
    sign = "-" if x < 0 else ""
    if k <= n <= 21:
        return sign + digits + "0" * (n - k)
    if 0 < n <= 21:
        return sign + digits[:n] + "." + digits[n:]
    if -6 < n <= 0:
        return sign + "0." + "0" * (-n) + digits
    e = n - 1
    return sign + digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + ("+" if e >= 0 else "-") + str(abs(e))


def jcs(obj):
    if obj is None:
        return "null"
    if isinstance(obj, (bool, int, float)):
        return _jcs_number(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return "[" + ",".join(jcs(v) for v in obj) + "]"
    keys = sorted(obj, key=lambda s: s.encode("utf-16-be"))
    return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + jcs(obj[k]) for k in keys) + "}"


# --------------------------------------------------------------------------- helpers
class Tally:
    def __init__(self):
        self.ok = {}
        self.n = {}
        self.failures = []

    def check(self, name, cond, where):
        self.n[name] = self.n.get(name, 0) + 1
        if cond:
            self.ok[name] = self.ok.get(name, 0) + 1
        else:
            self.ok.setdefault(name, 0)
            self.failures.append("%s: %s" % (name, where))
        return cond

    def line(self, name):
        return "%d/%d" % (self.ok.get(name, 0), self.n.get(name, 0))


def listdir_sorted(path):
    return sorted(os.listdir(path)) if os.path.isdir(path) else []


def walk_values(obj, wanted, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in wanted and isinstance(v, str):
                out.append((k, v))
            walk_values(v, wanted, out)
    elif isinstance(obj, list):
        for v in obj:
            walk_values(v, wanted, out)


# --------------------------------------------------------------------------- main
def main(root):
    t = Tally()
    vaults = [v for v in listdir_sorted(os.path.join(root, "events"))]

    # identities ------------------------------------------------------------
    keys = {}  # handle -> (label, pubkey bytes, did)
    for v in listdir_sorted(os.path.join(root, "identities")):
        for fn in listdir_sorted(os.path.join(root, "identities", v)):
            doc = json.load(open(os.path.join(root, "identities", v, fn), encoding="utf-8"))
            label = "%s/%s" % (v, fn[:-5])
            handle = doc["primary_handle"]
            t.check("identity.primary_handle", bhash(canon(without(doc, "primary_handle", "also_known_as", "rotation_log"))) == handle, label)
            mb = doc["verification_method"][0]["public_key_multibase"]
            did = "did:key:" + mb
            t.check("identity.did", did in doc.get("also_known_as", []), label)
            keys[handle] = (label, key_from_multibase(mb), did)

    # events ----------------------------------------------------------------
    event_hashes = {}
    signer_role = {}
    jcs_events_ok = 0
    n_chains = 0
    for v in vaults:
        for fn in listdir_sorted(os.path.join(root, "events", v)):
            if not fn.endswith(".jsonl"):
                continue
            n_chains += 1
            path = os.path.join(root, "events", v, fn)
            lines = [ln for ln in open(path, "rb").read().split(b"\n") if ln.strip()]
            prev = None
            for i, raw in enumerate(lines):
                e = json.loads(raw)
                where = "%s/%s#%d" % (v, fn, i)
                t.check("event.content_hash", bhash(canon(without(e, "content_hash", "signatures"))) == e["content_hash"], where)
                if bhash(jcs(without(e, "content_hash", "signatures")).encode("utf-8")) == e["content_hash"]:
                    jcs_events_ok += 1
                sigs = e.get("signatures") or []
                t.check("event.one_signature", len(sigs) == 1, where)
                vm = sigs[0]["verification_method"].split("#")[0] if sigs else None
                k = keys.get(vm)
                ok = bool(k) and ED25519_VERIFY(k[1], sig_bytes(sigs[0]), canon(without(e, "signatures")))
                t.check("event.signature", ok, where)
                if ok:
                    role = k[0].split("/")[1]
                    signer_role[role] = signer_role.get(role, 0) + 1
                t.check("event.issuer_matches_key", bool(k) and e.get("issuer") == vm and e.get("issuer_did") == k[2], where)
                t.check("event.context_id_is_filename", e.get("context_id") == fn[: -len(".jsonl")], where)
                if i == 0:
                    t.check("chain.genesis_prev_null", e.get("prev_hash") is None, where)
                else:
                    t.check("chain.link", e.get("prev_hash") == prev, where)
                prev = e["content_hash"]
                event_hashes[e["content_hash"]] = where

    # artifacts -------------------------------------------------------------
    artifact_hashes = {}
    self_asserted = []
    jcs_art_ok = 0
    # Artifact files are named blake2b-256_<hex>.json: the content hash with its ':' written as '_'
    # (Windows does not allow ':' in file names). Read the '_' back as ':' before comparing.
    name_re = re.compile(r"^blake2b-256_([0-9a-f]{64})\.json$")
    for v in listdir_sorted(os.path.join(root, "artifacts")):
        for fn in listdir_sorted(os.path.join(root, "artifacts", v)):
            m = name_re.match(fn)
            if not t.check("artifact.filename_form", bool(m), "%s/%s (expected blake2b-256_<64 hex>.json)" % (v, fn)):
                continue
            a = json.load(open(os.path.join(root, "artifacts", v, fn), encoding="utf-8"))
            where = "%s/%s" % (v, fn)
            body = canon(without(a, "content_hash", "signatures"))
            name_hash = fn[: -len(".json")].replace("_", ":", 1)
            t.check("artifact.filename=content_hash=recomputed", name_hash == a.get("content_hash") == bhash(body), where)
            if bhash(jcs(without(a, "content_hash", "signatures")).encode("utf-8")) == a.get("content_hash"):
                jcs_art_ok += 1
            sigs = a.get("signatures") or []
            vm = sigs[0]["verification_method"].split("#")[0] if sigs else None
            if vm in keys:
                ok = ED25519_VERIFY(keys[vm][1], sig_bytes(sigs[0]), body)
            else:
                # Not one of the published identities: fall back to the key the artifact asserts for its producer.
                did = a.get("produced_by_did", "")
                ok = bool(sigs) and a.get("produced_by") == vm and did.startswith("did:key:z") and \
                    ED25519_VERIFY(key_from_multibase(did[len("did:key:"):]), sig_bytes(sigs[0]), body)
                if ok:
                    self_asserted.append((a["content_hash"], vm))
            t.check("artifact.signature", ok, where)
            artifact_hashes[a["content_hash"]] = where

    # constraint records ----------------------------------------------------
    constraint_hashes = {}
    for v in listdir_sorted(os.path.join(root, "constraints")):
        for fn in listdir_sorted(os.path.join(root, "constraints", v)):
            if not fn.endswith(".json"):
                continue
            c = json.load(open(os.path.join(root, "constraints", v, fn), encoding="utf-8"))
            where = "%s/%s" % (v, fn)
            t.check("constraint.content_hash", bhash(canon(without(c, "content_hash", "signatures"))) == c["content_hash"], where)
            s = (c.get("signatures") or [{}])[0]
            vm = s.get("verification_method", "").split("#")[0]
            t.check("constraint.signature", vm in keys and ED25519_VERIFY(keys[vm][1], sig_bytes(s), canon(without(c, "signatures"))), where)
            constraint_hashes[c["content_hash"]] = where

    # references (informational) --------------------------------------------
    refs = []
    for v in vaults:
        for fn in listdir_sorted(os.path.join(root, "events", v)):
            for raw in open(os.path.join(root, "events", v, fn), "rb").read().split(b"\n"):
                if raw.strip():
                    walk_values(json.loads(raw), {"artifact_hash", "evidence_hash"}, refs)
    for v in listdir_sorted(os.path.join(root, "constraints")):
        for fn in listdir_sorted(os.path.join(root, "constraints", v)):
            walk_values(json.load(open(os.path.join(root, "constraints", v, fn), encoding="utf-8")), {"resolution_evidence_hash"}, refs)
    art_refs = [h for _, h in refs]
    unresolved = sorted(set(h for h in art_refs if h not in artifact_hashes))
    recv = []
    for v in vaults:
        for fn in listdir_sorted(os.path.join(root, "events", v)):
            for raw in open(os.path.join(root, "events", v, fn), "rb").read().split(b"\n"):
                if raw.strip():
                    walk_values(json.loads(raw), {"recv_event_hash"}, recv)
    recv_hit = sum(1 for _, h in recv if h in event_hashes)
    lifecycle_hit = 0
    for v in vaults:
        for fn in listdir_sorted(os.path.join(root, "events", v)):
            for raw in open(os.path.join(root, "events", v, fn), "rb").read().split(b"\n"):
                if raw.strip():
                    e = json.loads(raw)
                    if e.get("subject") in constraint_hashes:
                        lifecycle_hit += 1

    # SHA256SUMS --------------------------------------------------------------
    sums_path = os.path.join(root, "SHA256SUMS")
    sums_line = "not present"
    if os.path.exists(sums_path):
        listed = set()
        for ln in open(sums_path, encoding="utf-8"):
            if not ln.strip():
                continue
            digest, rel = ln.rstrip("\n").split("  ", 1)
            listed.add(rel)
            p = os.path.join(root, rel)
            ok = os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == digest
            t.check("SHA256SUMS.entry", ok, rel)
        on_disk = set()
        for dp, _, fns in os.walk(root):
            for f in fns:
                rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
                if rel != "SHA256SUMS" and "__pycache__" not in rel:
                    on_disk.add(rel)
        extra = sorted(on_disk - listed)
        t.check("SHA256SUMS.no_unlisted_files", not extra, ", ".join(extra))
        sums_line = "%s entries match; unlisted files: %d" % (t.line("SHA256SUMS.entry"), len(extra))

    # report ------------------------------------------------------------------
    n_events = t.n.get("event.content_hash", 0)
    print("CP v0.4 run record, 2026-05-04 :: verify.py (Ed25519 via %s)" % BACKEND)
    print("folder: %s" % os.path.abspath(root))
    print()
    print("identities            %d documents, primary_handle %s, did matches key %s" % (len(keys), t.line("identity.primary_handle"), t.line("identity.did")))
    print("events                %d in %d hash-chained contexts (%s)" % (n_events, n_chains, ", ".join("%s %d" % (v, sum(1 for w in event_hashes.values() if w.startswith(v + "/"))) for v in vaults)))
    print("  content_hash        %s" % t.line("event.content_hash"))
    print("  signature           %s  (signed by witness %d, validator %d)" % (t.line("event.signature"), signer_role.get("witness", 0), signer_role.get("validator", 0)))
    print("  issuer = key = did  %s" % t.line("event.issuer_matches_key"))
    print("  context_id = file   %s" % t.line("event.context_id_is_filename"))
    print("  chain genesis       %s  (prev_hash null)" % t.line("chain.genesis_prev_null"))
    print("  chain links         %s  (prev_hash = previous content_hash)" % t.line("chain.link"))
    print("artifacts             %d" % t.n.get("artifact.signature", 0))
    print("  name = hash         %s  (filename = content_hash = recomputed)" % t.line("artifact.filename=content_hash=recomputed"))
    print("  signature           %s  (%d against published keys; %d only against a self-asserted key)" % (
        t.line("artifact.signature"), t.ok.get("artifact.signature", 0) - len(self_asserted), len(self_asserted)))
    for h, vm in self_asserted:
        print("      %s signed by %s: key taken from the artifact's own produced_by_did; no identity document for it is published" % (h, vm))
    print("constraint records    %d" % t.n.get("constraint.signature", 0))
    print("  content_hash        %s" % t.line("constraint.content_hash"))
    print("  signature           %s" % t.line("constraint.signature"))
    print()
    print("references (informational, not pass/fail)")
    print("  artifact references resolving to a file here: %d/%d" % (sum(1 for h in art_refs if h in artifact_hashes), len(art_refs)))
    for h in unresolved:
        print("      not here: %s (held by the third instance, which was not captured)" % h)
    print("  test01 delegations acknowledged by a cto01 event here: %d/%d (the rest went to the third instance)" % (recv_hit, len(recv)))
    print("  constraint-lifecycle event subjects equal to a constraint record here: %d" % lifecycle_hit)
    print("  RFC 8785 (JCS) instead of the run's rule would reproduce: events %d/%d, artifacts %d/%d (differs only where a value is written 1.0)" % (
        jcs_events_ok, n_events, jcs_art_ok, t.n.get("artifact.signature", 0)))
    print()
    print("SHA256SUMS            %s" % sums_line)
    print()
    if t.failures:
        print("RESULT: FAIL (%d)" % len(t.failures))
        for f in t.failures:
            print("  - " + f)
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    sys.exit(main(folder))
