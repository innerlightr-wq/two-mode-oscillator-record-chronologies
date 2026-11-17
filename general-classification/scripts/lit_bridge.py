"""lit_bridge.py -- the two precise bridges to classical theory.

(L1) eps is a monotone function of the MULTIPLICATIVE error:
         eps = |m alpha - k|/(m alpha + k) = |tanh( (1/2) log(k/(m alpha)) )|,
     so records minimise |log(k/m) - log alpha| under the weighted height
     H = m alpha + k.  Verified numerically to 12 digits.

(L2) The classical congruence-restricted best approximations -- the lattice
     points minimising |xi| = |k - m alpha| with H increasing, i.e. the vertices
     of the Klein sail of the congruence sublattice -- are ALL eps-records, and
     the containment is STRICT.  Proof of the inclusion: if |xi| strictly
     decreases while H increases then eps = |xi|/H strictly decreases.
     The strictness is exhibited by explicit witnesses.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys, math
pass  # path set by the shim below
from gq import *

NF = NT = 0
def chk(ok, label, extra=''):
    global NF, NT
    NT += 1
    print(('  PASS  ' if ok else '  FAIL  ') + label + (('   ' + extra) if extra else ''))
    if not ok: NF += 1

odd = [(1, 1)]
CASES = [
 (1, -1, -1, 1, 2, odd, 'phi, odd/odd', 800),
 (1, -2, -2, 1, 2, odd, '1+sqrt3, odd/odd', 800),
 (1,  0, -3, 1, 2, odd, 'sqrt3, odd/odd', 800),
 (1,  0, -2, 1, 2, odd, 'sqrt2, odd/odd', 800),
 (3, -1, -1, 1, 2, odd, '3x^2-x-1, odd/odd', 900),
 (1,  0, -6, 1, 3, [(1,1)], 'sqrt6, (1,1) mod 3', 900),
]
print('(L1) eps = |tanh( log(k/(m alpha))/2 )|')
for (A, B, C, s, M, R, nm, cap) in CASES:
    S = Setup(A, B, C, s, M, R, nm)
    worst = 0.0
    for m in range(1, 40):
        for k in range(1, 40):
            a = S.alpha.f()
            e = abs(m * a - k) / (m * a + k)
            t = abs(math.tanh(0.5 * math.log(k / (m * a))))
            worst = max(worst, abs(e - t))
    chk(worst < 1e-12, f'{nm}: identity holds', f'max deviation {worst:.2e}')

STRICT = []
print('\n(L2) classical congruence-restricted best approximations vs eps-records')
for (A, B, C, s, M, R, nm, cap) in CASES:
    S = Setup(A, B, C, s, M, R, nm)
    F = Fast(S)
    states = []
    m = 1
    while True:
        km = kmax_for(S, m, cap)
        if km == 0: break
        for k in range(1, km + 1):
            if (m % S.M, k % S.M) in S.R:
                states.append((m, k))
        m += 1
    af = S.alpha.f()
    states.sort(key=lambda v: v[0] * af + v[1])
    for i in range(len(states) - 1):
        assert F.h_cmp(states[i], states[i + 1]) < 0
    # classical best approximations in the class: running minima of |xi|
    def absxi_cmp(v1, v2):
        a1, b1 = F.absxi_ab(*v1); a2, b2 = F.absxi_ab(*v2)
        return sgn_ab(a1 - a2, b1 - b2, S.Delta)
    bestxi, cls = None, []
    for v in states:
        if bestxi is None or absxi_cmp(v, bestxi) < 0:
            cls.append(v); bestxi = v
    epsrec, best = [], None
    for v in states:
        if best is None or F.eps_cmp(v, best) < 0:
            epsrec.append(v); best = v
    chk(set(cls) <= set(epsrec),
        f'{nm}: every classical best approximation in the class is an eps-record',
        f'{len(cls)} classical, {len(epsrec)} eps-records')
    extra = [v for v in epsrec if v not in cls]
    print('        containment %s; extra eps-records: %s'
          % ('STRICT' if extra else 'is an EQUALITY below this cap', extra[:4]))
    STRICT.append((nm, bool(extra)))
chk(any(b for _, b in STRICT), 'the inclusion is strict for at least one instance',
    'strict: ' + ', '.join(n for n, b in STRICT if b))
chk(any(not b for _, b in STRICT),
    'and for at least one instance there is NO extra eps-record below the cap, '
    'so strictness is NOT a theorem (this is a finite range, NOT an equality of sets)',
    'no extra below cap: ' + ', '.join(n for n, b in STRICT if not b))
print('=' * 70)
print(f'lit_bridge: {NT - NF}/{NT} checks passed, {NF} failures')
