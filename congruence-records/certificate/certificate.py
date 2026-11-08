#!/usr/bin/env python3
"""certificate.py -- the completeness CERTIFICATE, separated from exploratory computation.

This file contains only what the proof depends on.  Exploratory scans live in brute.py,
candidates.py and compare_notions.py and are NOT used here.

For two states A, B the exact criterion from (M2) is

    eps_B < eps_A   <=>   2 alpha Gamma > t(|N_A| N_B - |N_B| N_A),
    Gamma := |N_A| eta_B^2 - |N_B| eta_A^2.                                    (CRIT)

Let A, B lie on admissible orbits with representatives rA, rB (reduced into [1,rho)), with A
in period p-d and B in period p, d >= 0.  Then eta_A = rA rho^{p-d}, eta_B = rB rho^p and

    Gamma = rho^{2p-2d} * Gamma_d,    Gamma_d := |N_A| rB^2 rho^{2d} - |N_B| rA^2,

so **sign(Gamma) = sign(Gamma_d) is constant in p**: one exact sign per (pair, d).  Two cases.

  * Gamma_d != 0.  The right side of (CRIT) is bounded by 2 t |N_A| |N_B| in absolute value,
    so (CRIT) is decided by sign(Gamma_d) as soon as
        2 alpha rho^{2p-2d} |Gamma_d| >= 2 t |N_A| |N_B|,
    which happens for all p >= P(pair,d), computed exactly below.
  * Gamma_d == 0.  No threshold exists and none is needed: (CRIT) reads
        0 > t(|N_A| N_B - |N_B| N_A),
    an integer condition in the norms ALONE, exact for every p.  Because rho may have norm -1
    (it does for phi: rho = phi^3), the signs of N_A and N_B can flip with p, so this case is
    reported per period parity.  This is exactly the phi tie, and C10 of an earlier draft
    tested it vacuously by advancing only B -- see RETRACTIONS_AUDIT.md, A1.
"""
import sys
from fractions import Fraction
from quad import Q, cmp_frac
from setups import PHI, S3, SQ3, LATTICE
from orbits import (admissible_primitive_orbits, ring_elt, rho, mul, state_from_ab,
                    norm_ab, enumerate_orbits)

def delta_rho(S):
    """delta = Norm(rho).  The signed norm is transported by  N_q = delta^q N_rep."""
    return norm_ab(S, *rho(S))

def cutoff(S, verbose=False):
    """Norm cutoff, by the SIGN-SEPARATED proof (external v2 audit R1 supplied it).

    Setting (all three slopes): t >= 0 and alpha' < 0, so eta > 0 on positive states.  With
    H = m alpha + k, D0 = alpha - alpha', z = (k - m alpha)/H, eps = |z|,

        eta = H(D0 + t z)/(2 alpha),      |N| = H^2 eps (D0 + t z)/(2 alpha).

    For successive positive ladder states A, C and a strict record B with H_A < H_B <= H_C
    (ladder heights increase, since the unit matrices have positive entries),

        |N_B| < H_C^2 eps_A (D0 + t eps_A)/(2 alpha) =: F(Y, n),      Y = eta_A^2, n = N_A.

    Only HEIGHT ordering is used.  Writing u = t/(2 alpha Y) when t > 0, and u = 1/(2 alpha Y)
    for phi where L = t = 1, the closed forms are

        phi, n = -1 :  F = R^2 (1 - u/R^2)^2 (1 + 2u)/(1 + u)^2  <  R^2 = phi^6 = 17.944...
                       because (1 - u/R^2)^2 < 1 and (1+2u)/(1+u)^2 < 1 for u > 0.
        phi, n = +1 :  F = R^2 (1 + u/R^2)^2/(1 - u)^2, INCREASING in u, so decreasing in Y;
                       its maximum is at the first positive-norm predecessor Y = phi^8.
        1+sqrt3     :  F = R^2 ((1 - u/R^2)/(1 - u))^2, increasing in u, so maximal at the
                       first ladder state Y = (2+sqrt3)^2.
        sqrt3 (t=0) :  F = L R^2 identically.

    **The previous justification -- "F is monotone in Y, so its maximum is in the first two
    states" -- is false.**  At phi the two sign branches move in OPPOSITE directions: the
    n = -1 subsequence increases (17.5116, 17.9435, 17.9443, ...) while the n = +1 subsequence
    decreases (18.1960, 17.9450, 17.9443, ...).  Sampling six values cannot bound an infinite
    ladder; separating the signs does.  The bounds themselves are unchanged.

    Returns the integer bound; the endpoint inequalities are decided exactly.
    """
    al=S.alpha(); R=ring_elt(S,*rho(S)); dl=delta_rho(S); lat=LATTICE[S.name]
    L=lat["L"]; etaL=ring_elt(S,*lat["ETA_L"]); nL=norm_ab(S,*lat["ETA_L"])
    D0=Q(0, 2*S.alpha().b, S.D)
    def F(Y, n):
        """F(Y,n) exactly, as a pair (num, den) of Q elements."""
        den = al*Y*2 - Q(S.t*n,0,S.D)                       # 2 alpha Y - t n > 0
        assert den.sign()>0
        epsN = D0*L                                          # eps_A = epsN/den
        hcn  = al*Y*R*R*2 - Q(S.t*dl*n,0,S.D)                # numerator of H_C/H_A
        hcd  = R*den
        top  = D0*den + epsN*S.t
        bot  = D0*den + epsN*(S.t*(1 if n>0 else -1))
        assert bot.sign()>0
        return hcn*hcn*top*L, hcd*hcd*bot
    cands=[]
    if S.t==0:
        cands.append((("t=0: F = L R^2 identically"), (R*R*L, Q(1,0,S.D))))
    elif dl==-1:
        # negative-norm branch bounded by R^2 (proved above, no endpoint needed);
        # positive-norm branch maximal at its FIRST predecessor.
        cands.append(("n<0 branch: F < R^2", (R*R, Q(1,0,S.D))))
        eta=etaL; n=nL
        while n>0 or True:
            if n>0: break
            eta=eta*R; n=n*dl
        cands.append(("n>0 branch: F at its first predecessor", F(eta*eta, n)))
    else:
        cands.append(("increasing in u: F at the first ladder state", F(etaL*etaL, nL)))
    best=None; label=None
    for lab,(fn,fd) in cands:
        if best is None or (fn*best[1]-best[0]*fd).sign()>0: best=(fn,fd); label=lab
    B=1
    while (best[0]-best[1]*B).sign()>0: B+=1
    B-=1
    if verbose:
        for lab,(fn,fd) in cands:
            v=(float(fn.a)+float(fn.b)*float(S.D)**0.5)/(float(fd.a)+float(fd.b)*float(S.D)**0.5)
            print("      %-44s %.10f"%(lab,v))
        print("      binding: %s  ->  integer cutoff %d"%(label,B))
    return B

def gamma_d(S, A, Bo, d):
    """Gamma_d = |N_A| rB^2 rho^{2d} - |N_B| rA^2, exact."""
    R=ring_elt(S,*rho(S))
    rA=ring_elt(S,A[2],A[3]); rB=ring_elt(S,Bo[2],Bo[3])
    t=rB*rB*A[0]
    for _ in range(2*d): t=t*R
    return t - rA*rA*Bo[0]

def least_decided_period(S, A, Bo, d, G):
    """Least p with 2 alpha rho^{2p-2d}|G| >= 2 t |N_A||N_B| ; None if G == 0."""
    if G.sign()==0: return None
    al=S.alpha(); R=ring_elt(S,*rho(S)); bound=Q(S.t*A[0]*Bo[0],0,S.D)
    # Gamma = rho^{2p-2d} Gamma_d, so at p = d the factor is rho^0 = 1 and NOTHING is
    # pre-multiplied.  An earlier version multiplied by rho^{2d} here, which inflated the left
    # side and returned p too small: at alpha = 1+sqrt3 that mispredicted 51 of the ordered
    # (A,B,d) comparisons, with the witness A = (|N|=3, N=-3), B = (|N|=193, N=193), d = 1,
    # where it claimed decidedness at p = 1 although eps(1,15) > eps(1,1) (external audit F2).
    lhs=al*abs(G); p=d
    while (lhs-bound).sign()<=0:          # STRICT domination before claiming a strict sign
        lhs=lhs*R*R; p+=1
        assert p<400
    return p

def tie_sign(S, A, Bo, d, p):
    """For Gamma_d == 0: the exact sign of eps_B - eps_A, as a THREE-WAY answer.

    With A at period p-d and B at period p, the transported signed norms are
    N_A = delta^{p-d} n_A and N_B = delta^p n_B, and the criterion with Gamma = 0 reads

        sign(eps_B - eps_A) = sign( t (|N_A| N_B - |N_B| N_A) ).

    Returns -1 (B strictly beats A), 0 (EXACTLY EQUAL -- so B is not a strict record), +1.
    An earlier `tie_rule` dropped the factor t and the offset d from the transport, so it
    could not express equality at all: for t = 0 (alpha = sqrt3) the right side is identically
    zero, i.e. permanent equality, which it reported as "B does not beat A" -- erasing the
    strict/weak distinction that Theorem C turns on (external audit F4).
    """
    dl=delta_rho(S)
    NA=A[1]*(dl**(p-d)); NB=Bo[1]*(dl**p)
    v=S.t*(A[0]*NB - Bo[0]*NA)
    return 0 if v==0 else (1 if v>0 else -1)

def order_UV(S, A, Bo, d, parity=0):
    """Cross-orbit HEIGHT ordering, exactly, with the SIGNED norm transported.

    With A at period q and B at period q+d, from 2h = (2 alpha eta - t N/eta)/sqrtDelta,

        2 sqrtDelta (h_B - h_A) = 2 alpha(eta_B - eta_A) - t(N_B/eta_B - N_A/eta_A).

    Substituting eta_A = rA rho^q, eta_B = rB rho^{q+d} and -- this is the part an earlier
    version got wrong -- the SIGNED norms N_A(q) = delta^q N_A, N_B(q+d) = delta^{q+d} N_B with
    delta = Norm(rho), then clearing the positive factor rho^{-q} rA rB rho^d:

        sign(h_B - h_A) = sign(rho^{2q} U - V),
        U := 2 alpha (rB rho^d - rA) rA rB rho^d,
        V := delta^q * t (delta^d N_B rA - N_A rB rho^d).

    U is independent of q; V depends on q only through delta^q, i.e. only through the PARITY of
    q when delta = -1 (which is the case for phi, rho = phi^3).  `parity` selects it.

    The earlier version used the representatives' norms unadjusted.  That was harmless on these
    three inputs -- the threshold below uses |V|, which is parity-independent, and the
    asymptotic sign is sign(U) -- but it is wrong wherever U == 0, and it is exactly the
    "magnitude forgets the iteration parity" failure that audit A2 and A11 already produced
    twice.  Sign is now part of the transported state (audit A16).
    """
    al=S.alpha(); R=ring_elt(S,*rho(S)); dl=delta_rho(S)
    rA=ring_elt(S,A[2],A[3]); rB=ring_elt(S,Bo[2],Bo[3])
    rBd=rB
    for _ in range(d): rBd=rBd*R
    U = al*(rBd-rA)*rA*rBd*2
    NA = A[1]*(dl**parity); NB = Bo[1]*(dl**(parity+d))
    V = (Q(NB,0,S.D)*rA - Q(NA,0,S.D)*rBd)*S.t
    return U, V

def u_zero_is_structural(S, orbs):
    """U_d = 0 cannot occur between DISTINCT normalised representatives, and would force V = 0.

    U_d = 2 alpha (rB rho^d - rA) rA rB rho^d with alpha, rA, rB, rho^d > 0, so

        U_d = 0  <=>  rA = rB rho^d.

    For d >= 1 that forces rA = rB rho^d >= rho, contradicting rA < rho; for d = 0 it forces
    rA = rB, i.e. the same representative, hence the same orbit.  So with distinct
    representatives in [1, rho) it never happens.  Moreover, were it to happen, taking norms
    gives N_A = delta^d N_B and substituting both identities into

        V = delta^q t(delta^d N_B rA - N_A rB rho^d)

    gives V = 0 identically.  So U_d = 0 means "the same arithmetic state after an index shift",
    not two distinct states with a parity-dependent height ordering -- unlike Gamma_d = 0, which
    genuinely occurs between distinct states and leaves the lower-order term to decide.

    Consequence for an exact checker: encountering U = 0 with V != 0 signals inconsistent data
    or an arithmetic error, and is asserted against below.
    """
    R=ring_elt(S,*rho(S)); one=Q(1,0,S.D)
    for o in orbs:
        e=ring_elt(S,o[2],o[3])
        assert (e-one).sign()>=0 and (e-R).sign()<0, "representative outside [1,rho)"
    seen={}
    for o in orbs:
        e=ring_elt(S,o[2],o[3]); key=(e.a,e.b)
        assert key not in seen, "two orbits share a representative"
        seen[key]=o
    bad=0
    for A in orbs:
        for Bo in orbs:
            for d in range(0,3):
                if A is Bo and d==0: continue
                for par in (0,1):
                    U,V=order_UV(S,A,Bo,d,parity=par)
                    if U.sign()==0:
                        bad+=1
                        assert V.sign()==0, "U == 0 with V != 0: inconsistent data"
                    if delta_rho(S)==1: break
    return bad

def representative_invariance(S, orbs, shifts=4, periods=5):
    """delta^{q'} N'_rep = delta^q N_rep when the representative is advanced j steps.

    The signed norm belongs to the arithmetic STATE; the iteration parity is relative to the
    chosen representative.  Changing representative by j steps sends N_rep -> delta^j N_rep and
    q -> q - j, so the reconstructed signed norm is unchanged.  Regression check.
    """
    dl=delta_rho(S); ok=True
    for o in orbs:
        for j in range(1, shifts):
            aa,bb=o[2],o[3]
            for _ in range(j): aa,bb=mul(S,(aa,bb),rho(S))
            Nrep2=norm_ab(S,aa,bb)
            if Nrep2 != (dl**j)*o[1]: ok=False
            for q in range(periods):
                if (dl**q)*o[1] != (dl**(q-j))*Nrep2: ok=False
    return ok

def least_ordered_period(S, U, V):
    """Least q with rho^{2q}|U| > |V| ; None if U == 0 (then the sign is -sign(V) for all q)."""
    if U.sign()==0: return None
    R=ring_elt(S,*rho(S)); lhs=abs(U); rhs=abs(V); q=0
    while (lhs-rhs).sign()<=0:
        lhs=lhs*R*R; q+=1; assert q<400
    return q

def classify(S, B=None):
    """Per-orbit status under the EXACT criterion, as a three-way answer.

    For each orbit O, compare its period-p state against the latest earlier-height state of
    every orbit (offsets d in {0,1}, both period parities where delta = -1), using

        eps_B < eps_A  <=>  2 alpha Gamma > t(|N_A| N_B - |N_B| N_A),   Gamma = rho^{2p-2d} Gamma_d,

    decided by sign(Gamma_d) above the certified threshold, and by `tie_sign` when Gamma_d = 0.
    Status is one of
        'strict'            -- beats every earlier competitor strictly, at every period parity
        'alternating'       -- beats them at ONE period parity and loses at the other; this is
                               the phi Lucas ladder, which records every other period
        'equality'          -- ties exactly with some earlier competitor, so NOT a strict record;
                               it supplies weak records forever (the sqrt(3) norm +6 companion)
        'excluded'          -- strictly loses at every parity.

    This replaces `orbits.decide`, which (a) compared leading terms only, (b) recorded an
    equality only against a SAME-period competitor and so missed the previous-period one, and
    (c) had no three-way outcome -- consequently labelling the sqrt(3) norm +6 companion a
    strict record family even though (1,3) repeats eps(1,1) exactly (external audit F4).
    """
    if B is None: B=cutoff(S)
    orbs=admissible_primitive_orbits(S,B); out=[]
    parities=(0,1) if delta_rho(S)==-1 else (0,)
    for i,Bo in enumerate(orbs):
        per={}
        for par in parities:
            v='strict'
            for j,A in enumerate(orbs):
                # Which A-state is the LATEST one strictly below B in height?  Decide it with
                # the certified cross-orbit ordering: order_UV(A,B,0) gives sign(h_B - h_A) at
                # equal periods.  If positive, A's period-p state is below B, so the competitor
                # offset is d = 0; otherwise it is the period-(p-1) state, d = 1.
                if i==j: dl_=[1]
                else:
                    U0,_=order_UV(S,A,Bo,0,parity=par)
                    dl_=[0] if U0.sign()>0 else [1]
                for d in dl_:
                    G=gamma_d(S,A,Bo,d)
                    if G.sign()==0:
                        ts=tie_sign(S,A,Bo,d,d+par)
                        if ts>0: v='excluded'
                        elif ts==0 and v=='strict': v='equality'
                    elif G.sign()<0:
                        v='excluded'
                    if v=='excluded': break
                if v=='excluded': break
            per[par]=v
        vals=set(per.values())
        if vals=={'strict'}:              verdict='strict'
        elif 'equality' in vals and 'excluded' not in vals: verdict='equality'
        elif vals=={'excluded'}:          verdict='excluded'
        else:                             verdict='alternating'   # records at one parity only
        out.append(Bo+(verdict,))
    return orbs, out

def run(S, label):
    print("="*78); print("CERTIFICATE: %s"%label); print("="*78)
    C=cutoff(S)
    L=LATTICE[S.name]["L"]
    print("  comparison ladder has |N| = %d ; cutoff: every record with a preceding ladder member"%L)
    print("  has |N| <= %d"%C)
    orbs=[o for o in admissible_primitive_orbits(S, C) ]
    _, cls = classify(S, C)
    strict=[r for r in cls if r[-1]=='strict']; eqs=[r for r in cls if r[-1]=='equality']
    alt=[r for r in cls if r[-1]=='alternating']
    print("  admissible primitive orbits with |N| <= %d : %d"%(C,len(orbs)))
    print("  classification: %d STRICT, %d ALTERNATING (record every other period), %d permanent-EQUALITY, %d excluded"
          %(len(strict),len(alt),len(eqs),len(cls)-len(strict)-len(alt)-len(eqs)))
    for r in strict: print("      strict  : N=%+d  eta=%s"%(r[1],ring_elt(S,r[2],r[3])))
    for r in alt:    print("      alternating: N=%+d  eta=%s  (records at one period parity)"%(r[1],ring_elt(S,r[2],r[3])))
    for r in eqs:    print("      equality: N=%+d  eta=%s  (weak records forever, not strict)"%(r[1],ring_elt(S,r[2],r[3])))
    # WINDOW LEMMA (audit A3, restated after review as THREE separate statements; eps-decrease
    # alone does NOT give d in {0,1}).
    #   (W1) eps decreases strictly along every orbit                        -- checked below
    #   (W2) normalisation: every representative lies in [1,rho), so for any orbits O, O'
    #        the period-(p-1) state of O lies below the period-p state of O' in eta, because
    #        r_O rho^{p-1} < r_O' rho^p  <=>  r_O/r_O' < rho, and r_O, r_O' in [1,rho).
    #   (W3) height-bracketing: ordering by eta equals ordering by h, valid once
    #        eta^2 > t|N|/(2 alpha) (differentiate (M1))                      -- checked below
    # Given (W1)+(W2)+(W3): if B beats every state of periods p and p-1 below it, it beats all
    # earlier states, since a state of orbit O in period q <= p-2 has eps larger than O's
    # period-(p-1) state, which (W2) places below B and B already beat.
    # eps decreases strictly along every orbit (checked below), so
    # if B beats every state of periods p and p-1 lying below it, it beats every earlier state
    # too: a state of orbit O in period q <= p-2 has eps > eps(O's state in period p-1), which
    # B already beat.  Hence only d in {0,1} must be certified.  An earlier draft used d <= 4
    # and then reported the height of EVERY orbit advanced 5 periods, which inflated the
    # finite-check requirement to 2h ~ 1.1e7 for no reason.
    DMAX=1
    al=S.alpha()
    # (W1) PROVED, not sampled.  eps = |N| sqrtDelta / G with G = 2 alpha eta^2 - t N, so eps
    # strictly decreases along an orbit iff G strictly increases.  One unit step sends
    # eta -> rho eta and N -> delta N, so
    #     G_next - G = 2 alpha eta^2 (rho^2 - 1) - t N (delta - 1).
    # For delta = +1 the second term vanishes and the first is positive (rho > 1): G increases
    # at EVERY step, unconditionally.  For delta = -1 the second term is -2tN, bounded by
    # 2t|N|, while the first grows like rho^{2q}; so once
    #     2 alpha eta^2 (rho^2 - 1) > 2 t |N|
    # holds it holds for all later steps, and the finitely many earlier steps are checked
    # directly.  An earlier version only sampled 8 steps per orbit, which is not a proof.
    mono=True; w1thr=0
    for O in orbs:
        aa,bb=O[2],O[3]; prev=None; q=0; settled=False
        while q<40:
            m,k=state_from_ab(S,aa,bb)
            if m>0 and k>0:
                n,dd=S.eps_parts(m,k)
                if prev is not None and cmp_frac(n,dd,prev[0],prev[1])>=0: mono=False
                prev=(n,dd)
                et=S.eta(m,k); R=ring_elt(S,*rho(S))
                lhs=al*et*et*(R*R-Q(1,0,S.D))*2
                if (lhs-Q(2*S.t*O[0],0,S.D)).sign()>0:
                    settled=True
                    d2=S.den_err(m,k); w1thr=max(w1thr,float(d2.a)+float(d2.b)*float(S.D)**0.5)
                    break
            aa,bb=mul(S,(aa,bb),rho(S)); q+=1
        assert settled or delta_rho(S)==1
    # sign ledger: the signed norm is transported, N_q = delta^q N_rep (audit A16)
    dl=delta_rho(S); led=True
    for o in orbs:
        aa,bb=o[2],o[3]
        for q in range(6):
            if norm_ab(S,aa,bb) != (dl**q)*o[1]: led=False
            aa,bb=mul(S,(aa,bb),rho(S))
    print("  (S)  sign ledger N_q = delta^q N_rep, delta = Norm(rho) = %+d : %s"%(dl,led))
    assert led
    print("  (W1) eps strictly decreasing along every orbit: %s  [proved: G_next-G = "
          "2a eta^2(rho^2-1) - tN(delta-1); %s]"
          %(mono, "unconditional since delta=+1" if delta_rho(S)==1
            else "dominant from 2h <= %.4g, earlier steps checked"%w1thr))
    assert mono
    # (W2) normalisation, verified on the representatives
    one=Q(1,0,S.D); Rq=ring_elt(S,*rho(S))
    w2=all((ring_elt(S,o[2],o[3])-one).sign()>=0 and (ring_elt(S,o[2],o[3])-Rq).sign()<0
           for o in orbs)
    print("  (W2) every representative lies in [1, rho): %s"%w2); assert w2
    # (W3) eta-order == h-order once eta^2 > t|N|/(2 alpha); report the threshold
    al=S.alpha(); thr=max([0]+[o[0] for o in orbs])
    w3ok=True; worst_eta=None
    for o in orbs:
        aa,bb=o[2],o[3]
        for _ in range(10):
            m,k=state_from_ab(S,aa,bb)
            if m>0 and k>0:
                et=S.eta(m,k)
                if (et*et*al*2 - Q(S.t*abs(S.N(m,k)),0,S.D)).sign()<=0:
                    w3ok=False
                    if worst_eta is None: worst_eta=(m,k)
            aa,bb=mul(S,(aa,bb),rho(S))
    # every (W3)-failing state must lie inside the finite check; report the largest such height
    w3h=0.0; w3n=0
    for o in orbs:
        aa,bb=o[2],o[3]
        for _ in range(12):
            m,k=state_from_ab(S,aa,bb)
            if m>0 and k>0:
                et=S.eta(m,k)
                if (et*et*al*2 - Q(S.t*abs(S.N(m,k)),0,S.D)).sign()<=0:
                    w3n+=1
                    dd=S.den_err(m,k); w3h=max(w3h,float(dd.a)+float(dd.b)*float(S.D)**0.5)
            aa,bb=mul(S,(aa,bb),rho(S))
    print("  (W3-old) 2 alpha eta^2 > t|N| on every positive state: %s  [INSUFFICIENT, see A13]"%w3ok)
    # (W3') the cross-orbit height ordering, certified pairwise
    DMAXO=2; worstq=None; ordties=[]
    for A in orbs:
        for Bo in orbs:
            for d in range(0,DMAXO+1):
                if A is Bo and d==0: continue
                for par in (0,1):
                    U,V=order_UV(S,A,Bo,d,parity=par)
                    q=least_ordered_period(S,U,V)
                    if q is None:
                        ordties.append((A[1],Bo[1],d,par,-V.sign()))
                    elif worstq is None or q>worstq[0]:
                        worstq=(q,A[1],Bo[1],d)
                    if delta_rho(S)==1: break      # V is parity-independent
    print("  (W3\') cross-orbit height ordering: every (pair,d) decided by sign(U) from period"
          " q = %d onward"%(worstq[0] if worstq else 0))
    if worstq: print("        worst: N_A=%d N_B=%d d=%d"%worstq[1:])
    nz=u_zero_is_structural(S,orbs)
    print("        U == 0 is STRUCTURALLY impossible between distinct normalised reps; found %d"%nz)
    print("        (and U == 0 would force V == 0, so it is an index shift, not a tie -- asserted)")
    print("  (R)  representative invariance delta^q' N'_rep = delta^q N_rep: %s"
          %representative_invariance(S,orbs))
    for tr in ordties: print("           N_A=%-4d N_B=%-4d d=%d parity=%d  sign(h_B-h_A) = %+d"%tr)
    worst=None; ties=[]; undecided=[]
    for A in orbs:
        for Bo in orbs:
            for d in range(0,DMAX+1):
                if A is Bo and d==0: continue
                G=gamma_d(S,A,Bo,d)
                if G.sign()==0:
                    lab={-1:"B beats A",0:"EXACTLY EQUAL (B not a strict record)",1:"A beats B"}
                    ties.append((A[1],Bo[1],d,
                                 lab[tie_sign(S,A,Bo,d,d)], lab[tie_sign(S,A,Bo,d,d+1)]))
                    continue
                p=least_decided_period(S,A,Bo,d,G)
                if worst is None or p>worst[0]: worst=(p,A[1],Bo[1],d)
    print("  pairs with Gamma_d == 0 (no threshold; integer rule, reported per parity): %d"%len(ties))
    for tr in ties:
        print("     N_A=%-4d N_B=%-4d d=%d : at p=d %s ; at p=d+1 %s"%tr)
    print("  all other (pair,d) decided by sign(Gamma_d) from period p = %d onward"%worst[0])
    print("     worst: N_A=%d N_B=%d d=%d"%worst[1:])
    # The finite check must cover every state that is NOT yet decided, i.e. for each pair the
    # states of orbit B strictly below period P(pair,d).  Take the max height over those.
    R=rho(S); hmax=0.0
    for A in orbs:
        for Bo in orbs:
            for d in range(0,DMAX+1):
                if A is Bo and d==0: continue
                G=gamma_d(S,A,Bo,d)
                P=least_decided_period(S,A,Bo,d,G)      # None exactly when Gamma_d == 0
                if P is None: P=d                        # Gamma=0 pairs are decided at every p,
                                                         # but still need the ORDERING threshold
                # The two thresholds use DIFFERENT period coordinates: the error threshold has
                # A at p-d and B at p; order_UV has A at q and B at q+d, so q = p - d and the
                # ordering threshold must be converted by +d before taking the max (audit F3).
                # Gamma_d == 0 pairs were previously skipped here entirely, which dropped their
                # ordering requirement from the finite-check aggregation.
                for par in (0,1):
                    U,V=order_UV(S,A,Bo,d,parity=par)
                    qo=least_ordered_period(S,U,V)
                    if qo is not None: P=max(P,qo+d)
                    if delta_rho(S)==1: break
                aa,bb=Bo[2],Bo[3]
                for _ in range(max(0,P)):
                    m,k=state_from_ab(S,aa,bb)
                    if m>0 and k>0:
                        dd=S.den_err(m,k); hv=float(dd.a)+float(dd.b)*float(S.D)**0.5
                        hmax=max(hmax,hv)
                    aa,bb=mul(S,(aa,bb),R)
    print("  => every comparison AND ordering is decided for 2h >= %.4g ; finite check covers below"%hmax)
    return C, orbs, worst, ties, hmax

if __name__=="__main__":
    todo=((PHI,"alpha = phi"),(S3,"alpha = 1 + sqrt(3)"),(SQ3,"alpha = sqrt(3)  [CONTROL: no norm-one states]"))
    for S,lab in todo:
        run(S,lab); print()
