# Changelog

This repository holds two pieces of work. The 2026-08 note on two-mode oscillator record
chronologies is the **baseline** and is frozen; the 2026-11 companion note on odd/odd records
for the relative error is new. Dates are the dates the work was done, not publication dates.

---

## [companion-1.0.0-rc1] — 2026-11-07 — release candidate, not published

Companion technical note *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
Classifications and an Exact Certificate*, plus its certificate bundle.

### Added

* `paper/congruence_records_note.tex`, `paper/congruence_records_note.pdf` — the companion
  note (16 pp.).
* `certificate/` — the standalone certificate bundle (see `certificate/README.md`):
  `quad.py`, `setups.py`, `orbits.py`, `certificate.py`, `verify_records.py`, `brute.py`,
  `candidates.py`, `tail_table.py`, `tables.py`, `hypotheses.py`, `PROOF_OR_OBSTRUCTION.md`,
  `THEOREM_TARGET.md`, `README_PACKAGE.md`, `tables/`, `outputs/`.
* `docs/CHANGELOG.md`, `docs/RELEASE_MANIFEST.md`, `docs/ZENODO_METADATA.md`,
  `docs/LICENSE_AND_SOURCE_INVENTORY.md`, `docs/REVIEW_SUMMARY.md`,
  `docs/EARLIER_NOTE_STATUS.md`.

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
  window. See `docs/EARLIER_NOTE_STATUS.md`. The baseline note and PDF are left unchanged.
* `README.md` cited the two completeness conjectures as "Conjectures 5.8, 5.10". The pinned
  PDF prints **Conjecture 5.11** and **Conjecture 5.13** (and **Remark 5.10** for the
  degenerate competition). The `README.md` reference is corrected in this release; the paper
  is not touched.
* `README.md` ended the citation section with a truncated sentence ("…please ensure the DOI in
  `CITATION.cff` is set to:"). Completed, pointing at the open DOI item in
  `docs/LICENSE_AND_SOURCE_INVENTORY.md`.

### Known open items

* `CITATION.cff` still carries the placeholder `doi: "10.5281/zenodo.XXXXXXXX"`.
  **Not resolved in this release** — see `docs/LICENSE_AND_SOURCE_INVENTORY.md`, item O-1.
* Novelty relative to the odd–odd continued fraction literature is unresolved.
* The uniform theorem is unproved.

---

## Certificate bundle lineage (internal versions, never published)

| version | sha256 of the archive | status |
|---|---|---|
| v1 | `a9fda5b01a6cca673b225bd67c5adce86535df856a4da38d2812e08758510eaf` | audited; 6 material defects (F1–F7) |
| v2 | `10ca883566637cc4bcd80c8e4a0f050214c949e44e91d7033d964319122d36bf` | F1–F7 repaired; re-audited; 3 defects (R1–R3) |
| v3 | `def4970b30d6fd0bf89c2ffbeaaf620b0318fdde719d3bba09c8de559cdf2d7b` | R1–R3 repaired; the basis of `certificate/` |

What the two audits found and how it was repaired is recorded in `certificate/README_PACKAGE.md`
and, for the mathematics, in `certificate/PROOF_OR_OBSTRUCTION.md`. The headline items:

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
