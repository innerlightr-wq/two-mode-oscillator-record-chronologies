#!/usr/bin/env python3
"""tables.py -- emit the machine-generated classification and exclusion tables.

Writes, for each slope: every normalised orbit representative with its signed norm and its
four-way classification, and -- for each excluded orbit -- a CHECKABLE exclusion witness.

Orbit identity.  The representative norm N_rep is NOT a unique identifier: at 1+sqrt(3) nearly
every value occurs twice (N_rep = -143 occurs four times) and at sqrt(3) two values occur
twice.  Each orbit therefore carries a stable ID "<slope-tag><index>", the index being its
position in the canonical enumeration, which is sorted by the representative eta.  The
representative eta is printed alongside, so a row identifies one orbit unambiguously.

Witness validity.  A row (B excluded by A at offset d, from period P) asserts that for every
p >= P the state of A at period p-d lies BELOW the state of B at period p in height and has
strictly smaller error.  P is therefore the maximum of
    * the error threshold of Prop. 6.1 (sign(Gamma_d) dominates), in B-period coordinates;
    * the ordering threshold of Prop. 6.3, converted from q- to p-coordinates by +d;
    * the first period at which BOTH states are positive.
Every emitted row is then re-verified exactly at p = P before it is written; a row that does
not verify is not emitted, and the program fails rather than printing an unchecked claim.

Outputs:  ../tables/classification.csv, ../tables/exclusions.csv,
          ../tables/classification.tex, ../tables/exclusions_summary.tex
"""
import os, csv
from quad import Q, cmp_frac
from setups import PHI, S3, SQ3
from orbits import admissible_primitive_orbits, ring_elt, state_from_ab, mul, rho
from certificate import (cutoff, classify, gamma_d, least_decided_period, order_UV,
                         least_ordered_period, tie_sign, delta_rho)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "tables"))
os.makedirs(OUT, exist_ok=True)

TAG = {"phi": "P", "1+sqrt3": "T", "sqrt3": "S"}
NAME = {"phi": r"$\varphi$", "1+sqrt3": r"$1+\sqrt3$", "sqrt3": r"$\sqrt3$"}

def fnum(q, D):
    return float(q.a) + float(q.b) * float(D) ** 0.5

def state_at(S, o, q):
    a, b = o[2], o[3]
    R = rho(S)
    for _ in range(q):
        a, b = mul(S, (a, b), R)
    return state_from_ab(S, a, b)

def first_positive_period(S, o, tries=60):
    for q in range(tries):
        m, k = state_at(S, o, q)
        if m > 0 and k > 0:
            return q
    return None

def eps_lt(S, x, y):
    """exact: eps(x) < eps(y)?"""
    n1, d1 = S.eps_parts(*x)
    n2, d2 = S.eps_parts(*y)
    return cmp_frac(n1, d1, n2, d2) < 0

def holds_at(S, A, B, d, p):
    """Exactly: is A at period p-d below B at period p in height, with smaller error?"""
    if p - d < 0 or p < 0:
        return False
    amk, bmk = state_at(S, A, p - d), state_at(S, B, p)
    if min(amk + bmk) <= 0:
        return False
    if (S.den_err(*bmk) - S.den_err(*amk)).sign() <= 0:
        return False
    return eps_lt(S, amk, bmk)

def threshold(S, A, B, d, G):
    """P in B-period coordinates: error threshold, ordering threshold (+d), positivity."""
    P = least_decided_period(S, A, B, d, G)
    if P is None:                     # Gamma_d == 0: the integer rule decides at every p
        P = d
    for par in (0, 1):
        U, V = order_UV(S, A, B, d, parity=par)
        qo = least_ordered_period(S, U, V)
        if qo is not None:
            P = max(P, qo + d)
        if delta_rho(S) == 1:
            break
    fb, fa = first_positive_period(S, B), first_positive_period(S, A)
    if fb is None or fa is None:
        return None
    return max(P, fb, fa + d)

def witness(S, orbs, bi):
    """The competitor that excludes orbit #bi, with data verified at the reported period."""
    B = orbs[bi]
    parities = (0, 1) if delta_rho(S) == -1 else (0,)
    cands = []
    for ai, A in enumerate(orbs):
        if ai == bi:
            continue
        for par in parities:
            U0, _ = order_UV(S, A, B, 0, parity=par)
            dl = [0] if U0.sign() > 0 else [1]
            for d in dl:
                G = gamma_d(S, A, B, d)
                if G.sign() > 0:
                    continue
                if G.sign() == 0 and tie_sign(S, A, B, d, d + par) <= 0:
                    continue
                P = threshold(S, A, B, d, G)
                if P is None:
                    continue
                # re-verify exactly at P and at the next two periods
                if not all(holds_at(S, A, B, d, P + j) for j in (0, 1, 2)):
                    continue
                rule = ("sign(Gamma_d) < 0" if G.sign() < 0
                        else "Gamma_d = 0, integer tie rule")
                cands.append((P, ai, d, rule, G))
    if not cands:
        return None
    cands.sort(key=lambda c: c[:3])     # prefer the witness certified earliest
    P, ai, d, rule, G = cands[0]
    A = orbs[ai]
    return dict(A_index=ai, A_id="%s%d" % (TAG[S.name], ai), N_A=A[1], d=d,
                sign_gamma=G.sign(), gamma=str(G), certified_from_period=P, rule=rule,
                A_state=state_at(S, A, P - d), B_state=state_at(S, B, P))

rows_c, rows_e = [], []
nver = 0
for S in (PHI, S3, SQ3):
    B = cutoff(S)
    orbs = admissible_primitive_orbits(S, B)
    _, cls = classify(S, B)
    index = {(r[0], r[1], r[2], r[3]): i for i, r in enumerate(orbs)}
    for r in cls:
        absN, N, a, b, status = r
        bi = index[(absN, N, a, b)]
        eta = ring_elt(S, a, b)
        fp = first_positive_period(S, orbs[bi])
        st = state_at(S, orbs[bi], fp) if fp is not None else None
        rows_c.append(dict(orbit_id="%s%d" % (TAG[S.name], bi), slope=S.name, cutoff=B,
                           abs_N=absN, N_rep=N, eta_a=str(eta.a), eta_b=str(eta.b),
                           eta_num="%.10f" % fnum(eta, S.D),
                           first_positive_period=fp,
                           first_positive_state=("(%d,%d)" % st) if st else "",
                           classification=status))
        if status == "excluded":
            w = witness(S, orbs, bi)
            assert w is not None, "no verified exclusion witness for %s%d (N_rep=%+d)" % (
                TAG[S.name], bi, N)
            nver += 1
            rows_e.append(dict(orbit_id="%s%d" % (TAG[S.name], bi), slope=S.name,
                               abs_N=absN, N_rep=N, eta_num="%.10f" % fnum(eta, S.D),
                               competitor_id=w["A_id"], competitor_N_A=w["N_A"],
                               offset_d=w["d"], sign_gamma=w["sign_gamma"], gamma=w["gamma"],
                               certified_from_period=w["certified_from_period"],
                               A_state="(%d,%d)" % w["A_state"],
                               B_state="(%d,%d)" % w["B_state"], rule=w["rule"]))

with open(os.path.join(OUT, "classification.csv"), "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows_c[0].keys())); wr.writeheader(); wr.writerows(rows_c)
with open(os.path.join(OUT, "exclusions.csv"), "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows_e[0].keys())); wr.writeheader(); wr.writerows(rows_e)

def longtable(f, cols, header, body, ncol):
    f.write("% machine-generated by certificate/tables.py -- do not edit\n")
    f.write("\\begin{longtable}{%s}\n\\hline\n" % cols)
    f.write(header + "\\endfirsthead\n\\hline\n" + header + "\\endhead\n"
            "\\hline\n\\multicolumn{%d}{r}{\\footnotesize continued}\\\\\n\\endfoot\n"
            "\\hline\n\\endlastfoot\n" % ncol)
    for line in body:
        f.write(line)
    f.write("\\end{longtable}\n")

with open(os.path.join(OUT, "classification.tex"), "w") as f:
    hdr = ("id & $\\alpha$ & $|N|$ & $N_{\\mathrm{rep}}$ & $\\eta$ (rep) & "
           "first positive state & class \\\\\n\\hline\n")
    body = ["%s & %s & %d & %+d & %.6f & %s & %s \\\\\n" %
            (r["orbit_id"], NAME[r["slope"]], r["abs_N"], r["N_rep"], float(r["eta_num"]),
             r["first_positive_state"] or "--", r["classification"]) for r in rows_c]
    longtable(f, "llrrlll", hdr, body, 7)

with open(os.path.join(OUT, "exclusions_summary.tex"), "w") as f:
    hdr = ("id & $\\alpha$ & $N_{\\mathrm{rep}}$ & by & $N_A$ & $d$ & $P$ & "
           "$A$ at $P-d$ & $B$ at $P$ & rule \\\\\n\\hline\n")
    body = ["%s & %s & %+d & %s & %+d & %d & %d & %s & %s & %s \\\\\n" %
            (r["orbit_id"], NAME[r["slope"]], r["N_rep"], r["competitor_id"],
             r["competitor_N_A"], r["offset_d"], r["certified_from_period"],
             r["A_state"], r["B_state"],
             "$\\Gamma_d<0$" if r["sign_gamma"] < 0 else "tie rule") for r in rows_e]
    longtable(f, "llrlrrrlll", hdr, body, 10)

print("classification rows: %d   exclusion rows: %d   (every exclusion re-verified exactly "
      "at P, P+1, P+2)" % (len(rows_c), len(rows_e)))
from collections import Counter
for S in (PHI, S3, SQ3):
    sub = [r for r in rows_c if r["slope"] == S.name]
    print("  %-9s %d orbits: %s" % (S.name, len(sub),
                                    dict(Counter(r["classification"] for r in sub))))
print("-> ../tables/{classification,exclusions}.csv, "
      "../tables/{classification,exclusions_summary}.tex")
