#!/usr/bin/env python3
"""tail_table.py -- the finite-check table of Section 7 of the technical note.

certificate.py reports, per slope, the largest height among the states that are not yet
decided pair-by-pair.  The note uses a deliberately more CONSERVATIVE convention, because
Proposition 7.2 (only offsets d in {0,1} matter) needs the predecessor window to be
populated:

  p0  = max over all (A, B, d) of the decision period P(A, B, d)  -- error threshold and
        ordering threshold, the latter converted from q- to p-coordinates by +d --
        then raised until EVERY orbit already has a positive state at some period <= p0 - 1;
  Hmax = max over all orbits and all periods q < p0 of H at the positive states;
  cap  = ceil(Hmax), the bound for the unpruned enumeration that covers the pre-tail segment.

Outputs the table and, for each slope, the number of admissible states below the cap.
Exact throughout: Hmax is kept as an element of Z[sqrt D] and the cap is an exact integer
enclosure.  Floats are printed for display only.
"""
from quad import Q
from setups import PHI, S3, SQ3
from orbits import admissible_primitive_orbits, state_from_ab, mul, rho
from certificate import (cutoff, gamma_d, least_decided_period, order_UV,
                         least_ordered_period, delta_rho)

DMAX = 1   # Proposition 7.2 of the note: only offsets d in {0,1} can matter
from brute import enumerate_states

def fnum(q, D):
    return float(q.a) + float(q.b) * float(D) ** 0.5

def decision_period(S, A, Bo, d):
    """P in B-period coordinates: error threshold, and ordering threshold shifted by +d."""
    G = gamma_d(S, A, Bo, d)
    P = least_decided_period(S, A, Bo, d, G)
    if P is None:                       # Gamma_d == 0: decided at every p by the integer rule
        P = d
    for par in (0, 1):
        U, V = order_UV(S, A, Bo, d, parity=par)
        qo = least_ordered_period(S, U, V)
        if qo is not None:
            P = max(P, qo + d)
        if delta_rho(S) == 1:
            break
    return P

def tail_start(S, orbs):
    p0 = 0
    for A in orbs:
        for Bo in orbs:
            for d in range(0, DMAX + 1):
                if A is Bo and d == 0:
                    continue
                p0 = max(p0, decision_period(S, A, Bo, d))
    # raise p0 until every orbit has a positive state at some period <= p0 - 1
    while True:
        if all(first_positive_period(S, o) is not None and
               first_positive_period(S, o) <= p0 - 1 for o in orbs):
            return p0
        p0 += 1

def first_positive_period(S, o, tries=60):
    a, b = o[2], o[3]
    R = rho(S)
    for q in range(tries):
        m, k = state_from_ab(S, a, b)
        if m > 0 and k > 0:
            return q
        a, b = mul(S, (a, b), R)
    return None

def pre_tail_max_height(S, orbs, p0):
    """Exact max of H over positive states at periods q < p0.  Returns (Q, (m,k))."""
    R = rho(S)
    best, arg = None, None
    for o in orbs:
        a, b = o[2], o[3]
        for q in range(p0):
            m, k = state_from_ab(S, a, b)
            if m > 0 and k > 0:
                H = S.den_err(m, k)
                if best is None or (H - best).sign() > 0:
                    best, arg = H, (m, k)
            a, b = mul(S, (a, b), R)
    return best, arg

def exact_ceiling(H, D):
    """Least integer c with H <= c, decided exactly."""
    c = int(fnum(H, D)) - 2
    while (H - Q(c, 0, D)).sign() > 0:
        c += 1
    return c

if __name__ == "__main__":
    print("%-10s %6s  %-26s %6s  %10s" %
          ("alpha", "p0", "largest pre-tail H", "cap", "states<=cap"))
    print("-" * 68)
    for S in (PHI, S3, SQ3):
        B = cutoff(S)
        orbs = admissible_primitive_orbits(S, B)
        p0 = tail_start(S, orbs)
        H, arg = pre_tail_max_height(S, orbs, p0)
        cap = exact_ceiling(H, S.D)
        n = len(enumerate_states(S, cap))
        print("%-10s %6d  %-26s %6d  %10d" %
              (S.name, p0, "%s = %.4f" % (H, fnum(H, S.D)), cap, n))
        print("%-10s %6s  attained at (m,k) = (%d,%d)" % ("", "", arg[0], arg[1]))
