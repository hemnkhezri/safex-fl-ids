"""Check the SHA-256 hashes recorded when each study plan was sealed.
Plans v1 and v3 have dated deviations appended after sealing (allowed by the plans). For v1 the recorded hash
covers the text before that entry; for v3 it covers the plan with its Deviations section reading "(none yet)".
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
plan = "study_plan_robustness_v3_SEALED"
text = open(os.path.join(D, plan + ".md"), "rb").read()
sealed = text[: text.find(b"## Deviations")] + b"## Deviations\n(none yet)\n"
lines = open(os.path.join(D, plan + ".sha256")).read().split("\n")
got = hashlib.sha256(sealed).hexdigest()
print(f"{plan}: {'OK' if got == lines[0].split()[0] else 'MISMATCH'} ({got})")
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "sealed_v3")
for line in lines[1:]:
    if line.strip():
        h, name = line.split()
        got = hashlib.sha256(open(os.path.join(S, os.path.basename(name)), "rb").read()).hexdigest()
        print(f"  sealed {os.path.basename(name)}: {'OK' if got == h else 'MISMATCH'}")
plan = "study_plan_scale_v4_SEALED"
lines = open(os.path.join(D, plan + ".sha256")).read().split("\n")
got = hashlib.sha256(open(os.path.join(D, plan + ".md"), "rb").read()).hexdigest()
print(f"{plan}: {'OK' if got == lines[0].split()[0] else 'MISMATCH'} ({got})")
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "sealed_v4")
for line in lines[1:]:
    if line.strip():
        h, name = line.split()
        got = hashlib.sha256(open(os.path.join(S, os.path.basename(name)), "rb").read()).hexdigest()
        print(f"  sealed {os.path.basename(name)}: {'OK' if got == h else 'MISMATCH'}")
plan = "study_plan_aci_v5_SEALED"
want = open(os.path.join(D, plan + ".sha256")).read().split()[0]
got = hashlib.sha256(open(os.path.join(D, plan + ".md"), "rb").read()).hexdigest()
print(f"{plan}: {'OK' if got == want else 'MISMATCH'} ({got})")
