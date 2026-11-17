"""emit.py -- run the classifier and write a self-contained certificate per
instance into certificates/<name>.json.

The certificate carries everything an independent checker needs: the Pell
solution, the automorph and its class-fixing power, the comparison family, the
cutoff with the attaining pair and the tail-bound data, the reduction box, the
full orbit list with defects and positive windows, B_comp, p_cert together with
the PER-PAIR signs and thresholds that justify the offset window, and the final
record tails / permanent ties / initial exceptions.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
import sys, json, os, time
pass  # path set by the shim below
from gq import *
from math import gcd
from fractions import Fraction as Fr

OUT = _os.path.join(_ROOT, 'certificates')
DLIST = [1, 2, 3, 5, 8, 13, 20, 30, 50, 80, 130, 200]


def frpair(x):
    """a Surd as [[num,den],[num,den]] over sqrt(D) with the ambient D."""
    return [[x.p.numerator, x.p.denominator], [x.q.numerator, x.q.denominator]]


def build(A, B, C, s, M, R, name, Dlist=DLIST, W=24):
    for _W in (W, 2 * W, 4 * W, 8 * W):
        try:
            return _build(A, B, C, s, M, R, name, Dlist, _W)
        except WindowTooSmall:
            continue
    raise WindowTooSmall(f'{name}: no window up to {8 * W} covered the eps_0 cutoff')


class WindowTooSmall(Exception):
    pass


def _build(A, B, C, s, M, R, name, Dlist=DLIST, W=24):
    S = Setup(A, B, C, s, M, R, name)
    F = Fast(S)
    P, rho, j = S.rho_matrix()
    X0, lam = fundamental_expander(S)
    T, U = S.pell4()
    Bcut, seeds, D, info, sc = auto_family2(S, P, rho, Dlist=Dlist)
    fam_pos = [first_positive(S, P, sd)[0] for sd in seeds]
    fam_pos = [v for v in fam_pos if v is not None]
    famH = min(fam_pos, key=lambda v: S.H(*v).f())
    # ---- the eps_0 starting threshold.  Everything above H(w) has eps < eps_0,
    # hence G > 0, hence Lemma 6.1 applies and the uniform blocker bound
    # |Q_V| <= 3|Q_B| holds; so Bcomp = 3 Bcut is safe without any per-candidate
    # test.  Everything below H(w) is an explicitly finite region.
    thr = eps0_threshold(S)
    w0 = find_eps0_state(S, P, [v for v in fam_pos], thr)
    assert w0 is not None, 'no family state reached the eps_0 threshold'
    eps_fam = S.eps_num_den(*w0)
    # Lemma 5.4 with eps < eps_0 is never vacuous, so the per-candidate blocker
    # bound is ALWAYS available -- that is the real gain from eps_0, and it is
    # much tighter than the crude uniform |Q_V| <= 3|Q_B|.  Both are recorded:
    # Bcomp is the per-candidate bound evaluated at w0 (proved, and used for the
    # enumeration), Bcomp_uniform = 3 Bcut is the coarse uniform version.
    Bcomp = Bcomp_from(S, Bcut, eps_fam)
    Bcomp_uniform = 3 * Bcut
    assert Bcomp <= Bcomp_uniform, 'per-candidate bound exceeds the uniform one'
    pruning = True
    orbs_raw, box, jj, nclass = enumerate_orbits2(S, P, rho, max(Bcut, Bcomp))
    Pi = S.matinv(P)
    orbs = []
    for rep, Q in orbs_raw:
        st = {}; w = rep
        for q in range(0, W + 1):
            st[q] = w; w = S.matapply(P, w)
        w = rep
        for q in range(-1, -W - 1, -1):
            w = S.matapply(Pi, w); st[q] = w
        win = sorted(q for q, v in st.items() if v[0] > 0 and v[1] > 0)
        if not win:
            continue
        e = S.eta(*rep)
        fwd = (e.sign() * S.dd.sign()) > 0
        nn = [q for q in win if q >= 0]
        q0 = nn[0] if nn else win[0]
        orbs.append(dict(rep=rep, Q=Q, st=st, win=win, fwd=fwd, enter=q0,
                         double=(fwd and min(win) <= -W + 2)))
    # ---- the TWO-CASE backward exclusion (review O1).
    # (i) An orbit with sgn(eta*dd) < 0 has G = A^2 eta dd H < 0 on every positive
    #     state, so eps >= sqrt(Delta)/|B| there -- and sqrt(Delta)/|B| > eps_0,
    #     so none of those states is a record above H(w) or a blocker of one.
    # (ii) A doubly-infinite orbit has G > 0 on its whole positive part, and on
    #     its BACKWARD ray eps rises to sqrt(Delta)/|B| FROM BELOW, so the floor
    #     of (i) does NOT apply.  There the cutoff is the explicit level bound
    #     Y <= Ystar <=> eps >= eps_0 of gq.eps0_level_cutoff, evaluated with the
    #     ATTAINED eps_0 = eps(w).
    e0n, e0d = eps_fam
    rtD_over_B = None if S.B == 0 else S.rt / Surd(abs(S.B), 0, S.D)
    def Y_of(v):
        e = S.eta(*v)
        return Surd(S.A ** 2, 0, S.D) * e * e
    def Gsign(v):
        return (Y_of(v) * 2 * S.alpha + Surd(S.B * S.Qf(*v), 0, S.D)).sign()
    def eps_ge_eps0(v):
        n, d = S.eps_num_den(*v)
        return (n * e0d - e0n * d).sign() >= 0
    case_i, case_ii = [], []
    for o in orbs:
        Ys = eps0_level_cutoff(S, o['Q'], e0n, e0d)
        o['Ystar'] = Ys
        if not o['fwd']:
            okG = all(Gsign(o['st'][q]) < 0 for q in o['win'])
            okf = (S.B == 0) or all(
                (S.eps_num_den(*o['st'][q])[0]
                 - rtD_over_B * S.eps_num_den(*o['st'][q])[1]).sign() >= 0
                for q in o['win'])
            o['case'] = 'i'
            o['case_i_ok'] = bool(okG and okf)
            case_i.append(o['case_i_ok'])
            o['lvl_eps0'] = None
            o['Lstar'] = None
        else:
            # the cutoff level L*, by the exact two-sided search of Lemma 6.0c:
            # the unique integer with Y_{L*} <= Ystar < Y_{L*+1}.  The two
            # witness values go into the certificate; monotonicity then proves
            # the exclusion for every level <= L*, with no appeal to the window.
            rep_eta = S.eta(*o['rep'])
            rr = rep_eta if rep_eta.sign() > 0 else -rep_eta
            Lst, Ylo, Yhi = level_cutoff_search(S, rho, rr, Ys)
            o['Lstar'] = Lst
            o['Ylo'] = Ylo
            o['Yhi'] = Yhi
            o['case'] = 'ii'
            o['lvl_eps0'] = Lst + 1
            # the equivalence Y <= Ystar <=> eps >= eps_0 on every window state
            eq = all(((Y_of(o['st'][q]) - Ys).sign() <= 0) == eps_ge_eps0(o['st'][q])
                     for q in o['win'] if Gsign(o['st'][q]) > 0)
            o['case_ii_ok'] = bool(eq)
            case_ii.append(o['case_ii_ok'])
    assert all(case_i), 'case (i) failed: a non-forward orbit violated G<0 or the eps floor'
    assert all(case_ii), 'case (ii) failed: the Ystar equivalence broke on a G>0 state'

    fwdorbs = [o for o in orbs if o['fwd']]
    cert_in = [dict(pos=o['st'][o['enter']], Q=o['Q']) for o in fwdorbs]

    # ---- the offset bound.
    # The "d in {0,1}" window reduction is FALSE when alpha' > 0: the height is
    # U-shaped in the eta-level there, so the state of largest level below H_B
    # inside a doubly-infinite orbit can be ~L levels down.  Those states are
    # harmless (eps is monotone in the level, so a low-level state has LARGE
    # eps and cannot block), and the correct bound is on BLOCKING offsets, not
    # on binding offsets:  d_star = least d with rho^{2d-2} > Bcomp, plus a level
    # threshold p_noblock -- see gq.dstar_and_noblock.
    dstar, p_noblock = dstar_and_noblock(S, rho, max(Bcut, Bcomp))
    dmax = dstar
    pc, worst = certify_tail(S, P, rho, cert_in, dmax=dmax)
    pc = max(pc, p_noblock)
    # and raise pc until every forward orbit's evaluated state has eps < eps_0,
    # which is what puts the whole tail analysis on the G > 0 branch.
    for _ in range(200):
        okall = True
        for o in orbs:
            if not o['fwd']:
                continue
            pev = o['enter'] + pc
            if pev not in o['win']:
                continue
            if not eps_lt_threshold(S, o['st'][pev], thr):
                okall = False
        if okall:
            break
        pc += 1

    def offsets(pc_try):
        """(binding offsets, blocking offsets) observed at the evaluation levels."""
        bind, block = set(), set()
        for o in orbs:
            if not o['fwd'] or abs(o['Q']) > Bcut:
                continue
            for p in range(pc_try, pc_try + 2):
                pev = o['enter'] + p
                if pev not in o['win']:
                    continue
                vB = o['st'][pev]
                for o2 in orbs:
                    cands = [x for x in o2['win']
                             if o2['st'][x] != vB and F.h_cmp(o2['st'][x], vB) < 0]
                    if not cands:
                        continue
                    bx = max(cands)
                    bind.add(pev - bx)
                    if F.eps_cmp(vB, o2['st'][bx]) >= 0:
                        block.add(pev - bx)
                    # a lower-level state of the same orbit must never block
                    for x in cands:
                        if x < bx and F.eps_cmp(vB, o2['st'][x]) >= 0:
                            block.add(pev - x)
        return sorted(bind), sorted(block)
    # every blocker of a candidate has eps < eps_0 (level >= lvl_eps0) and height
    # below the candidate (level <= its evaluation level, the height being
    # increasing above Ystar), so the window must contain [lvl_eps0, pev].
    # The condition is needed only for orbits that are still positive at the
    # window's lower edge -- the doubly-infinite ones.  An orbit whose positive
    # part BEGINS inside the window has no positive state outside it, so there is
    # nothing beyond the window to exclude.
    # Lemma 6.0c makes this a computed condition: the window must reach level
    # L* on every doubly-infinite orbit, so that the state witnessing
    # Y_{L*} <= Ystar is present.  Orbits whose positive part begins inside the
    # window have no positive state outside it and need no condition.
    win_ok = True
    for o in orbs:
        if not o['fwd'] or not o.get('double'):
            continue
        if o.get('Lstar') is None or o['Lstar'] < min(o['win']):
            win_ok = False
    if not win_ok:
        raise WindowTooSmall('the stored window does not reach the eps_0 level cutoff')

    # (P2) ONE level convention: stored period = absolute eta-level (every
    # representative is normalised to |eta| in [1,rho) and P scales |eta| by
    # exactly rho).  The absolute tail-start level of orbit i is
    #        T_i = enter_i + p_cert ,
    # and the partition is  P4: L <= L*_i ;  P5: L*_i < L < T_i ;  P6: L >= T_i.
    # Disjointness needs T_i > L*_i, which is certified here.
    tail_ok = True
    for o in orbs:
        if not o['fwd']:
            o['T'] = None
            continue
        o['T'] = o['enter'] + pc
        if o.get('Lstar') is not None and not (o['T'] > o['Lstar']):
            tail_ok = False
    assert tail_ok, 'T_i > L*_i failed on some orbit: the partition would not be disjoint'

    offs_final, block_final = offsets(pc)

    def Gpos(v):
        Q = S.Qf(*v); e = S.eta(*v)
        return (2 * S.alpha * Surd(S.A ** 2, 0, S.D) * e * e
                + Surd(S.B * Q, 0, S.D)).sign() > 0
    def offsets_Gpos(pc_try):
        """binding offsets when competitors are restricted to the G > 0 branch --
        the reviewer's claim is that these collapse to {0,1} eventually."""
        bind = set()
        for o in orbs:
            if not o['fwd'] or abs(o['Q']) > Bcut:
                continue
            for p in range(pc_try, pc_try + 2):
                pev = o['enter'] + p
                if pev not in o['win']:
                    continue
                vB = o['st'][pev]
                for o2 in orbs:
                    cands = [x for x in o2['win']
                             if o2['st'][x] != vB and F.h_cmp(o2['st'][x], vB) < 0
                             and Gpos(o2['st'][x])]
                    if cands:
                        bind.add(pev - max(cands))
        return sorted(bind)
    offs_Gpos = offsets_Gpos(pc)

    # ---- per-pair threshold ledger (what justifies the offset window)
    one = Surd(1, 0, S.D); A2 = S.A ** 2
    ledger = []
    reps = []
    for o in fwdorbs:
        r, _ = norm_rep(S, P, rho, o['st'][o['enter']])
        e = S.eta(*r)
        reps.append((o, (e if e.sign() > 0 else -e)))
    # The persistence argument needs, for each CANDIDATE B (|Q| <= Bcut) and each
    # competitor A, the eventual sign of the eps comparison and of the height
    # comparison.  Pairs of two non-candidates are irrelevant, so the ledger is
    # (competitor, candidate), not (competitor, competitor): with Bcomp = 3 Bcut
    # that is a threefold saving.
    # Rows are needed for every ORDERED pair in which at least one side is a
    # candidate.  (competitor, candidate) rows decide whether a competitor at an
    # EARLIER level blocks; (candidate, competitor) rows at d = 1 decide that a
    # competitor at a LATER level lies above the candidate in height, which is
    # what excludes negative offsets and pins the ledger to 0 <= d <= d*.
    # (competitor, candidate) rows at every d <= d* decide whether a competitor at
    # an EARLIER level blocks.  (candidate, competitor) rows at d = 1 ONLY are
    # what is needed for the other endpoint: they give sgn(H_comp(q+1) - H_cand(q)),
    # excluding competitors at LATER levels and so pinning the range to
    # 0 <= d <= d*.  Nothing else is required, so the ledger is not doubled.
    _cand = {id(x[0]) for x in reps if abs(x[0]['Q']) <= Bcut}
    for (oa, rA) in reps:
        for (ob, rB) in reps:
            a_is = id(oa) in _cand
            b_is = id(ob) in _cand
            if not (a_is or b_is):
                continue
            ds = list(range(0, dmax + 1)) if b_is else [1]
            for d in ds:
                QA, QB = oa['Q'], ob['Q']
                Gd = abs(QA) * rB * rB * rho.pow(2 * d) - abs(QB) * rA * rA
                rhs = S.B * (abs(QB) * QA - abs(QA) * QB)   # corrected sign (R1)
                row = dict(A=list(oa['rep']), B=list(ob['rep']), d=d,
                           QA=QA, QB=QB, rhs=rhs,
                           Gd_sign=Gd.sign())
                if Gd.sign() != 0:
                    p = d
                    while p <= 400:
                        if (2 * S.alpha * A2 * rho.pow(2 * (p - d)) * (Gd if Gd.sign() > 0 else -Gd)
                                - Surd(abs(rhs), 0, S.D)).sign() > 0:
                            break
                        p += 1
                    row['eps_threshold'] = p
                    row['eps_verdict'] = 'B_beats_A' if Gd.sign() > 0 else 'A_beats_B'
                else:
                    # Gamma_d = 0: the criterion is 0 > rhs (corrected sign)
                    row['eps_threshold'] = d
                    row['eps_verdict'] = ('B_beats_A' if rhs < 0 else
                                          ('equal' if rhs == 0 else 'A_beats_B'))
                Uq = 2 * S.alpha * A2 * rA * rB * rho.pow(d) * (rB * rho.pow(d) - rA)
                Vq = Surd(S.B, 0, S.D) * (Surd(QB, 0, S.D) * rA
                                          - Surd(QA, 0, S.D) * rB * rho.pow(d))
                if Uq.sign() == 0:
                    row['h_threshold'] = 0; row['h_verdict'] = 'same_orbit_index_shift'
                else:
                    q = 0
                    while q <= 400:
                        if (rho.pow(2 * q) * (Uq if Uq.sign() > 0 else -Uq)
                                - (Vq if Vq.sign() > 0 else -Vq)).sign() > 0:
                            break
                        q += 1
                    row['h_threshold'] = q + d
                    row['h_verdict'] = 'H_B_gt_H_A' if Uq.sign() > 0 else 'H_B_lt_H_A'
                ledger.append(row)

    # ---- verdicts
    fallback = [0, 0]
    def verdict(vB, qB):
        lim = None
        if pruning:
            fallback[1] += 1
            n, dn = S.eps_num_den(*vB)
            try:
                lim = Bcomp_from(S, abs(qB), (n, dn))
            except AssertionError:
                lim = None
                fallback[0] += 1
        tie = None
        for o in orbs:
            if lim is not None and abs(o['Q']) > lim:
                continue
            # Select the competitor of MINIMAL eps among this orbit's states of
            # height below H_B.  This is the definition of blocking and needs no
            # monotonicity hypothesis; the "largest period" rule of Lemma 6.5 is
            # equivalent only on the G > 0 branch (review item R2), so it is no
            # longer used for correctness.
            best, bq = None, None
            for q in o['win']:
                w = o['st'][q]
                if w == vB:
                    continue
                if F.h_cmp(w, vB) < 0 and (best is None or F.eps_cmp(w, best) < 0):
                    best, bq = w, q
            if best is None:
                continue
            c2 = F.eps_cmp(vB, best)
            if c2 > 0:
                return False, None, (o['rep'], o['Q'], best)
            if c2 == 0 and tie is None:
                tie = (o['rep'], o['Q'], best)
        return (tie is None), tie, None

    tails, ties, early = [], [], []
    for o in orbs:
        if o['fwd']:
            pev = o['enter'] + pc
            isrec, tie, lost = verdict(o['st'][pev], o['Q'])
            o['tail'] = 'record' if isrec else ('tie' if tie else 'excluded')
            if o['tail'] == 'record':
                tails.append(o)
            if o['tail'] == 'tie':
                ties.append(dict(orbit=list(o['rep']), Q=o['Q'],
                                 partner=list(tie[0]), partner_Q=tie[1]))
            # P5 is exactly the levels L*_i < L < T_i.  Levels <= L*_i are P4
            # (excluded by the eps_0 cutoff) and levels >= T_i are P6 (the
            # certified tail), so neither may contribute an "initial exception";
            # and states of height <= H(w) are P1, handled by the P1 scan.
            lo = o['Lstar'] if o.get('Lstar') is not None else min(o['win']) - 1
            rng = [q for q in o['win'] if lo < q < pev]
        else:
            # A case-(i) orbit contributes no P5 state: above H(w) its states are
            # excluded by the eps >= sqrt(Delta)/|B| floor, and below H(w) they
            # belong to P1.
            o['tail'] = 'finite_or_backward_window'
            rng = []
        for q in rng:
            ir, ti, lo_ = verdict(o['st'][q], o['Q'])
            if ir != (o['tail'] == 'record'):
                early.append(dict(state=list(o['st'][q]), Q=o['Q'], period=q,
                                  is_record_here=ir, tail=o['tail']))
    # P1: the records of height <= H(w), from the explicit bounds
    Hw = S.H(*w0)
    mmaxp1 = 0
    while (S.H(mmaxp1 + 1, 1) - Hw).sign() <= 0:
        mmaxp1 += 1
    p1 = []
    for mm in range(1, mmaxp1 + 1):
        kk = 1
        while (S.H(mm, kk) - Hw).sign() <= 0:
            if S.admissible(mm, kk):
                p1.append((mm, kk))
            kk += 1
    p1 = sort_heights(S, p1)
    p1rec, bst = [], None
    for v in p1:
        if bst is None or F.eps_cmp(v, bst) < 0:
            p1rec.append(v); bst = v
    cert = dict(
        name=name, A=A, B=B, C=C, s=s, M=M, R=sorted(map(list, S.R)),
        Delta=S.Delta, Dsqfree=S.D, T=T, U=U, X0=[list(r) for r in X0], j=j,
        P=[list(r) for r in P], pruning=pruning,
        family=[list(v) for v in sorted(seeds)], D=D,
        family_floor=list(famH),
        Bcut=Bcut, maxF_pair=[list(info['pair'][0]), list(info['pair'][1])],
        cutoff_periods=8, cutoff_tail_from=6,
        Bcomp=Bcomp, Bcomp_uniform=Bcomp_uniform, box=list(box), nclass=nclass, W=W,
        orbits=[dict(rep=list(o['rep']), Q=o['Q'], fwd=o['fwd'],
                     enter=o['enter'], win_lo=min(o['win']), win_hi=max(o['win']),
                     double=bool(o.get('double')), tail=o['tail'],
                     case=o['case'], lvl_eps0=o['lvl_eps0'],
                     Lstar=o.get('Lstar'), T=o.get('T'),
                     Ystar_num=[o['Ystar'].p.numerator, o['Ystar'].p.denominator,
                                o['Ystar'].q.numerator, o['Ystar'].q.denominator],
                     gcd=gcd(abs(o['rep'][0]), abs(o['rep'][1])))
                for o in orbs],
        p_cert=pc, p_cert_binding=list(worst) if worst else None,
        dmax=dmax, d_star=dstar, p_noblock=p_noblock,
        observed_binding_offsets=offs_final,
        observed_blocking_offsets=block_final,
        observed_binding_offsets_Gpos=offs_Gpos,
        eps0_state=list(w0), window_covers_blockers=bool(win_ok),
        p1_states=len(p1), p1_records=[list(v) for v in p1rec],
        sort_fallbacks=int(getattr(S, 'last_sort_fallback', False)),
        eps0_num=[eps_fam[0].p.numerator, eps_fam[0].p.denominator,
                                      eps_fam[0].q.numerator, eps_fam[0].q.denominator],
        blocker_fallback_calls=fallback[0], verdict_calls=fallback[1],
        ledger=ledger,
        record_tails=[list(o['rep']) for o in tails],
        ties=ties, initial_exceptions=early)
    return S, cert


odd = [(1, 1)]
CASES = [
 (1, -1, -1,  1, 2, odd,           'control_phi'),
 (1, -2, -2,  1, 2, odd,           'control_1plus_sqrt3'),
 (1,  0, -3,  1, 2, odd,           'control_sqrt3'),
 (1,  0, -2,  1, 2, odd,           'sqrt2_oddodd'),
 (1, -3,  1,  1, 2, odd,           'half3plussqrt5_oddodd'),
 (1, -3,  1, -1, 2, odd,           'half3minussqrt5_oddodd'),
 (2,  0, -1,  1, 2, odd,           'inv_sqrt2_oddodd_nonmonic'),
 (3, -1, -1,  1, 2, odd,           '3x2mx m1_oddodd_nonmonic'.replace(' ', ''),),
 (1,  0, -3,  1, 5, [(1,1),(2,3)], 'sqrt3_union_mod5'),
 (1,  0, -6,  1, 4, [(2,2)],       'sqrt6_22mod4'),
 (1,  0, -2,  1, 3, [(1,1)],       'sqrt2_11mod3'),
 (1,  0, -6,  1, 3, [(1,1)],       'sqrt6_11mod3'),
 (1, -5,  1,  1, 2, odd,           'half5plussqrt21_oddodd'),
]
# the near-equal-positive-conjugate stress family  alpha_N = N + sqrt2
for N in (2, 3, 4, 6, 8, 12, 20):
    CASES.append((1, -2 * N, N * N - 2, 1, 2, odd, f'Nplussqrt2_N{N}_oddodd'))
for N in (2, 5, 9):
    CASES.append((1, -2 * N, N * N - 2, 1, 3, [(1, 1)], f'Nplussqrt2_N{N}_11mod3'))
    CASES.append((1, -2 * N, N * N - 2, 1, 4, [(1, 3), (3, 1)], f'Nplussqrt2_N{N}_union_mod4'))

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for (A, B, C, s, M, R, nm) in CASES:
        t = time.time()
        try:
            S, cert = build(A, B, C, s, M, R, nm)
        except Exception as e:
            print('%-34s EMIT FAILED: %r' % (nm, e)); continue
        with open(f'{OUT}/{nm}.json', 'w') as f:
            json.dump(cert, f, indent=1)
        import math as _m
        _rt = _m.sqrt(S.Delta)
        _thr = (_rt / abs(S.B)) if S.B else float('inf')   # pruning needs eps < sqrt(D)/|B|
        print('%-34s a=%.6f ap=%+.6f  eps-budget=%.4g  pruning=%s  Bcut=%d  orbits=%d  '
              'p_cert=%d  tails=%d ties=%d exc=%d  (%.1fs)'
              % (nm, S.alpha.f(), S.alphap.f(), _thr, cert['pruning'],
                 cert['Bcut'], len(cert['orbits']), cert['p_cert'],
                 len(cert['record_tails']), len(cert['ties']),
                 len(cert['initial_exceptions']), time.time() - t))
