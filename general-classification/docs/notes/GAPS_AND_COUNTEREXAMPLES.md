# Gaps, counterexamples, and the defects produced and fixed in this round

Internal, 16 November 2026. Companion to `THEOREM_AND_PROOF.md`.

---

## 1. Stronger formulations that FAIL

**S-1. "…the eventual record set is a finite union of *complete forward orbits* from
computable seeds." — NOT refuted; my earlier claim here is WITHDRAWN.** A record tail beginning
at level `p₀` is a complete forward orbit of the seed `P^{p₀}v`, so initial exceptions are
perfectly compatible with the stronger formulation; the reviewer is right and the objection was
mine, not the formulation's. What the exceptions do establish is weaker and still worth
recording: **the seed is not the orbit's first positive state**, so an implementation that
reports "the orbit of `v`" rather than "the forward orbit of `P^{p₀}v`" is wrong, and `p₀` has
to be computed. Witnesses: at `α = (3+√5)/2`, odd/odd, the imprimitive orbit through `(3,3)`
(defect `−9`, `gcd 3`) is strictly **excluded at level 0** — `ε(3,3) = ε(1,1) = 0.4472…` loses
to `(1,3)`, whose `ε = 0.0680…` at the lower height `5.618 < 10.854` — and is a permanent exact
tie from level 1 on. At `α = (3−√5)/2` the orbit through `(3,5)` (defect `−11`) is likewise
excluded at its first positive state while its tail records.

*Note on the scaling direction:* `ε(3m,3k) = ε(m,k)` and `H(3m,3k) = 3H(m,k)`, so it is the
**unscaled** pair that is the lower-height competitor of the scaled one.

The genuine obstruction to "complete forward orbits" is a different one, S-2.

**S-2. "Some power of the automorph has non-negative entries, so positivity propagates
forward." — FALSE whenever `α' > 0`.** The two eigendirections `(1,α)`, `(1,α')` then both lie
in the open positive quadrant and `P^n/ρ^n` tends to a multiple of `(1,α)(−α',1)`, which has a
negative entry. Witnesses: `α = (3±√5)/2` gives `P = ((−3,8),(−8,21))`;
`α = (5+√21)/2` gives `P = ((−5,24),(−24,115))`; no power of either is entrywise positive.
Consequences, all realised in the runs:
* 7 of 21 orbits at `(3+√5)/2`, and 34 of 102 at `(5+√21)/2`, have only a finite or a
  **backward**-infinite positive window;
* orbits of negative defect are positive in **both** directions, so the positive part is a
  doubly-infinite ray;
* on such an orbit the height is **not monotone** in the period (see D-3), and `ε` tends
  backward to the explicit positive limit `|α−α'|/(α+α')` — `0.745356…` at `(3+√5)/2`,
  `0.916515…` at `(5+√21)/2`.

**S-3. "Imprimitive states never record, so one may restrict to primitive states." — FALSE for
a general class.** The published proof uses that the gcd of two odd numbers is odd. Verified
counterexamples, all reproduced here independently:
* `α = √6`, `R = {(1,1)} mod 3`: `(4,10)` has `gcd 2`, defect `+4`, and is a **strict record**;
  its reduction `(2,5)` is `(2,2) mod 3 ∉ R`. It is not an isolated exception — it generates a
  **permanent record tail**, and three further imprimitive record tails occur in the same
  instance (`(58,142)`, `(178,436)`, `(1366,3346)`).
* `α = √3`, `R = {(1,1),(2,3)} mod 5`: record tails through `(22,38)` (`gcd 2`, defect `−8`)
  and `(21,36)` (`gcd 3`, defect `−27`).
* `α = √2`, `R = {(1,1)} mod 3`: record tail through `(58,82)` (`gcd 2`, defect `−4`).
* `α = √6`, `R = {(2,2)} mod 4`: **every** admissible state is imprimitive; all six record
  tails have `gcd 2`. (Here the instance happens to be `2 ×` the odd/odd instance, since
  `(m,k) ≡ (2,2) mod 4 ⟺ (m,k) = 2(m',k')` with `m',k'` odd — a reduction that exists only
  because the class is a dilate.)

Note the published note's own `(4,10)` claim is **confirmed independently** here: by exact
brute force over 18 442 admissible states with `H ≤ 900`, by the certified-tail classification,
and by the gcd ledger.

**S-4. "Self-consistency": choose the comparison family to be all orbits of defect `≤ D` and
stop when `B_cut ≤ D`. — FAILS IN THE TESTED ITERATION; unattainability is WITHDRAWN.**
What is proved is `B_cut ≥ max_A|Q_A|` over the family, since each member contributes
`|Q_A|(H_C/H_A)² ≥ |Q_A|`. That does **not** rule out `B_cut ≤ D`, because the search ceiling
`D` need not equal the largest realised defect, and the floor in `B_cut = ⌊sup F⌋` also leaves
room. An earlier version of this file asserted unattainability; the claim is narrowed to the
observed fact. Measured at `φ`, odd/odd, with `D` running over realised defect values:

```
D       1    2    3    5    8   13   20   30   50   80  130  200  320  500  800 1300
B_cut  18   18   18   22   22   36   30   70   70  136  210  440  754 1152 1890 3183
```

so self-consistency failed at every tested `D` in every instance and the cutoff grew with `D`.
Whether some instance admits a self-consistent `D` is **open**. The algorithm does not need
one: it minimises `B_cut` over a short list of `D`.

**S-5. "η-order is height-order." — FALSE, as the published audit already found,** and in this
general setting it fails in a second, sharper way; see D-3.

**S-6. "The binding competitor sits at offset `d ∈ {0,1}`" — my refutation was WRONG about
which branch it measured; the lemma holds on the branch the theorem uses.** Index states by
`η`-level. Measured over all 26 instances: the realised binding offsets are `{0,1,2,3,4,5,6}`
with no branch restriction, and **exactly `{0,1}` once competitors are restricted to the
`G > 0` branch** — which is the only branch the tail analysis sees, by the `ε₀` threshold of
§6.0. The large offsets come from `G < 0` states inside doubly-infinite orbits (`α' > 0`), where
the height is U-shaped in the level; those states have `ε ≥ √Δ/|B|` and are excluded
analytically, not enumerated. My earlier claim that the binding offset is "unbounded and the
window unsalvageable" is therefore **withdrawn**: it was a statement about the excluded branch.
*What remains true and is what the certificate relies on:* only **blocking** matters, blocking
offsets are `{0,1}` in every instance, and they are bounded a priori by `d*` (`∈ {2,3}` measured)
with a level threshold `p_noblock`, so the certification does not depend on the collapse.

**S-7. Three lemma statements were wrong as displayed — all three confirmed by exact
counterexample, all three now repaired.** Details and the repairs are in
`THEOREM_AND_PROOF.md` §§6.0–6.3; the counterexamples are executable in `scripts/review3.py`
(25/25 checks) and the first and third are mandatory regressions in the independent checker.

| claim | status | effect on the implementation |
|---|---|---|
| Lemma 6.2's right-hand side had the **sign reversed** (`α = φ`, `a=(1,1)`, `b=(1,3)`, `Γ = 0`: the old display read `0 > −10` and predicted `ε_b < ε_a`, but `ε_a = √5−2 < ε_b = (10−3√5)/11`) | **confirmed** | none on any verdict: verdicts come from a direct exact `ε` comparison, and the thresholds use only `|Γ_d|`, `|RHS|`. The emitted ledger's `Γ_d = 0` label was inverted and is fixed |
| Lemma 6.1 ("`ε` decreases along every orbit") is **false on the `G < 0` branch** (`α = (3+√5)/2`, `P(55,21) = (3,1)`, both positive, `ε` rises from `0.745442` to `0.774116`) | **confirmed** | the binding rule depended on it. `verdict` now selects the **`ε`-minimal** competitor below `H_B`, which needs no monotonicity. Measured after the fact: all 588 evaluated candidates had `ε < √Δ/|B|`, so no blocker had in fact been missed — but that was luck, not design. The `ε₀` threshold of §6.0 now makes it design |
| Lemma 6.3's exponent should be **`ρ^{2q}`**, not `ρ^q` (`α = 2+√2`, `a₀=(−61,−30)`, `b₀=(−59,−29)`, `q=1`: `ρ^q U+V = −7196+5460√2 > 0` is the wrong sign, `ρ^{2q}U+V < 0` is right) | **confirmed** | the code used `ρ^q|U| > |V|` as a *threshold*, which implies the correct condition, so every emitted `p_cert` was **conservative** and remained valid. Now uses `ρ^{2q}`, lowering several thresholds |

The common cause is that §§6.1–6.3 were written for the `α' < 0` setting and then carried over
without a branch hypothesis. The `ε₀` threshold of §6.0 supplies that hypothesis once and for
all, and also replaces the per-candidate blocker bound by the uniform `B_comp = 3 B_cut`.

**S-8. "The backward rays are excluded by `ε ≥ √Δ/|B|`" — TRUE only in one of the two cases.**
That floor is a statement about the `G < 0` branch. A **doubly-infinite** orbit has `G > 0` on
its whole positive part, and along its backward ray `ε` rises to `√Δ/|B|` *from below*, so the
floor does not reach it. Counterexample (exact, `scripts/review4.py`): at `α = (3+√5)/2`,
`P^{-1}(1,1) = (13,5)` has `Q = −1`, `G = 3.006211 > 0`, and
`ε(13,5) = 0.743816… < √5/3 = 0.745356…`; every further backward state of the ray is also below
the floor. **Repair:** Lemma 6.0b splits the exclusion into case (i), orbits with no forward
tail, where `G < 0` throughout and the floor applies; and case (ii), doubly-infinite orbits,
where the explicit backward-level cutoff `Y ≤ Y* = (|Q|√Δ/ε₀ − BQ)/(2α)` applies instead, with
`ε₀` the **attained** `ε(w)`. A second subtlety surfaced here and is recorded because it is easy
to get wrong: `Y* > Y_min` — needed so that the height is strictly increasing on the surviving
region, which is what licenses Lemmas 6.3/6.5/6.6 there — holds **strictly** for the attained
`ε(w)` and only with **equality** if `ε₀` is taken to be the bound `√Δ/(2|B|)` itself. Both
cases are now certified per orbit and re-verified independently (check C6b).

**S-8b. Two over-statements inside the S-8 repair, both corrected.**
*(a) The strictness `Y* > Y_min` is not necessary.* I claimed that using the attained `ε(w)`
rather than the bound was forced, because the bound gives `Y* = Y_min`. It is not forced: the
retained condition is `Y > Y*`, so even at `Y* = Y_min` the retained region satisfies
`Y > Y_min` and the height is strictly increasing there. Using `ε(w)` gives extra margin and a
shallower `L*`, which is why the implementation does it — not because the argument needs it.
*(b) "Maximise `ε` below the bound" must name a finite candidate family.* There is no
guaranteed global maximum over all admissible states, and none is needed: `find_eps0_state`
maximises over an explicit finite set — the first state of each family seed's forward tail that
falls below the bound — and for the theorem **any** computable admissible `w` with `ε(w)` below
the threshold suffices.

**S-9. Verified approximate sorting was not enough: it needs a recovery path.** Checking every
adjacent pair with the exact comparator certifies a correctly ordered list, but on failure — or
on key-generation failure or overflow — the algorithm must still *produce* its classification,
or termination is not established for every input. **Repair:** `sort_heights` attempts the
approximate sort, verifies it exactly, and falls back to sorting with the exact algebraic
comparator whenever key generation or verification fails. The fallback path is exercised
directly by forcing key generation to fail and by a constant (degenerate) key, in both the
classifier (`review4.py` O2) and the independent checker (C12).

**S-10. "A state below the binding level has larger `ε` and cannot block" — FALSE.** At
`α = φ` with no congruence restriction, `b = (15,24) = 3·(5,8)` is blocked by `(5,8)`, which lies
**below** the `ε`-minimal state `(13,21)`:
`H(5,8) = 16.0902 < H(13,21) = 42.0344 < H(b) = 48.2705`, with
`ε(13,21) = 0.00081937 < ε(5,8) = ε(b) = 0.00560404` (exact; `review5.py` P1). **Repair:** the
sufficiency form, Lemma 6.6b — if any state blocks, the `ε`-minimal state below `H_B` blocks too,
so the three-way verdict read off it equals an exhaustive scan. The implementation already used
the `ε`-minimal rule, so no verdict was affected; only the justification was wrong. Check C9 now
tests sufficiency against exhaustive scans instead of the false exclusion.

**S-11. "Initial exceptions listed and individually correct" was not completeness — and
demanding completeness found a real implementation error.** The emitter had been listing **P1 and
P4 states as initial exceptions**: P1 states belong to the finite-region scan and P4 states are
excluded by the `ε₀` cutoff, so neither is a P5 anomaly. Caught by the first run of C14(b),
which reported `mine 0, theirs 2` on two certificates. **Repair:** the exception list is now
exactly the P5 anomalies (levels `L*_i < L < T_i` on candidate orbits), the certificate also
carries the P1 record set, and C14 verifies both by independent enumeration and **set equality**.

**S-12. The offset ledger's lower endpoint was unjustified.** `d ≤ d*` came from the no-block
bound, but nothing excluded negative offsets — competitors at levels *later* than the candidate.
**Repair:** the `(candidate, competitor)` `d = 1` height rows give
`sgn(H_comp(q+1) − H_cand(q))`, which with height monotonicity on the retained region excludes
every later level; the ledger now carries exactly those rows (not the full both-orders ledger,
which was tried first and cost ~20× more emission time for no extra content), and C9 verifies
each one exists with the right verdict. The obsolete `d ≤ 1` formula is gone from §7.

**S-13. Lemma 6.3's clearing factor was called positive without absolute values.**
`dd = α − α' < 0` when `α` is the smaller root (`−2.236068` at `α = (3−√5)/2`), so
`A²·dd·r_A r_B ρ^{q+d}` is not positive. **Repair:** `η·dd > 0` on the retained branch, so the
factor is `A²|dd|·r_A r_B ρ^{q+d}` with `r = |η|`.

---

## 2. Defects produced and fixed inside this round

Recorded because each one is a trap the general setting sets and the three published slopes do
not.

**D-1. `pkill`-style self-termination and float cancellation.** `Surd.f()` evaluated
`p + q√D` in double precision; with `p, q` huge Fractions of opposite sign this suffers total
cancellation and returned `0.0` for `ε ≈ 10⁻²⁴`. Any decision taken from `.f()` is therefore
unsound. *Fix:* `Surd.approx(bits=200)` (exact rational `√D` approximation) for sort keys and
display, and an exact `floor_int()` by binary search with integer sign tests for every integer
extraction. No decision in the final code reads a float.

**D-2. Verdict logic: a tie must not short-circuit a loss.** The first `classify` returned on
the first blocker found, so an orbit that both ties with one competitor and strictly loses to
another was labelled a "permanent tie". *Witness:* at `φ`, the orbit through `(9,15) = 3·(3,5)`
ties with the `(3,5)` orbit but loses to the `(7,11)` orbit, so it is **excluded**, not a tie.
*Fix:* scan all competitors; a strict loss overrides any tie.

**D-3. The binding competitor is the one of largest PERIOD, not of largest HEIGHT.** This is
the deepest defect of the round, and it is specific to `α' > 0`.
`H = 2αη/dd + BQ/(A²η dd)` has `H'(η) = (2αA²η² − BQ)/(A²η² dd)`, so the height is **U-shaped**
in `η` whenever `BQ/dd > 0` and the orbit reaches `η² < BQ/(2αA²)`. On a doubly-infinite
positive orbit (`α' > 0`, `Q < 0`) that happens, and the state of largest height below a
candidate then lies on the **backward** branch, where `ε` is large; selecting it hides the true
binding competitor on the forward branch.
*Witness:* at `α = (3+√5)/2`, odd/odd, take the candidate `3·(F₃₅,F₃₇) = (27682395, 72473451)`
(defect `−9`) and the competitor `(F₃₅,F₃₇) = (9227465, 24157817)` (defect `−1`). Scaling by `3`
leaves `ε` unchanged and multiplies the height by `3`, so it is the **unscaled** pair that is the
lower-height blocker:
`H(9227465,24157817) = 4.832·10⁷ < 1.449·10⁸ = H(27682395,72473451)`, with
`ε` **exactly equal**. Hence the candidate is a permanent tie, not a record — but a
height-selected binding state from the competitor's own orbit (on its backward branch) masks
this, and the candidate was reported as a record. Verified directly:
`h_cmp(unscaled, scaled) = −1`, `eps_cmp = 0`, `scaled = 3·unscaled`. *Fix:* select by largest period, which
is correct because `ε` is monotone in the period on the positive part (Lemma 6.1) and
`{p : H(p) < H_{B*}}` is an interval.
This is the same *class* of error as the published audit's F1/W3 ("a fixed-`N` derivative in
`η` orders nothing across norms"), in a setting the published cases cannot reach.

**D-4. Evaluating the tail verdict at the wrong end of a doubly-infinite orbit.** After
positive windows were introduced, the tail period was taken relative to `min(window)`, which
for a doubly-infinite orbit is `−60`: the "tail" was evaluated on the backward ray, where
`ε ≈ 0.745`, and three record families at `(3±√5)/2` and `(5+√21)/2` were lost. *Fix:* evaluate
at the first non-negative window period plus `p_cert`, and treat the backward ray analytically
via its explicit `ε` limit.

**D-5. Seeds in the backward sector cannot serve as a ladder.** `cutoff()` asserted that every
seed reaches the positive quadrant within 200 forward steps; with `α' > 0` that is false for
the backward-sector orbits, and the whole cutoff stage aborted with "no usable family" at both
`(3±√5)/2`. *Fix:* drop such seeds explicitly (they are reported), and prove the remaining
family is non-empty via Lemma 3.1.

**D-6. A half-open normalisation boundary drops an orbit.** `η(1,3) = (3+√5)/2 = λ` exactly at
`α = (3+√5)/2`, so the window `[1,λ)` excludes it; the orbit is recovered only because
Prop 5.2 walks the `j` translates of the `λ`-class representative `(0,1)`. Any implementation
that normalises and then filters by residue **before** translating will silently lose orbits
whose admissible member is not the normalised one.

**D-7. Over-broad test claims (mine).** Two assertions failed because the *test*, not the
mathematics, was wrong, and both are recorded rather than quietly relaxed:
* "every predicted permanent-tie state below the brute-force cap is a weak tie" — false, since
  the eventual verdict is a statement about periods `≥ p_cert` only (S-1);
* "the inclusion of classical best approximations in `ε`-records is strict" — false at `√3`,
  where the two sets coincide below the tested cap. Strictness holds at `φ`, `1+√3`, `√2`,
  `3x²−x−1`, `√6 mod 3`, with explicit witnesses, but it is **not** a theorem.

---

## 3. Remaining obligations

1. **The offset bound is now `d ≤ d*`, certified, and emitted as data** — superseding the
   earlier `d ≤ 1` obligation recorded here. `d* = least d with ρ^{2d−2} > B_comp` plus the
   level threshold `p_noblock` bound the **blocking** offsets outright (Prop 6.6); the ledger in
   each certificate carries, for every (competitor, candidate) pair and every `d ≤ d*`, the
   `Γ_d` sign, the right-hand side and both thresholds, and the independent checker recomputes
   all of them and re-measures the realised offsets. What is *not* written out is a single
   closed-form `d*` uniform over all inputs; see item 3.
2. **The `√Δ ≤ |B|ε` regime of Lemma 5.4 — now measured.** The blocker bound is vacuous when
   `√Δ/|B|` is small. The family `α_N = N + √2` (`Δ = 8`, `B = −2N`, `√Δ/|B| = √2/(2N) → 0`)
   exercises it, and was run at `N = 2,…,20` with odd/odd, `(1,1) mod 3` and a union mod 4.
   All terminate with valid certificates, and `d*`, `p_cert` stay in `{2,3}`. The measurement
   that replaces the earlier "no instance hit the fallback": across all 26 instances the
   per-candidate bound is unavailable in **10 556 of 13 088 verdict calls (81%)**, so the
   unpruned path is the normal one. Correctness never depended on the pruning; the cost
   estimate of §7 does, and should be read as an optimistic case.
3. **The uniform a priori bound on `d*` is not derived in closed form.** `d*` is computed
   per instance as the least `d` with `ρ^{2d−2} > B_comp`, which is explicit; the accompanying
   statement "blocking offsets are bounded" is proved, but a single closed-form bound uniform
   over all `(A,B,C,s,M,R)` is not written out. The checker re-derives `d*` and re-measures
   the blocking offsets, so the gap is in presentation, not in verification.
4. ~~**A proved a-priori bound on the window depth is not written out.**~~ **CLOSED** by
   Lemma 6.0c. `Y_L = A²r²ρ^{2L}` is strictly increasing in `L` with `Y_L → 0` as `L → −∞` and
   `Y_L → ∞` as `L → +∞`, and `Y*` is finite and positive, so a two-sided expanding **exact**
   search locates the unique `L*` with `Y_{L*} ≤ Y* < Y_{L*+1}` in finitely many steps. Those
   two inequalities *are* the certificate: monotonicity then proves the exclusion for every
   level `L ≤ L*`. The orbit list is finite, so every such search terminates — which is the
   universal termination argument that finite test results could not supply. No logarithm and
   no rounding enter: the implementation compares exact powers. Measured: `L* ∈ {−1,0,1}` over
   all 788 case-(ii) orbits, so the stored window is ample by a wide margin, and it is now set
   from `L*` rather than guessed. The certificate carries `Lstar` and `Ystar` per orbit and the
   checker recomputes both witnesses (C6b).
5. **No formal verification.** Nothing is machine-checked in a proof assistant. The
   arithmetic is exact and independent of the published certificate, but it is software. What
   does exist is an independent re-implementation: `scripts/check.py` shares no code, no
   representation and no decision routine with the classifier, and audits the emitted
   certificates: **1159/1159 checks, 0 failures over all 26 certificates**. Its first run,
   before the offset bound was corrected, failed check C9 on all 26.
6. **The finite part below `H(A₁)` is scanned by brute force.** Harmless at the tested scale
   (`H(A₁) ∈ [1.38, 7.80]`), but it should be replaced by the same orbit machinery for a
   self-contained certificate.
7. **Weak records are classified only in the exact-equality mechanism.** Imprimitive weak
   records and the full weak-record set are not classified, exactly as in the published note.
8. **Novelty of the objective is unsettled.** See `LITERATURE_MAP.md`.
9. **`α` not quadratic** is outside everything here, as in the published note (its `e` and `π`
   chronologies remain computational).
