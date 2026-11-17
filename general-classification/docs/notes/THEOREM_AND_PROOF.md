# A universal effective classification of congruence-restricted relative-error records

Internal investigation, 16 November 2026. **Internal only** — nothing here has been
published, deposited, pushed or committed; the repository
`two-mode-oscillator-record-chronologies` was read at `b8f207d` and is byte-unchanged
(hashes in `sources/SOURCE_AUDIT.txt`).

---

## 0. The problem, in the general form

Let `A, B, C` be coprime integers with `A > 0` and `Δ = B² − 4AC > 0` not a square. For a
sign `s ∈ {±1}` put

```
α  = (−B + s√Δ)/(2A),      α' = (−B − s√Δ)/(2A),      dd = α − α' = s√Δ/A,
```

and require only `α > 0`. No further hypothesis: `α` may be `< 1`, may be the **smaller**
root, `α'` may be **positive**, and `α` need not be an algebraic integer (`A > 1` allowed).

Fix `M ≥ 1` and a nonempty `R ⊆ (Z/MZ)²`. A **state** is a pair of positive integers
`(m,k)` with `(m mod M, k mod M) ∈ R`. **No coprimality is imposed.** Put

```
H(m,k) = mα + k > 0,        ε(m,k) = |mα − k| / (mα + k) ∈ (0,1),
ξ = k − mα,   η = k − mα',   Q(m,k) = A k² + B m k + C m² = A ξ η .
```

`(m,k)` is a **strict record** if `ε(m,k) < ε(m',k')` for every state with
`H(m',k') < H(m,k)`; a **weak record** if `≤` holds. `H` separates states (α irrational), so
the order is total.

### What this objective is, and is not

`ε = |tanh( ½ log(k/(mα)) )|` (verified to 10⁻¹⁶, `lit_bridge` L1), so records minimise the
**multiplicative** error `|log(k/m) − log α|` under the **weighted** height `mα + k`. It is
therefore *not* ordinary best approximation, which minimises `|k − mα|` under the height `m`.
The two are related in one direction only:

> **Proposition 0.1.** Every congruence-restricted classical best approximation — a state
> whose `|ξ|` is smaller than at every admissible state of smaller `H` — is a strict
> `ε`-record. (If `|ξ|` strictly decreases while `H` increases then `ε = |ξ|/H` strictly
> decreases.) The inclusion can be strict and can be an equality.

Verified (`lit_bridge` L2): strict at `φ`, `1+√3`, `√2`, `3x²−x−1`, `√6 mod 3` with explicit
witnesses — e.g. `(7,11)` at `φ` is an `ε`-record but `|7φ−11| > |3φ−5|` with `3 < 7`; an
equality below the tested cap at `√3`. So **no transfer from the continued-fraction or
odd–odd-continued-fraction literature can be assumed in either direction**; §Literature map.

---

## 1. The theorem

> **Theorem 1 (universal effective classification).** There is an algorithm which, on input
> `(A,B,C,s,M,R)` as above, terminates and outputs
>
> 1. a state `A₁` and an integer `B_cut` such that **every** strict record of height
>    `> H(A₁)` has `|Q| ≤ B_cut`;
> 2. a finite list of orbits `O₁,…,O_N` of one explicit unimodular matrix `P`, together
>    containing every admissible state with `|Q| ≤ B_comp` (where `B_comp ≥ B_cut` is the
>    explicit blocker bound of Lemma 5.4);
> 3. an integer `p_cert` and, for each `O_i` carrying an infinite forward positive tail, a
>    verdict in `{record, permanent tie, excluded}` which is **correct at every period
>    `≥ p_cert`**;
> 4. an exact verdict for the remaining states, which split as follows. The states of height
>    `≤ H(w)` and the states of each `O_i` at levels `< p_cert` are **finite in number** and are
>    decided exactly. The orbits without a forward tail can carry **infinitely many** positive
>    states — when `α' > 0` a negative-defect orbit is positive in both directions — and those
>    are excluded **analytically**, not enumerated, in the two cases of Lemma 6.0b: by the
>    `ε ≥ √Δ/|B|` floor when the orbit has no forward tail, and by the explicit backward-level
>    cutoff `Y ≤ Y*` on a doubly-infinite orbit, where that floor fails. After that exclusion
>    the remainder is genuinely finite;
>
> and the union of 3 and 4 is the complete set of strict records, with a finite certificate in
> exact integer and `Z[√Δ]` arithmetic. The weak-but-not-strict records that arise from an
> exact `ε`-equality are classified at the same time.

All the constants are explicit functions of `(A,B,C,s,M,R)`; §7 states them and the cost.

### Status of the pieces

| stage | content | status |
|---|---|---|
| A | class-fixing proper automorph power `P` | **proved**, no hypotheses |
| B | admissible comparison family | **proved**, no hypotheses (and strengthened: see §3) |
| C | the defect cutoff | **proved**, no sign hypotheses (new form, §4) |
| D | finite orbit enumeration | **proved**, classical, no PID/class-number input |
| E | certified tail (`p_cert`) | **proved**, and *simpler* than in the three published cases |
| F | binding rule / finite part | **proved**, with one correction the published cases never meet (§6.3) |

---

## 2. Stage A — the class-fixing automorph

Let `(T,U)` be the least positive solution of `T² − Δ U² = 4`. Because
`T² ≡ Δ U² ≡ B²U² (mod 4)` we have `T ≡ BU (mod 2)`, so

```
X₀ : (m,k) ↦ ( ((T+BU)/2) m + A U k ,  (−C U) m + ((T−BU)/2) k )
```

is integral, `det X₀ = 1`, and `Q(X₀ v) = Q(v)` identically: `X₀` is the proper automorph of
the form `Q`, and it acts on `η` as multiplication by the unit `λ = (T + U√Δ)/2` of the order
of discriminant `Δ` (orient `X₀` or `X₀^{-1}` so that `λ > 1`). Then `ξ ↦ ξ/λ`.

**Lemma 2.1.** `X₀ mod M` lies in the finite group `GL₂(Z/M)`, so `P := X₀^j ≡ I (mod M)` for
some `j ≤ |GL₂(Z/M)|`. `P` preserves the defect `Q` exactly, fixes **every** residue class
mod `M`, and — being in `GL₂(Z)` — preserves `gcd(m,k)`. Hence imprimitive orbits stay
imprimitive and stay inside `R`.

*Checked exactly in `qr_general` (checks A) for all 14 instances.*

**Remark 2.2 (why norm `+1` only).** The published note uses `ρ = u^j` for the fundamental
*unit* `u`, which may have norm `−1` (it does at `φ`, `ρ = φ³`); then `N ↦ −N` along the orbit
and the whole argument needs signed transport `N_p = δ^p N_rep`, a parity-dependent
`Γ_d = 0` rule, and an "alternating" verdict. Using only **proper** automorphs makes `Q`
constant along every orbit. The cost is that each old orbit splits into at most two; the gain
is that *every* comparison below has a constant right-hand side, there are **no alternating
verdicts**, and `ε`-monotonicity becomes unconditional (Lemma 6.1). The `φ` "tie decided by an
integer" of the published Theorem 8.4 reappears simply as: the `Q=−5` orbit records and the
`Q=+5` orbit does not.

**Remark 2.3 (positivity is not available in general).** When `α' > 0` the two eigendirections
`(1,α)` and `(1,α')` both lie in the open positive quadrant; `P^n/ρ^n` tends to a multiple of
`(1,α)·(−α',1)`, which has a negative entry. **No power of the automorph is entrywise
positive, and the positive quadrant is not forward invariant.** Confirmed at
`α = (3±√5)/2` and `(5+√21)/2`: `P = ((−3,8),(−8,21))` and `((−5,24),(−24,115))`. The
published proofs' step "the ladders have positive entries, so once a state has `m,k>0` all its
successors do" is therefore unavailable here and is replaced by Lemma 6.4.

---

## 3. Stage B — the comparison family

**Lemma 3.1 (existence, unconditional).** Any admissible positive state `A₀` serves: its
forward `P`-orbit stays in `R`, has `Q` constant, and (Lemma 6.4) has an infinite positive
tail as soon as `sgn(η) = sgn(dd)`. Such a state exists for every nonempty `R`: the open interval with endpoints `mα'` and `mα` —
that is `(mα', mα)` when `α > α'` and `(mα, mα')` when `α` is the **smaller** root — has length
`m|dd| → ∞`, so for `m ≡ a (mod M)` large it contains a full residue system mod `M`, and any
`k ≡ b (mod M)` inside it has `k` strictly between `mα'` and `mα`, hence `sgn(η) = sgn(dd)`. Its
defect is a nonzero computable integer. **No prescribed or minimal `|Q|` is needed.**

This settles the one input the published programme left open ("what remains hard is a
prescribed or minimal `|L|`"): for the *theorem*, nothing is needed beyond existence. A small
`|Q|` only improves the constant.

**Lemma 3.2 (families, not ladders).** Stage C needs only an admissible family
`A₁ < A₂ < …` of states with heights `→ ∞`. Taking the union of the forward tails of **all**
admissible orbits with `|Q| ≤ D` — obtained from the fundamental-domain box of §5, with no
height search — gives a family whose consecutive height ratios shrink as `D` grows. This is
what makes hard instances tractable: at `√6` with `(m,k) ≡ (1,1) mod 3`, where
`ρ = (5+2√6)⁶ = 940898`, a single-orbit ladder gives `B_cut ≈ 7.3·10⁸` (infeasible), while the
family of all orbits with `|Q| ≤ 50` gives **`B_cut = 135`** and the instance is solved in
under a second.

---

## 4. Stage C — the cutoff, with no sign hypotheses

Write `z = ξ/H`, so `|z| = ε`. From `k = (H+ξ)/2`, `mα = (H−ξ)/2`,

```
η = (H·dd − (B/A) ξ) / (2α),        Q = A ξ η = H² z (A·dd − B z) / (2α) .      (4.1)
```

Hence, using `A|dd| = √Δ`,

```
|Q| = H² ε |A·dd − B z| / (2α)  ≤  H² ε (√Δ + |B| ε) / (2α) .                   (4.2)
```

> **Theorem 4.1 (cutoff).** Let `A,C` be consecutive members of an admissible comparison
> family and let `B*` be a strict record with `H_A < H_{B*} ≤ H_C`. Then
> ```
>   |Q_{B*}|  <  |Q_A| · (H_C/H_A)² · (1 + θ_A),
>   θ_A = (B Q_A + |B Q_A|)/(2 α A² η_A²) = 2 max(u_A, 0),   u = B Q/(2 α A² η²).   (4.3)
> ```

*Proof.* `B*` is a record above `A`, so `ε_{B*} < ε_A`; `x ↦ x(√Δ + |B|x)` is strictly
increasing on `x ≥ 0`; with `H_{B*} ≤ H_C`, (4.2) gives
`|Q_{B*}| < H_C² ε_A(√Δ + |B|ε_A)/(2α)`. Now put `Y = A²η_A²` and `G = 2αY + BQ`. From (4.1),
`H = G/(A²η·dd)` and `ε = A|Q||dd|/|G| = |Q|√Δ/|G|`, with `sgn G = sgn(η·dd) = +` on the
positive tail. Substituting `H_A² = G_A²/(YΔ)` and `ε_A = |Q_A|√Δ/G_A` and simplifying gives
(4.3). ∎

No use is made of `B ≤ 0`, of `α' < 0`, of `α > 1`, of `A = 1`, or of primitivity. In
`u`-coordinates

```
F := |Q_A| (ρ²+u_C)²(1+u_A) / ((ρ²)(1+u_A)²) · … → |Q_A| r²   (r = lim H_C/H_A),
```

and since `u ↦ u/ρ²` along the family, a **certified tail bound** for all later periods is

```
F ≤ |Q_A| r² ((1+w)/(1−w))² (1 + 2w),      w = max(|u_A|,|u_C|) at the cut period,   (4.4)
```

so `B_cut = ⌊ max( F over the finitely many pre-tail pairs, bound (4.4) ) ⌋` is explicit.

**Regression check.** Theorem 4.1 reproduces the three published cutoffs *exactly*, from one
formula with no case analysis:

| `α` | published `F_max` | computed here |
|---|---|---|
| `φ` | `18.1960225…` → 18 | `18.196023` → **18** |
| `1+√3` | `204.5520518…` → 204 | `204.552052` → **204** |
| `√3` | `27.8564064…` → 27 | `27.856406` → **27** |

(and the `φ` two-branch values `17.5116…, 17.9435…, 17.9443…` / `18.1960…` of the published
Remark appear as consecutive family pairs, so the published sign-separated monotonicity
argument is not needed.)

---

## 5. Stage D — finite enumeration, and the blocker bound

**Proposition 5.1 (reduction box).** Normalise `|η|` into `[1, λ)` by powers of the
fundamental automorph. Then `|ξ| = |Q|/(A|η|) ≤ B/A`, and `m = (η−ξ)/dd`,
`k = ξ + mα` give `|m| ≤ (λ + B/A)/|dd| + 1`, `|k| ≤ B/A + |m|α + 1`. An exhaustive scan of
that box meets every `λ`-class with `0 < |Q| ≤ B`. This is the classical reduction theory of
the generalised Pell equation; **no class-number or principal-ideal hypothesis is used**, and
representatives with non-positive coordinates must be kept.

**Proposition 5.2 (splitting).** Each `λ`-class splits into at most `j` `P`-orbits; walking
`p = 0,…,j−1` from the class representative and keeping the translates whose residue lies in
`R` enumerates exactly the admissible `P`-orbits.

Using `λ` rather than `ρ = λ^j` for the box is essential: the box size is `O(λ + B)` instead
of `O(λ^j + B)`.

**Lemma 5.3 (imprimitive states are retained).** `P ∈ GL₂(Z)` preserves `gcd`, so the orbits
of imprimitive states are separate orbits inside `R`, and `|Q| ≤ B` bounds `g = gcd` by
`√(B/|Q₀|)`. They are **not** discardable in general: the published Lemma "imprimitive states
never record" uses that the gcd of two odd numbers is odd. Witnesses here: at `√6` with
`(m,k) ≡ (1,1) mod 3`, `(4,10)` (gcd 2) is a strict record whose reduction `(2,5)` leaves the
class, and it generates a **permanent record tail**, not an isolated exception; at `√3` with
`R = {(1,1),(2,3)} mod 5`, `(22,38)` (gcd 2) and `(21,36)` (gcd 3) are record tails.

**Lemma 5.4 (blocker bound).** If `V` blocks a record `B*`, i.e. `H_V < H_{B*}` and
`ε_V ≤ ε_{B*}`, then by (4.2) applied twice
```
|Q_V| ≤ |Q_{B*}| (√Δ + |B| ε_{B*}) / (√Δ − |B| ε_{B*})      whenever √Δ > |B| ε_{B*}.
```
So only orbits of comparable defect can block, and the competitor set may be pruned per
candidate. When `√Δ ≤ |B| ε` the bound is vacuous and the unpruned competitor set is used;
the implementation detects this and falls back.

---

## 6. Stage E/F — the certified tail and the finite part

Because `P` is a proper automorph, `Q` is **constant** along every orbit. Write `r_A ∈ [1,ρ)`
for the normalised `|η|` of orbit `A`.

### 6.0 The `ε₀` starting threshold

Three of the lemmas below were originally stated without a branch hypothesis and are **false
without one** (§6.1, counterexample). The repair is to start the tail analysis above an
explicit error threshold, which excludes the bad branch outright.

> **Definition.** `ε₀ := min( 1, √Δ/(2|B|) )`, the second term omitted when `B = 0`. Choose
> an admissible comparison state `w` on a family forward tail with `ε(w) < ε₀`; one exists
> because `ε → 0` along every forward tail. The **tail analysis is conducted only above
> `H(w)`**, and `H ≤ H(w)` is an explicitly finite region handled directly.

> **Lemma 6.0.** If `ε(m,k) < √Δ/|B|` then `η·(α−α') > 0`, hence `G := 2αA²η² + BQ > 0`.
>
> *Proof.* From (4.1), `η = (H·dd − (B/A)ξ)/(2α)` and `|ξ| = εH`, so
> `η·dd ≥ H|dd|(|dd| − |B|ε/A)/(2α) > 0` exactly when `ε < A|dd|/|B| = √Δ/|B|`. And
> `G = A²η·dd·H` by the identity `H = G/(A²η dd)`. ∎

> **Lemma 6.0b (backward exclusion, TWO cases).** Let `w` be the chosen comparison state and
> `ε₀ := ε(w) < min(1, √Δ/(2|B|))` its **attained** error. Then no state in either case below
> is a strict record above `H(w)`, nor can block one.
>
> *Case (i) — orbits with `sgn(η·dd) < 0` (no forward tail).* There `G = A²η·dd·H < 0` on
> **every** positive state, so by Lemma 6.1 `ε ≥ √Δ/|B|`, and `√Δ/|B| > 2ε₀ > ε₀`.
>
> *Case (ii) — doubly-infinite orbits (`G > 0` throughout their positive part).* The floor of
> case (i) **does not apply**: along the backward ray `η → 0⁺`, `G → BQ > 0`, and `ε` rises to
> `√Δ/|B|` **from below**. Instead, on `G > 0`,
> ```
> ε = |Q|√Δ / (2αA²η² + BQ) ,     so with  Y := A²η²,
> ε ≥ ε₀   ⟺   Y ≤ Y* := ( |Q|√Δ/ε₀ − BQ ) / (2α) ,
> ```
> an explicit **backward-level cutoff**: the levels with `Y ≤ Y*` have `ε ≥ ε₀` and are
> excluded, and only the finitely many levels with `Y > Y*` lying below the evaluation level
> remain, which are scanned.

**The surviving region lies at or beyond the height minimum.** When `BQ > 0` the height
`H = 2αη/dd + BQ/(A²η dd)` has its minimum at `Y_min = BQ/(2α)`, and

```
Y* ≥ Y_min   ⟺   |Q|√Δ/ε₀ ≥ 2BQ ,
```

which holds because `ε₀ ≤ √Δ/(2|B|)` and `BQ ≤ |B||Q|`. The retained condition is `Y > Y*`, so
on the retained region `Y > Y* ≥ Y_min` and the height is **strictly** increasing in the level —
which is what licenses Lemmas 6.3, 6.5 and 6.6 there. *Correction to an earlier version of this
paragraph:* it claimed that the strict inequality `Y* > Y_min`, and hence the *attained* `ε(w)`
rather than the bound, was **necessary**. It is not: even in the boundary case `Y* = Y_min` the
retained condition `Y > Y*` already gives `Y > Y_min`. Using `ε(w)` supplies an extra margin and
a shallower cutoff level, which is why the implementation does it, but the argument does not
depend on it.

> **Lemma 6.0c (the cutoff level, with universal termination).** Fix an orbit with normalised
> `|η| = r ∈ [1,ρ)` and put `Y_L = A² r² ρ^{2L}`, the value of `Y` at level `L`. Since `ρ > 1`,
> `Y_L` is strictly increasing in `L`, with `Y_L → 0` as `L → −∞` and `Y_L → ∞` as `L → +∞`.
> `Y*` is finite and positive, so there is a **unique** integer `L*` with
> ```
>                           Y_{L*}  ≤  Y*  <  Y_{L*+1} ,
> ```
> and an expanding exact search in both directions locates it in finitely many steps. Those two
> inequalities are the entire certificate: by monotonicity they prove `Y_L ≤ Y*`, hence `ε ≥ ε₀`,
> for **every** level `L ≤ L*`, and `Y_L > Y*`, hence `ε < ε₀`, for every `L > L*`. The orbit
> list is finite, so every such search terminates.

This replaces the earlier adaptive-window loop and the appeal to a window that happened to be
wide enough: the cutoff level is now computed, not discovered, and its justification is two
exact inequalities rather than a measurement. Written logarithmically it is
`L* = ⌊ log(Y*/(A²r²)) / (2 log ρ) ⌋`, but the implementation and the certificate use exact power
comparisons only, so no rounding enters. The stored window is then set from `max_orbits |L*|`
rather than guessed.

**The case split is necessary.** Counterexample to a single-inequality version (verified
exactly, `scripts/review4.py`): at `α = (3+√5)/2`, `P^{-1}(1,1) = (13,5)` lies on a
doubly-infinite positive orbit with `Q = −1` and `G = 3.006211 > 0`, yet

```
ε(13,5) = 0.743816…  <  √Δ/|B| = √5/3 = 0.745356… ,
```

and every further backward state of that ray is likewise below the floor. So the floor alone
does **not** exclude the backward rays; Case (ii)'s level cutoff does.

Two consequences, both used below.

* **(a)** Every strict record above `H(w)` has `ε < ε₀`, and so does every competitor that
  blocks it; by Lemma 6.0 all of them have `G > 0`. The branch on which `ε` *increases* along
  an orbit (§6.1) is therefore absent from the tail analysis.
* **(b)** Lemma 5.4's blocker bound `|Q_V| ≤ |Q_B|(√Δ+|B|ε)/(√Δ−|B|ε)` is now **never
  vacuous** — that is the substantive gain, since the earlier implementation had to fall back to
  an unpruned competitor set in 81% of calls. Under `ε < √Δ/(2|B|)` it is at most `3|Q_B|`, so
  **`B_comp = 3·B_cut` is always safe**; the implementation uses the tighter per-candidate value
  (measured `B_comp/B_cut ∈ [1.00, 2.33]`) and records both.

### 6.1 `ε` along an orbit — corrected

> **Lemma 6.1.** On the `G > 0` branch, `ε` strictly decreases along an orbit as `|η|` grows.
> On the `G < 0` branch it strictly **increases**, and there `ε ≥ √Δ/|B|`.

*Proof.* `ε = |Q|√Δ/|G|` and `G` is strictly increasing in `η²`; where `G > 0`, `|G|` grows and
`ε` falls; where `G < 0`, `|G| = |BQ| − 2αA²η²` falls and `ε` grows, and there
`|G| ≤ |BQ|` gives `ε ≥ |Q|√Δ/|BQ| = √Δ/|B|`. ∎

**The earlier unconditional statement was false.** Counterexample (verified exactly,
`scripts/review3.py` R2): `α = (3+√5)/2`, `P = ((−3,8),(−8,21))`, `P(55,21) = (3,1)` with both
states positive, `Q = 1` on both, yet

```
ε(55,21) = 0.745442…  <  ε(3,1) = 0.774116…      and   G = −2.9997, −2.8885 .
```

Both lie above the floor `√Δ/|B| = √5/3 = 0.745356…`, as Lemma 6.1 requires. With §6.0 in
force this branch cannot appear among tail candidates or their blockers.

### 6.2 The `ε` comparison — corrected sign

> **Lemma 6.2.** For `G_A, G_B > 0`, with `A` at level `p−d` and `B` at level `p`,
> ```
> ε_B < ε_A  ⟺  |Q_A| G_B − |Q_B| G_A > 0
>            ⟺  2 α A² Γ  >  B( |Q_B| Q_A − |Q_A| Q_B ),
> Γ = ρ^{2(p−d)} Γ_d,   Γ_d = |Q_A| r_B² ρ^{2d} − |Q_B| r_A² .
> ```

*Proof.* `ε = |Q|√Δ/G`, so `ε_B < ε_A ⟺ |Q_B|G_A < |Q_A|G_B`; expanding
`G = 2αA²η² + BQ` gives `2αA²Γ + B(|Q_A|Q_B − |Q_B|Q_A) > 0`, which is the display. ∎

**An earlier version displayed the negative of that right-hand side.** Counterexample
(`review3.py` R1, now a mandatory regression in both the classifier verifier and the
independent checker): `α = φ`, `a = (1,1)`, `b = (1,3)`, so `Q_a = −1`, `Q_b = 5`, `Γ = 0`
exactly, and `G_a, G_b > 0`. The old display read `0 > −10`, predicting `ε_b < ε_a`; in fact

```
ε_a = √5 − 2 = 0.236068…   <   ε_b = (10 − 3√5)/11 = 0.299254… .
```

The corrected right-hand side is `+10`, and `0 > 10` is false — the right answer.
*Effect on the implementation:* none on any verdict. All verdicts are decided by a direct exact
comparison of `|ξ_1|H_2` against `|ξ_2|H_1`, never through this formula, and the thresholds use
only `|Γ_d|` and `|RHS|`, which are sign-independent. The emitted ledger's label for the
`Γ_d = 0` case was inverted and is fixed.

The right-hand side is a constant integer, so one exact sign per `(pair, d)` decides all large
`p`, certified once `2αA²ρ^{2(p−d)}|Γ_d| > |RHS|`. If `Γ_d = 0` the verdict is the constant
sign of `−RHS`: three-way, and for `B = 0` an **exact permanent equality**.

### 6.3 The height comparison — corrected exponent

> **Lemma 6.3.** With `A` at level `q` and `B` at level `q+d`, on the `G > 0` branch
> ```
> sgn(H_B − H_A) = sgn( ρ^{2q} U + V ),
> U = 2 α A² r_A r_B ρ^d (r_B ρ^d − r_A),      V = B( Q_B r_A − Q_A r_B ρ^d ),
> ```
> certified once `ρ^{2q}|U| > |V|`; `U = 0` forces `r_A = r_B ρ^d`, the same orbit after an
> index shift, and then `V = 0` as well.

*Proof.* `H = G/(A²η·dd)` with `G = A²η·dd·H`, and on the retained branch `η·dd > 0`, so writing
`r = |η|` the quantity `A²|dd|·r_A r_B ρ^{q+d}` is **positive** — which is the factor to clear,
not `A²·dd·…`, since `dd < 0` when `α` is the smaller root. Multiplying `H_B − H_A` by it turns
the first term into `ρ^{2q}U` and the second into exactly `V`. (The representatives `r_A, r_B`
are `|η|`-normalised throughout, so `U` and `V` as displayed are already in terms of `|η|`.) ∎
*Correction:* an earlier version called `A²·dd·r_A r_B ρ^{q+d}` positive, which fails for the
smaller root; `|dd|` is required. Verified: at `α = (3−√5)/2`, `dd = −2.236068` while `η·dd > 0`
on every retained state (`review5.py`).

**An earlier version displayed `ρ^q U + V`.** Counterexample (`review3.py` R3): `α = 2+√2`,
`X₀ = ((−1,2),(−4,7))`, `ρ = 3+2√2`, normalised representatives `a₀ = (−61,−30)`,
`b₀ = (−59,−29)` (both with `|η| ∈ [1,ρ)`), which map to `a₁ = (1,34)`, `b₁ = (1,33)`, so
`H_{b₁} − H_{a₁} = −1` exactly. At `q = 1`, `d = 0`:

```
ρ^q U + V  = −7196 + 5460√2 = +525.6061…   (wrong sign)
ρ^{2q}U + V = −525.6061…                    (right sign)
```

*Effect on the implementation:* the code used `ρ^q|U| > |V|` as the **threshold**. Since
`ρ > 1` and `q ≥ 0`, that condition implies the correct one, so every emitted threshold was
**conservative** and `p_cert` remained valid — merely larger than necessary. The code now uses
`ρ^{2q}`, which lowers several thresholds.

**Lemma 6.4 (positive windows).** `η` keeps its sign along an orbit and `ξ → 0` forward, so
`m = (η−ξ)/dd → +∞` iff `sgn(η) = sgn(dd)`; this is exactly the criterion for an **infinite
forward positive tail** (verified for all 14 instances). When `α' < 0` every orbit either has
such a tail or only finitely many positive states. When `α' > 0`, an orbit with `Q < 0` is
positive in **both** directions, and going backward `ε` increases to the explicit limit
`|dd|/(α+α') > 0` — e.g. `0.745356…` at `(3+√5)/2` and `0.916515…` at `(5+√21)/2`. Such rays
hold no record beyond an explicit height.

**Lemma 6.5 (binding rule — now an optimisation, not a correctness requirement).** Among the
states of one orbit with height below `H_{B*}`, the one of smallest `ε` is the one of **largest
period** — *on the `G > 0` branch*, by Lemma 6.1; on the `G < 0` branch the rule is reversed.
The implementation therefore no longer relies on it: `verdict` selects the competitor
**minimising `ε`** among those of height below `H_{B*}`, which is the definition of blocking and
needs no monotonicity hypothesis. Lemma 6.5 survives as the statement that, under §6.0, the
cheaper largest-period rule agrees with it.
It need **not** be the one of largest height: `H = 2αη/dd + BQ/(A²η·dd)` has
`H'(η) = (2αA²η² − BQ)/(A²η²dd)`, so `H` is **U-shaped** in `η` whenever `BQ/dd > 0` and the
orbit reaches `η² < BQ/(2αA²)`. That happens only when `α' > 0` (the doubly-infinite orbits
reach `η → 0`). Selecting the competitor by largest height instead of largest period then
picks a backward state of large `ε` and misses the true binding competitor. *This defect was
produced and then fixed in this round* (§GAPS, D-3); it cannot arise in the three published
slopes, where `α' < 0`.

**Proposition 6.6 (offset bound) — CORRECTED, and then simplified by §6.0.** An earlier
version asserted that the binding competitor always sits at offset `d ∈ {0,1}`. Index states by
`η`-**level**: `level(w)` is the integer `L` with `|η(w)|/ρ^L ∈ [1,ρ)`; representatives are
normalised into `[1,ρ)` and `P` multiplies `|η|` by exactly `ρ`, so the level of the state at
stored period `x` is exactly `x`.

* *Measured without a branch restriction*, the binding offset is **not** bounded by 1: with
  `α' > 0` the height is U-shaped in the level, and a doubly-infinite orbit's last level below
  `H_{B*}` lies several levels down (offsets up to 10 observed).
* *Those offsets are measured on `G < 0` states*, which §6.0 removes from the analysis. With
  competitors restricted to the `G > 0` branch the offsets **collapse to exactly `{0,1}`**:
  measured over all 26 instances, the realised binding offsets are `{0,1,2,3,4,5,6}` with no
  branch restriction and `{0,1}` with it. So the window lemma is correct on the branch the
  theorem uses, and my earlier report of "unbounded offsets" was measuring the branch that §6.0
  excludes. This is what the limits
  `H_A(p−1)/H_B(p) → r_A/(ρ r_B) < 1` and `H_A(p+1)/H_B(p) → ρ r_A/r_B > 1`
  predict, together with eventual height monotonicity on that branch; the effective threshold
  they need is exactly Lemma 6.3's.
* *The certified bound retained in the certificate* does not rely on that collapse. Only
  **blocking** matters (`ε_A ≤ ε_{B*}` as well as lower height), and blocking offsets are
  bounded outright: on the `G > 0` branch `ε_A > ε_{B*}` as soon as `|Q_A|G_{B*} > |Q_{B*}|G_A`,
  and with `r_A < ρ`, `r_{B*} ≥ 1` it suffices that
  ```
  2 α A² ρ^{2L} ( |Q_A| − |Q_{B*}| ρ^{2−2d} )  >  |Q_A||B Q_{B*}| + |Q_{B*}||B Q_A| ,
  ```
  whose bracket is positive for every pair with `|Q| ≤ B_comp` once `ρ^{2d−2} > B_comp`. That
  defines `d* = least d ≥ 1 with ρ^{2d−2} > B_comp`, and the additive part fixes a level
  threshold `p_noblock`. Hence **for `d > d*` nothing can block at any level `≥ p_noblock`**,
  and only `d ≤ d*` needs the `Γ_d` thresholds.

So `p_cert := max( Lemma 6.2–6.3 thresholds for all d ≤ d*, p_noblock, the least level at
which every candidate has ε < ε₀ )`, and the emitted ledger covers every (competitor,
candidate) pair at every `d ≤ d*`.

Finally, comparing only the **`ε`-minimal** state of each orbit is sufficient, and the reason is
a **sufficiency** statement, not an exclusion:

> **Lemma 6.6b (sufficiency).** If *any* state of an orbit blocks the candidate `B*` — i.e. has
> height below `H_{B*}` and `ε ≤ ε_{B*}` — then the state `V*` of minimal `ε` among those of
> height below `H_{B*}` also blocks it, since `ε_{V*} ≤ ε_V ≤ ε_{B*}`. Moreover the three-way
> verdict read off `V*` equals the verdict of an exhaustive scan: if `ε_{V*} > ε_{B*}` nothing
> blocks; if `ε_{V*} = ε_{B*}` every blocker ties; if `ε_{V*} < ε_{B*}` there is a strict loss.
> So it is enough to test `V*`.

**An earlier version of this paragraph asserted instead that "a state below the binding level has
larger `ε` and cannot block". That is FALSE.** Counterexample (verified exactly,
`scripts/review5.py` P1): at `α = φ` with no congruence restriction, take `b = (15,24) = 3·(5,8)`
and the orbit `(5,8) → (13,21) → (34,55)` of `((1,1),(1,2))`. Then

```
H(5,8) = 16.0902 < H(13,21) = 42.0344 < H(b) = 48.2705 < H(34,55) = 110.0132 ,
ε(13,21) = 0.00081937 < ε(5,8) = ε(b) = 0.00560404 ,
```

so `(13,21)` is the `ε`-minimal state below `H(b)` — yet the **earlier** state `(5,8)` also
blocks `b`, by exact equality of `ε`. Lemma 6.6b is unaffected and is what the implementation
uses; the exclusion claim is withdrawn. Verified on 976 sampled candidates against exhaustive
scans (`review5.py` P1b), and re-verified independently as check C9.


**The finite part, under one convention.** Levels are **absolute `η`-levels** throughout: a
representative is normalised to `|η| ∈ [1,ρ)`, `P` multiplies `|η|` by exactly `ρ`, so the
state at stored period `x` sits at level `x`. For orbit `i` write `enter_i` for the first
non-negative level at which the state is positive and define the **tail-start level**

```
T_i := enter_i + p_cert ,     certified to satisfy   T_i > L*_i .
```

The reference height is `H(w)`, the comparison state of §6.0 — **not** `H(A₁)`: `H(w) ≥ H(A₁)`,
and the `ε₀` argument needs `H > H(w)`, so `H ≤ H(w)` is the finite region. By Theorem 4.1 every
record above `H(w)` has `|Q| ≤ B_cut`, and by Lemma 5.4 every blocker of one has `|Q| ≤ B_comp`;
both are enumerated in Stage D. So the classification reduces to

* a direct scan of `H ≤ H(w)`, bounded explicitly by `1 ≤ m ≤ ⌊H(w)/α⌋`, `1 ≤ k ≤ ⌊H(w)⌋`
  followed by the exact height and residue filters;
* exact verdicts at the finitely many levels `L*_i < L < T_i` of each candidate orbit (which may
  include negative `L`);
* the certified tail `L ≥ T_i`.

`H(w)` is `1.7…–26.1` over the instances tested, and `T_i − L*_i − 1` is between 1 and 4.

---

## 7. Constants, and the cost

```
j        ≤ |GL₂(Z/M)|                  (index of the class-fixing automorph power)
ρ        = λ^j,  λ = (T+U√Δ)/2         (T²−ΔU²=4 least positive solution)
B_cut    = ⌊ max over consecutive family pairs of |Q_A|(H_C/H_A)²(1+θ_A) ⌋, with (4.4)
B_comp   = the per-candidate Lemma 5.4 bound at w (always available under eps_0),
           and <= 3 B_cut, the coarse uniform version; measured ratio B_comp/B_cut
           in [1.00, 2.33] over the 26 instances
box      = ±((λ+B_comp/A)/|dd| + 1) × ±(B_comp/A + …)
p_cert   = max( Lemma 6.2-6.3 thresholds over every ORDERED pair with at least one
           candidate side, at every 0 <= d <= d*;  p_noblock;  the least level at
           which every candidate has eps < eps_0 )
```

**Lower bound on what the method can give — NARROWED.** Every family member contributes
`|Q_A|(H_C/H_A)² ≥ |Q_A|`, so

```
B_cut ≥ max_A |Q_A| over the family                                        (proved)
```

and therefore a self-consistent step (`B_cut ≤ D`, where `D` is the *search ceiling* of the
family "all admissible orbits with `|Q| ≤ D`") requires `max_A|Q_A| ≤ B_cut ≤ D`. This is
**not** an impossibility: `D` need not equal the largest defect actually represented, so if the
realised defects below `D` are sparse — in the extreme, if the only admissible defect `≤ D` is
`1` and there are many defect-`1` orbits spread in phase — then `B_cut ≈ r² ` could fall below
`D`. An earlier version of this document claimed unattainability; that claim is **withdrawn**.
What is established is: (i) the displayed inequality; (ii) in the iteration actually tested —
`D` ranging over the realised defect values, so that `max_A|Q_A| = D` — self-consistency failed
at **every** `D` in **every** instance, and the cutoff **trended upward but not monotonically**
(at `φ`: `18, 18, 18, 22, 22, 36, 30, 70, 70, 136, 210, 440, …` for
`D = 1,2,3,5,8,13,20,30,50,80,130,200` — note `36` then `30`, so monotonicity is **not** claimed).
Whether some `(A,B,C,s,M,R)` admits a self-consistent `D` is **open**; the algorithm does not
need one, since it simply minimises `B_cut` over a short list of `D`.

**Cost.** The dominant cost is the Stage D box, `O(λ · B_comp/|dd|)` lattice points, with
`B_comp = Θ(min_D D r(D)²)` and `r(D) ≥ ρ^{1/ν(D)} = λ^{j/ν(D)}`. So the algorithm is
*effective* always, and *feasible* when a modest `D` already supplies enough orbits to make
`r(D)` small. All 14 instances tested finish in `< 4 s`. The worst case is governed by `j`,
which is bounded only by `|GL₂(Z/M)| = O(M⁴)`; a single-orbit ladder in the `√6 mod 3`
instance already costs `≈ 7·10⁸`, which the family construction of Lemma 3.2 reduces to `135`.

**Corollary 7.1 (accumulation values).** Along a fixed-defect orbit
`H²ε → 2α|Q|/√Δ`, i.e. `h²ε → α|Q|/(2√Δ)` with `h = H/2`. These are values *at* records, not
the envelope of `H ↦ H²ε` between records.

---

## 8. Results: the regression controls and the stress cases

`qr_general.py`: **98/98 checks pass, 0 failures** (log `results/qr_general.log`);
**Ordering keys, with a guaranteed fallback.** Every height-ordered list is produced by
`sort_heights`: presort with an approximate key, **verify exactly on all adjacent pairs**, and —
if key generation raises, or if any adjacent pair fails — **re-sort with the exact algebraic
comparator**. Because the height order is a strict total order, adjacent-pair correctness
implies the whole list is sorted, so the verification is a complete certificate and not a spot
check; and because of the fallback, verification failure or key degeneracy (overflow to `±inf`,
a constant key) costs a slower sort rather than an abort, so **termination with a correctly
ordered list is established for every input**. Verification alone would only prevent a wrong
answer, not guarantee an answer. No ordering decision is ever taken from an approximate key, and
the 200-bit rational `√D` in those keys therefore needs no separation bound. The fallback path
is exercised directly: forcing key generation to fail reproduces the exact order
(`review4.py` O2, and check C12).

`lit_bridge.py`: **14/14**. All arithmetic exact; floats only printed. Independent of the
published certificate: no code is shared with `congruence-records/certificate/`.

| instance | `λ` | `j` | `B_cut` | orbits | `p_cert` | record tails | permanent ties |
|---|---|---|---|---|---|---|---|
| **CONTROL `φ`, odd/odd** | 2.618 | 3 | 18 | 14 | 2 | 3: `Q = −1, +1, −5` | 1 (imprimitive `(3,3)`) |
| **CONTROL `1+√3`, odd/odd** | 3.732 | 2 | 44 | 31 | 3 | 3: `Q = −3, +1, −11` | 1 |
| **CONTROL `√3`, odd/odd** | 3.732 | 2 | 27 | 14 | 1 | 2: `Q = −2, −2` | 4 (incl. the `Q=+6` companion) |
| `√2`, odd/odd | 5.828 | 1 | 18 | 6 | 1 | 2: `Q = −1, +7` | 1 |
| `(3+√5)/2`, odd/odd (`α'>0`) | 2.618 | 3 | 18 | 21 | 2 | 3: `Q = +1, −5, −1` | 1 |
| `(3−√5)/2`, odd/odd (smaller root, `α<1`) | 2.618 | 3 | 18 | 72 | 4 | 3 | 1 |
| `1/√2`, odd/odd (`A = 2`) | 5.828 | 1 | 18 | 6 | 1 | 2: `Q = +1, −7` | 1 |
| `3x²−x−1`, odd/odd (`A = 3`) | 10.908 | 3 | 32 | 36 | 1 | **9** | 3 |
| `√3`, `R = {(1,1),(2,3)} mod 5` | 3.732 | 3 | 164 | 32 | 1 | **6**, two imprimitive | 0 |
| `√6`, `(2,2) mod 4` (all states imprimitive) | 9.899 | 2 | 113 | 12 | 1 | 6, all gcd 2 | 0 |
| `√2`, `(1,1) mod 3` | 5.828 | 4 | 61 | 33 | 1 | **9**, one gcd 2 | 2 |
| `√6`, `(1,1) mod 3` (the `(4,10)` case) | 9.899 | 6 | 135 | 84 | 1 | **20**, four imprimitive | 6 |
| `√5`, unrestricted | 2.236 | 1 | — | — | — | see log | — |
| `(5+√21)/2`, odd/odd (`α'>0`) | 4.791 | 3 | 77 | 102 | 2 | 6 | 2 |

The three controls are reproduced exactly, independently, including both published equality
mechanisms: the `φ` cycle `(−1,+1,−5)`, the `1+√3` cycle `(−3,+1,−11)`, the `√3` ladder of
constant defect `−2`, and the `√3` companion family of defect `+6` with **permanently equal
`ε`**. An independent brute-force scan (`H ≤ 800–900`, up to 265 076 admissible states) agrees
with the certified tails in every instance, in both directions.

---

## 8b. The near-equal-positive-conjugate stress family, and the certificate

### 8b.1 `α_N = N + √2`

This is the regime in which the blocker bound of Lemma 5.4 is hardest: `Δ = 8` and `B = −2N`,
so the bound needs `ε < √Δ/|B| = √2/N → 0`, while `λ = 3 + 2√2` is independent of `N`.
All instances terminate with valid certificates.

| instance | `α` | `ε`-budget `√Δ/|B|` | `d*` | `p_cert` | `B_cut` | orbits | tails | ties | initial exc. | blocker fallbacks |
|---|---|---|---|---|---|---|---|---|---|---|
| `Nplussqrt2_N2_oddodd` | 3.4142 | 0.7071 | 3 | 3 | 33 | 17 | 2 | 1 | 0 | 254/298 |
| `Nplussqrt2_N3_oddodd` | 4.4142 | 0.4714 | 3 | 3 | 15 | 18 | 2 | 0 | 1 | 254/302 |
| `Nplussqrt2_N4_oddodd` | 5.4142 | 0.3536 | 3 | 3 | 33 | 19 | 2 | 1 | 1 | 148/200 |
| `Nplussqrt2_N6_oddodd` | 7.4142 | 0.2357 | 3 | 3 | 33 | 19 | 2 | 1 | 2 | 95/147 |
| `Nplussqrt2_N8_oddodd` | 9.4142 | 0.1768 | 3 | 3 | 33 | 19 | 2 | 1 | 2 | 95/147 |
| `Nplussqrt2_N12_oddodd` | 13.4142 | 0.1179 | 3 | 3 | 33 | 19 | 2 | 1 | 2 | 96/147 |
| `Nplussqrt2_N20_oddodd` | 21.4142 | 0.07071 | 3 | 3 | 33 | 19 | 2 | 1 | 2 | 96/147 |
| `Nplussqrt2_N2_11mod3` | 3.4142 | 0.7071 | 2 | 2 | 85 | 89 | 9 | 2 | 0 | 1528/1708 |
| `Nplussqrt2_N5_11mod3` | 6.4142 | 0.2828 | 2 | 2 | 85 | 95 | 9 | 2 | 1 | 1490/1681 |
| `Nplussqrt2_N9_11mod3` | 10.4142 | 0.1571 | 2 | 2 | 85 | 89 | 9 | 2 | 3 | 1318/1496 |
| `Nplussqrt2_N2_union_mod4` | 3.4142 | 0.7071 | 2 | 2 | 78 | 43 | 5 | 2 | 0 | 628/715 |
| `Nplussqrt2_N5_union_mod4` | 6.4142 | 0.2828 | 2 | 2 | 89 | 56 | 4 | 2 | 2 | 777/884 |
| `Nplussqrt2_N9_union_mod4` | 10.4142 | 0.1571 | 2 | 2 | 92 | 60 | 4 | 2 | 3 | 725/843 |

Three things the family shows.

1. **The fallback is the common path, not the exception.** Over all 26 instances the
   per-candidate blocker bound is unavailable in **10 556 of 13 088 verdict calls (81%)**, so
   the unpruned competitor set is what actually runs. Correctness never depended on the
   pruning — it is a speed optimisation — and the earlier remark that the fallback was
   "untested" is replaced by this measurement.
2. **Initial exceptions grow with `N`** (0, 1, 1, 2, 2, 2, 2 for `N = 2,3,4,6,8,12,20`), then
   stabilise, as do the orbit and tail counts (19 orbits, 2 tails) and `B_cut = 33`. That
   stabilisation is expected: `Δ`, `λ` and `ρ` do not depend on `N`.
3. **`d*` and `p_cert` stay small** (`d* ∈ {2,3}`, `p_cert ∈ {2,3}`) even as the `ε`-budget
   falls to `0.07`, so the corrected offset bound of Proposition 6.6 is not sensitive to this
   degeneracy.

### 8b.2 The emitted certificate and the independent checker

`scripts/emit.py` writes one JSON certificate per instance into `certificates/`, carrying: the
Pell solution `(T,U)`; `X₀`, `j`, `P`; the comparison family and `D`; `B_cut` with the attaining
pair and the tail-bound period; `B_comp` and whether the blocker bound was available; the
reduction box, the `λ`-class count and the full orbit list (representative, defect, gcd,
forward flag, positive window, doubly-infinite flag, tail verdict); `d*`, `p_noblock`,
`p_cert`; the **per-pair ledger** of `Γ_d` signs, right-hand sides and both thresholds at every
`d ≤ d*`; the observed binding and blocking offset sets; and the record tails, permanent ties
and initial exceptions.

`scripts/check.py` is an **independent checker**. It imports nothing from `gq.py`: its
arithmetic is a different representation of `Q(√Δ)` — `(a + b√Δ)/d` with one integer
denominator, over `Δ` itself rather than over the squarefree part — and its sign, floor, matrix
and comparison routines are written separately. It **does not use the blocker lemma**: every
competitor comparison is unpruned. It verifies, per certificate:

| check | content |
|---|---|
| C1 | `T² − ΔU² = 4`, minimality of `U`, `Δ` non-square, primitivity, `α > 0` |
| C2 | `det X₀ = 1`, `Q`-invariance, `η`-multiplier `= λ`, `λ > 1` |
| C3 | `P = X₀^j`, `P ≡ I (mod M)`, `Q`-invariance, gcd preservation, `η ↦ ρη` |
| C4 | family admissibility, `|Q| ≤ D`, the declared floor is lowest |
| C5 | `B_cut = ⌊sup F⌋` recomputed from the definition, with the tail bound; `B_comp ≥ B_cut` |
| C7 | the orbit list re-derived by an **independent scan of the reduction box**, defects, forward flags and windows |
| C8 | every ledger row recomputed; `p_cert` dominates the `d ≤ d*` thresholds; the same-orbit `d=1` rows give `ε`-decrease and `H`-increase on every forward orbit |
| C9 | `d*` and `p_noblock` recomputed; the ledger covers every pair at every `d ≤ d*`; **blocking offsets re-measured exhaustively**; no state below an orbit's binding level ever blocks |
| C10 | verdicts re-evaluated **unpruned** at `p_cert, +1, +2`; record tails and ties reproduced; each tie confirmed an exact `ε`-equality at lower height |
| C12 | an independent brute-force scan: records lie in certified tails or declared exceptions, and the cutoff holds |

Its first run **failed C9 on all 26 certificates**, which is how the offset gap of
Proposition 6.6 was found. That is the intended use.

---

## 9. What was already implicit in the three published examples, and what is new

**Already there** (credit to the published note and its audits): the master identities; the
defect as the governing invariant; the idea of a height-only cutoff; the `Γ_d`/`U,V` shape of
the two comparisons; the `Γ_d = 0` three-way rule and the two equality mechanisms; the
window/`d ∈ {0,1}` reduction; the classical reduction box; the four-way verdict vocabulary.

**New in this round.**

1. **Theorem 4.1**: one cutoff inequality valid for every real quadratic `α > 0` and every
   `(M,R)`, with **no** sign hypotheses (`t ≥ 0`, `α' < 0`, `α > 1`, `A = 1` all dropped),
   replacing the per-slope closed forms and the sign-separated monotonicity argument — and
   reproducing the published constants `18, 204, 27` exactly.
2. **Lemma 3.1**: ladder existence is unconditional and needs no prescribed or minimal defect;
   this closes the input the published `THEOREM_TARGET.md` listed as missing.
3. **Lemma 3.2 + Prop 5.2**: comparison *families* of bounded defect, enumerated through the
   **fundamental** domain (`λ`, not `ρ`). This is what turns the hard congruence instances
   from infeasible into sub-second (`√6 mod 3`: `7.3·10⁸ → 135`).
4. **Proper automorphs only** (Remark 2.2): `Q` constant, no signed transport, no parity
   bookkeeping, no alternating verdicts, and Lemma 6.1 unconditional.
5. **Lemma 5.4**, the blocker bound: the competitor set is bounded by the candidate's own
   defect, which is what makes the finite part finite *without* brute force.
6. **Lemma 6.4 / Remark 2.3**: the `α' > 0` structure — no entrywise-positive automorph power,
   doubly-infinite positive orbits, and the explicit backward `ε` limit `|dd|/(α+α')`.
7. **Lemma 6.5**: the binding competitor is the one of largest *period*, not largest *height*;
   the two differ exactly when `BQ/dd > 0` and `η² < BQ/(2αA²)`, i.e. only when `α' > 0`.
8. **§7 lower bound**: `B_cut ≥ max|Q|` over the family, so the cutoff cannot be driven down
   indefinitely; the honest cost statement that follows.
9. **Proposition 0.1** and the `tanh` identity: the exact relation to classical best
   approximation (inclusion, sometimes strict, sometimes equality).

**Not new, and not claimed:** the finiteness of the orbits of a given defect under the unit
group, and the bounded region exhibiting a representative of each — classical (generalised
Pell reduction).

---

## 10. Answers to the questions posed

1. **Does the method work universally for the stated domain?** Yes. Every stage is proved for
   an arbitrary real quadratic irrational `α > 0` given by an arbitrary primitive integral
   quadratic polynomial with `A > 0`, an arbitrary modulus `M`, and an arbitrary nonempty
   `R ⊆ (Z/M)²`, with no coprimality assumption. The three sign hypotheses and the odd/odd
   primitivity reduction that the published note identified as obstacles are all removed.
2. **If not, what is the largest domain proved?** Not applicable to the *theorem*; the
   limitation is computational (§7) and is stated as a cost, not a restriction.
3. **Complete classification or only a finite candidate reduction?** A **complete
   classification**: stages A–D give the finite candidate reduction, Lemmas 6.1–6.6 give the
   certified eventual verdicts with an explicit `p_cert`, and §6 shows the remaining finite
   part is the enumerated orbits' low periods plus a trivial region below the family floor.
   The equality cases are classified alongside.
4. **Does the algorithm provably terminate?** Yes: Lemma 2.1 (finite `j`), Theorem 4.1 with the
   certified tail bound (4.4) (finite `B_cut`), Prop 5.1 (finite box), Lemmas 6.2–6.3 (finite
   thresholds, each reached after finitely many exactly-tested periods).
5. **Which parts were implicit in the three examples / which needed new arguments?** §9.
6. **What does this resolve?** It resolves the **internal** target stated in
   `congruence-records/certificate/THEOREM_TARGET.md` ("three theorems plus a method whose
   every lemma is proved, needing assembly and the ladder-existence input"): the assembly is
   done, the ladder input is discharged, and the scope restrictions `t ≥ 0`, `α' < 0`,
   odd/odd are removed. It is an **effective formulation of classical structure** (the unit
   action on an indefinite form, plus reduction theory) for a non-classical objective; it does
   **not** resolve any external open question known to me, and the novelty of the objective
   itself remains unsettled (§Literature map).
