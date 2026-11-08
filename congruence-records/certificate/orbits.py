"""Exact orbit classification and the log-periodic record criterion.

Framework (derived in theory.md / PROOF_OR_OBSTRUCTION.md).  Every state is determined by
(N, eta) and

    eps = |N| sqrtDelta / (2 alpha eta^2 - t N),      so eps is strictly decreasing in
    S   = (2 alpha eta^2 - t N)/|N| = T - t*sign(N),  T := 2 alpha eta^2/|N|.

T is EXACTLY geometric along an orbit (eta -> rho*eta multiplies T by rho^2), so with
W := eta^2/|N| the record order is the running maximum of W among states ordered by eta,
ties in W broken by the integer rule sign(|N_B| N_A - N_B) > 0.

CAUTION (external v2 audit R3): the phase/score picture below orders states by eta.  **eta
ordering is NOT height ordering across different norms** -- 2h = (2 alpha eta - tN/eta)/sqrtDelta
depends on N as well, and at phi the states (3,1) and (1,3) have eta_A < eta_B but h_A > h_B.
Height ordering is certified separately, pairwise, by `certificate.order_UV`.  This module now
only enumerates orbits; all comparison and classification logic lives in `certificate.py`.
"""
from math import gcd, isqrt
from fractions import Fraction
from quad import Q
from setups import PHI, S3, SQ3, LATTICE

def ring_elt(S, a, b):
    """eta as an element of Z[sqrt D]: for phi, eta = a + b*phi = (a + b/2) + (b/2) sqrt5."""
    if S is PHI:
        return Q(Fraction(2*a+b, 2), Fraction(b, 2), 5)
    return Q(a, b, S.D)

def norm_ab(S, a, b):
    return LATTICE[S.name]["NORM"](a, b)

def state_from_ab(S, a, b):
    """(m,k) from eta's coordinates, per-setup (see setups.LATTICE)."""
    return LATTICE[S.name]["MK"](a, b)

def rho(S):
    """The least unit > 1 preserving the admissibility class (see setups.LATTICE)."""
    return LATTICE[S.name]["RHO"]

def mul(S, x, y):
    a, b = x; c, d = y
    if S is PHI:  # (a+b phi)(c+d phi), phi^2 = phi + 1
        return (a*c + b*d, a*d + b*c + b*d)
    return (a*c + S.D*b*d, a*d + b*c)

def admissible(S, a, b):
    """(m,k) both odd, expressed in the eta coordinates (see setups.LATTICE)."""
    return LATTICE[S.name]["ADM"](a, b)

def enumerate_orbits(S, B, verbose=False):
    """All admissible orbits with |N| <= B, each with a representative eta in [1, rho)."""
    R = rho(S); Rq = ring_elt(S, *R)
    seen = {}
    # search a generous box of (a,b) and reduce each admissible element into [1, rho)
    # Box bound: for a representative with eta in [1,rho) and |N| <= B we have |xi| = |N|/eta
    # <= B, and a = (eta+xi)/2, b*sqrt(D) = (eta-xi)/2, so |a| <= (rho+B)/2 and
    # |b| <= (rho+B)/(2 sqrt D).  LIM below is a generous multiple of that.
    LIM = 2*B + 40
    # iterate over ALL (a,b) and let the per-setup admissibility test decide: an earlier
    # draft hard-coded "a even, b odd", which is right for phi and 1+sqrt3 but finds NOTHING
    # for sqrt3, where admissibility is "a odd, b odd" (audit A4).
    for b in range(-LIM, LIM+1, 1):
        for a in range(-LIM, LIM+1, 1):
            N = norm_ab(S, a, b)
            if N == 0 or abs(N) > B: continue
            e = ring_elt(S, a, b)
            if e.sign() <= 0: continue
            aa, bb = a, b
            # reduce into [1, rho) by multiplying/dividing by rho
            guard = 0
            while True:
                guard += 1; assert guard < 10000
                e = ring_elt(S, aa, bb)
                if (e - Q(1, 0, S.D)).sign() < 0:
                    aa, bb = mul(S, (aa, bb), R)                 # too small: multiply
                    continue
                if (e - Rq).sign() >= 0:
                    # divide by rho: multiply by rho^{-1} = conj(rho)/Norm(rho)
                    nr = norm_ab(S, *R)
                    ca, cb = (R[0] + R[1], -R[1]) if S is PHI else (R[0], -R[1])
                    # for phi: conj(a+b phi) = (a+b) - b phi
                    pa, pb = mul(S, (aa, bb), (ca, cb))
                    assert pa % nr == 0 and pb % nr == 0, (pa, pb, nr)
                    aa, bb = pa//nr, pb//nr
                    continue
                break
            if not admissible(S, aa, bb):
                continue
            # BUG FIX (audit A2): N must be recomputed from the REDUCED representative.
            # Reduction multiplies by rho, and Norm(rho) = -1 for phi, so the sign of N
            # changes under reduction; storing the pre-reduction N mislabels every
            # phi orbit's sign and silently broke the Gamma_d == 0 tie rule.
            Nred = norm_ab(S, aa, bb)
            assert abs(Nred) == abs(N)
            key = (abs(Nred), aa, bb)
            if key not in seen:
                seen[key] = (abs(Nred), Nred, aa, bb)
    return sorted(seen.values(), key=lambda r: float(ring_elt(S, r[2], r[3]).a)
                                               + float(ring_elt(S, r[2], r[3]).b)*float(S.D)**0.5)

# NOTE (external v2 audit R3): `sigma_gt` and `decide` were REMOVED.  `decide` compared only
# leading scores, recorded an equality only against a same-period competitor, and had no
# three-way outcome -- so it labelled the sqrt(3) norm +6 companion a strict record family.
# The authoritative classifier is `certificate.classify`, which uses the exact criterion, the
# certified cross-orbit ordering, and the three-way `tie_sign`.  Nothing imports these any more.

def primitive(S, a, b):
    m, k = state_from_ab(S, a, b)
    return gcd(abs(m), abs(k)) == 1

def admissible_primitive_orbits(S, B):
    """Every admissible PRIMITIVE orbit with |N| <= B, one representative each in [1, rho).

    Imprimitive orbits are dropped because an imprimitive state has the same eps as its
    primitive reduction at strictly smaller height, so it never records (section 1 of
    PROOF_OR_OBSTRUCTION.md).  That reduction is specific to the odd/odd class: the gcd is odd,
    so dividing it preserves oddness.  It is NOT valid for a general congruence class -- at
    alpha = sqrt(6) with (m,k) = (1,1) mod 3 the state (4,10) is a strict record in the class
    although gcd = 2 and its reduction (2,5) leaves the class (external v2 audit R7).
    """
    return [o for o in enumerate_orbits(S, B) if primitive(S, o[2], o[3])]
