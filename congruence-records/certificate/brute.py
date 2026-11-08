"""Independent exact brute-force record finder.  Written from the problem statement only.

A state (m,k), m,k positive odd, is a STRICT CHRONOLOGICAL RECORD iff
  eps(m,k) < eps(m',k')  for every state with 2h' < 2h, and
  eps(m,k) <= eps(m',k')  for every state with 2h' == 2h  (weak minimality at equal height).
For irrational alpha distinct states have distinct heights, so the tie clause is vacuous;
it is implemented anyway rather than assumed away.

Enumeration is over ALL odd pairs with 2h = m*alpha + k <= bound -- no pruning, no window,
no defect cutoff.  Ordering and every eps comparison is an exact sign test in Z[sqrt D].
"""
import sys
from fractions import Fraction
from quad import Q, cmp_frac
from setups import PHI, S3

def enumerate_states(S, two_h_bound):
    """All (m,k) odd positive with m*alpha + k <= two_h_bound."""
    al = S.alpha()
    # m*alpha <= bound  =>  m <= bound/alpha ; use exact rational bound via conjugate
    out = []
    m = 1
    while True:
        # smallest 2h for this m is m*alpha + 1
        lo = S.den_err(m, 1)
        if (lo - Q(two_h_bound, 0, S.D)).sign() > 0:
            break
        k = 1
        while True:
            d = S.den_err(m, k)
            if (d - Q(two_h_bound, 0, S.D)).sign() > 0:
                break
            out.append((m, k))
            k += 2
        m += 2
    return out

def records(S, two_h_bound, verbose=False):
    st = enumerate_states(S, two_h_bound)
    # exact sort by 2h; float only as a presort key, then verified pairwise exactly
    def fkey(mk):
        d = S.den_err(*mk)
        return float(d.a) + float(d.b)*(float(S.D)**0.5)
    st.sort(key=fkey)
    for i in range(len(st)-1):                      # verify the order exactly
        c = (S.den_err(*st[i+1]) - S.den_err(*st[i])).sign()
        assert c >= 0, "presort order not confirmed exactly at %d" % i
    recs = []
    best_n, best_d = None, None
    i = 0
    while i < len(st):
        j = i
        H = S.den_err(*st[i])
        while j+1 < len(st) and (S.den_err(*st[j+1]) - H).sign() == 0:
            j += 1
        group = st[i:j+1]                            # equal-height group
        winners = []
        for (m, k) in group:
            n, d = S.eps_parts(m, k)
            if best_n is None:
                winners.append((m, k, n, d)); continue
            c = cmp_frac(n, d, best_n, best_d)
            if c < 0:
                winners.append((m, k, n, d))
        if winners:
            # strict against everything lower; weakly minimal within the group
            bn, bd = None, None
            for (m, k, n, d) in winners:
                if bn is None or cmp_frac(n, d, bn, bd) < 0: bn, bd = n, d
            for (m, k, n, d) in winners:
                if cmp_frac(n, d, bn, bd) == 0:
                    recs.append((m, k))
            best_n, best_d = bn, bd
        i = j+1
    return recs, len(st)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    for S in ([PHI, S3] if which == "both" else [PHI if which=="phi" else S3]):
        recs, nst = records(S, B)
        print("%s: brute force over %d odd states with 2h <= %d -> %d records"
              % (S.name, nst, B, len(recs)))
        for (m, k) in recs:
            print("    m=%-8d k=%-8d N=%-6d" % (m, k, S.N(m, k)))
