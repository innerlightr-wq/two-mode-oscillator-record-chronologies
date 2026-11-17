"""review6_sail.py -- the coset-hull (sail) counterexample of the sixth review.

Claim under test.  For alpha = 2 + sqrt2 and (m,k) = (1,1) mod 3, the state
(7,25) is a strict relative-error record, yet it lies in the INTERIOR of the
triangle spanned by three admissible states of the same residue class in the
cone k > alpha*m:

        (7,25) = (3/5)(1,4) + (1/5)(31,106) + (1/5)(1,7).

Hence (7,25) is neither a vertex nor an edge point of the convex hull of the
admissible points of that cone: a record need not be a hull (sail) vertex of its
coset, so the natural coset-hull reduction fails.  All arithmetic is exact.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
from gq import *
from fractions import Fraction as Fr

NF = NT = 0
def ck(ok, lbl, extra=''):
    global NF, NT
    NT += 1
    print(('  PASS  ' if ok else '  FAIL  ') + lbl + (('   ' + extra) if extra else ''))
    if not ok: NF += 1

print('=' * 78)
print('alpha = 2 + sqrt2  (A,B,C,s) = (1,-4,2,+1),  M = 3,  R = {(1,1)}')
print('=' * 78)
S = Setup(1, -4, 2, 1, 3, [(1, 1)], '2+sqrt2 mod 3')
F = Fast(S)
ck(abs(S.alpha.f() - (2 + 2 ** 0.5)) < 1e-12, 'alpha = 2 + sqrt2', '%.10f' % S.alpha.f())
b = (7, 25)
ck(S.admissible(*b), '(7,25) is admissible')

# ---- 1. is (7,25) a strict record?  enumerate every admissible state below it
Hb = S.H(*b)
cap = int(Hb.f()) + 2
lower = []
m = 1
while True:
    km = kmax_for(S, m, cap)
    if km == 0:
        break
    for k in range(1, km + 1):
        if S.admissible(m, k) and (m, k) != b and F.h_cmp((m, k), b) < 0:
            lower.append((m, k))
    m += 1
lower = sort_heights(S, lower)
print('  admissible states of smaller height: %d' % len(lower))
ck(len(lower) == 42, 'there are exactly 42 admissible states of smaller height',
   str(len(lower)))
import functools
best = min(lower, key=functools.cmp_to_key(F.eps_cmp))
ck(best == (4, 13), 'the best of them is (4,13)', str(best))
ck(F.eps_cmp(b, best) < 0, 'eps(7,25) < eps(4,13), so (7,25) IS a strict record',
   'eps(7,25) = %.8f  <  eps(4,13) = %.8f'
   % ((S.eps_num_den(*b)[0] / S.eps_num_den(*b)[1]).f(),
      (S.eps_num_den(*best)[0] / S.eps_num_den(*best)[1]).f()))
ck(all(F.eps_cmp(b, v) < 0 for v in lower),
   'and it beats EVERY one of the 42, checked individually')

# ---- 2. the convex combination is exact
v1, v2, v3 = (1, 4), (31, 106), (1, 7)
c1, c2, c3 = Fr(3, 5), Fr(1, 5), Fr(1, 5)
mm = c1 * v1[0] + c2 * v2[0] + c3 * v3[0]
kk = c1 * v1[1] + c2 * v2[1] + c3 * v3[1]
ck(c1 + c2 + c3 == 1 and c1 > 0 and c2 > 0 and c3 > 0,
   'the coefficients 3/5, 1/5, 1/5 are positive and sum to 1')
ck((mm, kk) == (Fr(7), Fr(25)), '(3/5)(1,4) + (1/5)(31,106) + (1/5)(1,7) = (7,25) exactly',
   f'({mm}, {kk})')

# ---- 3. the three vertices are admissible and lie in the cone k > alpha*m
ok3 = all(S.admissible(*v) for v in (v1, v2, v3))
ck(ok3, 'all three vertices are admissible, i.e. (1,1) mod 3 with positive coordinates')
ok4 = all(S.xi(*v).sign() > 0 for v in (v1, v2, v3))     # xi = k - m*alpha > 0
ck(ok4, 'all three satisfy k > alpha*m, so they lie in one open cone',
   ', '.join('%s: k - alpha m = %+.6f' % (v, S.xi(*v).f()) for v in (v1, v2, v3)))
ck(S.xi(*b).sign() > 0, 'and so does (7,25)', 'k - alpha m = %+.6f' % S.xi(*b).f())

# ---- 4. the triangle is nondegenerate
det = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
ck(det != 0, 'the triangle is nondegenerate', f'det = {det}')

# ---- 5. so (7,25) is interior: not a vertex, not on an edge
#    strict positivity of all three barycentric coordinates is exactly interiority
ck(min(c1, c2, c3) > 0 and det != 0,
   '(7,25) is therefore STRICTLY INSIDE the triangle: neither a hull vertex nor an '
   'edge point of the admissible points of that cone')

# ---- 6. where does the classifier put it?
P, rho, j = S.rho_matrix()
print()
print('  classifier context: j = %d, rho = %.6g, P = %s' % (j, rho.f(), P))
Q = S.Qf(*b)
print('  Q(7,25) = %d ;  Q(4,13) = %d ;  Q(1,4) = %d, Q(31,106) = %d, Q(1,7) = %d'
      % (Q, S.Qf(*best), S.Qf(*v1), S.Qf(*v2), S.Qf(*v3)))
ck(True, 'recorded for the note')

print()
print('=' * 78)
print(f'review6_sail: {NT - NF}/{NT} checks passed, {NF} failures')
print('=' * 78)
