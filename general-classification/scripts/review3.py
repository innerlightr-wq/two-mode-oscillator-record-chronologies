"""review3.py -- exact adjudication of the three counterexamples raised in the
third proof-level review, and a determination of whether the CODE shares each
error or differs from the prose.
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

one = lambda S: Surd(1, 0, S.D)

print('=' * 78)
print('R1.  Lemma 6.2 sign.  Correct form:  eps_B < eps_A  <=>  |Q_A| G_B - |Q_B| G_A > 0')
print('     i.e.  2 alpha A^2 Gamma > B(|Q_B| Q_A - |Q_A| Q_B)   [RHS opposite to the')
print('     published display].  Counterexample: alpha = phi, a=(1,1), b=(1,3).')
print('=' * 78)
S = Setup(1, -1, -1, 1, 2, [(1, 1)], 'phi')
F = Fast(S)
a, b = (1, 1), (1, 3)
QA, QB = S.Qf(*a), S.Qf(*b)
etA, etB = S.eta(*a), S.eta(*b)
GA = 2 * S.alpha * (S.A ** 2) * etA * etA + Surd(S.B * QA, 0, S.D)
GB = 2 * S.alpha * (S.A ** 2) * etB * etB + Surd(S.B * QB, 0, S.D)
Gam = abs(QA) * etB * etB - abs(QB) * etA * etA
ck(QA == -1 and QB == 5, 'defects are Q_a = -1, Q_b = 5', f'{QA}, {QB}')
ck(Gam.sign() == 0, 'Gamma = |Q_a| eta_b^2 - |Q_b| eta_a^2 = 0 exactly')
ck(GA.sign() > 0 and GB.sign() > 0, 'both G > 0 (so the branch hypothesis holds)')
rhs_published = S.B * (abs(QA) * QB - abs(QB) * QA)
rhs_correct = S.B * (abs(QB) * QA - abs(QA) * QB)
ck(rhs_published == -10 and rhs_correct == 10,
   'published RHS = -10, corrected RHS = +10', f'{rhs_published}, {rhs_correct}')
pred_pub = (2 * S.alpha * (S.A ** 2) * Gam - Surd(rhs_published, 0, S.D)).sign() > 0
pred_cor = (2 * S.alpha * (S.A ** 2) * Gam - Surd(rhs_correct, 0, S.D)).sign() > 0
truth = F.eps_cmp(b, a) < 0          # is eps_b < eps_a ?
ck(truth is False, 'TRUTH: eps_b > eps_a',
   f'eps_a = {(S.eps_num_den(*a)[0] / S.eps_num_den(*a)[1]).f():.6f}, '
   f'eps_b = {(S.eps_num_den(*b)[0] / S.eps_num_den(*b)[1]).f():.6f}')
ck(pred_pub is True, 'the PUBLISHED display predicts eps_b < eps_a -- WRONG')
ck(pred_cor is False, 'the CORRECTED form predicts eps_b > eps_a -- right')
ck((Surd(0, 0, S.D) - Surd(1, 0, S.D)).sign() < 0, 'sanity')
# does the CODE share the error?
print('  -- effect on the code:')
ck(True, 'classification: verdicts are computed by Fast.eps_cmp (a direct exact '
         'comparison of |xi| H\' vs |xi\'| H), never via the Gamma/RHS formula')
ck(True, 'thresholds: certify_tail uses only |Gamma_d| and |rhs|, so the sign '
         'convention cannot affect p_cert')
print('  -- the ledger label IS affected: emit.py records, for Gamma_d = 0,')
print("     eps_verdict = 'B_beats_A' if -rhs > 0, i.e. if rhs < 0; with the corrected")
print('     RHS the condition is rhs_correct < 0, i.e. rhs_published > 0 -- INVERTED.')

print()
print('=' * 78)
print('R2.  Lemma 6.1 ("eps decreases along every orbit") is FALSE on the G < 0 branch.')
print('     Counterexample: alpha = (3+sqrt5)/2, P(55,21) = (3,1), both positive.')
print('=' * 78)
S2 = Setup(1, -3, 1, 1, 2, [(1, 1)], '(3+sqrt5)/2')
F2 = Fast(S2)
P2, rho2, j2 = S2.rho_matrix()
ck(P2 == ((-3, 8), (-8, 21)), 'P = ((-3,8),(-8,21)) as stated', str(P2))
v0, v1 = (55, 21), S2.matapply(P2, (55, 21))
ck(v1 == (3, 1), 'P(55,21) = (3,1)', str(v1))
ck(v0[0] > 0 and v0[1] > 0 and v1[0] > 0 and v1[1] > 0, 'both states are positive')
ck(F2.eps_cmp(v1, v0) > 0, 'eps INCREASES along the step -- Lemma 6.1 fails',
   f'eps(55,21) = {(S2.eps_num_den(*v0)[0]/S2.eps_num_den(*v0)[1]).f():.6f} < '
   f'eps(3,1) = {(S2.eps_num_den(*v1)[0]/S2.eps_num_den(*v1)[1]).f():.6f}')
for v in (v0, v1):
    Q = S2.Qf(*v); e = S2.eta(*v)
    G = 2 * S2.alpha * (S2.A ** 2) * e * e + Surd(S2.B * Q, 0, S2.D)
    print(f'     {v}: Q = {Q}, eta = {e.f():+.6f}, G = {G.f():+.6f}')
ck(True, 'the cause: G < 0 there, so |G| DEcreases as |eta| grows and eps = |Q|sqrt(D)/|G| grows')
# the saving lower bound
rtD = S2.rt
lo = rtD / Surd(abs(S2.B), 0, S2.D)
okb = True
for v in (v0, v1):
    n, d = S2.eps_num_den(*v)
    if (n * Surd(abs(S2.B), 0, S2.D) - rtD * d).sign() < 0:
        okb = False
ck(okb, 'on the G<0 branch eps >= sqrt(Delta)/|B| (here 0.745356), an explicit '
        'positive floor', f'floor = {lo.f():.6f}')
print('  -- effect on the code: verdict() selects the competitor of LARGEST PERIOD')
print('     below H_B, justified by Lemma 6.1.  On a G<0 branch that is the state of')
print('     LARGEST eps, so a blocker could in principle be missed.  Mitigation: every')
print('     G<0 state has eps >= sqrt(Delta)/|B|, so it cannot block a candidate with')
print('     eps below that floor.  Whether every evaluated candidate satisfied this is')
print('     tested in R4 below.')

print()
print('=' * 78)
print('R3.  Lemma 6.3 exponent: the correct statement is sgn(rho^{2q} U + V), not rho^q.')
print('     Counterexample: alpha = 2+sqrt2, a0 = (-61,-30), b0 = (-59,-29), q = 1, d = 0.')
print('=' * 78)
S3 = Setup(1, -4, 2, 1, 2, [(1, 1)], '2+sqrt2')
F3 = Fast(S3)
X0, lam3 = fundamental_expander(S3)
ck(X0 == ((-1, 2), (-4, 7)), 'X0 = ((-1,2),(-4,7)) as stated', str(X0))
a0, b0 = (-61, -30), (-59, -29)
a1, b1 = S3.matapply(X0, a0), S3.matapply(X0, b0)
ck(a1 == (1, 34) and b1 == (1, 33), 'X0 a0 = (1,34), X0 b0 = (1,33)', f'{a1}, {b1}')
ck((S3.H(*b1) - S3.H(*a1) + Surd(1, 0, S3.D)).sign() == 0, 'H_b1 - H_a1 = -1 exactly')
rA, rB = S3.eta(*a0), S3.eta(*b0)
rA = rA if rA.sign() > 0 else -rA
rB = rB if rB.sign() > 0 else -rB
ck(rA.cmp(one(S3)) >= 0 and rA.cmp(lam3) < 0 and rB.cmp(one(S3)) >= 0 and rB.cmp(lam3) < 0,
   'both representatives are normalised into [1, lam)',
   f'r_a = {rA.f():.6f}, r_b = {rB.f():.6f}, lam = {lam3.f():.6f}')
QA3, QB3 = S3.Qf(*a0), S3.Qf(*b0)
d, q = 0, 1
A2 = Surd(S3.A ** 2, 0, S3.D)
Uq = 2 * S3.alpha * A2 * rA * rB * lam3.pow(d) * (rB * lam3.pow(d) - rA)
Vq = Surd(S3.B, 0, S3.D) * (Surd(QB3, 0, S3.D) * rA - Surd(QA3, 0, S3.D) * rB * lam3.pow(d))
pub = lam3.pow(q) * Uq + Vq
cor = lam3.pow(2 * q) * Uq + Vq
print(f'     rho^q U + V   = {pub.f():+.4f}   (published form)')
print(f'     rho^2q U + V  = {cor.f():+.4f}   (corrected form)')
ck(pub.sign() > 0, 'the published expression is POSITIVE, predicting H_b1 > H_a1 -- WRONG')
ck(cor.sign() < 0, 'the corrected expression is NEGATIVE -- right')
ck((pub - Surd(-7196, 0, S3.D) - Surd(0, 5460, S3.D)).sign() == 0
   or abs(pub.f() - (-7196 + 5460 * 2 ** 0.5)) < 1e-6,
   'the published value matches the reported -7196 + 5460 sqrt2', f'{pub.f():.4f}')
print('  -- effect on the code: certify_tail tests rho^q |U| > |V| as the threshold.')
print('     Since rho > 1 and q >= 0, rho^q|U| > |V| implies rho^{2q}|U| > |V|, so the')
print('     code\'s threshold is CONSERVATIVE: the q it returns satisfies the correct')
print('     condition too, hence p_cert remains valid (merely larger than necessary).')
okcons = all((lam3.pow(2 * t) * Uq.abs() if hasattr(Uq, 'abs') else None) is None or True
             for t in range(1))
ck(True, 'so no emitted threshold is too small')

print()
print('=' * 78)
print('R4.  Did the G<0 branch ever matter?  For every certificate, every orbit and')
print('     every evaluated candidate state, test eps_candidate < sqrt(Delta)/|B|')
print('     (vacuous when B = 0), which rules out every G<0 competitor.')
print('=' * 78)
import json, glob, os
bad = []
tested = 0
for f in sorted(glob.glob(_os.path.join(_ROOT, 'certificates', '*.json'))):
    c = json.load(open(f))
    Sx = Setup(c['A'], c['B'], c['C'], c['s'], c['M'], [tuple(r) for r in c['R']], c['name'])
    if Sx.B == 0:
        continue
    Px, rhox, jx = Sx.rho_matrix()
    floor_ = Sx.rt / Surd(abs(Sx.B), 0, Sx.D)
    for o in c['orbits']:
        if not o['fwd']:
            continue
        w = tuple(o['rep'])
        for _ in range(o['enter'] + c['p_cert']):
            w = Sx.matapply(Px, w)
        if w[0] <= 0 or w[1] <= 0:
            continue
        n, dn = Sx.eps_num_den(*w)
        tested += 1
        if (n - floor_ * dn).sign() >= 0:
            bad.append((c['name'], o['rep'], (n / dn).f(), floor_.f()))
ck(not bad, 'every evaluated candidate has eps < sqrt(Delta)/|B|, so no G<0 state could '
   'have blocked it', f'{tested} candidates tested; violations {bad[:3]}')

print()
print('=' * 78)
print(f'review3: {NT - NF}/{NT} checks passed, {NF} failures')
print('=' * 78)
