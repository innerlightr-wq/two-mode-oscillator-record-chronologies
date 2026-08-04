# Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum

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

**Conjectural.** Completeness of the φ and 1+√3 chronologies (Conjectures 5.8, 5.10 in
the note).

## Repository layout

```
paper/    oscillator_records.tex, oscillator_records.pdf   — the note (16 pp.)
code/     audit.py          — boundary theorem + √2 audit (all proofs' exact checks)
          chronologies.py   — φ, 1+√3, 3/2, 5/3, e, π chronologies
data/     records_sqrt2_first30.csv   — first 30 √2 records, exact algebraic forms
          chron_phi.csv, chron_1plus_sqrt3.csv
          chron_rational_3_2.csv, chron_rational_5_3.csv
          chron_e.csv, chron_pi.csv
docs/     REPORT.md         — 16-section audit status report (source of truth for the note)
SHA256SUMS, VERSIONS.txt
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

The repository includes a `CITATION.cff` file with the corresponding citation metadata. Please ensure the DOI in `CITATION.cff` is set to:

## License

- Manuscript (`paper/`): CC BY 4.0.
- Code (`code/`) and data (`data/`): MIT (see `LICENSE`).

## Acknowledgements

AI assistance (Anthropic's Claude) was used for adversarial auditing, exact-arithmetic
computational design and execution, proof checking, and manuscript preparation. All
conceptual choices and final responsibility for the work belong to the author.
