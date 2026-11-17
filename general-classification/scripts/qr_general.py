"""qr_general.py -- the complete certified algorithm, run on regression
controls and stress cases.  Exact arithmetic throughout; floats only printed.

Pipeline per instance (A,B,C,s,M,R):
  A. class-fixing proper automorph power P (P = I mod M, eta -> rho*eta, rho>1)
  B. comparison family: ALL admissible orbits with |Q| <= D, from the
     fundamental-domain box, for the D minimising the cutoff
  C. cutoff          : every strict record of height > H_min(family) has |Q| <= Bcut
  D. enumeration     : all admissible orbits with |Q| <= Bcomp  (Bcomp >= Bcut
     from the blocker lemma), through the same box
  E. certified tail  : p_cert from the exact thresholds (E2),(E3)
  F. finite part     : exact verdicts at every period 0..p_cert of every
     enumerated orbit, plus brute force below H_min(family)
  G. validation      : the merged record list is compared with an independent
     brute-force scan.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys, time
pass  # path set by the shim below
from gq import *
from math import gcd

odd = [(1, 1)]
CASES = [
 (1, -1, -1,  1, 2, odd,           'CONTROL phi, odd/odd',                      800),
 (1, -2, -2,  1, 2, odd,           'CONTROL 1+sqrt3, odd/odd',                  800),
 (1,  0, -3,  1, 2, odd,           'CONTROL sqrt3, odd/odd',                    800),
 (1,  0, -2,  1, 2, odd,           'sqrt2, odd/odd',                            800),
 (1, -3,  1,  1, 2, odd,           '(3+sqrt5)/2, odd/odd   [two positive conjugates]', 800),
 (1, -3,  1, -1, 2, odd,           '(3-sqrt5)/2, odd/odd   [smaller root, alpha<1]',   900),
 (2,  0, -1,  1, 2, odd,           '1/sqrt2, odd/odd       [nonmonic A=2, alpha<1]',   800),
 (3, -1, -1,  1, 2, odd,           '3x^2-x-1, odd/odd      [nonmonic A=3]',     900),
 (1,  0, -3,  1, 5, [(1,1),(2,3)], 'sqrt3, union {(1,1),(2,3)} mod 5',          900),
 (1,  0, -6,  1, 4, [(2,2)],       'sqrt6, (2,2) mod 4     [every state imprimitive]', 900),
 (1,  0, -2,  1, 3, [(1,1)],       'sqrt2, (1,1) mod 3',                        900),
 (1,  0, -6,  1, 3, [(1,1)],       'sqrt6, (1,1) mod 3     [the (4,10) case]',  900),
 (1,  0, -5,  1, 1, [(0,0)],       'sqrt5, unrestricted',                       600),
 (1, -5,  1,  1, 2, odd,           '(5+sqrt21)/2, odd/odd  [two positive conjugates]', 900),
]
DLIST = [1, 2, 3, 5, 8, 13, 20, 30, 50, 80, 130]

NF = NT = 0
def chk(ok, label, extra=''):
    global NF, NT
    NT += 1
    print(('  PASS  ' if ok else '  FAIL  ') + label + (('   ' + extra) if extra else ''))
    if not ok: NF += 1

for (A, B, C, s, M, R, nm, cap) in CASES:
    print('=' * 78); print(nm); print('=' * 78)
    t0 = time.time()
    S = Setup(A, B, C, s, M, R, nm)
    F = Fast(S)
    P, rho, j = S.rho_matrix()
    X0, lam = fundamental_expander(S)
    print('  alpha = %.10f   alpha\' = %+.10f   Delta = %d   A = %d, B = %d, C = %d'
          % (S.alpha.f(), S.alphap.f(), S.Delta, A, B, C))
    print('  fundamental automorph multiplier lam = %.8g ; class-fixing index j = %d ; '
          'rho = lam^j = %.8g' % (lam.f(), j, rho.f()))
    print('  P = %s  (entrywise positive: %s)'
          % (P, all(P[i][l] > 0 for i in range(2) for l in range(2))))
    # ---- A
    chk(all(S.Qf(*v) == S.Qf(*S.matapply(P, v)) for v in
            [(1,1),(2,3),(5,-7),(11,4),(0,1),(1,0),(-3,2)]),
        'A: P preserves the defect Q exactly (proper automorph)')
    chk(all((S.matapply(P, v)[0] % M, S.matapply(P, v)[1] % M) == (v[0] % M, v[1] % M)
            for v in [(1,1),(2,3),(5,7),(0,1),(3,0),(4,10)]),
        'A: P fixes every residue class mod M')
    chk(all(gcd(abs(v[0]), abs(v[1])) ==
            gcd(abs(S.matapply(P, v)[0]), abs(S.matapply(P, v)[1]))
            for v in [(2,2),(3,6),(4,10),(6,9),(1,1)]),
        'A: P preserves gcd, so imprimitive orbits stay imprimitive and in R')
    # ---- B, C
    Bcut, seeds, D, info, sc = auto_family2(S, P, rho, Dlist=DLIST)
    famH = None
    fam_pos = []
    for sd in seeds:
        pv, p0 = first_positive(S, P, sd)
        if pv is not None:
            fam_pos.append(pv)
    famH = min(fam_pos, key=lambda v: S.H(*v).f())
    print('  B: comparison family = all admissible orbits with |Q| <= %d  '
          '(%d orbits, %d forward-positive); lowest member %s at H = %.6g'
          % (D, len(seeds), len(fam_pos), famH, S.H(*famH).f()))
    print('  C: CUTOFF  every strict record of height > %.6g has |Q| <= %d'
          '   (max F = %.6f, certified tail bound %.6f)'
          % (S.H(*famH).f(), Bcut, info['maxF'].f(), info['tail'].f()))
    # ---- D
    eps_fam = S.eps_num_den(*famH)
    try:
        Bcomp = Bcomp_from(S, Bcut, eps_fam)
        pruning = True
    except AssertionError:
        Bcomp, pruning = Bcut, False
        print('  D: blocker bound VACUOUS at this eps (sqrt(Delta) <= |B| eps); '
              'using the unpruned competitor set')
    orbs_raw, box, jj, nclass = enumerate_orbits2(S, P, rho, max(Bcut, Bcomp))
    # Positive windows.  When alpha' > 0 the positive quadrant is NOT forward
    # invariant (no automorph power is entrywise positive), so an orbit's
    # positive states can be a finite window, or a BACKWARD-infinite ray.  An
    # orbit has an infinite FORWARD positive tail iff sgn(eta)=sgn(alpha-alpha'),
    # since m = (eta-xi)/(alpha-alpha') and xi -> 0.
    W = 60
    orbs = []
    Pi = S.matinv(P)
    for rep, Q in orbs_raw:
        states = {}
        w = rep
        for q in range(0, W + 1):
            states[q] = w; w = S.matapply(P, w)
        w = rep
        for q in range(-1, -W - 1, -1):
            w = S.matapply(Pi, w); states[q] = w
        win = sorted(q for q, v in states.items() if v[0] > 0 and v[1] > 0)
        if not win:
            continue
        e = S.eta(*rep)
        fwd = (e.sign() * S.dd.sign()) > 0
        nonneg = [q for q in win if q >= 0]
        q0 = nonneg[0] if nonneg else win[0]
        orbs.append(dict(rep=rep, Q=Q, st=states, win=win, fwd=fwd,
                         pos=states[q0], enter=q0,
                         double=(fwd and min(win) <= -W + 2),
                         exitp=(None if fwd else win[-1])))
    chk(all(o['fwd'] == (max(o['win']) >= W - 2) for o in orbs),
        'D: sgn(eta)*sgn(alpha-alpha\') > 0 characterises the orbits with an '
        'infinite forward positive tail',
        f"{sum(1 for o in orbs if o['fwd'])} forward-infinite of {len(orbs)}")
    print('  D: reduction box +-%d x +-%d -> %d lam-classes -> %d admissible orbits, '
          '%d forward-positive;  Bcomp = %d'
          % (box[0], box[1], nclass, len(orbs_raw), len(orbs), Bcomp))
    # ---- E   (thresholds only involve the forward-infinite orbits)
    fwdorbs = [o for o in orbs if o['fwd']]
    pc, worst = certify_tail(S, P, rho, fwdorbs)
    print('  E: tail certified from period p_cert = %d (binding threshold: %s)'
          % (pc, worst[0] if worst else '-'))
    # ---- F: exact verdicts
    PW = pc + 3
    def verdict(vB, qB):
        """(is_record, tie, lost) by exact comparison against the binding
        (largest height strictly below) positive state of every enumerated
        orbit.  Binding is the right test because eps strictly decreases along
        every orbit (E1), so among an orbit's states below H_B the smallest eps
        is the one of largest period."""
        lim = None
        if pruning:
            n, d = S.eps_num_den(*vB)
            try:
                lim = Bcomp_from(S, abs(qB), (n, d))
            except AssertionError:
                lim = None
        tie = None
        for o in orbs:
            if lim is not None and abs(o['Q']) > lim:
                continue
            # The binding state is the one of LARGEST PERIOD with height below
            # H_B, not the one of largest height.  eps is monotone decreasing in
            # the period on the positive part (eps = A|Q||dd|/G, G = 2 alpha A^2
            # eta^2 + B Q, and G has constant sign there), whereas the HEIGHT
            # H = 2 alpha eta/dd + B Q/(A^2 eta dd) is U-shaped in eta whenever
            # B*Q/dd > 0 and the orbit reaches eta^2 < B Q/(2 alpha A^2).  That
            # happens only when alpha' > 0, where a Q-negative orbit is positive
            # in both directions; picking by height then selects a backward
            # state of large eps and misses the true binding competitor.
            best, bq = None, None
            for q in o['win']:
                w = o['st'][q]
                if w == vB:
                    continue
                if F.h_cmp(w, vB) < 0 and (bq is None or q > bq):
                    best, bq = w, q
            if best is None:
                continue
            c2 = F.eps_cmp(vB, best)
            if c2 > 0:
                return False, None, (o['pos'], o['Q'], best)
            if c2 == 0 and tie is None:
                tie = (o['pos'], o['Q'], best)
        return (tie is None), tie, None
    tails, early, tieorb = [], [], []
    for o in orbs:
        if o['fwd']:
            pev = o['enter'] + pc
            v = o['st'][pev]
            isrec, tie, lost = verdict(v, o['Q'])
            o['tail'] = 'record' if isrec else ('tie' if tie else 'excluded')
            if o['tail'] == 'record': tails.append(o)
            if o['tail'] == 'tie': tieorb.append((o, tie))
            # only the forward part before the certified period: on a
            # doubly-infinite orbit the backward ray has eps increasing to the
            # explicit limit |alpha-alpha'|/(alpha+alpha') > 0, so it holds no
            # record beyond an explicit height and is treated analytically.
            rng = [q for q in o['win'] if o['enter'] <= q < pev]
        else:
            o['tail'] = 'finite/backward positive window'
            rng = [q for q in o['win'] if q >= o['enter'] - 6]
        for q in rng:
            w = o['st'][q]
            ir, ti, lo = verdict(w, o['Q'])
            if ir and o['tail'] != 'record':
                early.append((w, o['Q'], 'a record at this state, but %s in the tail' % o['tail']))
            if (not ir) and o['tail'] == 'record':
                early.append((w, o['Q'], 'NOT a record here though the tail records'))
    print('  F: %d record orbit(s) in the certified tail, %d permanent tie(s), '
          '%d initial exception(s); %d orbit(s) have only a finite/backward positive window'
          % (len(tails), len(tieorb), len(early), sum(1 for o in orbs if not o['fwd'])))
    nd = sum(1 for o in orbs if o.get('double'))
    if nd:
        _d = S.dd; _d = _d if _d.sign() > 0 else -_d
        lim = _d / (S.alpha + S.alphap)
        print('       %d orbit(s) are positive in BOTH directions (alpha\' > 0): their '
              'height is U-shaped in the period and eps -> %.6f backward'
              % (nd, lim.f()))
    for o in sorted(tails, key=lambda o: S.H(*o['pos']).f()):
        print('       record tail: first positive %s, Q = %d, gcd = %d'
              % (o['pos'], o['Q'], gcd(*o['pos'])))
    for o, t in tieorb[:8]:
        print('       permanent tie: %s, Q = %d  (exactly equals %s, Q = %d)'
              % (o['pos'], o['Q'], t[0], t[1]))
    for e in early[:8]:
        print('       initial exception: %s, Q = %d -- %s' % e)
    # ---- G: validation against an independent brute-force scan
    st, wk, nst = brute_records_fast(S, cap)
    print('  G: brute force to H <= %d : %d admissible states, %d strict records, %d weak ties'
          % (cap, nst, len(st), len(wk)))
    print('       records: %s' % (st[:12],))
    print('       defects: %s' % ([S.Qf(*v) for v in st[:12]],))
    tailreps = set()
    for o in tails:
        r, _ = norm_rep(S, P, rho, o['pos'])
        tailreps.add(r)
    Hfam = S.H(*famH)
    bad = []
    for v in st:
        if (S.H(*v) - Hfam).sign() <= 0:
            continue
        r, _ = norm_rep(S, P, rho, v)
        if r not in tailreps:
            # allowed only if it is one of the listed initial exceptions
            if not any(v == e[0] for e in early):
                bad.append((v, S.Qf(*v)))
    chk(not bad, 'G: every brute-force record above the family floor lies in a certified '
                 'record tail (or is a listed initial exception)', f'exceptions {bad[:4]}')
    miss = []
    for o in tails:
        for q in o['win']:
            if q < o['enter'] + pc:
                continue
            w = o['st'][q]
            if (S.H(*w) - Surd(cap, 0, S.D)).sign() > 0:
                break
            if w not in st and not any(w == e[0] for e in early):
                miss.append((w, o['Q']))
    chk(not miss, 'G: every certified record-tail state below the brute cap is a brute-force '
                  'record (or a listed initial exception)', f'missing {miss[:4]}')
    chk(all(abs(S.Qf(*v)) <= Bcut for v in st if (S.H(*v) - Hfam).sign() > 0),
        'C: the cutoff holds on every brute-force record above the family floor',
        f'max |Q| = {max([abs(S.Qf(*v)) for v in st if (S.H(*v)-Hfam).sign()>0] or [0])} <= {Bcut}')
    print('  total %.1fs' % (time.time() - t0))
print('=' * 78)
print(f'qr_general: {NT - NF}/{NT} checks passed, {NF} failures')
print('=' * 78)
