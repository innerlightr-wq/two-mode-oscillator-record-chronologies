#!/usr/bin/env python3
"""hypotheses.py -- H1 and H3 proved in the setting actually used, with no PID hypothesis.

H1 (admissible unit exists, effectively).  The fundamental unit u acts on the rank-2 lattice
O = Z + Z w by a matrix U in GL_2(Z) (det = +-Norm(u) = +-1).  Reducing mod M puts U mod M in
the finite group GL_2(Z/M), so some U^j = I mod M; multiplication by u^j is then the identity
mod M and therefore preserves EVERY congruence class mod M, as well as primitivity (it is a
unit) and, if Norm(u^j) = +1, the norm.  For the odd/odd condition M = 2 and
|GL_2(Z/2)| = 6, so j <= 6 (12 if a norm-one power is also wanted).  The MINIMAL admissible
power is then a search over j <= that bound -- and it can be strictly smaller than the order of
U, because U mod M need only FIX the class, not act as the identity: at alpha = sqrt(3) the
class (odd, odd) is fixed by the swap U = [[0,1],[1,0]] mod 2, so rho = u itself.

H3 (finite enumeration, no unique factorisation).  Let |N| <= B and reduce eta by unit powers
until 1 <= eta < rho.  Then |xi| = |N|/eta <= B automatically, so (eta, xi) lies in the bounded
rectangle [1,rho) x [-B,B] in the two real embeddings.  Since
    m = (eta - xi)/sqrtDelta,   k = (alpha eta - alpha' xi)/sqrtDelta,
the integer coordinates are explicitly bounded and an exhaustive search over that box finds
every orbit.  No class-group or PID input is used; the earlier write-up invoked unique
factorisation only to DESCRIBE the orbits (e.g. "(sqrt5) is the only ideal of norm 5"), which is
expository, not load-bearing.  This is the classical generalized-Pell reduction; cf. Conrad,
"The generalized Pell equation", Thms 1.1 and 2.1.
"""
from itertools import product
from fractions import Fraction
from quad import Q
from setups import PHI, S3, SQ3, LATTICE
from orbits import ring_elt, rho, mul, admissible, norm_ab

def unit_matrix(S):
    """Matrix of multiplication by the fundamental unit u on the basis (1, w), w = phi or sqrt(D).

    phi    : u = phi,     phi*1 = phi,       phi*phi = 1 + phi        -> [[0,1],[1,1]]
    sqrt(3): u = 2+sqrt3, u*1 = 2 + sqrt3,   u*sqrt3 = 3 + 2 sqrt3    -> [[2,3],[1,2]]
    (1+sqrt3 uses the same order Z[sqrt3], hence the same u and U.)
    """
    if S is PHI: return ((0,1),(1,1)), "phi"
    return ((2,3),(1,2)), "2+sqrt3"

def mat_mul(A,B,M=None):
    r=tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    if M: r=tuple(tuple(x%M for x in row) for row in r)
    return r

def order_mod(S, M=2):
    U,_=unit_matrix(S); I=((1,0),(0,1))
    Um=tuple(tuple(x%M for x in row) for row in U); P=Um; j=1
    while P!=I:
        P=mat_mul(P,Um,M); j+=1; assert j<100
    return j

def minimal_admissible_power(S, M=2, cap=24):
    """Least j >= 1 with multiplication by u^j preserving the admissibility class."""
    U,_=unit_matrix(S)
    # u^j as an element (a,b) in the (1,w) basis: column action on (1,0)
    e=(1,0)
    for j in range(1,cap+1):
        # e <- e * u  in the ring
        e = mul(S, e, (U[0][0], U[1][0]))      # multiply by u = U applied to basis vector 1
        ok=True
        for a,b in product(range(M*2), repeat=2):
            if not admissible(S,a,b): continue
            c,d = mul(S,(a,b),e)
            if not admissible(S,c,d): ok=False; break
        if ok: return j, e
    return None, None

if __name__=="__main__":
    print("H1: admissible unit power, M = 2  (|GL_2(Z/2)| = 6, so j <= 6)")
    print("  %-9s %-12s %-22s %-10s %-22s %s"%("slope","u","order of U mod 2","minimal j","u^j","matches rho?"))
    for S in (PHI,S3,SQ3):
        U,un=unit_matrix(S); o=order_mod(S,2)
        j,e=minimal_admissible_power(S,2)
        R=rho(S)
        print("  %-9s %-12s %-22d %-10s %-22s %s"
              %(S.name,un,o,j,str(e),e==R))
    print()
    print("H3: bounded rectangle, no PID.  |a|,|b| bounds vs the search box actually used:")
    from certificate import cutoff
    import math
    for S in (PHI,S3,SQ3):
        B=cutoff(S); R=ring_elt(S,*rho(S))
        rf=float(R.a)+float(R.b)*float(S.D)**0.5
        sD=2*float(S.alpha().b)*float(S.D)**0.5
        if S is PHI:   bb=(rf+B)/math.sqrt(5); aa=(rf+B+bb)/2
        else:          aa=(rf+B)/2;            bb=(rf+B)/(2*math.sqrt(3))
        print("  %-9s |N| <= %-4d rho = %-8.4f  =>  |a| <= %-8.2f |b| <= %-8.2f   search box used: %d"
              %(S.name,B,rf,aa,bb,2*B+40))
