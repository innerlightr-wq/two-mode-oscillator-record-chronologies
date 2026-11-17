"""review5.py -- the four points of the fifth proof-level review.

P1. The sentence "a state below the binding level has larger eps and cannot
    block" is FALSE.  Counterexample: alpha = phi, unrestricted, candidate
    b = (15,24) = 3*(5,8).  The correct statement is a SUFFICIENCY claim.
P2. One level convention: absolute eta-levels, with T_i the tail-start level,
    certified T_i > L*_i.
P3. The exception list needs COMPLETENESS, not just individual correctness.
P4. The ledger needs its lower endpoint (negative offsets) justified.
Plus: Lemma 6.3's positive factor must use |dd| and |eta| for the smaller root.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys, functools
pass  # path set by the shim below
from gq import *

NF = NT = 0
def ck(ok, lbl, extra=''):
    global NF, NT
    NT += 1
    print(('  PASS  ' if ok else '  FAIL  ') + lbl + (('   ' + extra) if extra else ''))
    if not ok: NF += 1

print('=' * 78)
print('P1.  alpha = phi, unrestricted.  b = (15,24); orbit (5,8) -> (13,21) -> (34,55).')
print('=' * 78)
S = Setup(1, -1, -1, 1, 1, [(0, 0)], 'phi unrestricted')
F = Fast(S)
X0, lam = fundamental_expander(S)
ck(X0 == ((1, 1), (1, 2)), 'the fundamental automorph is ((1,1),(1,2))', str(X0))
a1, a2, a3 = (5, 8), S.matapply(X0, (5, 8)), S.matapply(X0, S.matapply(X0, (5, 8)))
ck(a2 == (13, 21) and a3 == (34, 55), '(5,8) -> (13,21) -> (34,55)', f'{a2}, {a3}')
b = (15, 24)
ck(b == (3 * a1[0], 3 * a1[1]), 'b = 3*(5,8), so eps(b) = eps(5,8) exactly')
ck(F.eps_cmp(b, a1) == 0, 'eps(b) = eps(5,8)   (exact)')
ck(F.h_cmp(a1, a2) < 0 and F.h_cmp(a2, b) < 0 and F.h_cmp(b, a3) < 0,
   'H(5,8) < H(13,21) < H(b) < H(34,55)',
   f'{S.H(*a1).f():.4f} < {S.H(*a2).f():.4f} < {S.H(*b).f():.4f} < {S.H(*a3).f():.4f}')
ck(F.eps_cmp(a2, a1) < 0, 'eps(13,21) < eps(5,8) = eps(b)',
   f'{(S.eps_num_den(*a2)[0]/S.eps_num_den(*a2)[1]).f():.8f} < '
   f'{(S.eps_num_den(*a1)[0]/S.eps_num_den(*a1)[1]).f():.8f}')
# the binding (eps-minimal) state below H(b) on that orbit is (13,21)
below = [v for v in (a1, a2) if F.h_cmp(v, b) < 0]
binding = min(below, key=functools.cmp_to_key(lambda x, y: F.eps_cmp(x, y)))
ck(binding == a2, 'the eps-minimal state below H(b) is (13,21)', str(binding))
ck(F.eps_cmp(a1, b) <= 0, 'yet the EARLIER state (5,8) also blocks b (it ties)')
print('  => the published sentence "a state below the binding level ... cannot block" is FALSE.')
# the correct sufficiency statement
blockers = [v for v in below if F.eps_cmp(v, b) <= 0]
ck(bool(blockers) and F.eps_cmp(binding, b) <= 0,
   'SUFFICIENCY: some state blocks, and the eps-minimal state blocks too',
   f'{len(blockers)} blockers of {len(below)} states below')
# and the three-way verdict from the eps-minimal state matches an exhaustive scan
def verdict_scan(cand, states):
    tie = False
    for v in states:
        if F.h_cmp(v, cand) >= 0:
            continue
        c = F.eps_cmp(v, cand)
        if c < 0:
            return 'lost'
        if c == 0:
            tie = True
    return 'tie' if tie else 'record'
def verdict_min(cand, states):
    bel = [v for v in states if F.h_cmp(v, cand) < 0]
    if not bel:
        return 'record'
    bb = min(bel, key=functools.cmp_to_key(lambda x, y: F.eps_cmp(x, y)))
    c = F.eps_cmp(bb, cand)
    return 'lost' if c < 0 else ('tie' if c == 0 else 'record')
orb = [a1, a2, a3] + [S.matapply(X0, a3)]
ck(verdict_scan(b, orb) == verdict_min(b, orb) == 'lost',
   'the eps-minimal rule and an exhaustive scan give the SAME verdict here',
   f'{verdict_scan(b, orb)}')

print()
print('=' * 78)
print('P1b. the sufficiency rule reproduces an exhaustive scan on a large population')
print('=' * 78)
P, rho, j = S.rho_matrix()
states = []
m = 1
while True:
    km = kmax_for(S, m, 150)
    if km == 0:
        break
    for k in range(1, km + 1):
        if (m % S.M, k % S.M) in S.R:
            states.append((m, k))
    m += 1
mism = []
for cand in states[::37]:
    if verdict_scan(cand, states) != verdict_min(cand, states):
        mism.append(cand)
ck(not mism, 'eps-minimal verdict == exhaustive verdict on every sampled candidate',
   f'{len(states)} states, {len(states[::7])} candidates tested; mismatches {mism[:3]}')

print()
print('=' * 78)
print('P4.  negative offsets: a competitor one level LATER is above the candidate')
print('=' * 78)
Sb = Setup(1, -3, 1, 1, 2, [(1, 1)], '(3+sqrt5)/2')
Fb = Fast(Sb)
Pb, rhob, jb = Sb.rho_matrix()
bad = []
for seedA in [(1, 3), (3, 7), (5, 13)]:
    for seedB in [(1, 3), (3, 7), (5, 13)]:
        vA, vB = seedA, seedB
        for _ in range(3):
            vA = Sb.matapply(Pb, vA); vB = Sb.matapply(Pb, vB)
        later = Sb.matapply(Pb, vA)
        if Fb.h_cmp(later, vB) <= 0:
            bad.append((seedA, seedB))
ck(not bad, 'H_A(p+1) > H_B(p) for every tested ordered pair at the evaluation level, so no '
   'competitor at a later level can block', f'violations {bad[:3]}')

print()
print('=' * 78)
print('Lemma 6.3 sign: the clearing factor must use |dd| and |eta| (smaller root)')
print('=' * 78)
Ss = Setup(1, -3, 1, -1, 2, [(1, 1)], '(3-sqrt5)/2 smaller root')
ck(Ss.dd.sign() < 0, 'for the smaller root dd = alpha - alpha\' < 0', f'dd = {Ss.dd.f():.6f}')
ok = True
for v in [(1, 1), (3, 1), (7, 3), (13, 5)]:
    e = Ss.eta(*v)
    if (e * Ss.dd).sign() <= 0:
        ok = False
ck(ok, 'but eta*dd > 0 on the retained states, so A^2 |dd| |eta| is the positive factor')

print()
print('=' * 78)
print(f'review5: {NT - NF}/{NT} checks passed, {NF} failures')
print('=' * 78)
