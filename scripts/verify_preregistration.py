"""Check the SHA-256 hashes recorded when each study plan was sealed.
Plan v1 has a dated deviation appended after sealing (allowed by the plan); the recorded hash covers the text
before that entry, so it is checked on the sealed part only.
"""
import hashlib
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "preregistration")
for plan, marker in (("study_plan_hybrid_v1_SEALED", b"\n- 2026-10-10 (before any confirmatory run)"),
                     ("study_plan_experts_v2_SEALED", None)):
    text = open(os.path.join(D, plan + ".md"), "rb").read()
    sealed = text[: text.find(marker)].rstrip(b"\n") + b"\n" if marker else text
    want = open(os.path.join(D, plan + ".sha256")).read().split()[0]
    got = hashlib.sha256(sealed).hexdigest()
    print(f"{plan}: {'OK' if got == want else 'MISMATCH'} ({got})")
