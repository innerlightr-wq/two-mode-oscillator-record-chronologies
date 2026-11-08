# Changelog

This repository holds two pieces of work. The 2026-08 note on two-mode oscillator record
chronologies is the **baseline** and is frozen; the 2026-11 companion note on odd/odd records
for the relative error is new. Dates are the dates the work was done, not publication dates.

---

## [companion-1.0.0-rc2] — 2026-11-07 — release candidate, not published

Pre-upload review of rc1 by an external reviewer. Five repairs; **no classification changed**,
and the counts 4/64/6 orbits and 1+1 / 3 / 1+1 non-excluded are unaltered.

### Repaired

| # | finding | repair |
|---|---|---|
| **P-1** | **Proposition 7.2 was stated without hypotheses and is false before the tail.** Confirmed by exact search: at `1+sqrt(3)` there are **13** pairs, all at `p = 0`, where the latest competitor state below `B` sits at period `p+1`, outside the `d in {0,1}` window. Witness: `B = (7,1)`, defect `-111`, `H = 8+7sqrt(3) = 20.1244…`; the defect-`+193` orbit has no positive state at period 0, its first being `(1,15)` at period 1 with `H = 16+sqrt(3) = 17.7320…`. | the proposition now carries hypotheses (a) every orbit has a positive state at period `<= p0-1` and (b) every ordering threshold is decisive, and concludes for `p >= p0`. New Remark 7.3 gives the witness. Both hypotheses were already what `tail_table.py` computes, so `p0 = 2, 2, 3` and the caps 23/302/46 are unchanged; every violating pair lies inside the enumerated region. |
| **P-2** | **The appendix could not be used to re-derive a row.** Competitors were named by `N_rep`, which is **not unique** — at `1+sqrt(3)` thirty values label two orbits each and `-143` labels **four**; at `sqrt(3)` two values label two each. The reported period came from the error threshold alone, ignoring the ordering threshold and positivity, so an independent audit found **66 of 67** rows unusable as stated (65 ambiguous, 1 naming a non-positive state). | every orbit now carries a stable ID (`P`/`T`/`S` + canonical index); the certified period `P` is the max of the error threshold, the ordering threshold converted by `+d`, and first positivity; the states of `A` and `B` at `p = P` are printed. `tables.py` re-verifies each row at `P, P+1, P+2` and refuses to emit an unverified one. |
| **P-3** | **The weak-record definition contradicted itself** — it required equality at some lower state, which no strict record satisfies, yet the next sentence asserted every strict record is weak. | equality requirement removed from the definition and reserved for "weak but not strict". |
| **P-4** | **The cutoff proof asserted `0 < u < 1` unconditionally**, but `u = t/(2 alpha Y) = 0` at `sqrt(3)`, where `t = 0`. | the `t = 0` case is separated first (`F = L rho^2` identically, no bound on `u` needed); `0 < u < 1` is now claimed only for `t > 0`. The cutoffs 18/204/27 are unchanged. |
| **P-5** | **Theorem C(ii) showed `eps_B = eps_A` at larger height but never that `B` precedes the next strict record**, which is what makes it tie the running minimum. | added `H_A < sqrt(3) H_A < (2+sqrt(3)) H_A = H_{rho A}` as eq. (13), with the proof closing on it. |

### Added

* **Check C11** in `verify_records.py`: re-derives all 67 exclusion rows from the orbit each
  one names and tests height order and error order at `p = P … P+11`. The verifier now runs
  **31** checks.
* Remark 7.3 (both hypotheses of Proposition 7.2 are needed), with the explicit witness.

### Changed — repository layout

On the reviewer's recommendation the companion work moved into a self-contained
`congruence-records/` folder: `paper/`, `certificate/`, `tables/`, `docs/`, with its own
`README.md` and a folder-wide `SHA256SUMS`. `tables/` is now a sibling of `certificate/`
rather than a subdirectory, so `tables.py` writes to `../tables/` and the note `\input`s
`../tables/`. The top-level `README.md` now introduces both notes and their relationship.
Nothing in `paper/`, `code/`, `data/`, `docs/REPORT.md`, `LICENSE`, `CITATION.cff`,
`SHA256SUMS` or `VERSIONS.txt` at the repository root was touched.

---

## [companion-1.0.0-rc1] — 2026-11-07 — superseded by rc2

Companion technical note *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
Classifications and an Exact Certificate*, plus its certificate bundle.

### Added

* `paper/congruence_records_note.tex`, `paper/congruence_records_note.pdf` — the companion
  note (16 pp.).
* `certificate/` — the standalone certificate bundle (see `certificate/README.md`):
  `quad.py`, `setups.py`, `orbits.py`, `certificate.py`, `verify_records.py`, `brute.py`,
  `candidates.py`, `tail_table.py`, `tables.py`, `hypotheses.py`, `PROOF_OR_OBSTRUCTION.md`,
  `THEOREM_TARGET.md`, `README_PACKAGE.md`, `tables/`, `outputs/`.
* `CHANGELOG.md`, `RELEASE_MANIFEST.md`, `ZENODO_METADATA.md`,
  `LICENSE_AND_SOURCE_INVENTORY.md`, `REVIEW_SUMMARY.md`,
  `EARLIER_NOTE_STATUS.md`.

### Mathematical results new in this release

* **Theorem A** (`alpha = phi`) and **Theorem B** (`alpha = 1 + sqrt(3)`): the two completeness
  statements left conjectural in the baseline note are proved.
* **Theorem C** (`alpha = sqrt(3)`): a new slope, with an exactly-tying companion family.
* The norm cutoff, **assumed** in the baseline note for `phi` and `1 + sqrt(3)`, is **derived**
  (Theorem 4.1), giving `|N| <= 18`, `204`, `27`.

### Corrected relative to the baseline note

* **Observation 5.12** of the baseline claims three records per multiplicative height period
  `(2 + sqrt(3))^2`. Exact multiplicativity holds for `eta`, not for `H`:
  `H_next - rho*H = t*N*(rho - delta/rho)/(D0*eta)`, and `H(7,19) - rho*H(1,1) = -8*sqrt(3)`.
  The companion note proves only `H_next/H -> rho` and does **not** assert a fixed count per
  window. See `EARLIER_NOTE_STATUS.md`. The baseline note and PDF are left unchanged.
* `README.md` cited the two completeness conjectures as "Conjectures 5.8, 5.10". The pinned
  PDF prints **Conjecture 5.11** and **Conjecture 5.13** (and **Remark 5.10** for the
  degenerate competition). The `README.md` reference is corrected in this release; the paper
  is not touched.
* `README.md` ended the citation section with a truncated sentence ("…please ensure the DOI in
  `CITATION.cff` is set to:"). Completed, pointing at the open DOI item in
  `LICENSE_AND_SOURCE_INVENTORY.md`.

### Known open items

* `CITATION.cff` still carries the placeholder `doi: "10.5281/zenodo.XXXXXXXX"`.
  **Not resolved in this release** — see `LICENSE_AND_SOURCE_INVENTORY.md`, item O-1.
* Novelty relative to the odd–odd continued fraction literature is unresolved.
* The uniform theorem is unproved.

---

## Certificate bundle lineage (internal versions, never published)

| version | sha256 of the archive | status |
|---|---|---|
| v1 | `a9fda5b01a6cca673b225bd67c5adce86535df856a4da38d2812e08758510eaf` | audited; 6 material defects (F1–F7) |
| v2 | `10ca883566637cc4bcd80c8e4a0f050214c949e44e91d7033d964319122d36bf` | F1–F7 repaired; re-audited; 3 defects (R1–R3) |
| v3 | `def4970b30d6fd0bf89c2ffbeaaf620b0318fdde719d3bba09c8de559cdf2d7b` | R1–R3 repaired; the basis of `certificate/` |

What the two audits found and how it was repaired is recorded in `../certificate/README_PACKAGE.md`
and, for the mathematics, in `../certificate/PROOF_OR_OBSTRUCTION.md`. The headline items:

* **F2 / R1** — the cutoff proof. v1 used a rejected argument; v2 replaced it with "F is
  monotone in Y", which is **false** (at `phi` the `n = -1` branch increases towards `phi^6`
  while the `n = +1` branch decreases towards it). v3 proves the two sign branches separately.
  The bounds 18 / 204 / 27 were unchanged by both repairs.
* **F3** — `least_decided_period` pre-multiplied by `rho^{2d}`, giving 51 wrong predictions at
  `1 + sqrt(3)`; and the error and ordering thresholds were aggregated in mismatched period
  coordinates.
* **F4** — strict versus weak was not implemented, so the `sqrt(3)` norm-`+6` companion was
  labelled a strict record. It ties exactly, forever.
* **R2** — check C2 asserted nothing at `sqrt(3)` and printed `PASS`. It now asserts
  `k^2 - 3m^2 = 6 (mod 8)` and fails for an unhandled slope.
* **A5** (first audit round) — the identification of this record set with ordinary
  first-kind approximation was **withdrawn** and is not resurrected: `eps` and `|alpha - r|`
  order opposite sides of `alpha` differently (absolute error ties at the arithmetic mean of
  the two sides, `eps` at the geometric mean).

---

## [1.0.0] — 2026-08-04 — baseline, deposited

E. De Jesús, *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum*,
Zenodo, doi:10.5281/zenodo.21796640. Repository commit `10ea1c6`,
`paper/oscillator_records.pdf` sha256
`f36c23ab099a7a0bca1e68dfe699ea02e15ef6e767bbc52428a77b272da247b3`.

Contents: `paper/`, `code/audit.py`, `code/chronologies.py`, `data/`, `docs/REPORT.md`.
Proved there: the boundary record theorem for every `alpha > 1`, interior completeness at
`alpha = sqrt(2)`, and the rational dichotomy. Left conjectural there: completeness at `phi`
and at `1 + sqrt(3)`.
