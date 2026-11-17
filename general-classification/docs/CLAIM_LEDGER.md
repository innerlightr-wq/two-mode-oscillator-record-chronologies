# Claim ledger

Every substantive statement in `main.pdf`, where it is proved, what computational support exists,
and what remains open. "Checked" means a check in `archive/scripts/check.py` re-derives it from
the definitions on all 26 archived certificates; "run here" means I executed it and the log is in
`archive/results/`.

---

## Proved statements

| # | statement | location | computational support | limitation |
|---|---|---|---|---|
| 1 | Basic identities: `H = G/(A²ηδ)`, `ε = |Q|√Δ/|G|`, `Q = H²z(Aδ − Bz)/(2α)`, and the bound `|Q| ≤ H²ε(√Δ+|B|ε)/(2α)` | Lemma 2.1 | used by every check; C5 recomputes the cutoff from it | none |
| 2 | `H` is a strict total order on admissible states | Remark 2.3 | C5, C12 verify every sort exactly | none |
| 3 | `ε = |tanh(½ log(k/(mα)))|` | §2.1, eq. (3) | `lit_bridge.py` L1, run here (6/6) | identity only; no transfer follows |
| 4 | Every class best approximation is a strict ε-record; the inclusion can be strict | Prop. 2.4 | `lit_bridge.py` L2, run here (8/8): strict at φ, 1+√3, √2, 3x²−x−1, √6 mod 3 | compares two notions **both** ordered by `H`; no bridge to the denominator order. **Whether the inclusion is ever an equality is NOT claimed**: the √3 agreement is over a finite height range only |
| 4b | **A record need not be a vertex of its coset hull**: at `α = 2+√2`, `M = 3`, `R = {(1,1)}`, `(7,25)` is a strict record and lies strictly inside the triangle `(1,4), (31,106), (1,7)` of admissible cone points, with barycentric coordinates `3/5, 1/5, 1/5` | Prop. 2.7 | `review6_sail.py`, run here (14/14): the 42 lower states, both ε comparisons, the exact convex identity, the residues, the cone memberships, `det = 90` | refutes **only** the coset-hull reduction; no other geometric description is ruled out and no novelty follows (Remark 2.8) |
| 5 | **Main theorem**: terminating algorithm, finite output, strict records = finite part + complete forward orbits of computed seeds | Theorem 3.2 | instantiated on 26 inputs; C13 verifies the partition end to end per instance | asserts termination, not cost |
| 6 | The class-fixing automorph: `X₀` integral, `det = 1`, `Q`-invariant, `η ↦ λη`; `P = X₀^j ≡ I (mod M)` for some `j ≤ |GL₂(Z/M)|`; `P` preserves `Q`, every class, and `gcd` | Lemma 4.1 | C1, C2, C3 (checked) | `j` bounded only by `|GL₂(Z/M)|` |
| 7 | No power of the automorph is entrywise positive when `α' > 0` | Remark 4.3 | exhibited at `(3±√5)/2`, `(5+√21)/2`, `N+√2` | — |
| 8 | Positive-window trichotomy: forward tail iff `sgn(ηδ) > 0`; with `α' < 0` the alternative is finitely many positive states; with `α' > 0` a `Q < 0` orbit is positive in both directions with backward `ε → |δ|/(α+α')` | Lemma 5.1 | C7 verifies the `fwd` flag and the windows (checked) | — |
| 9 | A comparison family exists unconditionally; no prescribed or minimal defect is needed | Lemma 5.2 | C4 (checked) | a small defect only improves the constant |
| 10 | **Cutoff**: `|Q_{B*}| < |Q_A|(H_C/H_A)²(1+θ_A)`, no sign hypotheses | Theorem 6.1 | C5 recomputes `B_cut` (checked); C12/C13 verify it on every brute-force record | — |
| 11 | The computable majorant, and `B_cut` as a certified bound | Lemma 6.2 | C5 (checked) | `B_cut` is **an upper bound, not the supremum** (Warning 6.3) |
| 12 | `B_cut ≥ max_A|Q_A|` over any family | Remark 6.4 | measured at φ: `18,18,18,22,22,36,30,70,…` for `D = 1,…,30` | whether some input admits a self-consistent `D` is open |
| 13 | Reduction box; splitting into `j` translates; imprimitive orbits retained | Props. 7.1, 7.2, Lemma 7.3 | C7 re-scans the box independently (checked) | no PID or class-number input used |
| 14 | `ε < √Δ/|B| ⟹ ηδ > 0 ⟹ G > 0` | Lemma 8.1 | C6 (checked) | — |
| 15 | **Blocker bound** `|Q_V| ≤ |Q_{B*}|(√Δ+|B|ε)/(√Δ−|B|ε) ≤ 3|Q_{B*}|` under `ε ≤ √Δ/(2|B|)` | Lemma 8.2 | C6 (checked); measured `B_comp/B_cut ∈ [1.00, 2.33]` | the uniform `3B_cut` is crude; the per-candidate value is used |
| 16 | Error monotonicity **with its branch**: decreasing on `G>0`, increasing on `G<0` where `ε ≥ √Δ/|B|` | Lemma 9.1 | `review3.py` R2, run here | the unconditional form is **false** (Warning 9.2) |
| 17 | **Backward exclusion, two cases**: the `G<0` floor, and the `Y ≤ Y*` level cutoff on doubly-infinite orbits | Lemma 9.3 | C6b, both cases, on 255 case-(i) and 788 case-(ii) orbits (checked) | the single-floor version is **false** (Warning 9.4) |
| 18 | **Cutoff level** `L*` with witnesses `Y_{L*} ≤ Y* < Y_{L*+1}`, and termination of the two-sided search | Lemma 9.5 | C6b recomputes `L*` and both witnesses (checked); measured `L* ∈ {−1,0,1}` | — |
| 19 | `Y* ≥ Y_min` when `BQ > 0`, so the height is strictly increasing on the retained region | Lemma 9.6 | C6b (checked) | the attained `ε_w` gives margin but is **not required** (Remark 9.7) |
| 20 | **Error comparison** `ε_B < ε_A ⟺ 2αA²Γ > B(|Q_B|Q_A − |Q_A|Q_B)`, with `Γ = ρ^{2(p−d)}Γ_d` and an explicit threshold; `Γ_d = 0` gives a three-way constant, and `B = 0` an exact permanent equality | Lemma 10.1 | C8 recomputes every ledger row (checked); `review3.py` R1 pins the sign | the opposite sign is **false** (Warning 10.2) |
| 21 | **Height comparison** `sgn(H_B − H_A) = sgn(ρ^{2q}U + V)` with the `|δ|` clearing factor | Lemma 10.3 | C8 (checked); `review3.py` R3 and `review5.py` pin the exponent and the sign | `ρ^q` and a `δ`-signed factor are both **false** (Warning 10.4) |
| 22 | **Upper offset endpoint** `d ≤ d*` with `p_noblock` | Lemma 11.1 | C9 recomputes both (checked); measured `d* ∈ {2,3}` | — |
| 23 | **Lower offset endpoint** `d ≥ 0` from the `d = 1` height rows | Lemma 11.2 | C9 verifies the rows exist with the right verdict (checked); `review5.py` P4 | — |
| 24 | **Binding-state sufficiency** | Lemma 12.1 | C9 compares the ε-minimal verdict against exhaustive scans (checked); `review5.py` P1, P1b (976 sampled candidates) | the exclusion form is **false** (Warning 12.2) |
| 25 | **Exhaustive disjoint partition** into `P1, P2a, P2b, P3, P4, P5, P6` | Prop. 13.1 | C13 verifies exhaustiveness and each part's property per instance (checked) | verified on a bounded population per instance, not symbolically |
| 26 | `P1` and `P5` completeness by independent enumeration and set equality | Remark 13.2 | C14(a), C14(b) (checked) | — |
| 27 | **Termination** of every search | Prop. 13.3 | all runs terminated | no cost bound |
| 28 | Exact ordering with a guaranteed exact-comparator fallback | Remark 13.4 | C5, C12, including a forced key failure; `review4.py` O2 | — |
| 29 | `H²ε → 2α|Q|/√Δ` along a fixed-defect orbit | §17, extension question 6 | arithmetic consequence of Lemma 2.1 | values **at** records, not the envelope between them |

## Instantiations (computational, not part of the proof)

| # | statement | support |
|---|---|---|
| 30 | The worked example at `φ` odd/odd reproduces the published classification: three record tails of defects `−1, +1, −5`, merged cycle, plus the imprimitive permanent tie `3·(1,1)` | `archive/certificates/control_phi.json`; agrees with doi:10.5281/zenodo.24046651 |
| 31 | The three published control classifications (`φ`, `1+√3`, `√3`) are reproduced | certificates + `qr_general.py`, run here |
| 32 | Imprimitive records occur: `(4,10)` at `√6`, `(1,1) mod 3` (gcd 2, defect 4), generating a permanent record tail; 4 such tails there, 2 at `√3` with `R = {(1,1),(2,3)} mod 5`, 2 at `√2` `(1,1) mod 3`, and all 6 at `√6` `(2,2) mod 4` | certificates, re-verified by C7/C10 |
| 33 | Over the 26 instances: `p_cert ∈ {2,3}`, `d* ∈ {2,3}`, `L* ∈ {−1,0,1}`, blocking offsets `{0,1}`, all `P5` exception lists empty | certificates + C6b, C9, C14 |

## Open obligations and limitations

1. **No cost bound.** Termination is proved; running time is not bounded. The dominant cost grows with `ρ = λ^j`, `j ≤ |GL₂(Z/M)|`. No closed form for `d*` uniform in the input is written out (it is computed per instance and re-derived by the checker).
2. **`B_cut` is an upper bound**, not the supremum of the cutoff functional.
3. **`P1` is scanned**, not resolved by the orbit machinery; legitimate for effectiveness, and small in every instance tested, but a scan.
4. **Weak records.** Only strict records are classified. Ties are detected and the certified tie families are genuine infinite families of weak records; a full weak-record classification, in particular of imprimitive ones, is not claimed.
5. **No formal verification.** Nothing is machine-checked in a proof assistant; nothing is refereed.
6. **Novelty unsettled.** Targeted searches found no matching treatment, which is not evidence. A prior treatment is plausible and has not been excluded. The note now separates (a) *all sufficiently late records lie in finitely many automorph orbits* — classical reduction theory, claimed by no one here — from (b) *which tails are records, at which level, with a completeness certificate*, and labels effectiveness, generality and certificate completeness the **proposed** contribution pending a fuller literature comparison. The nearest works consulted (Kushwaha–Sarma; Han–Lee; Spalding–Veselov) are distinguished individually in §17, item 6.
7. **`H`-order versus denominator order.** No bridge is established; nothing here is a statement about best 1-rational approximations in the sense of Kim–Lee–Liao.
8. **`R` is a union of cosets**, a sublattice only when it is a subgroup containing `(0,0)`; the Klein-sail picture applies coset by coset at best, and Prop. 2.7 rules out the coset-hull reduction outright. Whether some *other* geometric description of the record set exists is open.
9. **Prop. 13.1 is verified on a bounded population** per instance by C13; the disjointness and exhaustiveness argument itself is the symbolic part.
10. **Equality in Prop. 2.4 is open.** The inclusion is proved and its strictness is witnessed; whether the two sets ever coincide as infinite sets is not decided. The agreement at √3 odd/odd holds over a finite range of heights only and is an observation, not a theorem (Rem. 2.5).
