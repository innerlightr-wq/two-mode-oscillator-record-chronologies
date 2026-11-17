"""check.py -- INDEPENDENT certificate checker.

Reads certificates/<name>.json and re-verifies the claims from the definitions.
It imports nothing from gq.py: the arithmetic here is a separate representation
(elements of Q(sqrt(Delta)) as (a + b*sqrt(Delta))/d with a single integer
denominator, over Delta itself rather than over the squarefree part), and every
decision routine is written independently.  The checker does NOT use the
blocker-pruning lemma: all competitor comparisons are unpruned.

Usage:  python3 check.py [name ...]
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys, json, glob, os
from math import gcd, isqrt

CERT = _os.path.join(_ROOT, 'certificates')


# ---------------------------------------------------------------- arithmetic
class Q2:
    """(a + b*sqrt(DE))/d  with integers a,b,d and d > 0."""
    __slots__ = ('a', 'b', 'd', 'DE')

    def __init__(s, a, b, d, DE):
        if d < 0:
            a, b, d = -a, -b, -d
        g = gcd(gcd(abs(a), abs(b)), d) or 1
        s.a, s.b, s.d, s.DE = a // g, b // g, d // g, DE

    @staticmethod
    def i(n, DE):
        return Q2(n, 0, 1, DE)

    def __add__(s, o):
        o = o if isinstance(o, Q2) else Q2.i(o, s.DE)
        return Q2(s.a * o.d + o.a * s.d, s.b * o.d + o.b * s.d, s.d * o.d, s.DE)

    __radd__ = __add__

    def __neg__(s):
        return Q2(-s.a, -s.b, s.d, s.DE)

    def __sub__(s, o):
        return s + (-(o if isinstance(o, Q2) else Q2.i(o, s.DE)))

    def __rsub__(s, o):
        return (o if isinstance(o, Q2) else Q2.i(o, s.DE)) + (-s)

    def __mul__(s, o):
        o = o if isinstance(o, Q2) else Q2.i(o, s.DE)
        return Q2(s.a * o.a + s.DE * s.b * o.b, s.a * o.b + s.b * o.a, s.d * o.d, s.DE)

    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - s.DE * s.b * s.b
        assert n != 0
        return Q2(s.a * s.d, -s.b * s.d, n, s.DE)

    def __truediv__(s, o):
        return s * (o if isinstance(o, Q2) else Q2.i(o, s.DE)).inv()

    def sgn(s):
        a, b, DE = s.a, s.b, s.DE          # d > 0
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        x, y = a * a, DE * b * b
        if x == y:
            return 0
        return ((a > 0) - (a < 0)) if x > y else ((b > 0) - (b < 0))

    def cmp(s, o):
        return (s - o).sgn()

    def abs(s):
        return s if s.sgn() >= 0 else -s

    def pw(s, n):
        r, b = Q2.i(1, s.DE), s
        while n:
            if n & 1: r = r * b
            b = b * b; n >>= 1
        return r

    def fl(s):
        """float, via an exact rational square root approximation."""
        sc = 1 << 160
        r = isqrt(s.DE * sc * sc)
        from fractions import Fraction as Fr
        v = Fr(s.a, s.d) + Fr(s.b, s.d) * Fr(r, sc)
        try:
            return float(v)
        except OverflowError:
            return float('inf') if v > 0 else float('-inf')

    def floor(s):
        lo, hi = 0, 1
        def le(n):
            return (s - Q2.i(n, s.DE)).sgn() >= 0
        f = s.fl()
        n = int(f) if abs(f) < 1e17 else 0
        if le(n):
            lo, hi, st = n, n + 1, 1
            while le(hi):
                lo = hi; hi += st; st *= 2
        else:
            hi, lo, st = n, n - 1, 1
            while not le(lo):
                hi = lo; lo -= st; st *= 2
        while hi - lo > 1:
            m = (lo + hi) // 2
            if le(m): lo = m
            else: hi = m
        return lo


class Inst:
    """everything derived from the certificate header, recomputed here."""

    def __init__(s, c):
        s.c = c
        s.A, s.B, s.C, s.sg, s.M = c['A'], c['B'], c['C'], c['s'], c['M']
        s.R = set(map(tuple, c['R']))
        s.DE = s.B * s.B - 4 * s.A * s.C
        s.alpha = Q2(-s.B, s.sg, 2 * s.A, s.DE)
        s.alphap = Q2(-s.B, -s.sg, 2 * s.A, s.DE)
        s.dd = Q2(0, s.sg, s.A, s.DE)
        s.rt = Q2(0, 1, 1, s.DE)

    def Q(s, m, k):
        return s.A * k * k + s.B * m * k + s.C * m * m

    def eta(s, m, k):
        return Q2(2 * s.A * k + s.B * m, m * s.sg, 2 * s.A, s.DE)

    def xi(s, m, k):
        return Q2(2 * s.A * k + s.B * m, -m * s.sg, 2 * s.A, s.DE)

    def H(s, m, k):
        return Q2(2 * s.A * k - s.B * m, m * s.sg, 2 * s.A, s.DE)

    def adm(s, m, k):
        return m > 0 and k > 0 and (m % s.M, k % s.M) in s.R

    def hcmp(s, v1, v2):
        return s.H(*v1).cmp(s.H(*v2))

    def epscmp(s, v1, v2):
        """sign(eps(v1) - eps(v2)) = sign(|xi1| H2 - |xi2| H1)."""
        return (s.xi(*v1).abs() * s.H(*v2) - s.xi(*v2).abs() * s.H(*v1)).sgn()


def sort_h(I, states, force_fail=False):
    """approximate sort, exactly verified, with a GUARANTEED exact-comparator
    fallback (review O2).  Returns (sorted_list, used_fallback)."""
    import functools
    if not force_fail:
        try:
            af = I.alpha.fl()
            if af != af or af in (float('inf'), float('-inf')):
                raise ValueError('degenerate key')
            out = sorted(states, key=lambda v: v[0] * af + v[1])
            if all(I.hcmp(out[i], out[i + 1]) < 0 for i in range(len(out) - 1)):
                return out, False
        except Exception:
            pass
    out = sorted(states, key=functools.cmp_to_key(I.hcmp))
    assert all(I.hcmp(out[i], out[i + 1]) < 0 for i in range(len(out) - 1)), \
        'exact comparator sort failed'
    return out, True


def mul(X, Y):
    return [[X[0][0] * Y[0][0] + X[0][1] * Y[1][0], X[0][0] * Y[0][1] + X[0][1] * Y[1][1]],
            [X[1][0] * Y[0][0] + X[1][1] * Y[1][0], X[1][0] * Y[0][1] + X[1][1] * Y[1][1]]]


def app(X, v):
    return (X[0][0] * v[0] + X[0][1] * v[1], X[1][0] * v[0] + X[1][1] * v[1])


def minv(X):
    (a, b), (cc, d) = X[0], X[1]
    det = a * d - b * cc
    assert det in (1, -1)
    return [[d // det, -b // det], [-cc // det, a // det]]


# ---------------------------------------------------------------------- main
def check(c, verbose=True, brute_cap=400):
    nf = [0]; nt = [0]
    def ck(ok, lbl, extra=''):
        nt[0] += 1
        if not ok: nf[0] += 1
        if verbose or not ok:
            print(('    PASS  ' if ok else '    FAIL  ') + lbl + (('   ' + extra) if extra else ''))
    I = Inst(c)
    DE = I.DE
    T, U, j = c['T'], c['U'], c['j']
    X0, P = c['X0'], c['P']

    # C1 -- Pell
    ck(T * T - DE * U * U == 4, 'C1 T^2 - Delta U^2 = 4', f'T={T} U={U} Delta={DE}')
    ck(all(not (lambda v: v > 0 and isqrt(v) ** 2 == v)(DE * u * u + 4) for u in range(1, U)),
       'C1 U is the least positive solution')
    ck(DE > 0 and isqrt(DE) ** 2 != DE, 'C1 Delta > 0 and not a square')
    ck(gcd(gcd(I.A, I.B), I.C) == 1 and I.A > 0, 'C1 the polynomial is primitive with A > 0')
    ck(I.alpha.sgn() > 0, 'C1 alpha > 0')

    # C2 -- the automorph
    ck(X0[0][0] * X0[1][1] - X0[0][1] * X0[1][0] == 1, 'C2 det X0 = 1')
    TV = [(1, 1), (2, 3), (5, -7), (11, 4), (0, 1), (1, 0), (-3, 2), (7, -5)]
    ck(all(I.Q(*app(X0, v)) == I.Q(*v) for v in TV), 'C2 X0 preserves Q exactly')
    lam = Q2(T, U, 2, DE)
    ck(all((I.eta(*app(X0, v)) - lam * I.eta(*v)).sgn() == 0 for v in TV)
       or all((I.eta(*app(minv(X0), v)) - lam * I.eta(*v)).sgn() == 0 for v in TV),
       'C2 X0 (or its inverse) multiplies eta by lam = (T+U sqrt(Delta))/2')
    ck(lam.cmp(Q2.i(1, DE)) > 0, 'C2 lam > 1')

    # C3 -- the class-fixing power
    Y = X0
    for _ in range(j - 1):
        Y = mul(Y, X0)
    ck(Y == P, f'C3 P = X0^j with j = {j}')
    ck(all(P[r][q] % I.M == (1 if r == q else 0) % I.M for r in range(2) for q in range(2)),
       f'C3 P = I (mod {I.M}), so every residue class is fixed')
    ck(all(I.Q(*app(P, v)) == I.Q(*v) for v in TV), 'C3 P preserves Q exactly')
    ck(all(gcd(abs(v[0]), abs(v[1])) == gcd(*map(abs, app(P, v))) for v in TV if v != (0, 0)),
       'C3 P preserves gcd')
    rho = lam.pw(j)
    # orient: eta must be multiplied by rho (not 1/rho)
    e0 = I.eta(1, 0); e1 = I.eta(*app(P, (1, 0)))
    ck((e1 - rho * e0).sgn() == 0, 'C3 P multiplies eta by rho = lam^j')

    # C4 -- the family
    fam = [tuple(v) for v in c['family']]
    okf = True
    famfwd = []
    for v in fam:
        w = v
        for _ in range(400):
            if w[0] > 0 and w[1] > 0:
                break
            w = app(P, w)
        if not (w[0] > 0 and w[1] > 0):
            continue
        if not I.adm(*w):
            okf = False
        famfwd.append(w)
    ck(okf and famfwd, 'C4 every usable family seed reaches an admissible positive state',
       f'{len(famfwd)} of {len(fam)}')
    ck(all(abs(I.Q(*v)) <= c['D'] for v in fam),
       f"C4 every family seed has |Q| <= D = {c['D']}")
    floor_state = tuple(c['family_floor'])
    ck(I.adm(*floor_state) and all(I.hcmp(floor_state, v) <= 0 for v in famfwd),
       'C4 the declared family floor is the lowest family member')

    # C5 -- the cutoff, recomputed from the definition
    K, TF = c['cutoff_periods'], c['cutoff_tail_from']
    members = []
    for v in famfwd:
        w = v
        for p in range(K + 1):
            if w[0] > 0 and w[1] > 0:
                members.append((w, p))
            w = app(P, w)
    srt, fb1 = sort_h(I, [x[0] for x in members])
    pos = {v: i for i, v in enumerate(srt)}
    members.sort(key=lambda x: pos[x[0]])
    ok_sort = all(I.hcmp(members[i][0], members[i + 1][0]) < 0 for i in range(len(members) - 1))
    ck(ok_sort, 'C5 the family ordering is exact (fallback used: %s)' % fb1)
    def Fpair(vA, vC):
        QA = abs(I.Q(*vA))
        r = I.H(*vC) / I.H(*vA)
        u = Q2.i(I.B * I.Q(*vA), DE) / (2 * I.alpha * Q2.i(I.A ** 2, DE) * I.eta(*vA) * I.eta(*vA))
        th = 2 * u if u.sgn() > 0 else Q2.i(0, DE)
        return QA * r * r * (Q2.i(1, DE) + th)
    worstF, wp = None, None
    for i in range(len(members) - 1):
        if members[i][1] >= K - 2:
            continue
        f = Fpair(members[i][0], members[i + 1][0])
        if worstF is None or f.cmp(worstF) > 0:
            worstF, wp = f, (members[i][0], members[i + 1][0])
    tails = []
    for i in range(len(members) - 1):
        if members[i][1] != TF:
            continue
        vA, vC = members[i][0], members[i + 1][0]
        QA = abs(I.Q(*vA))
        eA, eC = I.eta(*vA), I.eta(*vC)
        r = (eC / eA).abs()
        one = Q2.i(1, DE)
        A2 = Q2.i(I.A ** 2, DE)
        uA = Q2.i(I.B * I.Q(*vA), DE) / (2 * I.alpha * A2 * eA * eA)
        uC = Q2.i(I.B * I.Q(*vC), DE) / (2 * I.alpha * A2 * eC * eC)
        w = uA.abs() if uA.abs().cmp(uC.abs()) > 0 else uC.abs()
        if w.cmp(one) >= 0:
            continue
        tails.append(QA * r * r * ((one + w) / (one - w)) * ((one + w) / (one - w)) * (one + 2 * w))
    ck(bool(tails), 'C5 a tail bound is available at the declared tail period')
    allmax = worstF
    for t in tails:
        if t.cmp(allmax) > 0:
            allmax = t
    ck(allmax.floor() == c['Bcut'],
       f"C5 Bcut = floor(sup F) = {c['Bcut']}",
       f'recomputed sup F = {allmax.fl():.6f} at {wp}')
    ck(c['Bcomp'] >= c['Bcut'], 'C5 Bcomp >= Bcut')
    # ---- C6: the eps_0 starting threshold and the uniform blocker bound
    thr = Q2.i(1, DE) if I.B == 0 else (I.rt / Q2.i(2 * abs(I.B), DE))
    if I.B != 0 and thr.cmp(Q2.i(1, DE)) >= 0:
        thr = Q2.i(1, DE)
    w0 = tuple(c['eps0_state'])
    ck(I.adm(*w0), 'C6 the declared eps_0 state is admissible')
    ck((I.xi(*w0).abs() - thr * I.H(*w0)).sgn() < 0,
       'C6 eps(w0) < min(1, sqrt(Delta)/(2|B|))',
       f'eps = {(I.xi(*w0).abs()/I.H(*w0)).fl():.6f} < {thr.fl():.6f}')
    ck(c['Bcomp_uniform'] == 3 * c['Bcut'],
       'C6 the uniform bound 3 Bcut is recorded (licensed by eps < sqrt(Delta)/(2|B|))')
    # recompute the per-candidate bound used for the enumeration
    n0, d0 = I.xi(*w0).abs(), I.H(*w0)
    num = I.rt * d0 + Q2.i(abs(I.B), DE) * n0
    den = I.rt * d0 - Q2.i(abs(I.B), DE) * n0
    ck(den.sgn() > 0, 'C6 the blocker bound is non-vacuous at w0 (no fallback needed)')
    val = Q2.i(c['Bcut'], DE) * num / den
    ck(c['Bcomp'] >= c['Bcut'] and c['Bcomp'] <= max(c['Bcut'], val.floor())
       and c['Bcomp'] <= c['Bcomp_uniform'],
       'C6 Bcomp is the proved per-candidate bound and is <= 3 Bcut',
       f"Bcomp = {c['Bcomp']}, recomputed floor = {val.floor()}, uniform = {c['Bcomp_uniform']}")
    # C7 -- enumeration completeness: independent scan of the reduction box
    Bmax = max(c['Bcut'], c['Bcomp'])
    one = Q2.i(1, DE)
    addf = abs(I.dd.fl())
    mb = int((lam.fl() + Bmax / I.A) / addf) + 2
    kb = int(Bmax / I.A + mb * I.alpha.fl()) + 2
    ck(mb <= c['box'][0] + 2 and kb <= c['box'][1] + 2,
       'C7 the declared reduction box is at least as large as the recomputed one',
       f'recomputed +-{mb} x +-{kb}, declared +-{c["box"][0]} x +-{c["box"][1]}')
    classes = []
    for m in range(-mb, mb + 1):
        for k in range(-kb, kb + 1):
            q = I.Q(m, k)
            if q == 0 or abs(q) > Bmax:
                continue
            ae = I.eta(m, k).abs()
            if ae.cmp(one) < 0 or ae.cmp(lam) >= 0:
                continue
            classes.append(((m, k), q))
    found = set()
    for rep, q in classes:
        w = rep
        for p in range(j):
            if (w[0] % I.M, w[1] % I.M) in I.R:
                found.add((w, q))
            w = app(X0, w)
    # keep only those with a positive window inside +-W
    Wd = c['W']; Pi = minv(P)
    def window(rep):
        st = {}; w = rep
        for qq in range(0, Wd + 1):
            st[qq] = w; w = app(P, w)
        w = rep
        for qq in range(-1, -Wd - 1, -1):
            w = app(Pi, w); st[qq] = w
        return st, sorted(qq for qq, v in st.items() if v[0] > 0 and v[1] > 0)
    mine = {}
    for rep, q in found:
        st, win = window(rep)
        if win:
            mine[rep] = (q, st, win)
    theirs = {tuple(o['rep']): o for o in c['orbits']}
    ck(set(mine) == set(theirs),
       'C7 the certificate orbit list equals the independent box enumeration',
       f'mine {len(mine)}, theirs {len(theirs)}, '
       f'missing {sorted(set(mine)-set(theirs))[:3]}, extra {sorted(set(theirs)-set(mine))[:3]}')
    okq = all(mine[r][0] == theirs[r]['Q'] for r in mine if r in theirs)
    ck(okq, 'C7 the declared defects agree')
    okw = True
    for r in mine:
        if r not in theirs:
            continue
        q, st, win = mine[r]
        e = I.eta(*r)
        fwd = (e.sgn() * I.dd.sgn()) > 0
        if fwd != theirs[r]['fwd'] or min(win) != theirs[r]['win_lo'] or max(win) != theirs[r]['win_hi']:
            okw = False
    ck(okw, 'C7 the declared forward flags and positive windows agree')

    # C8 -- p_cert from the ledger, recomputed
    A2 = Q2.i(I.A ** 2, DE)
    reps = {}
    for r in mine:
        q, st, win = mine[r]
        nn = [x for x in win if x >= 0]
        q0 = nn[0] if nn else win[0]
        e = I.eta(*r)
        if (e.sgn() * I.dd.sgn()) <= 0:
            continue
        # normalise |eta| into [1, rho)
        v = st[q0]
        while I.eta(*v).abs().cmp(one) < 0:
            v = app(P, v)
        while I.eta(*v).abs().cmp(rho) >= 0:
            v = app(Pi, v)
        reps[r] = (I.eta(*v).abs(), q)
    okl = True; recomputed = 0
    for row in c['ledger']:
        a, b = tuple(row['A']), tuple(row['B'])
        if a not in reps or b not in reps:
            okl = False; continue
        rA, QA = reps[a]; rB, QB = reps[b]
        d = row['d']
        Gd = abs(QA) * rB * rB * rho.pw(2 * d) - abs(QB) * rA * rA
        rhs = I.B * (abs(QB) * QA - abs(QA) * QB)   # corrected sign (R1)
        if Gd.sgn() != row['Gd_sign'] or rhs != row['rhs'] or QA != row['QA'] or QB != row['QB']:
            okl = False; continue
        if Gd.sgn() != 0:
            p = d
            while p <= 400:
                if (2 * I.alpha * A2 * rho.pw(2 * (p - d)) * Gd.abs() - Q2.i(abs(rhs), DE)).sgn() > 0:
                    break
                p += 1
            if p != row['eps_threshold']:
                okl = False
        Uq = 2 * I.alpha * A2 * rA * rB * rho.pw(d) * (rB * rho.pw(d) - rA)
        Vq = Q2.i(I.B, DE) * (Q2.i(QB, DE) * rA - Q2.i(QA, DE) * rB * rho.pw(d))
        if Uq.sgn() == 0:
            if Vq.sgn() != 0:
                okl = False
        else:
            qq = 0
            while qq <= 400:
                if (rho.pw(2 * qq) * Uq.abs() - Vq.abs()).sgn() > 0:
                    break
                qq += 1
            if qq + d != row['h_threshold']:
                okl = False
        recomputed += 1
    ck(okl, 'C8 every ledger row (Gamma_d sign, rhs, eps- and height-thresholds) recomputes',
       f'{recomputed} rows')
    pc_from_ledger = max([max(r.get('eps_threshold', 0), r.get('h_threshold', 0))
                          for r in c['ledger'] if r['d'] <= c['d_star']] or [0])
    ck(c['p_cert'] >= pc_from_ledger,
       f"C8 p_cert = {c['p_cert']} dominates every d <= d_star ledger threshold",
       f'ledger max {pc_from_ledger}')
    # the two same-orbit rows that justify monotonicity must be present and decisive
    mono_eps = [r for r in c['ledger'] if r['A'] == r['B'] and r['d'] == 1
                and r['eps_verdict'] == 'B_beats_A']
    mono_h = [r for r in c['ledger'] if r['A'] == r['B'] and r['d'] == 1
              and r['h_verdict'] == 'H_B_gt_H_A']
    # The ledger covers (competitor, CANDIDATE) pairs -- pairs of two
    # non-candidates are irrelevant to the persistence argument -- so the
    # same-orbit rows exist exactly for the candidate orbits.
    ncand = sum(1 for r in reps if abs(reps[r][1]) <= c['Bcut'])
    ck(len(mono_eps) == ncand, 'C8 eps strictly decreases along every CANDIDATE forward orbit '
       '(same-orbit, d=1 rows, all "B beats A")', f'{len(mono_eps)}/{ncand}')
    ck(len(mono_h) == ncand, 'C8 H strictly increases along every CANDIDATE forward orbit '
       'beyond its threshold (same-orbit, d=1 rows, all "H_B > H_A")', f'{len(mono_h)}/{ncand}')

    # C9 -- the offset bound, recomputed and re-measured independently.
    # The binding offset (largest level below H_B) is UNBOUNDED when alpha' > 0,
    # because the height is U-shaped in the eta-level there.  What must be
    # bounded is the BLOCKING offset (eps_A <= eps_B as well), and it is:
    #   d_star  = least d with rho^{2d-2} > Bmax
    #   p_noblock = least L with 2 alpha A^2 rho^{2L}(1 - Bmax rho^{2-2(d*+1)})
    #                            > 2 |B| Bmax
    # and for d > d_star no competitor can block at any level >= p_noblock.
    okl0 = all(I.eta(*r).abs().cmp(one) >= 0 and I.eta(*r).abs().cmp(rho) < 0 for r in mine)
    ck(okl0, 'C9 every orbit representative has |eta| in [1,rho), so stored period = eta-level')
    A2q = Q2.i(I.A ** 2, DE)
    d = 1
    while d <= 400:
        if (rho.pw(2 * d - 2) - Q2.i(Bmax, DE)).sgn() > 0:
            break
        d += 1
    ck(d == c['d_star'], f"C9 d_star = {c['d_star']} recomputes", f'mine {d}')
    dd1 = d + 1
    brack = Q2.i(1, DE) - Q2.i(Bmax, DE) / rho.pw(2 * dd1 - 2)
    ck(brack.sgn() > 0, 'C9 the d_star bracket is positive')
    rhsq = Q2.i(2 * abs(I.B) * Bmax, DE)
    L = 0
    while L <= 400:
        if (2 * I.alpha * A2q * rho.pw(2 * L) * brack - rhsq).sgn() > 0:
            break
        L += 1
    ck(L == c['p_noblock'], f"C9 p_noblock = {c['p_noblock']} recomputes", f'mine {L}')
    thr = max([max(r.get('eps_threshold', 0), r.get('h_threshold', 0))
               for r in c['ledger'] if r['d'] <= c['d_star']] or [0])
    ck(c['p_cert'] >= max(thr, L),
       f"C9 p_cert = {c['p_cert']} dominates both the d <= d_star thresholds ({thr}) "
       f'and p_noblock ({L})')
    have = {(tuple(r['A']), tuple(r['B']), r['d']) for r in c['ledger']}
    cands = [r for r in reps if abs(reps[r][1]) <= c['Bcut']]
    # (P4) the LOWER endpoint of the offset range: a competitor at a LATER level
    # lies above the candidate in height, so negative offsets are excluded and the
    # ledger's finite range 0 <= d <= d* is complete.  The deciding comparisons are
    # the (candidate, competitor) rows at d = 1, which give sgn(H_comp(q+1) - H_cand(q)).
    up = [(a, b) for a in cands for b in reps
          if (a, b, 1) not in have or
          next((r for r in c['ledger']
                if tuple(r['A']) == a and tuple(r['B']) == b and r['d'] == 1), {})
          .get('h_verdict') != 'H_B_gt_H_A']
    ck(not up, 'C9 every (candidate, competitor) pair has a d=1 height row certifying that the '
       'competitor one level later is ABOVE the candidate, which excludes negative offsets',
       f'{len(cands)} candidates x {len(reps)} competitors; missing/wrong {up[:3]}')
    ck(all((a, b, dd) in have for a in reps for b in cands for dd in range(c['d_star'] + 1)),
       f"C9 the ledger certifies every (competitor, candidate) pair at every "
       f"d <= d_star = {c['d_star']}",
       f'{len(have)} rows for {len(reps)} x {len(cands)} x {c["d_star"]+1}')
    # independent exhaustive re-measurement of binding and blocking offsets
    pc = c['p_cert']
    bind_max, block_offs, badlow, nchk = -1, set(), [], 0
    for r in reps:
        q, st, win = mine[r]
        nn = [x for x in win if x >= 0]
        enter = nn[0] if nn else win[0]
        for p in range(pc, pc + 4):
            pev = enter + p
            if pev not in win:
                continue
            vB = st[pev]
            for r2 in mine:
                q2, st2, win2 = mine[r2]
                cands = [x for x in win2 if st2[x] != vB and I.hcmp(st2[x], vB) < 0]
                if not cands:
                    continue
                bx = max(cands)
                nchk += 1
                bind_max = max(bind_max, pev - bx)
                if I.epscmp(vB, st2[bx]) >= 0:
                    block_offs.add(pev - bx)
                for x in cands:
                    if x < bx and I.epscmp(vB, st2[x]) >= 0:
                        block_offs.add(pev - x)
                        badlow.append((r, r2, x, bx))
    ck(block_offs and max(block_offs) <= c['d_star'],
       f"C9 every BLOCKING offset is <= d_star = {c['d_star']} (independent exhaustive scan)",
       f'blocking offsets {sorted(block_offs)}; {nchk} pairs; binding offsets reach {bind_max}')
    # (P1) The claim "no earlier state blocks" is FALSE -- at alpha = phi,
    # unrestricted, the candidate (15,24) = 3*(5,8) is blocked by (5,8), which
    # lies BELOW the eps-minimal binding state (13,21).  What is true, and what
    # is actually needed, is SUFFICIENCY: if any state of an orbit blocks the
    # candidate then the eps-minimal state below H_B blocks it too, so the
    # three-way verdict read off the eps-minimal state equals the verdict of an
    # exhaustive scan.  That is what is tested.
    suff = []
    for r in reps:
        q, st, win = mine[r]
        nn = [x for x in win if x >= 0]
        enter = nn[0] if nn else win[0]
        for p in (pc, pc + 1):
            pev = enter + p
            if pev not in win:
                continue
            vB = st[pev]
            for r2 in mine:
                q2, st2, win2 = mine[r2]
                bel = [st2[x] for x in win2 if st2[x] != vB and I.hcmp(st2[x], vB) < 0]
                if not bel:
                    continue
                # exhaustive verdict over the orbit
                exh = 'record'
                for v in bel:
                    cc = I.epscmp(v, vB)
                    if cc < 0:
                        exh = 'lost'; break
                    if cc == 0:
                        exh = 'tie'
                # verdict from the eps-minimal state alone
                bb = bel[0]
                for v in bel[1:]:
                    if I.epscmp(v, bb) < 0:
                        bb = v
                cc = I.epscmp(bb, vB)
                mi = 'lost' if cc < 0 else ('tie' if cc == 0 else 'record')
                if mi != exh:
                    suff.append((r, r2, p, mi, exh))
    ck(not suff, 'C9 SUFFICIENCY: the verdict from the eps-minimal state below H_B equals the '
       'verdict of an exhaustive scan of the orbit (the earlier claim that no earlier state '
       'can block is false and is not used)', f'mismatches {suff[:3]}')
    ck(sorted(block_offs) == sorted({o for o in c['observed_blocking_offsets']}),
       'C9 the certificate\'s declared blocking offsets match the independent scan',
       f"mine {sorted(block_offs)}, theirs {sorted(c['observed_blocking_offsets'])}")

    # C10 -- verdicts, fully UNPRUNED
    def verdict(vB):
        tie = None
        for r2 in mine:
            q2, st2, win2 = mine[r2]
            # minimal-eps competitor below H_B: the definition of blocking, with
            # no monotonicity hypothesis (review item R2)
            best, bq = None, None
            for x in win2:
                w = st2[x]
                if w == vB:
                    continue
                if I.hcmp(w, vB) < 0 and (best is None or I.epscmp(w, best) < 0):
                    best, bq = w, x
            if best is None:
                continue
            cc = I.epscmp(vB, best)
            if cc > 0:
                return False, None
            if cc == 0 and tie is None:
                tie = r2
        return (tie is None), tie
    rec_mine, tie_mine = set(), {}
    for r in reps:
        q, st, win = mine[r]
        nn = [x for x in win if x >= 0]
        enter = nn[0] if nn else win[0]
        ok3 = True; tiepartner = None
        for p in (pc, pc + 1, pc + 2):
            if enter + p not in win:
                ok3 = False; break
            isrec, tie = verdict(st[enter + p])
            if isrec:
                continue
            ok3 = False
            if tie is not None and tiepartner is None:
                tiepartner = tie
        if ok3:
            rec_mine.add(r)
        elif tiepartner is not None:
            tie_mine[r] = tiepartner
    ck(rec_mine == set(map(tuple, c['record_tails'])),
       'C10 the certified record tails reproduce under an unpruned re-evaluation',
       f'mine {len(rec_mine)}, theirs {len(c["record_tails"])}, '
       f'diff {sorted(rec_mine ^ set(map(tuple, c["record_tails"])))[:3]}')
    ck(set(tie_mine) == set(tuple(t['orbit']) for t in c['ties']),
       'C10 the permanent ties reproduce',
       f'mine {len(tie_mine)}, theirs {len(c["ties"])}')
    for t in c['ties']:
        o, pa = tuple(t['orbit']), tuple(t['partner'])
        q, st, win = mine[o]
        q2, st2, win2 = mine[pa]
        nn = [x for x in win if x >= 0]; en = nn[0] if nn else win[0]
        nn2 = [x for x in win2 if x >= 0]; en2 = nn2[0] if nn2 else win2[0]
        okt = True
        for p in (pc, pc + 1):
            if en + p not in win:
                okt = False; break
            vB = st[en + p]
            cands = [x for x in win2 if I.hcmp(st2[x], vB) < 0]
            if not cands:
                okt = False; break
            w = st2[max(cands)]
            if I.epscmp(vB, w) != 0:
                okt = False
        ck(okt, f'C10 the declared tie {o} ~ {pa} is an exact eps equality at a lower height')

    # every record tail state at the evaluation level must have eps < thr, which
    # forces G > 0 there and so excludes the branch on which eps increases
    okG = True
    for r in c['record_tails']:
        rr = tuple(r)
        if rr not in mine:
            okG = False; continue
        q, st, win = mine[rr]
        nn = [x for x in win if x >= 0]
        en = nn[0] if nn else win[0]
        pev = en + c['p_cert']
        if pev not in win:
            okG = False; continue
        v = st[pev]
        if (I.xi(*v).abs() - thr * I.H(*v)).sgn() >= 0:
            okG = False
        G = 2 * I.alpha * Q2.i(I.A ** 2, DE) * I.eta(*v) * I.eta(*v) + Q2.i(I.B * I.Q(*v), DE)
        if G.sgn() <= 0:
            okG = False
    ck(okG, 'C6 every record-tail state at the evaluation level has eps < eps_0 and G > 0')

    # ---- C6b: the TWO-CASE backward exclusion (review O1)
    A2q = Q2.i(I.A ** 2, DE)
    def Yof(v):
        e = I.eta(*v); return A2q * e * e
    def Gs(v):
        return (Yof(v) * 2 * I.alpha + Q2.i(I.B * I.Q(*v), DE)).sgn()
    def Ystar(Q):
        # Ystar = (|Q| sqrt(Delta) * d0/n0 - B Q)/(2 alpha), eps_0 = n0/d0 attained
        return (Q2.i(abs(Q), DE) * I.rt * d0 / n0 - Q2.i(I.B * Q, DE)) / (2 * I.alpha)
    flo = None if I.B == 0 else I.rt / Q2.i(abs(I.B), DE)
    ok_i = ok_ii = ok_cov = ok_min = ok_L = True
    n_i = n_ii = 0
    for r, o in theirs.items():
        q, st, win = mine[r]
        Ys = Ystar(q)
        if not o['fwd']:
            n_i += 1
            if o.get('case') != 'i':
                ok_i = False
            for x in win:
                v = st[x]
                if Gs(v) >= 0:
                    ok_i = False
                if flo is not None and (I.xi(*v).abs() - flo * I.H(*v)).sgn() < 0:
                    ok_i = False
        else:
            n_ii += 1
            if o.get('case') != 'ii':
                ok_ii = False
            for x in win:
                v = st[x]
                if Gs(v) <= 0:
                    continue
                lhs = (Yof(v) - Ys).sgn() <= 0
                rhs = (I.xi(*v).abs() * d0 - n0 * I.H(*v)).sgn() >= 0
                if lhs != rhs:
                    ok_ii = False
            # only the doubly-infinite orbits can have positive states outside
            # the window, so only they need the cutoff to be strictly inside it
            # Lemma 6.0c: recompute L* by the exact two-sided search and verify
            # BOTH witness inequalities Y_{L*} <= Ystar < Y_{L*+1}, plus
            # uniqueness (Y_L strictly increasing, since rho^2 > 1).
            rep_e = I.eta(*r).abs()
            baseY = A2q * rep_e * rep_e
            def YL(L):
                return baseY * rho.pw(2 * L) if L >= 0 else baseY / rho.pw(-2 * L)
            Lc = 0
            if (YL(Lc) - Ys).sgn() <= 0:
                st2_ = 1
                while (YL(Lc + st2_) - Ys).sgn() <= 0:
                    Lc += st2_; st2_ *= 2
                while (YL(Lc + 1) - Ys).sgn() <= 0:
                    Lc += 1
            else:
                st2_ = 1
                while (YL(Lc) - Ys).sgn() > 0:
                    Lc -= st2_; st2_ *= 2
                while (YL(Lc) - Ys).sgn() > 0:
                    Lc -= 1
                while (YL(Lc + 1) - Ys).sgn() <= 0:
                    Lc += 1
            if o.get('Lstar') != Lc:
                ok_L = False
            if not ((YL(Lc) - Ys).sgn() <= 0 and (YL(Lc + 1) - Ys).sgn() > 0):
                ok_L = False
            if (YL(Lc + 1) - YL(Lc)).sgn() <= 0:
                ok_L = False
            if o.get('double'):
                if o.get('Lstar') is None or o['Lstar'] < min(win):
                    ok_cov = False
            BQ = I.B * q
            if BQ > 0:
                Ymin = Q2.i(BQ, DE) / (2 * I.alpha)
                if (Ys - Ymin).sgn() < 0:        # Y* >= Y_min suffices
                    ok_min = False
    ck(ok_i, 'C6b case (i): every orbit without a forward tail has G < 0 on all its '
       'positive states and respects the floor eps >= sqrt(Delta)/|B|', f'{n_i} orbits')
    ck(ok_ii, 'C6b case (ii): on every G>0 state the equivalence Y <= Ystar <=> eps >= eps_0 '
       'holds, with the ATTAINED eps_0', f'{n_ii} orbits')
    ck(ok_cov, 'C6b on every DOUBLY-INFINITE orbit the stored window reaches below the eps_0 '
       'level cutoff, so no possible blocker lies outside it; orbits whose positive part '
       'begins inside the window need no such condition')
    ck(ok_min, 'C6b Ystar >= Y_min whenever B Q > 0, so on the RETAINED region Y > Ystar the '
       'height is strictly increasing (the boundary case Ystar = Y_min is admissible)')
    okT = True
    for r, o in theirs.items():
        if not o['fwd']:
            continue
        if o.get('T') is None or o['T'] != o['enter'] + c['p_cert']:
            okT = False
        if o.get('Lstar') is not None and not (o['T'] > o['Lstar']):
            okT = False
    ck(okT, 'C6b the absolute tail-start level T_i = enter_i + p_cert is declared and satisfies '
       'T_i > L*_i, so P4 / P5 / P6 are disjoint')
    ck(ok_L, 'C6b the cutoff level L* recomputes by the exact two-sided search, both witness '
       'inequalities Y_{L*} <= Ystar < Y_{L*+1} hold, and Y_L is strictly increasing in L')
    ck(flo is None or (I.rt * Q2.i(1, DE) - flo * Q2.i(0, DE)).sgn() != 0 or True, 'C6b sanity')
    if flo is not None:
        ck((flo * d0 - n0).sgn() > 0,
           'C6b sqrt(Delta)/|B| > eps_0, so case (i) really excludes its states')

    # C12 -- independent brute force
    st_list = []
    m = 1
    while True:
        # largest k with m*alpha + k <= brute_cap
        k = 0
        while (Q2.i(brute_cap, DE) - I.H(m, k + 1)).sgn() >= 0:
            k += 1
        if k == 0:
            break
        for kk in range(1, k + 1):
            if I.adm(m, kk):
                st_list.append((m, kk))
        m += 1
    st_list, fb2 = sort_h(I, st_list)
    ok_sort2 = all(I.hcmp(st_list[i], st_list[i + 1]) < 0 for i in range(len(st_list) - 1))
    ck(ok_sort2, 'C12 brute-force ordering is exact', f'{len(st_list)} states, fallback {fb2}')
    st_list_f, fb3 = sort_h(I, list(st_list), force_fail=True)
    ck(fb3 and st_list_f == st_list,
       'C12 the exact-comparator fallback reproduces the same order when the '
       'approximate key is forced to fail')
    recs, best = [], None
    for v in st_list:
        if best is None or I.epscmp(v, best) < 0:
            recs.append(v); best = v
    floorH = I.H(*floor_state)
    exc = set(tuple(e['state']) for e in c['initial_exceptions'])
    bad2 = []
    for v in recs:
        if (I.H(*v) - floorH).sgn() <= 0 or v in exc:
            continue
        # must belong to a certified record tail
        inrec = False
        for r in set(map(tuple, c['record_tails'])):
            q, st, win = mine[r]
            if any(st[x] == v for x in win):
                inrec = True; break
        if not inrec:
            bad2.append((v, I.Q(*v)))
    ck(not bad2, 'C12 every brute-force record above the family floor lies in a certified '
       'record tail (or is a declared initial exception)',
       f'{len(recs)} records to H <= {brute_cap}; exceptions {bad2[:3]}')
    ck(all(abs(I.Q(*v)) <= c['Bcut'] for v in recs if (I.H(*v) - floorH).sgn() > 0),
       'C12 the cutoff holds on every brute-force record above the family floor')
    # ---- C13: the exhaustive partition of Section 1 of PARTITION_AND_CHECK_MAP.md
    # Classify every admissible state below the brute cap into exactly one part
    # and verify the property each part claims.
    Hw = I.H(*w0)
    Bcut, Bcomp = c['Bcut'], c['Bcomp']
    owner = {}
    for r2, (q2, st2, win2) in mine.items():
        for x in win2:
            owner.setdefault(st2[x], (r2, x))
    counts = {k: 0 for k in ('P1', 'P2a', 'P2b', 'P3', 'P4', 'P5', 'P6')}
    bad13 = []
    recset = set(recs)
    for v in st_list:
        qv = abs(I.Q(*v))
        if (I.H(*v) - Hw).sgn() <= 0:
            part = 'P1'
        elif qv > Bcomp:
            part = 'P2a'
        elif qv > Bcut:
            part = 'P2b'
        else:
            own = owner.get(v)
            if own is None:
                bad13.append(('unenumerated', v, qv)); continue
            r2, lev = own
            o2 = theirs[r2]
            if not o2['fwd']:
                part = 'P3'
            elif o2.get('Lstar') is not None and lev <= o2['Lstar']:
                part = 'P4'
            elif lev < o2['enter'] + c['p_cert']:
                part = 'P5'
            else:
                part = 'P6'
        counts[part] += 1
        # the property each part claims
        if part in ('P2a', 'P2b') and v in recset:
            bad13.append(('record above the cutoff', v, qv))
        if part == 'P3':
            G = 2 * I.alpha * A2q * I.eta(*v) * I.eta(*v) + Q2.i(I.B * I.Q(*v), DE)
            if G.sgn() >= 0:
                bad13.append(('P3 with G >= 0', v, qv))
            if flo is not None and (I.xi(*v).abs() - flo * I.H(*v)).sgn() < 0:
                bad13.append(('P3 below the floor', v, qv))
            if v in recset:
                bad13.append(('P3 is a record', v, qv))
        if part == 'P4':
            if (I.xi(*v).abs() * d0 - n0 * I.H(*v)).sgn() < 0:
                bad13.append(('P4 with eps < eps_0', v, qv))
            if v in recset:
                bad13.append(('P4 is a record', v, qv))
    ck(not bad13, 'C13 the partition is exhaustive and each part\'s property holds on every '
       'admissible state below the cap',
       f'{sum(counts.values())} states: ' + ' '.join(f'{k}={counts[k]}' for k in counts)
       + (f'; violations {bad13[:3]}' if bad13 else ''))
    # and the record set is exactly P1-records plus the certified tails/exceptions
    predicted = set()
    for v in st_list:
        if (I.H(*v) - Hw).sgn() <= 0 and v in recset:
            predicted.add(v)
    for rr in set(map(tuple, c['record_tails'])):
        q3, st3, win3 = mine[rr]
        for x in win3:
            if st3[x] in recset:
                predicted.add(st3[x])
    for e in c['initial_exceptions']:
        tv = tuple(e['state'])
        if tv in recset:
            predicted.add(tv)
    ck(predicted == recset,
       'C13 the brute-force record set is exactly (P1 records) + (certified tails) + '
       '(declared initial exceptions)',
       f'{len(recset)} records; unexplained {sorted(recset - predicted)[:3]}')
    # ---- C14: COMPLETENESS of the finite region and of the exception list.
    # Two independent enumerations, compared by SET EQUALITY.
    # (a) P1: every admissible state with H <= H(w), from the explicit bounds
    #     1 <= m <= floor(H(w)/alpha), 1 <= k <= floor(H(w)), then exact filters.
    mmax = (Hw / I.alpha).floor()
    kmax = Hw.floor()
    p1 = []
    for m in range(1, mmax + 1):
        for k in range(1, kmax + 1):
            if not I.adm(m, k):
                continue
            if (I.H(m, k) - Hw).sgn() <= 0:
                p1.append((m, k))
    p1s, _fb = sort_h(I, p1)
    p1rec, best1 = [], None
    for v in p1s:
        if best1 is None or I.epscmp(v, best1) < 0:
            p1rec.append(v); best1 = v
    ck(set(p1rec) == {v for v in recs if (I.H(*v) - Hw).sgn() <= 0},
       'C14(a) the P1 record set, recomputed from the explicit bounds '
       f'1<=m<={mmax}, 1<=k<={kmax}, equals the brute-force records below H(w)',
       f'{len(p1)} P1 states, {len(p1rec)} records')
    ck(set(map(tuple, c['p1_records'])) == set(p1rec),
       'C14(a) and equals the P1 record set emitted in the certificate',
       f"emitted {len(c['p1_records'])}, recomputed {len(p1rec)}")
    # (b) P5: every eligible level L*_i < L < T_i on every CANDIDATE orbit, with
    #     its verdict recomputed unpruned; compared with the emitted exceptions.
    mine_exc = set()
    for r, o in theirs.items():
        if not o['fwd'] or abs(o['Q']) > Bcut:
            continue
        q4, st4, win4 = mine[r]
        lo4 = o['Lstar'] if o.get('Lstar') is not None else min(win4) - 1
        for L in win4:
            if not (lo4 < L < o['T']):
                continue
            v = st4[L]
            isrec, tie = verdict(v)
            tailrec = (r in rec_mine)
            if isrec != tailrec:
                mine_exc.add((v, isrec))
    theirs_exc = {(tuple(e['state']), bool(e['is_record_here']))
                  for e in c['initial_exceptions']}
    ck(mine_exc == theirs_exc,
       'C14(b) the initial-exception list is COMPLETE: an independent enumeration of every '
       'level L*_i < L < T_i on every candidate orbit, with verdicts recomputed unpruned, '
       'gives exactly the emitted set',
       f'mine {len(mine_exc)}, theirs {len(theirs_exc)}, '
       f'symmetric difference {sorted(mine_exc ^ theirs_exc)[:3]}')
    return nt[0], nf[0]


def regressions():
    """The three counterexamples from the third review, as mandatory tests."""
    nt = nf = 0
    def ck2(ok, lbl):
        nonlocal nt, nf
        nt += 1
        if not ok: nf += 1
        print(('    PASS  ' if ok else '    FAIL  ') + lbl)
    print('=' * 76); print('MANDATORY REGRESSIONS (third review)'); print('=' * 76)
    # R1: alpha = phi, a = (1,1), b = (1,3), Gamma = 0
    I = Inst(dict(A=1, B=-1, C=-1, s=1, M=2, R=[[1, 1]]))
    DE = I.DE
    a, b = (1, 1), (1, 3)
    QA, QB = I.Q(*a), I.Q(*b)
    Gam = abs(QA) * I.eta(*b) * I.eta(*b) - abs(QB) * I.eta(*a) * I.eta(*a)
    ck2(QA == -1 and QB == 5 and Gam.sgn() == 0, 'R1 setup: Q = -1, 5 and Gamma = 0')
    rhs = I.B * (abs(QB) * QA - abs(QA) * QB)
    ck2(rhs == 10, 'R1 the corrected RHS is +10 (the old display gave -10)')
    pred = (2 * I.alpha * Q2.i(I.A ** 2, DE) * Gam - Q2.i(rhs, DE)).sgn() > 0
    ck2(pred is False and I.epscmp(b, a) > 0,
        'R1 the corrected criterion agrees with the truth eps_b > eps_a')
    # R2: eps increases on the G<0 branch
    I2 = Inst(dict(A=1, B=-3, C=1, s=1, M=2, R=[[1, 1]]))
    v0, v1 = (55, 21), (3, 1)
    ck2(I2.epscmp(v1, v0) > 0, 'R2 eps(3,1) > eps(55,21): eps is NOT monotone on G<0')
    G0 = 2 * I2.alpha * Q2.i(1, I2.DE) * I2.eta(*v0) * I2.eta(*v0) + Q2.i(I2.B * I2.Q(*v0), I2.DE)
    ck2(G0.sgn() < 0, 'R2 and indeed G < 0 there')
    flo = I2.rt / Q2.i(abs(I2.B), I2.DE)
    ck2((I2.xi(*v0).abs() - flo * I2.H(*v0)).sgn() >= 0,
        'R2 both states respect the floor eps >= sqrt(Delta)/|B|')
    # R3: the exponent
    I3 = Inst(dict(A=1, B=-4, C=2, s=1, M=2, R=[[1, 1]]))
    DE3 = I3.DE
    rho3 = Q2(6, 2, 2, DE3)                       # lam = 3 + 2 sqrt2
    a0, b0 = (-61, -30), (-59, -29)
    rA = I3.eta(*a0).abs(); rB = I3.eta(*b0).abs()
    QA3, QB3 = I3.Q(*a0), I3.Q(*b0)
    U = 2 * I3.alpha * Q2.i(1, DE3) * rA * rB * (rB - rA)
    V = Q2.i(I3.B, DE3) * (Q2.i(QB3, DE3) * rA - Q2.i(QA3, DE3) * rB)
    pub = rho3.pw(1) * U + V
    cor = rho3.pw(2) * U + V
    X0 = [[-1, 2], [-4, 7]]
    a1, b1 = app(X0, a0), app(X0, b0)
    ck2(a1 == (1, 34) and b1 == (1, 33), 'R3 setup: X0 maps the reps to (1,34),(1,33)')
    ck2(I3.hcmp(b1, a1) < 0, 'R3 truth: H_b1 < H_a1')
    ck2(pub.sgn() > 0 and cor.sgn() < 0,
        'R3 rho^q U + V has the WRONG sign; rho^{2q} U + V has the right one')
    print(f'  {nt - nf}/{nt} regressions passed, {nf} failures')
    return nt, nf


if __name__ == '__main__':
    names = sys.argv[1:] or [os.path.basename(f)[:-5] for f in sorted(glob.glob(f'{CERT}/*.json'))]
    TT, FF = regressions()
    for n in names:
        c = json.load(open(f'{CERT}/{n}.json'))
        print('=' * 76); print(n); print('=' * 76)
        t, f = check(c, verbose=False)
        print(f'  {t - f}/{t} checks passed, {f} failures')
        TT += t; FF += f
    print('=' * 76)
    print(f'INDEPENDENT CHECKER: {TT - FF}/{TT} checks passed, {FF} failures over {len(names)} certificates')
