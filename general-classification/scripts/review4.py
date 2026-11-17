"""review4.py -- the two obligations of the fourth review.

O1. The backward-ray exclusion needs TWO cases.  The floor eps >= sqrt(Delta)/|B|
    is a statement about the G < 0 branch only.  A doubly-infinite orbit has
    G > 0 on its whole positive part, and on its BACKWARD ray eps rises to
    sqrt(Delta)/|B| FROM BELOW, so the floor does not exclude it.
    Counterexample: alpha = (3+sqrt5)/2, P^{-1}(1,1) = (13,5).

O2. Approximate sorting needs an exact-comparator fallback, not only a
    verification, or termination is not established for every input.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys
pass  # path set by the shim below
from gq import *

NF = NT = 0
def ck(ok, lbl, extra=''):
    global NF, NT
    NT += 1
    print(('  PASS  ' if ok else '  FAIL  ') + lbl + (('   ' + extra) if extra else ''))
    if not ok: NF += 1

print('=' * 78)
print('O1.  alpha = (3+sqrt5)/2 : P^{-1}(1,1) = (13,5) has G > 0 and eps < sqrt(D)/|B|')
print('=' * 78)
S = Setup(1, -3, 1, 1, 2, [(1, 1)], '(3+sqrt5)/2')
F = Fast(S)
P, rho, j = S.rho_matrix()
Pi = S.matinv(P)
v = S.matapply(Pi, (1, 1))
ck(v == (13, 5), 'P^{-1}(1,1) = (13,5)', str(v))
Q = S.Qf(*v); e = S.eta(*v)
A2 = Surd(S.A ** 2, 0, S.D)
G = 2 * S.alpha * A2 * e * e + Surd(S.B * Q, 0, S.D)
ck(Q == -1, 'Q = -1')
ck(e.sign() > 0 and S.dd.sign() > 0, 'sgn(eta) = sgn(alpha-alpha\'): the orbit HAS a forward tail')
ck(G.sign() > 0, 'G > 0 on this state', f'G = {G.f():.6f}')
n, d = S.eps_num_den(*v)
flo = S.rt / Surd(abs(S.B), 0, S.D)
ck((n - flo * d).sign() < 0,
   'eps(13,5) < sqrt(Delta)/|B| -- the G<0 floor does NOT apply here',
   f'eps = {(n/d).f():.6f} < {flo.f():.6f}')
# and the whole backward ray approaches the limit from below
w = v
below = True
for _ in range(8):
    w = S.matapply(Pi, w)
    if w[0] <= 0 or w[1] <= 0:
        break
    nn, dd_ = S.eps_num_den(*w)
    if (nn - flo * dd_).sign() >= 0:
        below = False
ck(below, 'and so does every further backward state of that ray')

print()
print('=' * 78)
print('O1 repair.  On G > 0:  eps = |Q| sqrt(D) / (2 alpha A^2 eta^2 + B Q), so')
print('    eps >= eps_0   <=>   eta^2 <= Ystar := (|Q| sqrt(D)/eps_0 - B Q)/(2 alpha A^2).')
print('    This is an explicit BACKWARD-LEVEL cutoff, valid on the G>0 branch.')
print('=' * 78)
bound = eps0_threshold(S)
w0 = find_eps0_state(S, P, [(1, 1)], bound)
e0n, e0d = S.eps_num_den(*w0)
print(f'    bound = min(1, sqrt(Delta)/(2|B|)) = {bound.f():.8f}')
print(f'    chosen state w = {w0}, ATTAINED eps_0 = eps(w) = {(e0n/e0d).f():.8f}')
ck((e0n - bound * e0d).sign() < 0, 'eps(w) < the bound, strictly')
def Ystar(Q):
    return eps0_level_cutoff(S, Q, e0n, e0d)
ok_equiv = True
rows = []
probes = [(1, 1), (13, 5), (3, 1), (55, 21), (1, 3), (3, 7), (5, 13)]
# add deep forward states (eps far below eps_0) and deep backward ones
for seed in [(1, 1), (1, 3), (5, 13)]:
    u = seed
    for _ in range(3):
        u = S.matapply(P, u)
        if u[0] > 0 and u[1] > 0:
            probes.append(u)
    u = seed
    for _ in range(3):
        u = S.matapply(Pi, u)
        if u[0] > 0 and u[1] > 0:
            probes.append(u)
nboth = [0, 0]
for o in probes:
    if o[0] <= 0 or o[1] <= 0:
        continue
    Qo = S.Qf(*o); eo = S.eta(*o)
    Go = 2 * S.alpha * A2 * eo * eo + Surd(S.B * Qo, 0, S.D)
    if Go.sign() <= 0:
        continue
    Y = A2 * eo * eo            # A^2 eta^2
    lhs = (Y - Ystar(Qo)).sign() <= 0                # A^2 eta^2 <= Ystar
    no, do = S.eps_num_den(*o)
    rhs = (no * e0d - e0n * do).sign() >= 0          # eps >= eps_0
    rows.append((o, Qo, (no / do).f(), lhs, rhs))
    nboth[0 if lhs else 1] += 1
    ok_equiv &= (lhs == rhs)
for r in rows[:9]:
    print(f'    {r[0]}: Q={r[1]:+d} eps={r[2]:.6f}  Y<=Ystar:{r[3]}  eps>=eps_0:{r[4]}')
ck(ok_equiv, 'the equivalence Y <= Ystar  <=>  eps >= eps_0 holds on every tested G>0 state',
   f'{len(rows)} states, {nboth[0]} with Y<=Ystar and {nboth[1]} with Y>Ystar')
ck(nboth[0] > 0 and nboth[1] > 0, 'both sides of the cutoff are exercised')

print()
print('    The STRICT inequality eps(w) < sqrt(D)/(2|B|) is exactly what is needed:')
print('    Ystar > Y_min = B Q/(2 alpha) (when B Q > 0) iff |Q| sqrt(D)/eps_0 > 2 B Q,')
print('    which holds strictly for the attained eps_0 and only with EQUALITY if')
print('    eps_0 is taken to be the bound itself.')
ok_min = True
for Qo in [-1, 1, -5, 5, -9, 9, -11, 11]:
    BQ = S.B * Qo
    if BQ <= 0:
        continue
    etamin2 = Surd(BQ, 0, S.D) / (2 * S.alpha)       # Y_min in Y = A^2 eta^2
    if (Ystar(Qo) - etamin2).sign() <= 0:
        ok_min = False
ck(ok_min, 'Ystar > eta^2_min for every defect with B Q > 0, so the height is strictly '
           'increasing on the surviving region eta^2 > Ystar')

print()
print('=' * 78)
print('O2.  exact-comparator fallback for the height sort')
print('=' * 78)
import functools, random
rnd = random.Random(7)
st = []
m = 1
while len(st) < 400:
    km = kmax_for(S, m, 4000)
    for k in range(1, km + 1):
        if (m % S.M, k % S.M) in S.R:
            st.append((m, k))
    m += 1
st = st[:400]
rnd.shuffle(st)
exact = sorted(st, key=functools.cmp_to_key(lambda a, b: F.h_cmp(a, b)))
ck(all(F.h_cmp(exact[i], exact[i + 1]) < 0 for i in range(len(exact) - 1)),
   'the exact comparator alone sorts correctly (the fallback path)')
# a deliberately broken key must be caught and the fallback must recover
broken = sorted(st, key=lambda v: 0.0)
caught = not all(F.h_cmp(broken[i], broken[i + 1]) < 0 for i in range(len(broken) - 1))
ck(caught, 'a constant (degenerate) key is caught by the adjacent-pair verification')
rec = sort_heights(S, st)
ck(rec == exact, 'sort_heights returns the exactly-sorted list')
rec2 = sort_heights(S, st, _force_key_failure=True)
ck(rec2 == exact, 'and still does so when key generation is forced to fail')

print()
print('=' * 78)
print(f'review4: {NT - NF}/{NT} checks passed, {NF} failures')
print('=' * 78)
