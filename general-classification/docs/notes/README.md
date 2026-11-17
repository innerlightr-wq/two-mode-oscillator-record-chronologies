# Quadratic relative-error records: the general effective theorem (internal, 16 Nov 2026)

**Internal research only.** Nothing here is published, deposited, pushed or committed. The
repository `two-mode-oscillator-record-chronologies` was read at commit `b8f207d` and is
byte-unchanged; see `sources/SOURCE_AUDIT.txt` for the exact files and hashes examined.

## Deliverables
| file | content |
|---|---|
| `THEOREM_AND_PROOF.md` | the strongest fully proved statement, all stages, constants, cost, and the new-vs-implicit ledger |
| `GAPS_AND_COUNTEREXAMPLES.md` | failed stronger formulations, the seven defects produced and fixed here, remaining obligations |
| `LITERATURE_MAP.md` | classical / corollary / new-effective / unproved, with sources |
| `scripts/gq.py` | independent exact arithmetic and the general machinery (shares no code with the published certificate) |
| `scripts/qr_general.py` | the full certified algorithm on 3 regression controls + 11 stress cases — **98/98 checks** |
| `scripts/lit_bridge.py` | the two bridges to classical best approximation — **14/14 checks** |
| `PARTITION_AND_CHECK_MAP.md` | the exhaustive partition and the proof ↔ certificate ↔ checker cross-walk |
| `scripts/emit.py` | writes one self-contained JSON certificate per instance into `certificates/` — 26 instances, including the `α_N = N+√2` near-equal-positive-conjugate stress family |
| `scripts/check.py` | **independent certificate checker**: its own arithmetic, no classifier routines, no use of the blocker lemma. Its first run failed C9 on all 26 certificates and located the offset gap |
| `certificates/*.json` | the 26 certificates, each carrying the Pell solution, automorph, family, cutoff, orbit list, `d*`/`p_noblock`/`p_cert`, the per-pair threshold ledger, and the record tails / ties / initial exceptions |
| `scripts/run_all.py` | an earlier, superseded pass; its two failures located defects D-2 and D-3 |
| `results/*.log` | complete logs |

## One-line verdict
The universal effective classification **holds**: every stage generalises to an arbitrary real
quadratic irrational `α > 0` given by an arbitrary primitive integral quadratic (any `A > 0`,
either root, `α'` of either sign, `α` ≷ 1), an arbitrary modulus `M`, an arbitrary nonempty
`R ⊆ (Z/M)²`, and no coprimality — and the result is a complete classification with a certified
cutoff, not merely a finite candidate reduction. The limitation is cost, not scope.

## Corrections made after the first proof-level review
1. **The `d ≤ 1` offset window is FALSE when `α' > 0`** (U-shaped heights), so `p_cert` as first
   computed certified the wrong offsets. The classifier's verdicts were never affected — it
   scans whole positive windows — but the persistence claim was uncertified there. Closed by
   bounding *blocking* rather than *binding* offsets: `d*` = least `d` with `ρ^{2d−2} > B_comp`,
   plus a level threshold `p_noblock`. Over 26 instances `d* ∈ {2,3}`, `p_cert ∈ {2,3,4}`, and
   the observed blocking offsets are `⊆ {0,1}` while binding offsets reach `10`.
2. **The claim that self-consistency (`B_cut ≤ D`) is unattainable is WITHDRAWN.** Only
   `B_cut ≥ max_family|Q|` is proved; the search ceiling need not equal the largest realised
   defect. Narrowed to: it failed at every `D` in every instance tested.
3. **A prose error corrected:** scaling by `3` leaves `ε` fixed and triples `H`, so the
   *unscaled* pair is the lower-height blocker. The underlying tests were right.
4. **The blocker-pruning fallback is the normal path**, firing in 10 556 of 13 088 verdict
   calls (81%), not an untested corner.

## Note on the logs
`results/sweepA.log` and `results/sweepB.log` are **superseded exploratory sweeps**, kept
because their failures are findings, not noise: `sweepA` shows the cutoff stage aborting at
both `α' > 0` instances (defect D-5), and both show the single-orbit-ladder cutoff blowing up
to `7·10⁸` at `√6 mod 3` — the infeasibility that the bounded-defect **family** construction
of Lemma 3.2 reduces to `135`. The final results are `qr_general.log` and `lit_bridge.log`,
both with zero failures and exit 0.

## Independent audit result
`scripts/check.py` over `certificates/`: **1577/1577 checks passed, 0 failures over all 26
certificates** (`results/check_v5.log`), including the **9 mandatory regressions** for the
counterexamples of the third review, the `L*` witness checks of Lemma 6.0c, and the end-to-end
partition check **C13**. Classifier side: `qr_general` 98/98, `lit_bridge` 14/14,
`review3` 25/25, `review4` 13/13.

## Corrections made after the sixth review
1. **One binding assertion was FALSE and is replaced by a sufficiency lemma.** The sentence "a
   state below the binding level has larger ε and cannot block" fails: at `α = φ`, unrestricted,
   `b = (15,24) = 3·(5,8)` is blocked by `(5,8)`, which lies **below** the ε-minimal state
   `(13,21)`. The correct and sufficient statement (Lemma 6.6b) is: if any state of an orbit
   blocks, the ε-minimal state below `H_B` blocks too, so the three-way verdict read off that
   state equals an exhaustive scan. That is what the implementation already did, and check C9 now
   tests the sufficiency statement rather than the false exclusion.
2. **One level convention.** Stored period = absolute η-level (no offset). The tail-start level
   is `T_i = enter_i + p_cert`, certified `T_i > L*_i`, and the partition is `P4: L ≤ L*_i`,
   `P5: L*_i < L < T_i`, `P6: L ≥ T_i`. The finite region is `H ≤ H(w)`, not `H(A₁)`.
   P3/P4 now conclude `ε ≥ ε(w)` (the earlier `ε₀ > ε(w)` was vacuous since `ε₀ = ε(w)`).
3. **Completeness of the exception list, not just correctness.** This caught a real category
   error: the emitter had been listing P1 and P4 states as "initial exceptions". The exception
   list is now exactly the P5 anomalies, the certificate also carries the P1 record set, and
   check **C14** verifies both by independent enumeration and **set equality** — P1 from the
   explicit bounds `1 ≤ m ≤ ⌊H(w)/α⌋`, `1 ≤ k ≤ ⌊H(w)⌋`, and P5 from the levels
   `L*_i < L < T_i` on each candidate orbit.
4. **The offset ledger is complete at both ends.** `d ≤ d*` from the no-block bound, and
   `d ≥ 0` because a competitor one level later lies above the candidate in height — certified by
   the `(candidate, competitor)` `d = 1` height rows, which the ledger now carries. The obsolete
   `d ≤ 1` formula is gone from §7.
5. **Lemma 6.3's clearing factor** must use `|dd|` and `|η|`: `dd = α − α' < 0` for the smaller
   root, while `η·dd > 0` on the retained branch.

## Corrections made after the fifth review
1. **The adaptive-window obligation is CLOSED analytically** (Lemma 6.0c). `Y_L = A²r²ρ^{2L}` is
   strictly increasing with `Y_L → 0` and `→ ∞` at the two ends and `Y*` finite positive, so a
   two-sided expanding exact search finds the unique `L*` with `Y_{L*} ≤ Y* < Y_{L*+1}`; those
   two inequalities are the certificate, monotonicity does the rest, and the finite orbit list
   makes every search terminate. Measured `L* ∈ {−1,0,1}` over 788 case-(ii) orbits.
2. **Two over-statements inside the previous repair, corrected.** `Y* > Y_min` is *not*
   necessary — the retained condition `Y > Y*` already gives `Y > Y_min` even at the boundary;
   and "maximise ε below the bound" now names the explicit finite candidate family it ranges
   over, with the note that any computable `w` below the threshold suffices for the theorem.
3. **`PARTITION_AND_CHECK_MAP.md`** is new: the exhaustive seven-part partition of the
   admissible states, the obligation attached to each part, and a twenty-row cross-walk from
   each obligation to its lemma, its certificate fields and its checker check — the audit the
   review asked for. Check **C13** verifies the partition end to end per instance; on
   `(3+√5)/2` odd/odd it classifies 7639 states as `P1=2, P2a=7599, P2b=9, P3=7, P4=11, P5=11,
   P6=0` and confirms the brute-force record set is exactly `(P1 records) + (certified tails) +
   (declared initial exceptions)`, with nothing unexplained.

## Corrections made after the fourth review
1. **The backward-ray exclusion needed two cases.** The floor `ε ≥ √Δ/|B|` covers only the
   `G < 0` branch. A doubly-infinite orbit has `G > 0` throughout and its backward ray
   approaches `√Δ/|B|` *from below* — witness `P^{-1}(1,1) = (13,5)` at `α = (3+√5)/2`, with
   `G = 3.006211 > 0` and `ε = 0.743816 < √5/3 = 0.745356`. Case (ii) now uses the explicit
   level cutoff `Y ≤ Y* = (|Q|√Δ/ε₀ − BQ)/(2α)`. A further subtlety found by the test: `Y*`
   exceeds the height minimum `Y_min` **strictly** only for the *attained* `ε(w)`; using the
   bound itself gives equality and loses the monotonicity that Lemmas 6.3/6.5/6.6 need there.
   Both cases are certified per orbit (255 case-(i) and 788 case-(ii) orbits) and re-verified
   independently as check C6b.
2. **Approximate sorting now has a guaranteed exact fallback.** `sort_heights` presorts with an
   approximate key, verifies all adjacent pairs exactly, and re-sorts with the exact algebraic
   comparator whenever key generation or verification fails — so termination with a correct
   order is established for every input, not merely protection against a wrong one. The
   fallback path is exercised directly (forced key failure, constant key) in both
   implementations.

Measured over the 26 instances after these repairs: `p_cert ∈ {2,3}`, `d* ∈ {2,3}`, the
`ε₀` level cutoff sits at level `0`, `1` or `2` (so the stored window is ample),
`B_comp/B_cut ∈ [1.00, 2.33]`, blocking offsets `{0,1}`, and binding offsets `{0,1}` on the
`G > 0` branch.

## Corrections made after the third (proof-level) review
Three displayed lemmas were wrong; all three were confirmed by exact counterexample and
repaired. Details in `THEOREM_AND_PROOF.md` §§6.0–6.3 and `GAPS_AND_COUNTEREXAMPLES.md` S-7.

| | claim | effect on the implementation |
|---|---|---|
| R1 | Lemma 6.2's right-hand side had the **sign reversed** (`φ`, `(1,1)` vs `(1,3)`, `Γ=0`) | none on any verdict; the emitted ledger's `Γ_d=0` label was inverted and is fixed |
| R2 | Lemma 6.1 is **false on the `G<0` branch** (`(3+√5)/2`, `P(55,21)=(3,1)`, ε rises) | the binding rule depended on it; `verdict` now takes the **ε-minimal** competitor |
| R3 | Lemma 6.3's exponent is **`ρ^{2q}`**, not `ρ^q` (`2+√2`, `q=1`) | the old threshold was conservative, so `p_cert` stayed valid; now tighter |

Adopted from the review: the **`ε₀` starting threshold** `ε₀ = min(1, √Δ/(2|B|))`. It puts the
whole tail analysis on the `G>0` branch, makes Lemma 5.4's blocker bound **never vacuous**
(it previously fell back in 81% of calls), and licenses `B_comp ≤ 3B_cut`.

Also withdrawn: my claim that binding offsets are unbounded. Measured over 26 instances the
binding offsets are `{0,…,6}` unrestricted but **exactly `{0,1}` on the `G>0` branch** — the
window lemma holds on the branch the theorem uses, and my refutation measured the excluded one.
And S-1 no longer claims to refute the "complete forward orbits" formulation: a tail starting at
level `p₀` *is* a complete forward orbit of the seed `P^{p₀}v`.

Nothing in the audit relies on the classifier: separate arithmetic, separate decision routines,
independent re-scan of the reduction box, and no use of the blocker-pruning lemma.

## Logs
Current: `emit4.log` (certificate generation), `check4.log` (independent audit, 1324/1324),
`qr_general2.log` (98/98), `lit_bridge.log` (14/14), `review3.log` (25/25 — the three
counterexamples adjudicated). Earlier runs are in `results/superseded/` and are kept only
because their failures are findings: `check_final.log` is the audit that failed C9 on all 26
certificates and located the offset gap; `check3.log` is a run aborted by a checker-side
ordering bug and then by stale `C8`/`C9` expectations after the ledger was restricted to
(competitor, candidate) pairs; `sweepA/B.log` show the single-ladder cutoff blowing up to
`7·10⁸` at `√6 mod 3`.
