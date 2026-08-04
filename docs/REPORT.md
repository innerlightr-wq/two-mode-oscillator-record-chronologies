# Two-Mode Oscillator Audit — Status Report

**Scope:** boundary record theorem (Task I) and √2 interior strict-record chronology (Task II), exact arithmetic throughout. No coupling, no three-mode systems, no cosmology, no paper draft. All floating-point tables from earlier sessions are superseded; floats appear below only as display decimals and presort keys, with every ordering decision re-verified in exact arithmetic over ℚ(√d).

**Companion files:** `audit.py` (exact-arithmetic source, all checks reproduced by running it), `records_sqrt2_first30.csv` (first 30 strict records, exact algebraic forms), `README.md`, `SHA256SUMS`.

---

## 1. Audit verdict

Both target proofs are now complete. The boundary record theorem is proved with an exact exceptional set, and the candidate formula S(α) from the interrupted code is **correct as written**, with one substantive correction to the earlier informal claims about when S(α) is empty: there is a previously unnoticed exceptional window **α ∈ (2, √5)** on which S(α) = {2}. The √2 interior strict-record chronology is **fully proved**, not merely computationally verified: the merged two-orbit sequence P₀, S₀, P₁, S₁, … is the complete set of strict chronological balance records, with signed defects Q = −1, +7, −1, +7, …. The proof rests on four exact inequalities and two congruence lemmas, all listed below and all machine-verified in exact arithmetic. The suggested envelope constants liminf = 1/4 and limsup = (57+40√2)/28 are confirmed by derivation from the proven chronology.

## 2. Corrected boundary record theorem

**Theorem (boundary records).** Fix α > 1 and let states be odd pairs (m,k), h = (mα+k)/2, ε_edge = min(mα,k)/(mα+k). The strict chronological record minima of ε_edge are exactly

  𝓑 ∪ { (1, 2n+1) : n ∈ S(α) },  𝓑 = {(m,1) : m odd},

where

  **S(α) = { n ≥ 1 : α²(2⌊n/α⌋+1) < 2n+1 }.**

Every element of 𝓑 is a record; the exceptional states (1, 2n+1) — i.e. (n₁,n₂) = (0,n) — are records precisely for n ∈ S(α). No state with n₁ ≥ 1 and n₂ ≥ 1 is ever a record, with no exceptions for any α > 1. On 𝓑 the exact identity h·ε_edge = 1/2 holds, and for irrational α no exact height ties occur; for rational α the tie analysis in §3 shows the theorem statement is unchanged.

## 3. Boundary proof

*Step 1 — interior states are never records.* Let m, k ≥ 3. If the minimum is the k-side (k < mα is not needed; only k ≥ 3), compare with (m,1), which has strictly lower height: 1/(mα+1) < k/(mα+k) ⇔ mα+k < kmα+k ⇔ mα < kmα, true since k > 1. If the minimum is the m-side (mα < k), compare with (1,k), strictly lower height: α/(α+k) < mα/(mα+k) ⇔ k < mk, true since m > 1. Both dominations are strict, so no mixed state can be a record for any α > 1. (Machine check across 14 values of α: zero mixed records.)

*Step 2 — every rung (m,1) is a record.* ε(m,1) = 1/(mα+1) is strictly decreasing in m, so lower rungs are beaten. For any (1,k) of lower height, k < (m−1)α+1, and 1/(mα+1) < α/(α+k) ⇔ k < α²m, which follows because α²m − ((m−1)α+1) = (αm+1)(α−1) > 0. Mixed states of lower height are dominated (Step 1) by ladder states that are themselves beaten. For rational α, if (m,1) shares a height u with another state, its ε = 1/u is strictly minimal in the height class (any other state at that height has min(m′α, k′) > 1), so ties never disqualify a rung.

*Step 3 — the exceptional condition.* The state (1, 2n+1) beats all earlier (1,k′) automatically (ε strictly decreasing along the ladder), and mixed states reduce to ladder comparisons, so the binding competitor is the most recent main rung below it: (2j+1, 1) with (2j+1)α+1 < α+2n+1 ⇔ jα < n ⇔ **j = ⌊n/α⌋** (this is the role of j: it indexes the last main-ladder record already set when (1,2n+1) arrives; when jα = n exactly, the two heights tie and the main rung wins strictly since 1/u < α/u, so the strict inequality in S(α) is correct there too). The record condition is α/(α+2n+1) < 1/((2j+1)α+1), which rearranges exactly to α²(2j+1) < 2n+1. The interrupted code's candidate formula is therefore **correct**, derived rather than replaced.

*Step 4 — finiteness and bound.* Since ⌊n/α⌋ > n/α − 1, membership forces α²(2n/α − 1) < 2n+1, i.e.

  **n < (1+α²) / (2(α−1)).**

This is the practical exact upper bound for max S(α); it is finite for every α > 1 and diverges as α ↓ 1. (Machine check: satisfied in all 14 test values.)

## 4. Exact exceptional-set formula

S(α) = { n ≥ 1 : α²(2⌊n/α⌋+1) < 2n+1 }, with strict inequality, and S(α) ⊂ [1, (1+α²)/(2(α−1))). The formula was validated by exact brute-force record scans (Fraction/ℚ(√d) arithmetic, exact tie handling) at α = √2, √3, φ, 2, 5/2, 3, 11/10, 21/20, 173/100, 174/100, 129/100, 130/100, 199/100, 201/100 — perfect agreement in every case, including all rational-α tie situations.

## 5. Boundary thresholds and examples

S(α) changes exactly at two families of α: the quadratic surds **α = √((2n+1)/(2j+1))** where the defining inequality changes sign (with j = ⌊n/α⌋ consistent on the relevant side), and the rationals **α = n/j** where the floor jumps. Computed exceptional sets:

| range / value | S(α) | verification |
|---|---|---|
| α ↓ 1 | {1, 2, …, N(α)}, N(α) ~ 1/(α−1); e.g. S(21/20) = {1,…,10}, S(11/10) = {1,…,5} | exact scan |
| α = √2 | {1} | exact scan |
| α = φ | {1} | exact scan |
| α = √(5/3) ≈ 1.2910 | threshold for n = 2 (j = 1): S(129/100) = {1,2}, S(130/100) = {1} | exact scan |
| α = √3 | threshold for n = 1: S(173/100) = {1}, S(√3) = S(174/100) = ∅ | exact scan |
| α ∈ [√3, 2] | ∅ | exact scan at √3, 199/100, 2 |
| **α ∈ (2, √5)** | **{2}** (j = 0 window; the floor jump at α = 2 re-opens the condition α² < 5) | exact scan at 201/100 |
| α ≥ √5 | ∅ (n with j = 0 requires n < α < √(2n+1), forcing n ≤ 2) | exact scan at 5/2, 3 |

The (2, √5) window is the substantive correction to the earlier simplified claim: S(α) is **not** always an initial interval and is **not** empty for all α > √3.

## 6. Boundary counting and envelope

Records up to height h are essentially the odd m with (mα+1)/2 ≤ h, plus |S(α)| exceptional states, giving **N_edge(h) = h/α + O_α(1)**, dimensionally N_edge(H) = H/(ħω₁) + O_α(1). Consecutive record heights differ by α (consecutive odd m), so h_{j+1}/h_j → 1. On the ladder h·ε_edge = 1/2 exactly; since the running minimum at height h is the last rung's ε = 1/(2h_rec) with h − h_rec = O(α), the envelope h·min_{h(T)≤h} ε_edge(T) → 1/2, i.e. **H·min ε_edge → ½ ħω₂**.

## 7. √2 norm-form analysis

For odd m,k: k² ≡ 1 (mod 8) and 2m² ≡ 2 (mod 16), so **Q = k² − 2m² ≡ 7 (mod 8)** (machine-verified on a grid; two-line proof). Consequently Q ∈ {…, −17, −9, −1, 7, 15, 23, …}: the branches Q = +1 and Q = −7 are impossible, so |Q| = 1 occurs only as Q = −1 and |Q| = 7 only as Q = +7. **Congruence exclusion mod 3:** if 3 | Q then k² ≡ 2m² (mod 3), which forces 3 | m and 3 | k (2 is a non-residue mod 3), contradicting coprimality — so **no primitive pair has |Q| = 9 or 15** (machine check: zero primitive pairs with 3 | Q below 400). The smallest primitive values are |Q| = 1, 7, 17 (at (3,1)), 23 (at (1,5)), and |Q| = 25 is likewise impossible primitively because 5 is inert in ℤ[√2].

## 8. Orbit classification

A = [[3,2],[4,3]] acts on u = m√2 + k as multiplication by λ = 3+2√2 = (1+√2)², and Q(A(m,k)) = Q(m,k) by direct expansion (machine-verified). By the unit-group structure of ℤ[√2] (fundamental unit ω = 1+√2, norm −1): all positive solutions of Q = −1 are u = ω^{2j+1}, a **single A-orbit** P_j = (1,1), (5,7), (29,41), … — parity odd/odd and coprimality automatic. The prime 7 splits (3² ≡ 2 mod 7), so norm-7 elements are associates of 3±√2, and the positive odd solutions of Q = +7 form **exactly two A-orbits**: T_j starting at (m,k) = (1,3) with u = (3+√2)λ^j, and S_j starting at (3,5) with u = (5+3√2)λ^j (since (3−√2)ω² = 5+3√2). All norm-7 solutions have m,k odd automatically (mod-8 argument). This corrects and completes the "two candidate orbits" picture: there are three orbits on the two feasible branches, of which T never records (§10).

## 9. Orbit interlacing

Exact closed forms: u(P_j) = (1+√2)λ^j, u(S_j) = (5+3√2)λ^j, u(T_j) = (3+√2)λ^j. The exact identities (1+√2)(1+2√2) = 5+3√2 and (5+3√2)(5+4√2) = 7λ(1+√2) (both machine-verified in ℤ[√2]) give

  h(S_j)/h(P_j) = **1+2√2** ≈ 3.828,  h(P_{j+1})/h(S_j) = **(5+4√2)/7** ≈ 1.522,  h(T_j)/h(P_j) = 2√2−1 ≈ 1.828,

so P_j < T_j < S_j < P_{j+1} strictly for **all j ≥ 0** (no index shift needed), and both subsequences grow geometrically with multiplier exactly λ = 3+2√2.

## 10. Record-completeness theorem — PROVED

**Theorem.** Every strict chronological balance record for α = √2 is in the merged sequence P₀, S₀, P₁, S₁, … and the signed defects alternate −1, +7, −1, +7, ….

*Proof sketch (route 2 + 4 of the proposed list: unit-group classification plus direct gap comparison).* An interloper at height h in the gap (h(P_j), h(S_j)) must satisfy |Q|/(4h²) < 1/(4h(P_j)²), i.e. h > √|Q|·h(P_j). For |Q| ≥ 15 this exceeds (1+2√2)h(P_j) = h(S_j) because **15 > 9+4√2** (exact: 36 > 32) — impossible. |Q| = 9 has no primitive solutions (mod 3). |Q| = 7 interlopers in this gap are exactly the T-orbit at ratio 2√2−1, and **(2√2−1)² = 9−4√2 < 7** (exact: 4 < 32), so T_j never beats P_j. In the gap (h(S_j), h(P_{j+1})) an interloper needs h > √(|Q|/7)·h(S_j); for |Q| ≥ 17 this exceeds ((5+4√2)/7)h(S_j) = h(P_{j+1}) because **7·17 = 119 > 57+40√2** (exact: 3844 > 3200) — impossible; |Q| ∈ {9, 15} are non-primitive (mod 3), and there are no further norm-1 or norm-7 solutions besides the classified orbits. Each merged element strictly improves the running minimum (ratios (9+4√2)/7 > 1 and (57+40√2)/7 > 1), so all are records; P₀ = (1,1) is the lowest state overall. ∎

The critical boxed question — can every primitive odd pair with |2m² − k²| ≥ 9 be proved unable to create a new record? — is answered **yes**: |Q| = 9, 15 by the mod-3 congruence, |Q| ≥ 17 by the exact gap inequalities, with the load-bearing margins 15 vs 9+4√2 ≈ 14.657 and 119 vs 57+40√2 ≈ 113.569 both strict but slim. This is a complete proof; completeness is not inferred from computation. Computation independently confirms it: an exact pruned scan (justified by the record bound |Q| < 17, run with margin |Q| ≤ 60) to m ≤ 2×10⁶ (h up to ≈ 1.6×10⁶, 17 records) matches the merged orbit exactly, defects −1,+7 alternating, and a full unpruned brute force over all 14,141 odd pairs (including imprimitive) with u ≤ 400 agrees state-for-state.

## 11. Exact record counting

Records come two per factor of λ in height, so N_bal(h) = **2·log(2h/(1+√2)) / log(3+2√2)** + O(1). The coefficient is **2/log(3+2√2)**, confirming the correction from the earlier incorrect 3/log λ. (Scan: N = 17 at h ≈ 1.6×10⁶ vs predicted 18.0 — consistent with the O(1) term.)

## 12. Exact envelope constants

With E_bal(H) = H²·min_{h(T)≤H} ε_bal(T) and ε(P_j) = (3−2√2)λ^{−2j} exactly, ε(S_j) = ((43−30√2)/7)λ^{−2j} exactly:

liminf E_bal = **1/4** (attained at H = h(P_j); the S-records give the larger value 7/4). The supremum on each cycle is approached just below the next record: h(S_j)²ε(P_j) = (9+4√2)/4 ≈ 3.6642 and h(P_{j+1})²ε(S_j) = **(57+40√2)/28** ≈ 4.0560, so limsup E_bal = **(57+40√2)/28** — the interrupted computation's value, now **derived from the proven interlacing** rather than assumed. Multiplicative envelope-oscillation ratio: limsup/liminf = (57+40√2)/7. Record improvement ratios (exact identities, machine-verified): ε(P_j)/ε(S_j) = **(9+4√2)/7** ≈ 2.0938 and ε(S_j)/ε(P_{j+1}) = **(57+40√2)/7** ≈ 16.2241, whose product is λ² as required. The scaled envelope is exactly periodic in log H with period log λ from the first cycle onward — eventually periodic, in fact immediately periodic for j ≥ 0.

## 13. First 30 strict records

Delivered in `records_sqrt2_first30.csv` with exact columns j, (m,k), (n₁,n₂), Q, h = (m√2+k)/2 in exact form plus 18-digit decimal, ε in the exact rationalized form ε = (2m²+k² − 2mk√2)/|Q| (an identity, since u²·ū² = Q²), and the alternating exact ratios h_{j+1}/h_j ∈ {1+2√2, (5+4√2)/7}, ε_j/ε_{j+1} ∈ {(9+4√2)/7, (57+40√2)/7}. First rows: (1,1), (3,5), (5,7), (19,27), (29,41), (111,157), (169,239), (647,915), …

## 14. Corrections to all earlier claims

The defect pattern is 1,7,1,7,… (signed: −1,+7,…), not 1,9,7; norm-9 records are impossible outright (no primitive solutions), so the earlier norm-9 entries were necessarily ties or imprimitive repetitions. The orbit picture needs a third orbit: T_j = (1,3)·A^j has norm 7 but never records. The earlier simplified boundary exceptional-set claim is replaced by the derived S(α), whose structure near α = 1 is a long initial interval but which also contains the isolated window S(α) = {2} for α ∈ (2, √5) — so "S empty for α large" must be stated as α ≥ √5 (or α ∈ [√3, 2]). The record-count coefficient is 2/log λ, not 3/log λ. The limsup (57+40√2)/28 survives audit; the competing per-cycle peak (9+4√2)/4 is strictly smaller.

## 15. Reproducibility package — status

Delivered now: `audit.py` (single-file exact-arithmetic source; exact ℚ(√d) sign tests for every ordering and every ε comparison; float presort keys verified pairwise in exact arithmetic; strict-record tie handling per definition; embedded assertion-style unit tests covering height ordering, error comparison, tie exclusion, primitivity/scaling, matrix preservation of Q, and the exceptional-set formula across 14 α values), `records_sqrt2_first30.csv`, this report, `README.md` with software versions, and `SHA256SUMS`. All outputs above were produced by the run shown; nothing is claimed that was not executed. Remaining packaging work before deposit: split the embedded assertions into a pytest suite, emit the boundary-scan CSVs per α, and extend the orbit-generated validation table beyond the pruned-scan range (trivial via the closed forms, worth including for completeness).

## 16. Paper-readiness decision

**Ready.** Both standards are met: the boundary exceptional set is stated and proved exactly (§2–4), and the √2 strict-record chronology is fully proved (§10), not merely a finite computational theorem. The note can be drafted on request as: (i) boundary theorem with S(α), threshold catalogue including the (2,√5) window, counting, and ½ħω₂ envelope; (ii) interior theorem with the three-orbit classification, four exact gap inequalities, two congruence lemmas, counting coefficient 2/log(3+2√2), and envelope constants 1/4 and (57+40√2)/28; (iii) reproducibility appendix. Open items are presentational only: pytest packaging, per-α CSV emission, and a written-out (rather than sketched) unit-group classification lemma with full case bookkeeping.
