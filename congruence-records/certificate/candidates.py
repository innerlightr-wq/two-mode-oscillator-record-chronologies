"""Enumerate ALL odd states with |N| <= B up to a height bound, exactly.

This is a PRUNED scan, and the pruning is justified by the cutoff lemma proved in
PROOF_OR_OBSTRUCTION.md -- not by the conjecture.  For each odd m and each N with
|N| <= B we solve k^2 - t k m - s m^2 = N for k:
      k = (t m + sqrt(Delta m^2 + 4N)) / 2,     Delta = t^2 + 4 s,
taking the positive root and requiring an exact integer square and k odd positive.
"""
import math
from quad import Q, cmp_frac
from setups import PHI, S3

def isqrt_exact(n):
    if n < 0: return None
    r = math.isqrt(n)
    return r if r*r == n else None

def candidates(S, B, two_h_bound):
    Delta = S.t*S.t + 4*S.s
    out = []
    m = 1
    while True:
        if (S.den_err(m, 1) - Q(two_h_bound, 0, S.D)).sign() > 0:
            break
        for N in range(-B, B+1):
            r = isqrt_exact(Delta*m*m + 4*N)
            if r is None: continue
            for sgn in (+1, -1):
                num = S.t*m + sgn*r
                if num <= 0 or num % 2: continue
                k = num // 2
                if k <= 0 or k % 2 == 0: continue
                assert S.N(m, k) == N
                if (S.den_err(m, k) - Q(two_h_bound, 0, S.D)).sign() <= 0:
                    out.append((m, k))
        m += 2
    return sorted(set(out))

def records_from(S, states):
    """Exact strict-record filter on an arbitrary state list."""
    def fkey(mk):
        d = S.den_err(*mk)
        return float(d.a) + float(d.b)*(float(S.D)**0.5)
    st = sorted(states, key=fkey)
    for i in range(len(st)-1):
        assert (S.den_err(*st[i+1]) - S.den_err(*st[i])).sign() >= 0, "order unverified"
    recs = []; bn = bd = None; i = 0
    while i < len(st):
        j = i; H = S.den_err(*st[i])
        while j+1 < len(st) and (S.den_err(*st[j+1]) - H).sign() == 0: j += 1
        grp = st[i:j+1]
        cand = []
        for (m, k) in grp:
            n, d = S.eps_parts(m, k)
            if bn is None or cmp_frac(n, d, bn, bd) < 0: cand.append((m, k, n, d))
        if cand:
            mn = None
            for (m, k, n, d) in cand:
                if mn is None or cmp_frac(n, d, mn[0], mn[1]) < 0: mn = (n, d)
            for (m, k, n, d) in cand:
                if cmp_frac(n, d, mn[0], mn[1]) == 0: recs.append((m, k))
            bn, bd = mn
        i = j+1
    return recs
