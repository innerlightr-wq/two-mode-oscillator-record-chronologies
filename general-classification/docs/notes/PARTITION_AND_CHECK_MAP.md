# The exhaustive partition, and the proof ↔ certificate ↔ checker cross-walk

Internal, 16 November 2026. Companion to `THEOREM_AND_PROOF.md`. This file exists to answer
one question: **does the manuscript's argument partition the admissible states in exactly the
way the checker tests?** It lists the partition, the obligation attached to each part, where
that obligation is proved, what the certificate carries for it, and which check re-verifies it.

**One level convention.** Levels are **absolute `η`-levels**: a representative is normalised to
`|η| ∈ [1,ρ)` and `P` multiplies `|η|` by exactly `ρ`, so the state at stored period `x` sits at
level `x` — the implementation's stored period *is* the absolute level, with no offset. For
orbit `i`, `enter_i` is the first non-negative level at which the state is positive, and the
**tail-start level** is

```
T_i := enter_i + p_cert ,        certified to satisfy   T_i > L*_i .
```

That certification is what makes P4 / P5 / P6 disjoint, and it is check C6b.

Other notation as in `THEOREM_AND_PROOF.md`: `w` is the comparison state with `ε₀ = ε(w)`,
`Y = A²η²`, `L*_i` the cutoff level of Lemma 6.0c, `B_cut` the record-defect cutoff
(Theorem 4.1), `B_comp` the blocker bound (Lemma 5.4).

---

## 1. The partition

Every admissible state `(m,k)` (both coordinates positive, residue in `R`) lies in **exactly
one** of the following, and each split is a dichotomy on an explicitly computable quantity.

| part | defining condition | obligation |
|---|---|---|
| **P1** | `H ≤ H(w)` | decided by direct exhaustive scan of an explicitly bounded region |
| **P2a** | `H > H(w)`, `|Q| > B_comp` | neither a strict record nor a blocker of one |
| **P2b** | `H > H(w)`, `B_cut < |Q| ≤ B_comp` | not a record; retained as a competitor |
| **P3** | `H > H(w)`, `|Q| ≤ B_cut`, orbit has **no forward tail** | `G < 0`, so `ε ≥ √Δ/\|B\| > 2ε(w) ≥ ε(w)`: with `H > H(w)` it is not a strict record, and it cannot block one |
| **P4** | `H > H(w)`, `|Q| ≤ B_cut`, forward tail, `L ≤ L*_i` | `Y ≤ Y*`, so `ε ≥ ε(w)`: same conclusion |
| **P5** | `H > H(w)`, `|Q| ≤ B_cut`, forward tail, `L*_i < L < T_i` | finitely many levels (possibly negative `L`), decided exactly state by state |
| **P6** | `H > H(w)`, `|Q| ≤ B_cut`, forward tail, `L ≥ T_i` | the certified tail: one verdict per orbit, valid at every such level |

**Disjointness and exhaustiveness.** `P1` versus the rest is a height dichotomy. Inside
`H > H(w)`: `|Q| > B_comp` / `B_cut < |Q| ≤ B_comp` / `|Q| ≤ B_cut` is a three-way split on an
integer. Inside `|Q| ≤ B_cut`: forward tail or not, by `sgn(η·dd)` (Lemma 6.4). Inside the
forward-tail case: `L ≤ L*_i` or not, by the two witness inequalities of Lemma 6.0c; and then
`L < T_i` or not. Since `T_i > L*_i` is certified, P5 is well defined (possibly empty) and P4,
P5, P6 are disjoint. Nothing is left over and nothing is counted twice.

**The conclusion drawn in P3 and P4 is `ε ≥ ε(w)`**, not a strict inequality: a state with
`H > H(w)` and `ε ≥ ε(w)` is not a *strict* record, because `w` has lower height and error at
most its own. That is all that is needed. (An earlier version of this table wrote
`ε₀ > ε(w)`, which is vacuous since `ε₀ = ε(w)`.)

**Why P2a/P2b/P3/P4 need no enumeration.** P2a and P2b are excluded by one inequality each
(Theorem 4.1 for records, Lemma 5.4 for blockers). P3 and P4 are the two cases of the backward
exclusion (Lemma 6.0b): the `G < 0` floor and the `Y ≤ Y*` cutoff. These are the parts that can
be infinite — a doubly-infinite orbit has infinitely many positive states — so they must be
excluded analytically, and they are.

**What remains finite.** P1 is a bounded region. P5 is finitely many levels on finitely many
orbits. P6 is infinite but carries one verdict per orbit. The competitor set for P5 and P6 is
`{|Q| ≤ B_comp}`, enumerated in full.

---

## 2. Cross-walk

| # | obligation | proved in | certificate field(s) | checker |
|---|---|---|---|---|
| 1 | `T² − ΔU² = 4`, `U` minimal, `Δ` non-square, polynomial primitive, `α > 0` | §2 | `T`, `U`, `A,B,C,s`, `Delta` | C1 |
| 2 | `X₀` is a proper automorph; `det = 1`; `Q`-invariant; `η ↦ λη`, `λ > 1` | §2 Lemma 2.1 | `X0` | C2 |
| 3 | `P = X₀^j ≡ I (mod M)`; preserves `Q`, every residue class, and `gcd`; `η ↦ ρη` | §2 Lemma 2.1 | `P`, `j` | C3 |
| 4 | family admissible, `|Q| ≤ D`, declared floor lowest | §3 Lemmas 3.1–3.2 | `family`, `D`, `family_floor` | C4 |
| 5 | `B_cut = ⌊sup F⌋` with the certified tail bound | §4 Theorem 4.1 | `Bcut`, `maxF_pair`, `cutoff_periods`, `cutoff_tail_from` | C5 |
| 6 | `ε(w) < min(1, √Δ/(2\|B\|))`; blocker bound non-vacuous; `B_comp` proved and `≤ 3B_cut` | §6.0 Lemma 6.0 | `eps0_state`, `eps0_num`, `Bcomp`, `Bcomp_uniform` | C6 |
| 7 | **P3**: no-forward-tail orbits have `G < 0` throughout and respect the floor | §6.1 + Lemma 6.0b(i) | per-orbit `case = "i"` | C6b |
| 8 | **P4**: `Y ≤ Y* ⟺ ε ≥ ε₀` on every `G > 0` state | Lemma 6.0b(ii) | per-orbit `case = "ii"`, `Ystar_num` | C6b |
| 9 | **P4**: the cutoff level `L*` with its two witness inequalities `Y_{L*} ≤ Y* < Y_{L*+1}` | Lemma 6.0c | per-orbit `Lstar`, `lvl_eps0` | C6b |
| 10 | the retained region lies at or beyond the height minimum (`Y* ≥ Y_min`) | §6.0 | per-orbit `Ystar_num`, `Q` | C6b |
| 11 | orbit enumeration complete to `B_comp`, imprimitive retained, no PID input | §5 Props 5.1–5.3 | `box`, `nclass`, `orbits`, `W` | C7 |
| 12 | every ledger row: `Γ_d` sign, RHS, `ε`- and height-thresholds | §6.2–6.3 Lemmas 6.2–6.3 | `ledger` | C8 |
| 13 | `ε` decreasing and `H` increasing along every candidate orbit | §6.1, §6.3 | same-orbit `d=1` ledger rows | C8 |
| 14 | `d*`, `p_noblock`, and `p_cert` dominating both | Prop 6.6 | `d_star`, `p_noblock`, `p_cert` | C9 |
| 15 | every blocking offset `≤ d*`; ledger covers every (competitor, candidate) pair at `d ≤ d*` | Prop 6.6 | `observed_blocking_offsets`, `ledger` | C9 |
| 16 | **P6**: verdicts at `T_i, +1, +2`, unpruned; tails and ties reproduce; ties are exact `ε`-equalities at lower height | §6.2, §6.5 | `record_tails`, `ties` | C10 |
| 16b | **sufficiency**: the verdict from the `ε`-minimal state below `H_{B*}` equals an exhaustive scan of the orbit (the earlier "no earlier state can block" claim is false and unused) | Lemma 6.6b | — (behavioural) | **C9** |
| 16c | **offset range complete at BOTH ends**: `d ≤ d*` from the no-block bound, and `d ≥ 0` because a competitor one level later lies above the candidate — the `(candidate, competitor)` `d = 1` height rows | Prop 6.6, Lemma 6.3 | `ledger` (both orders) | **C9** |
| 17 | **P5**: initial exceptions listed, individually correct, **and the list COMPLETE** | S-1, §6 finite part | `initial_exceptions`, per-orbit `Lstar`, `T` | C10, C13, **C14(b)** |
| 17b | **P1** complete: every admissible state with `H ≤ H(w)` enumerated from the explicit bounds `1 ≤ m ≤ ⌊H(w)/α⌋`, `1 ≤ k ≤ ⌊H(w)⌋`, and its record set recomputed | §6 finite part | `eps0_state` | **C14(a)** |
| 17c | `T_i = enter_i + p_cert` declared, and `T_i > L*_i` | §6 finite part | per-orbit `T`, `Lstar` | C6b |
| 18 | ordering is exact, with a guaranteed exact-comparator fallback | §0 | — (behavioural) | C5, C12 |
| 19 | **P1** and the whole classification against an independent brute-force scan | §6 | `family_floor`, `record_tails`, `initial_exceptions` | C12 |
| 20 | **the partition is exhaustive and disjoint on a concrete population, and the class-specific property holds in each part** | §1 above | all of the above | **C13** |

Every row's checker column is a check that recomputes the quantity from the definitions in
`scripts/check.py`, which shares no code, no representation and no decision routine with the
classifier.

---

## 3. What this map does *not* establish

* It is a correspondence between the manuscript and **this** checker. A second, independent
  checker would test the checker.
* Row 20 verifies exhaustiveness on an explicitly bounded population per instance, not
  symbolically. The disjointness and exhaustiveness argument in §1 is the symbolic part; C13
  tests that the implementation's classification agrees with it.
* Nothing here is machine-checked in a proof assistant.
