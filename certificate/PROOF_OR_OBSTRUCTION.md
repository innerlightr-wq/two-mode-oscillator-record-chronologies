# Completeness of the phi and 1+sqrt(3) record chronologies

Both conjectures are **proved** here.  The two proofs share one framework and differ only in
how the last competing orbit is eliminated: at phi it survives to an exact tie that an integer
sign decides; at 1+sqrt(3) no tie occurs.

Throughout: alpha > 1 quadratic with minimal polynomial x^2 - t x - s, conjugate alpha',
Delta = t^2 + 4s, sqrtD := alpha - alpha' > 0.  A state is a pair (m,k) of positive odd
integers, with height h = (m alpha + k)/2 and balance error eps = |m alpha - k|/(m alpha + k).
Put xi = k - m alpha, eta = k - m alpha', and N = N(m,k) = k^2 - t k m - s m^2.

---

## 0. The two master formulas

Since alpha, alpha' are the roots of x^2 - tx - s,

    N = (k - m alpha)(k - m alpha') = xi * eta.

From eta - xi = m sqrtD and alpha eta - alpha' xi = k sqrtD one gets
m = (eta - xi)/sqrtD, k = (alpha eta - alpha' xi)/sqrtD and

    2h = m alpha + k = (2 alpha eta - t xi)/sqrtD.

Substituting xi = N/eta and writing G := 2 alpha eta^2 - t N > 0:

> **(M1)**  2h = G / (sqrtD * eta)
> **(M2)**  eps = |xi|/(2h) = |N| * sqrtD / G

So **eps depends only on (N, eta)**, and eps is strictly decreasing in G/|N|.  Define

    W := eta^2 / |N|,      S := G/|N| = 2 alpha W - t*sign(N).

eps is strictly decreasing in S, and W is *exactly* geometric along a unit orbit.  Written out,

    S = 2 alpha W - t sign(N),

so the **error score** is 2 alpha W corrected by a bounded term depending only on the SIGN of
N: records are the running maxima of S.  Height order is a **separate** question, handled in
section 5 by the pairwise certificate (W3'), because H = G/(D0 eta) depends on N as well as eta
and so is not a function of S.
(Checked in `verify_records.py`, C1.)

## 1. Reduction to primitive states

If g = gcd(m,k) > 1 then g is odd, (m/g, k/g) is again an odd state, it has the **same** eps
(both numerator and denominator scale by g), and strictly smaller height.  A strict record must
beat every state of strictly smaller height, so no imprimitive state is ever a record.  Hence
N may be assumed primitively represented.  (C3.)

## 2. The admissible lattice and the admissible unit

Write eta = a + b*w with w = phi resp. sqrt3; then m = b and k = a + b, so

    (m,k) both odd  <=>  a even and b odd.                                  (ADM)

*The unique-factorisation language below is expository: it describes the orbits compactly.  The
certificate does not use it -- orbits are found by a bounded search, which is exhaustive with no
class-number hypothesis (external audit).*

**phi.**  Z[phi] is a PID with unit group +-phi^Z and Norm(phi) = -1.  2 is inert, so
Z[phi]/2 = F_4 = {0,1,phi,phi^2} and (ADM) says exactly eta = phi (mod 2).  Multiplication by
phi^3 = 1 + 2phi sends (a,b) -> (a+2b, 2a+3b), so it preserves (ADM) and negates the norm;
phi^6 preserves both.  The admissible unit step is therefore rho := phi^3, and |N| is a
**rho-invariant**.

**1+sqrt(3).**  Z[sqrt3] is a PID with unit group +-(2+sqrt3)^Z, Norm(2+sqrt3) = +1, and
x^2 - 3y^2 = -1 is insoluble mod 3, so every unit has norm +1.  Multiplication by (2+sqrt3)
sends (a,b) -> (2a+3b, a+2b), which breaks (ADM); (2+sqrt3)^2 = 7+4sqrt3 sends
(a,b) -> (7a+12b, 4a+7b) and preserves it.  The admissible unit step is rho := (2+sqrt3)^2.

In the (m,k) coordinates: phi^3 acts by **[[1,2],[2,3]]**, i.e. (m,k) -> (m+2k, 2m+3k), sending
(1,1) to (3,5); the matrix of the conjecture,

    M_phi = [[5,8],[8,13]]      (m,k) -> (5m+8k, 8m+13k),

is **phi^6**, which sends (1,1) to (13,21) and is the step within a fixed-norm orbit.  An earlier
draft labelled [[5,8],[8,13]] as the phi^3 step, which is wrong (external audit F7).  For
1+sqrt(3), rho = (2+sqrt3)^2 acts by

    M_3   = [[3,4],[8,11]]      (m,k) -> (3m+4k, 8m+11k),

and for sqrt(3), rho = 2+sqrt3 acts by [[2,1],[3,2]].

## 3. Classification of the small-norm orbits

**|N| = 1 (both cases).**  eta is a unit.

*phi*: eta = +-phi^n, and (ADM) forces n = 1 (mod 3); then N = (-1)^n, and the state is
(F_n, F_{n+1}) because phi^{-n} = (-1)^n (F_{n+1} - F_n phi).  Conversely F_n and F_{n+1} are
both odd exactly when 3 does not divide n(n+1), i.e. n = 1 (mod 3).  **So the |N| = 1
admissible states are precisely (F_{3j+1}, F_{3j+2}), with N = -1 for 3j+1 odd and N = +1 for
3j+1 even** -- the conjecture's Fibonacci ladder, and nothing else.

*1+sqrt3*: eta = +-(2+sqrt3)^j and (ADM) forces j odd; N = +1 always.  The states are
(1,3), (15,41), (209,571), ... -- the conjecture's N = +1 ladder.

**|N| = 5 (phi).**  5 ramifies and (sqrt5) = (2phi-1) is the only ideal of norm 5, so
eta = +- sqrt5 * phi^n; (ADM) forces n = 1 (mod 3) and then **N = -5(-1)^n**.

**Imprimitive norms (phi).**  3 is inert, so an ideal of norm 9 or 15 is divisible by (3) and
an ideal of norm 25 by (5): every such state is imprimitive, excluded by section 1.

**Excluded residues (phi).**  4N = (2k-m)^2 - 5m^2 forces N = 0, 1, 4 (mod 5); in particular
|N| = 2, 3, 7, 13, 17 are not represented at all.

## 4. The cutoff lemma

> **Lemma (cutoff).**  Let (m,k) be a strict record whose height exceeds that of some admissible
> state on a fixed ladder of norm +-L.  Write H = m alpha + k, D0 = alpha - alpha',
> z = (k - m alpha)/H, eps = |z|, Y = eta_A^2, n = N_A, L = |n|.  Then
>
>     |N| < H_C^2 eps_A (D0 + t eps_A)/(2 alpha) =: F(Y, n),
>
> where A, C are successive positive ladder states bracketing it in HEIGHT.  Evaluating F
> gives |N| <= **18** for phi, **204** for 1+sqrt(3), **27** for sqrt(3).

*Proof.*  The identities eta = H(D0 + t z)/(2 alpha) and |N| = H^2 eps (D0 + t z)/(2 alpha)
follow from the master formulas.  The unit matrices have positive entries, so ladder heights
strictly increase and bracket every sufficiently large state: H_A < H_B <= H_C.  Since
eps_B < eps_A, t >= 0, |z_B| = eps_B, and x -> x(D0 + t x) is strictly increasing on x >= 0,

    |N_B| = H_B^2 eps_B (D0 + t z_B)/(2 alpha) < H_C^2 eps_A (D0 + t eps_A)/(2 alpha),

which is F(Y, n) after substituting eps_A = L D0/(2 alpha Y - t n) and
H_C/H_A = (2 alpha rho^2 Y - t delta n)/(rho(2 alpha Y - t n)).  **Only height ordering is
used.**  (An earlier proof instead inferred eta_B <= rho eta_A from a height bracket, using the
fixed-N derivative of H in eta, which orders nothing across norms -- see section 5.)

**Bounding F over the whole infinite ladder requires separating the two norm signs.**  Putting
u = t/(2 alpha Y) (and u = 1/(2 alpha Y) at phi, where L = t = 1), one has **0 < u < 1**: it
holds at the first ladder seed in each case (2 alpha Y > t there, checked exactly) and persists
as Y increases along the ladder, since Y is multiplied by rho^2 > 1 at each step while t and
alpha are fixed.  All the closed forms below are used only on that range.

| branch | closed form | behaviour | bound |
|---|---|---|---|
| phi, n = -1 | R^2 (1 - u/R^2)^2 (1+2u)/(1+u)^2 | both correction factors < 1 for u > 0 | **< R^2 = phi^6 = 17.9442719100** |
| phi, n = +1 | R^2 (1 + u/R^2)^2/(1 - u)^2 | increasing in u, so decreasing in Y | max at Y = phi^8: **18.1960225537** |
| 1+sqrt(3) | R^2 ((1 - u/R^2)/(1 - u))^2 | increasing in u | max at Y = (2+sqrt3)^2: **204.5520518132** |
| sqrt(3), t = 0 | L R^2 identically | constant | **27.8564064606** |

So |N| <= 18, 204, 27 respectively.  **A previous draft justified this by "F is monotone in Y,
so the maximum is in the first two states", which is false** (external v2 audit R1): at phi the
two branches move in opposite directions -- the n = -1 values increase (17.5116, 17.9435,
17.9443, ...) while the n = +1 values decrease (18.1960, 17.9450, 17.9443, ...).  Sampling six
ladder states cannot bound an infinite ladder; the sign separation above does.  The bounds are
unchanged.  Endpoint inequalities are decided exactly in `certificate.cutoff`.

**The ladder need not have norm one.**  The proof uses only |N_A| = L, so any admissible ladder
of known norm serves.  That matters because the |N| = 1 ladder can be empty: at alpha = sqrt(3),
odd m, k force k^2 - 3m^2 = 6 (mod 8).  The lemma applies there with L = 2.

With the mod-5 and primitivity restrictions of section 3, the admissible norms left at phi are
**|N| in {1, 5, 11}**.

## 5. Phase exclusion

All orbits step eta by rho and leave |N| fixed, so W = eta^2/|N| steps by rho^2.  Writing
x = log_rho(eta) mod 1 for an orbit's phase and sigma = 2x - log_rho|N| for its score, a state
of orbit O in period p has score sigma_O + 2p, and records are the running maxima.  Hence orbit
O records in every sufficiently late period iff

    (i)  sigma_O >  sigma_O'      for every O' with x_O' < x_O,  and
    (ii) sigma_O >  sigma_O' - 2  for every O' with x_O' > x_O.

Both are exact algebraic comparisons -- sigma_O > sigma_O' - 2c is
rho^{2c} eta_O^2 |N_O'| > eta_O'^2 |N_O| -- so **no logarithm is used in any decision**; the
logs are descriptive only.

**The "eventually" is explicit and small, and two degeneracies must be handled.**  For any two
states the exact criterion from (M2) is

    eps_B < eps_A  <=>  2 alpha Gamma > t(|N_A| N_B - |N_B| N_A),
    Gamma := |N_A| eta_B^2 - |N_B| eta_A^2.                                   (CRIT)

Parametrise by the relative period offset d >= 0 (A in period p-d, B in period p).  Then
Gamma = rho^{2p-2d} Gamma_d with Gamma_d := |N_A| rB^2 rho^{2d} - |N_B| rA^2, so **sign(Gamma) is
constant in p**: one exact decision per (pair, d).  Two cases, and the second is the tie:

* **Gamma_d != 0.**  The right side of (CRIT) is bounded by 2t|N_A||N_B|, so sign(Gamma_d)
  decides as soon as 2 alpha rho^{2p-2d}|Gamma_d| >= 2t|N_A||N_B|, i.e. for all p >= P(pair,d),
  computed exactly.
* **Gamma_d == 0.**  No threshold exists and none is needed: (CRIT) becomes the integer condition
  0 > t(|N_A| N_B - |N_B| N_A) in the norms alone.  Since rho may have norm -1 (it does for phi,
  rho = phi^3), the norm signs flip with p, so this case is decided **per period parity**.  This
  is exactly the phi tie of section 6.

Only d in {0,1} needs certifying, by a **window lemma with three separate ingredients** -- eps
decrease alone is not enough :

* **(W1)** eps decreases strictly along every orbit, **proved** rather than sampled: eps =
  |N| sqrtDelta/G with G = 2 alpha eta^2 - t N, and one unit step gives
  G_next - G = 2 alpha eta^2(rho^2 - 1) - t N(delta - 1).  For delta = +1 the second term
  vanishes and the first is positive, so G increases at every step unconditionally; for
  delta = -1 the second term is bounded by 2t|N| while the first grows like rho^{2q}, so once
  2 alpha eta^2(rho^2 - 1) > 2t|N| it holds forever and the finitely many earlier steps are
  checked directly (external audit F7);
* **(W2)** every representative is normalised into [1, rho), so for any orbits O, O' the
  period-(p-1) state of O lies below the period-p state of O', since r_O rho^{p-1} < r_O' rho^p
  iff r_O/r_O' < rho and both lie in [1, rho) -- **this is what forces d in {0,1}**;
* **(W3')** a *pairwise certified* cross-orbit height ordering.  The earlier (W3) -- "ordering
  by eta equals ordering by h once 2 alpha eta^2 > t|N|" -- is a derivative in eta at **fixed N**
  and is **insufficient**: at alpha = phi the states (3,1) [N = -11, eta ~ 2.854, 2h ~ 5.854] and
  (1,3) [N = +5, eta ~ 3.618, 2h ~ 4.618] both satisfy it yet have eta_A < eta_B and h_A > h_B
  (external audit).  The correct certificate uses
  2 sqrtDelta (h_B - h_A) = 2 alpha(eta_B - eta_A) - t(N_B/eta_B - N_A/eta_A): with A at period q
  and B at period q+d, clearing the positive factor rho^{-q} rA rB rho^d gives
  **sign(h_B - h_A) = sign(rho^{2q} U - V)**, where
  U = 2 alpha(rB rho^d - rA) rA rB rho^d is constant in q, and
  V = delta^q t(delta^d N_B rA - N_A rB rho^d) carries the norm-character factors delta^q and
  delta^d (delta = Norm(rho)), so it depends on q only through the parity of q when delta = -1.
  One exact sign per (pair, d) once rho^{2q}|U| > |V|.  Certified from period q = 1 (phi),
  2 (1+sqrt3), 0 (sqrt3).  **U = 0 cannot occur**: since alpha, rA, rB, rho^d > 0, U_d = 0 iff
  rA = rB rho^d, which for d >= 1 forces rA >= rho (contradicting rA < rho) and for d = 0 forces
  the same representative; and it would in any case force V = 0, because taking norms gives
  N_A = delta^d N_B and substituting both identities annihilates V.  So U = 0 would mean *the
  same state after an index shift*, not a parity-dependent ordering -- unlike Gamma_d = 0, which
  does occur between distinct states.  This is asserted, so U = 0 with V != 0 fails loudly as
  inconsistent data (external audit).

Given (W1), (W2) and (W3'), if B beats every state of periods p and p-1 lying below it, it beats every
earlier state too.  With that, the finite region left to check is

| slope | finite check must cover | unpruned brute force reaches |
|---|---|---|
| phi | 2h < **5.854** | 2h <= 3000 |
| 1+sqrt(3) | 2h < **100.9** | 2h <= 3000 |

(the bound is the max of the Gamma-decidedness and ordering thresholds)

both covered with large margin.  (An earlier draft of this section certified d <= 4 and reported
the height of every orbit advanced 5 periods, inflating the requirement to 2h < 7142 and
2h < 1.1e7 -- beyond the brute-force range, i.e. a real gap.  See the external audit reports.)

Applying (i)-(ii) to every admissible primitive orbit -- **together with the Gamma_d = 0 rule,
without which the alternating phi family is not classified at all** (C5, C6):

* **phi, |N| <= 18** (the height-based cutoff of section 4): of **4** orbits, **two are excluded
  strictly**.  The two |N| = 11 orbits have
  representatives eta = (3+phi)phi^2 and eta = 4-phi, with phases 0.726 and 0.601 against the
  requirement x in (0.1635, 0.3333); |N| = 19 is excluded because the admissible window
  (sqrt|N|, rho) = (4.359, 4.236) is **empty**.  Survivors: the |N| = 1 ladder, and the
  |N| = 5 orbits, which tie exactly with it.
* **1+sqrt(3), |N| <= 204**: of **64** orbits, **61 are excluded strictly**.  Survivors: N = +1,
  N = -3, N = -11 -- exactly the conjectured three ladders, with no tie.

## 6. The phi tie, decided by an integer

The surviving |N| = 5 orbits sit at eta = sqrt5 * phi^n against the ladder member at
eta_A = phi^n, so theta = eta/eta_A = sqrt5 and theta^2 = 5 = |N_B|: the leading term cancels
and the comparison in the proof of the cutoff lemma degenerates to

    0 < t(|N_B| N_A - N_B),   i.e.   B beats A  <=>  |N_B| N_A > N_B.

By section 3, N_B = -5(-1)^n = -5 N_A, so the condition is 5 N_A + 5 N_A > 0, i.e.
**N_A = +1**.  Equivalently, directly from (M2),

    eps(phi^n)       = sqrt5 / (2 phi^{2n+1} - (-1)^n),
    eps(sqrt5 phi^n) = sqrt5 / (2 phi^{2n+1} + (-1)^n),

the same leading term with the bounded term deciding.  Hence for n = 1 (mod 6) the norm-5 state
has N = +5 and **loses**; for n = 4 (mod 6) it has N = -5 and **wins**.  The winners are
eta = sqrt5 phi^{6j+4}, i.e. the Lucas pairs (L_{6j+4}, L_{6j+5}).  (C7 verifies the rule
against exact comparisons for n = 1, 4, ..., 28.)

This is the lemma Conjecture 5.8 asked for.  Note it is *not* the route the note suggested:
the deciding identity is N_B = -5 N_A together with the exact cancellation of 2 phi^{2n+1},
not bookkeeping of L_n^2 - 5 F_n^2 = 4(-1)^n.

## 7. The theorems

> **Theorem A (phi-completeness).**  For alpha = phi the strict chronological records of eps are
> exactly the states (F_{3j+1}, F_{3j+2}), j >= 0, together with (L_{6j+4}, L_{6j+5}), j >= 0,
> merged in increasing height, with defect cycle (-1, +1, -5).

> **Theorem B ((1+sqrt3)-completeness).**  For alpha = 1+sqrt(3) the strict chronological records
> of eps are exactly the three admissible unit orbits with N = -3, +1, -11, seeded at (1,1),
> (1,3), (5,13) and advanced by M_3, merged in increasing height, with defect cycle
> (-3, +1, -11).  **The height is not exactly multiplicative** -- see the correction below.

**Correction to an earlier form of Theorem B** (external audit F6).  An earlier statement said
"multiplicative period (2+sqrt3)^2 in height".  That is false: what scales exactly by rho is
eta, and with H = 2h,

    H_next - rho H = t N (rho - delta/rho)/(sqrtDelta eta),      delta = Norm(rho),

which vanishes only when t N = 0.  Concretely M_3(1,1) = (7,19) and
**H(7,19) - rho H(1,1) = -8 sqrt(3)**, not zero.  Height *ratios* tend to rho, and three records
fall in each multiplicative window of ratio rho asymptotically -- that is the correct form.  At
sqrt(3), t = 0 gives H = eta, so there the height period 2 + sqrt3 IS exact, and Theorem C keeps
that clause.

*Proof of both.*  Section 1 restricts to primitive states; section 4 bounds |N|; section 3 and
C5 enumerate every admissible primitive orbit with |N| under that bound; section 5 excludes all
but the survivors by a strict inequality, valid for every eta above an explicit threshold;
section 6 settles the single remaining tie at phi.  The finitely many states below the
thresholds are checked by unpruned brute force (C8), which also confirms the initial segment.
The surviving orbits then record as the classification says -- **and that is not "in every
period" for all of them**: at phi the norm-5 (Lucas) family is ALTERNATING, recording in exactly
the periods with N_A = +1, which is the content of section 6.  The leading-score conditions of
section 5 alone do not classify it; the Gamma_d = 0 integer rule does.  With that, the merge is
the stated one. []

### Remark on the information content of the observables (methodological)

The audit distinguishes magnitude information, sufficient for norm bounds and leading error
comparisons, from signed information required by correction terms.  This follows the author's
comparator methodology: identify which distinctions an observable removes before using it in
subsequent calculations.  Here the retained distinction is the norm character of unit iteration,
transported relative to an orbit representative -- concretely, N_q = delta^q N_rep with
delta = Norm(rho), so that |N| would discard the parity of the step count, which is exactly what
the phi tie turns on.  Two invariants are checked alongside the proof: the sign ledger (S) and
the representative invariance delta^{q'} N'_rep = delta^q N_rep (R), the latter recording that
the signed norm is intrinsic to the state while the parity is relative to the representative.
The theorem itself keeps its arithmetic formulation.

## 8. Status, and what a referee would still want

Nothing mathematical is missing: the cutoff is derived, the orbit list is complete, every
exclusion is a strict exact inequality, the tie is decided by an integer, and the finite region
below the decidedness crossing is covered by unpruned brute force.

**A third case comes free.**  Theorem C (see the sqrt(3) control below): for alpha = sqrt(3) the records are the
single norm -2 orbit (1,1), (3,5), (11,19), (41,71), ... with h^2 eps = 1/2 exactly.  Here t = 0,
so 2h = eta and eps = |N|/(2h)^2 with no correction term, and the whole analysis is the phase
comparison alone.

It is, however, a **computer-assisted proof**.  The two steps that are finite exact computation
rather than hand calculation are the orbit enumeration (**4** orbits for phi at the cutoff 18; **64** for 1+sqrt(3) at 204;
**6** for sqrt(3) at 27) and the **2 + 61 + 4** exclusions.  An earlier draft quoted 10/66 and a count of 63, from a run at looser bounds
(external audit F7).  The phi case is small enough to be done
by hand -- only |N| in {1, 5, 11} survive section 3-4, and section 5 dispatches 11 and 19 in
two lines -- so **Theorem A is hand-checkable as written**.  Theorem B is not: 61 exclusions at
|N| <= 204 is a table, and a referee would reasonably ask for either that table printed or a
sharper cutoff.  A sharper cutoff is plausible (the 1+sqrt(3) bound is weak precisely because
rho = (2+sqrt3)^2 is large, giving rho^2 = 194 where phi gives 17.9), and finding one is the
obvious way to make Theorem B as clean as Theorem A.
