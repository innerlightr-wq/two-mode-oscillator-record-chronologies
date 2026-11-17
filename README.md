# Record chronologies for odd/odd Diophantine approximation

This repository holds **three notes** and their reproducibility material.

| | note | status |
|---|---|---|
| **1** | *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum* (2026-08) | deposited, doi:[10.5281/zenodo.21796640](https://doi.org/10.5281/zenodo.21796640) |
| **2** | *Odd/Odd Records for a Relative Approximation Error: Three Quadratic Classifications and an Exact Certificate* (2026-11) | deposited 2026-11-08, doi:[10.5281/zenodo.24046651](https://doi.org/10.5281/zenodo.24046651), in [`congruence-records/`](congruence-records/) |
| **3** | *An Effective Classification of Congruence-Restricted Quadratic Relative-Error Records* (2026-11) | deposited 2026-11-17, doi:[10.5281/zenodo.24297228](https://doi.org/10.5281/zenodo.24297228), in [`general-classification/`](general-classification/) |

Note 3 **generalises** note 2: the same relative error and the same weighted height, but for an
arbitrary real quadratic `alpha > 0` given by any primitive integral `Ax^2+Bx+C`, either root,
either sign of the conjugate, `alpha` above or below 1, and an arbitrary nonempty set of
residue classes modulo any `M` — with no coprimality on the pairs, so imprimitive records are
admitted and do occur. All five hypotheses note 2 worked under are removed. Note 2's three
theorems remain true and are reproduced there as controls; note 3 neither corrects nor
supersedes them.

Note 2 is a companion to note 1: it **proves** note 1's two open completeness conjectures
(Conjectures 5.11 and 5.13), **derives** the norm cutoff that note 1 assumed, adds a third
slope `alpha = sqrt(3)`, and **corrects** note 1's claim that the record height scales exactly
by the fundamental unit. Note 1 is left byte-identical as the published version; what has
changed about its claims is recorded in
[`congruence-records/docs/EARLIER_NOTE_STATUS.md`](congruence-records/docs/EARLIER_NOTE_STATUS.md).

Everything below, until the companion section, describes **note 1**.

---

## Note 1 (2026-08)

Reproducibility companion for the note:

> E. De Jesús, *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum*, 2026.  
> Zenodo DOI: **[10.5281/zenodo.21796640](https://doi.org/10.5281/zenodo.21796640)** · ORCID: [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143)

The note studies chronological record minima on the exact spectrum of an uncoupled
two-mode harmonic oscillator, `E = ħω₁(n₁+½) + ħω₂(n₂+½)`, `α = ω₁/ω₂ > 1`.
Writing `m = 2n₁+1`, `k = 2n₂+1` (both odd) and `h = (mα+k)/2`, each level carries a
binary energy partition, and two observables are tracked as states are ordered by
height: the **balance error** `ε_bal = |mα−k|/(mα+k)` and the **boundary error**
`ε_edge = min(mα,k)/(mα+k)`. The emphasis is entirely mathematical; no physical
claims are made.

Methodological predecessors (record definition, gap-versus-ladder method,
envelope comparison):

- Record density on the quarter circle — doi:[10.5281/zenodo.21762285](https://doi.org/10.5281/zenodo.21762285)
- The Pell spine as an optimal rational separator — doi:[10.5281/zenodo.21674959](https://doi.org/10.5281/zenodo.21674959)
- Pell-spine extremality on the binary majorization order — doi:[10.5281/zenodo.21678483](https://doi.org/10.5281/zenodo.21678483)

## Main results

**Proved.**

1. **Boundary record theorem** (every `α > 1`). The records of `ε_edge` are exactly the
   ladder `(m,1)` together with the exceptional states `(1, 2n+1)` for `n` in

   ```
   S(α) = { n ≥ 1 : α²(2⌊n/α⌋+1) < 2n+1 },   max S(α) < (1+α²) / (2(α−1)).
   ```

   No mixed state (`n₁ ≥ 1` and `n₂ ≥ 1`) ever records. On the ladder `h·ε_edge = 1/2`
   exactly; counting is `N(h) = h/α + O(1)`. `S(α)` is nonempty near `α = 1` **and on the
   isolated window `(2, √5)`**, where `S = {2}`; it is empty on `[√3, 2]` and `[√5, ∞)`.

2. **Interior completeness at `α = √2`.** The records of `ε_bal` are exactly the merged
   orbits `P₀, S₀, P₁, S₁, …` of `A = [[3,2],[4,3]]` seeded at `(1,1)` and `(3,5)`, with
   signed defects `Q = k²−2m²` alternating `−1, +7, −1, +7, …`. Proof inputs: `Q ≡ 7 (mod 8)`;
   `3 | Q` forces imprimitivity (kills `|Q| = 9, 15`); unit-group orbit classification
   (a third norm-7 orbit `T_j = A^j(1,3)` never records); and four exact inequalities,
   `15 > 9+4√2`, `7·17 > 57+40√2`, `(2√2−1)² < 7`. Consequences: counting coefficient
   `2/log(3+2√2)`; envelope `liminf h²ε_bal = 1/4`, `limsup = (57+40√2)/28 ≈ 4.056`,
   exactly log-periodic.

3. **Rational dichotomy.** For `α = p/q` in lowest terms: if `pq` is odd, equipartition is
   attained at `(q,p)` and the chronology terminates (`α = 5/3`: two records, ending at
   `ε_bal = 0`); if `pq` is even, an infinite minimal-numerator ladder carries all records
   with boundary-type scaling (`α = 3/2`: one record per odd `m`, `h·ε_bal = 1/4` exactly).

**Computationally verified** (exact arithmetic; labelled, never promoted to theorems).

- `α = φ`: period-3 defect cycle `(−1, +1, −5)` merging all odd Fibonacci pairs
  `(F₃ⱼ₊₁, F₃ⱼ₊₂)` with every other odd Lucas pair (`(L₆ⱼ₊₄, L₆ⱼ₊₅)`, i.e. `N = −5` side).
  The two ladders are asymptotically **tied**: records are decided by the bounded term in
  `Lₙ² − 5Fₙ² = 4(−1)ⁿ`, with relative margins shrinking geometrically. Fixed-precision
  floating point would eventually misclassify this chronology; exact arithmetic is essential.
- `α = 1+√3`: period-3 defect cycle `(−3, +1, −11)`, period `(2+√3)²` in height.
- `α = e, π`: parity-restricted convergent/semiconvergent chronologies
  (π ends at `(113, 355)`, i.e. 355/113, with `ε_bal ≈ 4.2×10⁻⁸`).

**Conjectural in the 2026-08 note — now proved.** Completeness of the φ and 1+√3
chronologies (**Conjectures 5.11 and 5.13** of `paper/oscillator_records.pdf`; the numbers
5.8/5.10 given in earlier versions of this README were wrong). Both are proved, together with
a new classification at α = √3, in the companion note described below. One assertion of the
2026-08 note is also corrected there — see [`docs/EARLIER_NOTE_STATUS.md`](docs/EARLIER_NOTE_STATUS.md).

## Note 2 (2026-11): the companion — [`congruence-records/`](congruence-records/)

> E. De Jesús, *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
> Classifications and an Exact Certificate*. Zenodo (2026).
> doi:[10.5281/zenodo.24046651](https://doi.org/10.5281/zenodo.24046651) ·
> concept DOI (all versions) [10.5281/zenodo.24046650](https://doi.org/10.5281/zenodo.24046650) ·
> release tag `congruence-records-v1.0.0`.

Start at [`congruence-records/README.md`](congruence-records/README.md). The folder is
self-contained: the note and its LaTeX source in `paper/`, the exact-arithmetic verification
programs and their captured outputs in `certificate/`, the orbit data and exclusion witnesses
in `tables/`, and the changelog, release manifest, review summary, Zenodo metadata and licence
inventory in `docs/`.

**Proved there.** The strict records of `eps_bal` are classified completely at `alpha = phi`
(odd Fibonacci pairs plus every other odd Lucas pair, defect cycle `(-1,+1,-5)`), at
`alpha = 1+sqrt(3)` (three orbits of `[[3,4],[8,11]]`, defects `-3,+1,-11`) and at
`alpha = sqrt(3)` (one orbit of `[[2,1],[3,2]]`, defect `-2`, with `h^2 eps = 1/2` exactly).
The norm cutoff assumed in note 1 for `phi` and `1+sqrt(3)` is derived: `|N| <= 18`, `204`,
`27`. At `sqrt(3)` the companion family `(m,k) -> (k,3m)` has **exactly** equal error at larger
height — weak records that are never strict.

**Not claimed there.** A uniform theorem for general quadratic slopes and congruence classes;
a classification of all weak records; novelty relative to the odd–odd continued fraction
literature. The certificate is exact arithmetic, **not** formal verification, and the note has
**not** been refereed.

## Note 3 (2026-11): the general classification — [`general-classification/`](general-classification/)

> E. De Jesús, *An Effective Classification of Congruence-Restricted Quadratic Relative-Error
> Records*. Zenodo (2026).
> doi:[10.5281/zenodo.24297228](https://doi.org/10.5281/zenodo.24297228) ·
> concept DOI (all versions) [10.5281/zenodo.24297227](https://doi.org/10.5281/zenodo.24297227) ·
> release tag `general-classification-v1.0.0`.

Start at [`general-classification/README.md`](general-classification/README.md). The folder is
self-contained: the note and its LaTeX source in `paper/`, the algorithm and the independent
checker in `scripts/`, the 26 machine-readable certificates in `certificates/`, the complete run
logs in `results/`, and the claim ledger, release manifest, Zenodo metadata, provenance and
working notes in `docs/`. `paper/main.pdf` is byte-identical to the deposited file.

**Proved there, for arbitrary admissible input.** Let `A,B,C` be coprime with `A > 0` and
`Delta = B^2-4AC > 0` nonsquare, let `alpha = (-B + s sqrt(Delta))/(2A) > 0` for either sign
`s`, fix any `M >= 1` and any nonempty `R` in `(Z/MZ)^2`, and call `(m,k)` of positive integers
admissible when `(m,k) mod M` lies in `R` — **no coprimality is imposed**. Order admissible
states by `H = m alpha + k` and measure them by `eps = |m alpha - k|/(m alpha + k)`. Then the
strict records always consist of an explicitly bounded finite region, decided directly, together
with finitely many complete forward orbits of one integral matrix `P`, each rebased at a computed
starting level — and there is a terminating exact-arithmetic algorithm that outputs this data
with an independently checkable certificate. The mechanism is the proper automorph of the
integral defect `Q = Ak^2 + Bmk + Cm^2`, which a power `P` of it preserves while fixing every
residue class mod `M`; an explicit cutoff bounds `|Q|` on records; classical reduction theory of
indefinite binary quadratic forms makes the surviving orbits finite; and finitely many exact
comparisons decide each orbit's tail.

Two phenomena absent from the monic negative-conjugate case are isolated. When the conjugate is
positive, **no** power of the automorph has non-negative entries, the positive cone is not
forward invariant, and the height is U-shaped along an orbit, so "later" does not mean "higher".
And the natural error floor `eps >= sqrt(Delta)/|B|` is **false** on the resulting
doubly-infinite orbits — their backward rays approach it from below — so the backward exclusion
splits into two cases with different certificates, one of them an explicit level cutoff.

A separate negative result (Proposition 2.7): **a strict record need not be a vertex of the
convex hull of the admissible points of its cone**, so the records cannot in general be read off
a Klein/Arnold sail. At `alpha = 2+sqrt(2)`, `M = 3`, `R = {(1,1)}`, the record `(7,25)` lies
strictly inside the triangle spanned by the admissible cone points `(1,4)`, `(31,106)`, `(1,7)`,
with barycentric coordinates `3/5, 1/5, 1/5`. That refutes this one geometric reduction and
rules out no other.

**Not claimed there.** A classification of all *weak* records; any bound on the running time;
any `alpha` of degree > 2; equality in the comparison with class best approximation; and any
bridge to the **denominator**-ordered notion of best approximation, which is a different
ordering. Effectiveness, generality and certificate completeness are stated as the *proposed*
contribution, pending a fuller literature comparison, while the classical finite-orbit input is
credited as classical. The certificates are exact arithmetic, **not** formal verification, and
the note has **not** been refereed.

**Verification.** `scripts/check.py` shares no code, no data representation and no decision
routine with the classifier, and does not use the blocker bound, so all competitor comparisons
are unpruned: **1707/1707 exact checks, 0 failures** over the 26 certificates, reproduced from
the committed tree. `emit.py` run inside the frozen bundle regenerates all 26 certificates
byte-identically. Four regression controls (`review3`–`review6_sail`, 67 checks) each pin an
exact counterexample to a statement that was wrong in an earlier draft. Per-statement support
and the ten open obligations are in
[`general-classification/docs/CLAIM_LEDGER.md`](general-classification/docs/CLAIM_LEDGER.md).

## Repository layout

```
paper/    oscillator_records.tex, oscillator_records.pdf   — the note (16 pp.)
code/     audit.py          — boundary theorem + √2 audit (all proofs' exact checks)
          chronologies.py   — φ, 1+√3, 3/2, 5/3, e, π chronologies
data/     records_sqrt2_first30.csv   — first 30 √2 records, exact algebraic forms
          chron_phi.csv, chron_1plus_sqrt3.csv
          chron_rational_3_2.csv, chron_rational_5_3.csv
          chron_e.csv, chron_pi.csv
docs/     REPORT.md         — 16-section audit status report (source of truth for note 1)
SHA256SUMS, VERSIONS.txt

congruence-records/          — note 2, self-contained
  README.md
  paper/        congruence_records_note.tex, .pdf
  certificate/  exact-arithmetic verification programs, instructions, captured outputs
  tables/       per-orbit classification and exclusion witnesses (CSV and LaTeX)
  docs/         CHANGELOG, RELEASE_MANIFEST, REVIEW_SUMMARY, ZENODO_METADATA,
                LICENSE_AND_SOURCE_INVENTORY, EARLIER_NOTE_STATUS

general-classification/      — note 3, self-contained
  README.md
  paper/        main.tex, main.pdf (22 pp., byte-identical to the deposit), references.bib
  scripts/      gq.py (exact arithmetic + the algorithm), emit.py, check.py (independent
                checker), qr_general.py, lit_bridge.py, review3/4/5.py, review6_sail.py
  certificates/ the 26 machine-readable certificates, one per instance
  results/      the complete logs of every run quoted in the note
  docs/         CLAIM_LEDGER, RELEASE_MANIFEST, ZENODO_METADATA, PROVENANCE.txt, notes/
  SHA256SUMS
```

## Reproducing everything

Requirements: **Python ≥ 3.10, standard library only** (`math`, `fractions`, `csv`,
`hashlib`, `functools`). No third-party packages.

```bash
cd code
python3 audit.py          # ~1–2 min: boundary scans at 14 α values, √2 pruned scan to m ≤ 2×10⁶,
                          #   full brute force (14,141 states), all exact identity/inequality checks
python3 chronologies.py   # ~2–4 min: φ and 1+√3 scans (brute + pruned to m ≤ 3×10⁶),
                          #   rational scans, e/π two-precision surrogate scans; writes the CSVs
```

Both scripts print every check with a pass/fail line and abort on any assertion failure.
`chronologies.py` writes its CSVs into the working directory; compare against the shipped
versions with `diff chron_phi.csv ../data/chron_phi.csv` (etc.) — they should be identical.
To verify the integrity of the shipped files, run `sha256sum -c SHA256SUMS` from the
repository root.

## Methodology (summary)

- **No float-based ordering.** Every height comparison and every ε comparison is an exact
  sign test in `ℤ[√d]` (integer pairs `A + B√d`) or in exact rational arithmetic. Floats
  appear only as presort keys; sorted order is re-verified pairwise exactly.
- **Strict chronological records.** `ε(T) < ε(T′)` for all strictly lower `T′`, `≤` at equal
  height; ties with the running minimum at larger height are excluded. Height ties (rational α)
  are handled by exact equal-height grouping.
- **Pruned scans are justified, not assumed**, for √2 (the theorem gives `|Q| < 17` on any
  record; the scan uses margin `|Q| ≤ 60`). For φ and 1+√3 the pruned ranges are labelled
  computational precisely because the analogous bound is conjectural.
- **Non-quadratic α** (e, π): 60-digit rational surrogates, entire computation repeated at
  120 digits, record lists must agree verbatim.
- **Three-tier labels** — proved / computationally verified / conjectural — on every
  statement in the note; computation never upgrades a label.


## Citation

If you use this repository or the accompanying manuscript, please cite:

> E. De Jesús, *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum*. Zenodo (2026). https://doi.org/10.5281/zenodo.21796640

The repository includes a `CITATION.cff` file with metadata for **all three** notes.

Each note has two DOIs. The **version** DOI identifies one deposit and is what to cite when a
result depends on the exact files; the **concept** DOI always resolves to the latest version.

| note | version DOI | concept DOI |
|---|---|---|
| 1 (2026-08) | [10.5281/zenodo.21796640](https://doi.org/10.5281/zenodo.21796640) | [10.5281/zenodo.21796540](https://doi.org/10.5281/zenodo.21796540) |
| 2 (2026-11) | [10.5281/zenodo.24046651](https://doi.org/10.5281/zenodo.24046651) | [10.5281/zenodo.24046650](https://doi.org/10.5281/zenodo.24046650) |
| 3 (2026-11) | [10.5281/zenodo.24297228](https://doi.org/10.5281/zenodo.24297228) | [10.5281/zenodo.24297227](https://doi.org/10.5281/zenodo.24297227) |

For the computations behind note 2 cite the tagged release `congruence-records-v1.0.0`, and for
note 3 the tag `general-classification-v1.0.0`, rather than the branch.

## License

- Manuscripts (`paper/`, `congruence-records/paper/`, `general-classification/paper/`) and
  documentation (`docs/`, `congruence-records/docs/`, `general-classification/docs/`):
  CC BY 4.0.
- Code (`code/`, `congruence-records/certificate/`, `general-classification/scripts/`) and data
  (`data/`, `congruence-records/tables/`, `general-classification/certificates/`,
  `general-classification/results/`): MIT (see `LICENSE`; its header names only `code/` and
  `data/` — open item **O-2**).

## Acknowledgements

AI assistance (Anthropic's Claude) was used for adversarial auditing, exact-arithmetic
computational design and execution, proof checking, and manuscript preparation. All
conceptual choices and final responsibility for the work belong to the author.
