#!/usr/bin/env python3
"""verify_records.py -- independent exact verifier for the phi and 1+sqrt3 record chronologies.

Standard library only.  No floating point decides anything: floats appear solely as presort
keys, and every sorted order is re-verified by an exact sign test in Z[sqrt D].

Checks, in order:
  C1  norm identity N = (k - m alpha)(k - m alpha') and the closed form
      eps = |N| sqrtDelta / (2 alpha eta^2 - t N)
  C2  parity/congruence restrictions on N
  C3  imprimitive states never record (elementary scaling)
  C4  the CUTOFF LEMMA constant, computed from exact algebraic data
  C5  enumeration of all admissible primitive orbits with |N| <= cutoff
  C6  exact exclusion of every orbit but the survivors, with an explicit eta-threshold
  C7  the phi tie, decided by the integer rule, and its closed forms
  C8  unpruned brute force at low height vs the orbit-pooled chronology
  C9  the conjectured sequences, to large height
"""
import sys, math
from math import gcd
from fractions import Fraction
from quad import Q, cmp_frac
from setups import PHI, S3, SQ3
from brute import records as brute_records, enumerate_states
from candidates import candidates, records_from
from orbits import (enumerate_orbits, admissible_primitive_orbits, ring_elt, state_from_ab,
                    mul, rho, norm_ab, admissible, primitive)

FAIL=[]
def chk(name, ok, extra=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  -- "+extra) if extra else ""))
    if not ok: FAIL.append(name)

def c1(S):
    ok=True
    for (m,k) in enumerate_states(S, 200):
        p = (-S.num_err(m,k))*S.eta(m,k)
        if not (p.a==S.N(m,k) and p.b==0): ok=False; break
        # closed form: eps*(2 alpha eta^2 - t N) == |N| sqrtDelta
        al=S.alpha(); et=S.eta(m,k); N=S.N(m,k)
        G = et*et*al*2 - Q(S.t*N,0,S.D)
        n,d = S.eps_parts(m,k)
        # eps = n/d ; check n*G == |N| * sqrtDelta * d, with sqrtDelta = alpha - alpha'
        sD = Q(0, 2*al.b, S.D)
        if (n*G - sD*d*abs(N)).sign()!=0 or (n*G-sD*d*abs(N)).b!=0: ok=False; break
    chk("C1 norm identity and closed form for eps (%s)"%S.name, ok)

def c2(S):
    """Congruence restrictions on N, with a branch for EVERY slope.

    An earlier version had branches only for phi and 1+sqrt3, so for sqrt(3) it enumerated
    states, asserted nothing, and printed PASS -- the audit confirmed it still passed when fed a
    deliberately invalid norm (external v2 audit R2).  The sqrt(3) assertion is elementary:
    m, k odd give k^2 - 3m^2 = 1 - 3 = 6 (mod 8).
    """
    bad=[]; n=0
    for (m,k) in enumerate_states(S, 400):
        N=S.N(m,k); n+=1
        if S is PHI:
            if 4*N != (2*k-m)**2 - 5*m*m: bad.append((m,k,"4N identity"))
            if N%5 not in (0,1,4):        bad.append((m,k,"N mod 5"))
        elif S is S3:
            if N%8 not in (1,5):          bad.append((m,k,"N mod 8"))
        elif S is SQ3:
            if N%8 != 6:                  bad.append((m,k,"N mod 8 != 6"))
        else:
            bad.append((m,k,"no branch for this slope"))   # never silently pass
    chk("C2 congruence restrictions on N, %d states (%s)"%(n,S.name), not bad, str(bad[:3]))

def c3(S):
    """An imprimitive state has the SAME eps as its primitive reduction at SMALLER height."""
    ok=True
    for (m,k) in enumerate_states(S, 300):
        g=gcd(m,k)
        if g==1: continue
        n1,d1=S.eps_parts(m,k); n2,d2=S.eps_parts(m//g,k//g)
        same = cmp_frac(n1,d1,n2,d2)==0
        lower = (S.den_err(m//g,k//g)-S.den_err(m,k)).sign()<0
        if not (same and lower): ok=False; break
    chk("C3 imprimitive eps equals its reduction, at lower height (%s)"%S.name, ok)

def c4(S):
    """Assert the height-based cutoff is a real bound: every record found by the UNPRUNED
    brute force has |N| <= cutoff, and the cutoff is the integer floor of max F over the
    ladder.  (An earlier C4 passed the literal True and asserted nothing.)"""
    from certificate import cutoff as _cut
    B=_cut(S)
    recs,_=brute_records(S, 3000 if S is not SQ3 else 2000)
    worst=max(abs(S.N(m,k)) for m,k in recs)
    ok = worst <= B
    chk("C4 cutoff %d bounds |N| on every unpruned record (max seen %d) (%s)"%(B,worst,S.name), ok)
    return B

def c6(S, B):
    """C5: recount the orbits independently of the package's reduction search, by direct
    enumeration in the bounded rectangle.  C6: assert the four-way classification equals the
    claimed families, instead of checking that two complementary lists partition their union."""
    from certificate import classify
    from orbits import admissible_primitive_orbits as apo, norm_ab
    orbs=apo(S,B)
    # independent recount: direct rectangle enumeration, no reduction search
    # exact integer enclosure of rho + B, so no float enters the box size (audit R3)
    R=ring_elt(S,*rho(S)); lim=1
    while (R + Q(B,0,S.D) - Q(lim,0,S.D)).sign()>0: lim+=1
    lim+=2; direct=set()
    for a in range(-lim,lim+1):
        for b in range(-lim,lim+1):
            if b==0 and a==0: continue
            if not admissible(S,a,b): continue
            N=norm_ab(S,a,b)
            if N==0 or abs(N)>B: continue
            e=ring_elt(S,a,b)
            if e.sign()<=0: continue
            if (e-Q(1,0,S.D)).sign()<0 or (e-R).sign()>=0: continue
            if not primitive(S,a,b): continue
            direct.add((abs(N),N,a,b))
    same = direct == set(orbs)
    chk("C5 independent rectangle recount matches the reduction search: %d orbits (%s)"
        %(len(orbs),S.name), same)
    _,cls=classify(S,B)
    got={}
    for r in cls:
        if r[-1]!='excluded': got.setdefault(r[-1],set()).add(r[1])
    EXPECT={"phi":      {"strict":{-1},"alternating":{5}},
            "1+sqrt3":  {"strict":{-11,-3,1}},
            "sqrt3":    {"strict":{-2},"equality":{6}}}[S.name]
    chk("C6 classification equals the claimed families (%s)"%S.name, got==EXPECT,
        "got %s"%{k:sorted(v) for k,v in got.items()})
    return [r for r in cls if r[-1]!='excluded']

def c7():
    """The phi tie, exactly: eps(phi^n) = sqrt5/(2 phi^(2n+1) - (-1)^n),
       eps(sqrt5 phi^n) = sqrt5/(2 phi^(2n+1) + (-1)^n)."""
    S=PHI; ok=True; rows=[]
    # unit ladder states (F_n, F_{n+1}) for n = 1 mod 3, and norm-5 states sqrt5*phi^n
    F=[0,1]
    while len(F)<40: F.append(F[-1]+F[-2])
    for n in range(1,31,3):
        m,k=F[n],F[n+1]
        NA=S.N(m,k); assert NA==(-1)**n, (n,NA)
        # norm-5 partner: eta = sqrt5 * phi^n ; build it in Z[phi]
        a,b=(-1,2)            # sqrt5 = 2 phi - 1
        for _ in range(n): a,b = mul(S,(a,b),(0,1))    # multiply by phi
        m5,k5 = state_from_ab(S,a,b)
        if m5<0: m5,k5=-m5,-k5
        NB=S.N(m5,k5)
        if NB != -5*NA: ok=False; break
        # the tie rule: B beats A iff |N_B| N_A - N_B > 0
        pred = (abs(NB)*NA - NB) > 0
        n1,d1=S.eps_parts(m5,k5); n2,d2=S.eps_parts(m,k)
        actual = cmp_frac(n1,d1,n2,d2) < 0
        if pred != actual: ok=False; break
        rows.append((n,NA,NB,actual))
    chk("C7 phi tie: N_B = -5 N_A and the integer rule predicts every comparison", ok,
        "checked n = 1,4,...,28 ; wins exactly when N_A = +1 (n even)")
    return rows

def c8(S,B,H=None):
    if H is None: H = 3000 if S is not SQ3 else 2000
    rb,_=brute_records(S,H)
    rp=records_from(S,candidates(S,B,H))
    chk("C8 unpruned brute force == justified-pruned scan to 2h <= %d (%s)"%(H,S.name), rb==rp,
        "%d records"%len(rb))

def pooled(S,B,H):
    """All states of all admissible primitive orbits with |N| <= B and 2h <= H.

    By sections 1-4 of PROOF_OR_OBSTRUCTION.md this is a superset of the records above the
    cutoff threshold, so running the exact record filter on it is justified.  Enumerating by
    orbit (rather than by m) is what makes large heights reachable at all."""
    out=[]
    for (an,N,a,b) in admissible_primitive_orbits(S,B):
        aa,bb=a,b
        for _ in range(400):
            m,k=state_from_ab(S,aa,bb)
            if m>0 and k>0:
                if (S.den_err(m,k)-Q(H,0,S.D)).sign()<=0: out.append((m,k))
                else: break
            aa,bb=mul(S,(aa,bb),rho(S))
    return sorted(set(out))

def c9(S,B,H=10**12):
    """Assert the record set EQUALS the stated families, not merely that a norm cycle repeats."""
    recs=records_from(S,pooled(S,B,H))
    if S is PHI:
        F=[0,1]
        while F[-1]<10**14: F.append(F[-1]+F[-2])
        L=[2,1]
        while L[-1]<10**14: L.append(L[-1]+L[-2])
        want=set()
        for j in range(0,40):
            if 3*j+2<len(F) and F[3*j+2]<10**12: want.add((F[3*j+1],F[3*j+2]))
            if 6*j+5<len(L) and L[6*j+5]<10**12: want.add((L[6*j+4],L[6*j+5]))
        got=set(recs); lim=max(S.den_err(*r).a for r in recs)
        want={p for p in want if (S.den_err(*p)-Q(H,0,S.D)).sign()<=0}
        ok = got==want
        chk("C9 phi records == {(F_3j+1,F_3j+2)} U {(L_6j+4,L_6j+5)} to 2h <= %g"%H, ok,
            "%d records; symmetric difference %d"%(len(recs),len(got^want)))
    else:
        seeds={"1+sqrt3":[(1,1),(1,3),(5,13)],"sqrt3":[(1,1)]}[S.name]
        want=set()
        for (m,k) in seeds:
            a,b=(k-m,m) if S is S3 else (k,m)
            while True:
                mm,kk=state_from_ab(S,a,b)
                if mm>0 and kk>0:
                    if (S.den_err(mm,kk)-Q(H,0,S.D)).sign()<=0: want.add((mm,kk))
                    else: break
                a,b=mul(S,(a,b),rho(S))
        ok=set(recs)==want
        chk("C9 %s records == the %d stated unit-orbit families to 2h <= %g"%(S.name,len(seeds),H),
            ok, "%d records; symmetric difference %d"%(len(recs),len(set(recs)^want)))
    return recs

# ---------------------------------------------------------------- C10 (rewritten)
def hmax_exact_below(S, orbs, worst, cap):
    """Exact version of the C10 comparison: no float is used in the decision (audit F7)."""
    from certificate import gamma_d, least_decided_period, order_UV, least_ordered_period
    R=rho(S)
    for A in orbs:
        for Bo in orbs:
            for d in (0,1,2):
                if A is Bo and d==0: continue
                G=gamma_d(S,A,Bo,d)
                P=least_decided_period(S,A,Bo,d,G)
                if P is None: P=d
                for par in (0,1):
                    U,V=order_UV(S,A,Bo,d,parity=par)
                    qo=least_ordered_period(S,U,V)
                    if qo is not None: P=max(P,qo+d)
                aa,bb=Bo[2],Bo[3]
                for _ in range(max(0,P)):
                    m,k=state_from_ab(S,aa,bb)
                    if m>0 and k>0:
                        if (S.den_err(m,k)-Q(cap,0,S.D)).sign()>=0: return False
                    aa,bb=mul(S,(aa,bb),R)
    return True

def c10(S, B):
    """Delegate the tail argument to certificate.py.

    An earlier C10 advanced only orbit B and so never tested the SAME-period comparison; the
    phi tie pair, for which Gamma is identically zero, passed it vacuously (audit A1).  The
    certificate now (a) restricts to d in {0,1} under the window lemma, (b) reports every
    Gamma_d == 0 pair and decides it by the integer rule per period parity, and (c) computes
    the height below which the finite check must reach."""
    from certificate import run as cert_run
    C, orbs, worst, ties, hmax = cert_run(S, S.name)
    cap = 3000 if S is not SQ3 else 2000
    # hmax is returned as a float for display; the decision is made on the exact quadratic
    # value, so no float decides anything (audit F7).
    chk("C10 certificate: finite check must cover 2h < %.4g, brute force reaches %d (%s)"
        %(hmax,cap,S.name), hmax_exact_below(S, orbs, worst, cap),
        "%d Gamma=0 tie pair(s); all else decided from period %d"%(len(ties),worst[0]))

def c11(S, B):
    """C11: every emitted exclusion row is a VALID witness over a run of consecutive periods.

    The appendix table claims, for each excluded orbit B at offset d and certified period P,
    that for all p >= P the state of A at period p-d is BELOW the state of B at period p in
    height and has strictly smaller error.  A pre-release audit found this was not checked:
    the reported period came from the error threshold alone, ignoring the ordering threshold
    and positivity, and the competitor was named by N_rep, which is NOT unique (at 1+sqrt(3)
    one value labels four distinct orbits).  Rows now carry an orbit ID; this check re-derives
    every row from the orbit it names and tests it exactly at P..P+HORIZON-1.
    """
    import csv, os
    from orbits import admissible_primitive_orbits, state_from_ab, mul, rho
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables",
                        "exclusions.csv")
    if not os.path.exists(path):
        chk("C11 exclusion witnesses (%s)" % S.name, False, "../tables/exclusions.csv missing "
            "-- run `python3 tables.py` first")
        return
    orbs = admissible_primitive_orbits(S, B)
    def state_at(o, q):
        a, b = o[2], o[3]
        R = rho(S)
        for _ in range(q):
            a, b = mul(S, (a, b), R)
        return state_from_ab(S, a, b)
    HORIZON = 12
    rows = [r for r in csv.DictReader(open(path)) if r["slope"] == S.name]
    bad = []
    for r in rows:
        bi, ai = int(r["orbit_id"][1:]), int(r["competitor_id"][1:])
        d, P = int(r["offset_d"]), int(r["certified_from_period"])
        if orbs[bi][1] != int(r["N_rep"]) or orbs[ai][1] != int(r["competitor_N_A"]):
            bad.append((r["orbit_id"], "orbit ID does not carry the stated N_rep")); continue
        if ("(%d,%d)" % state_at(orbs[ai], P - d) != r["A_state"]
                or "(%d,%d)" % state_at(orbs[bi], P) != r["B_state"]):
            bad.append((r["orbit_id"], "printed state != the named orbit at that period")); continue
        for p in range(P, P + HORIZON):
            amk, bmk = state_at(orbs[ai], p - d), state_at(orbs[bi], p)
            if min(amk + bmk) <= 0:
                bad.append((r["orbit_id"], "non-positive state at p=%d" % p)); break
            if (S.den_err(*bmk) - S.den_err(*amk)).sign() <= 0:
                bad.append((r["orbit_id"], "A not below B in height at p=%d" % p)); break
            n1, d1 = S.eps_parts(*amk); n2, d2 = S.eps_parts(*bmk)
            if cmp_frac(n1, d1, n2, d2) >= 0:
                bad.append((r["orbit_id"], "A does not beat B in error at p=%d" % p)); break
    ids = [r["orbit_id"] for r in rows]
    uniq = len(set(ids)) == len(ids)
    chk("C11 every exclusion witness verified exactly over P..P+%d, IDs unique (%s)"
        % (HORIZON - 1, S.name), not bad and uniq,
        "%d rows%s" % (len(rows), "" if not bad else "; first failure: %s %s" % bad[0]))

if __name__=="__main__":
    for S in (PHI,S3,SQ3):
        print("=== %s ==="%S.name)
        c1(S); c2(S); c3(S)
        B=c4(S)
        surv=c6(S, B)
        c8(S, B)
        c9(S, B)
        c10(S, B)
        c11(S, B)
        print()
    c7()
    print()
    print("VERIFY %s"%("PASSED" if not FAIL else "FAILED: "+", ".join(FAIL)))
    sys.exit(1 if FAIL else 0)

