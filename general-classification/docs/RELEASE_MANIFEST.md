# Release manifest — `general-classification-v1.0.0`

The third technical note of this repository and its reproducibility material. The note is
**deposited** at doi:10.5281/zenodo.24297228 (2026-11-17); this repository holds the LaTeX
source, the algorithm, the independent checker, the 26 certificates and the logs, none of which
the deposit contains. Prepared 2026-11-16/17.

---

## 1. Identity

| field | value |
|---|---|
| manuscript | *An Effective Classification of Congruence-Restricted Quadratic Relative-Error Records* |
| manuscript version | `1.0.0` (eight internal review rounds before deposit; see §6) |
| author | Elias De Jesús, ORCID 0009-0007-0190-9143 |
| branch | `general-classification`, merged to `main` |
| release tag | `general-classification-v1.0.0` |
| release commit | not quoted here — a commit hash covers this file, so it cannot name itself. Resolve it with `git rev-parse general-classification-v1.0.0^{commit}`, and cite the **tag** rather than the branch. |
| folder | `general-classification/` (self-contained: `paper/`, `scripts/`, `certificates/`, `results/`, `docs/`) |
| source baseline | commit `b8f207d3d5ac23f33465327353f1973d36127ca7`, clean tree |
| draft folder | `~/scratch/quadratic-note-2026-11-16`, from research folder `~/scratch/quadratic-records-general-2026-11-16` (see `PROVENANCE.txt`) |
| DOI (version) | **10.5281/zenodo.24297228** — deposited 2026-11-17, CC BY 4.0 |
| DOI (concept) | 10.5281/zenodo.24297227 — resolves to the latest version |
| deposited file | `main.pdf`, 22 pp., 518356 bytes, `sha256 588bbb003bd8b8444d69d4bf40fa241b8e84d70dfef61cb757468725746dd7ba` — **byte-identical to `paper/main.pdf` in this release**, verified by downloading the record |

The DOI is **not** stamped into the PDF: keeping the committed PDF byte-identical to the
published one was preferred over a title-block DOI, following the precedent of
`congruence-records/docs/RELEASE_MANIFEST.md`. The DOI appears in `README.md`,
`docs/ZENODO_METADATA.md`, the root `README.md` and `CITATION.cff`.

## 2. What this release does not touch

Notes 1 and 2 and their material are unchanged by this release:

```
paper/oscillator_records.pdf              paper/oscillator_records.tex
code/  data/  docs/REPORT.md              congruence-records/  (whole folder)
LICENSE  VERSIONS.txt  SHA256SUMS
```

`README.md` and `CITATION.cff` at the repository root **are** updated, to introduce note 3 and
to add its citation entry. Nothing about notes 1 and 2 is restated or revised here; this note
neither corrects nor supersedes them.

## 3. Relationship to note 2

This is a **generalisation**, not a correction, of doi:10.5281/zenodo.24046651. That note's
three theorems remain true as stated and are reproduced here as controls (the first three rows
of the stress table in §15 of the note). What is new is that its five hypotheses — `B <= 0`,
`alpha' < 0`, `alpha > 1`, `A = 1`, and the odd/odd class — are all removed, and that the
classification is proved for arbitrary admissible input rather than slope by slope.

Several statements in the working notes behind note 2 turned out to be false in the general
setting; they are carried as explicit warnings in §§6–12 of the present note, as regression
controls rather than a correction diary. **None of them affects the three published
classifications.**

## 4. Release artefacts and their hashes

Paths are relative to the repository root.

```
588bbb003bd8b8444d69d4bf40fa241b8e84d70dfef61cb757468725746dd7ba  general-classification/paper/main.pdf   (22 pp., 518356 bytes)
```

`general-classification/SHA256SUMS` hashes all **59** files of this folder individually, with
paths relative to that folder. Verify with

```sh
cd general-classification && sha256sum -c SHA256SUMS
```

It is not self-hashed. It *does* cover this manifest, so `SHA256SUMS` is regenerated last; its
own hash is therefore not quoted here, to avoid a circular reference.

`docs/PROVENANCE.txt` carries a second, independent hash list, recorded in the draft folder
before the files were copied here. The two lists agree on every file they share; `PROVENANCE.txt`
uses the draft folder's `archive/...` paths, and additionally records the repository state at
draft time and the two post-freeze script changes.

## 5. Build of the manuscript

```sh
cd general-classification/paper
pdflatex -interaction=nonstopmode main.tex    # three times, for refs and the longtable
```

Toolchain: TeX Live `pdflatex`; packages `amsmath`, `amsthm`, `amssymb`, `geometry`, `booktabs`,
`longtable`, `array`, `hyperref`, `microtype`. The bibliography is a `thebibliography`
environment inside the `.tex`; `references.bib` mirrors it for convenience and **no BibTeX run
is needed**. No external file is `\input`.

**Outcome:** exit 0; 22 pages; **zero** errors, **zero** undefined references or citations.
Three cosmetic box warnings remain and were inspected: one overfull `\hbox` of 6.6 pt and two
underfull `\hbox`es, all three in the §15 stress table, none clipping any content. PDF metadata
(title, author, subject, keywords) is set in the preamble.

Build artefacts (`.aux`, `.log`, `.out`) are **not** committed.

**Rebuild check from a fresh clone.** The branch was cloned to a scratch directory and
`main.tex` rebuilt there with the same toolchain: exit 0, 22 pages, zero errors, zero undefined
references or citations, and the extracted text of the rebuilt PDF is **identical** to the
extracted text of the file downloaded from the Zenodo record. The two PDFs are not byte-identical
to each other, because a PDF embeds its creation timestamp; byte-identity is claimed only between
`paper/main.pdf` as committed and the deposited file, and that is verified by `sha256` above.

## 6. Verification

Python 3.14.7, standard library only, no network, no third-party packages. `check.py` shares no
code, no data representation and no decision routine with the classifier: it represents elements
of `Q(sqrt(Delta))` as `(a + b sqrt(Delta))/d` over `Delta` itself rather than over its
squarefree part, implements its own sign, floor, matrix and comparison routines, and **does not
use the blocker bound**, so all competitor comparisons are unpruned.

| command | checks | outcome | log |
|---|---|---|---|
| `python3 scripts/check.py` | 1707 | **1707/1707, 0 failures** over 26 certificates | `results/check_v8.log` |
| the same, re-run inside the frozen bundle | 1707 | 1707/1707, 0 failures | `results/check_archive.log` |
| `python3 scripts/emit.py` inside the bundle | — | 26 certificates, **byte-identical** (sha256 before/after) | `results/emit_archive.log` |
| `python3 scripts/qr_general.py` | 98 | 98/98, 0 failures | `results/qr_general2.log` |
| `python3 scripts/lit_bridge.py` | 14 | 14/14, 0 failures | `results/lit_bridge.log` |
| `python3 scripts/review3.py` | 25 | 25/25, 0 failures | `results/review3.log` |
| `python3 scripts/review4.py` | 14 | 14/14, 0 failures | `results/review4.log` |
| `python3 scripts/review5.py` | 14 | 14/14, 0 failures | `results/review5.log` |
| `python3 scripts/review6_sail.py` | 14 | 14/14, 0 failures | `results/review6_sail.log` |

`review3.py`–`review6_sail.py` are regression controls: each one pins an exact counterexample
to a statement that was wrong in an earlier draft, so the warnings in §§6–12 of the note cannot
silently regress. `review6_sail.py` verifies Proposition 2.7 (a strict record that is interior
to the convex hull of the admissible points of its cone) and reads nothing from
`certificates/`.

**Re-run from the committed tree.** `python3 scripts/check.py` was executed again from this
folder as committed, after the files were copied in and the paths rewritten: see §7.

## 7. Clean-tree re-run

`python3 scripts/check.py` was run from `general-classification/` exactly as committed, with no
`__pycache__` present beforehand:

```
INDEPENDENT CHECKER: 1707/1707 checks passed, 0 failures over 26 certificates
```

exit 0, zero `FAIL` lines. The full log is `results/check_repo.log`. `scripts/lit_bridge.py`
(14/14) and `scripts/check.py control_phi` (74/74) were run from the same tree beforehand as a
layout check, since `scripts/` resolves `certificates/` and `results/` relative to its own
parent directory.

## 8. What is and is not established

**Proved, for arbitrary admissible input** (coprime `A,B,C` with `A > 0`, nonsquare
`Delta = B^2 - 4AC > 0`, either root with `alpha > 0`, any `M >= 1`, any nonempty
`R` in `(Z/MZ)^2`, no coprimality on the pairs): the strict records of
`eps = |m alpha - k|/(m alpha + k)` under the height `H = m alpha + k` form an explicitly
bounded finite region, decided directly, together with finitely many complete forward orbits of
one integral matrix `P`, each rebased at a computed starting level; and there is a terminating
exact-arithmetic algorithm that outputs this data with a certificate.

**Not claimed.** A classification of all *weak* records (ties are detected and the certified tie
families reported, but not classified exhaustively); any bound on the running time; any `alpha`
of degree > 2; equality in Proposition 2.4; novelty — effectiveness, generality and certificate
completeness are stated as the *proposed* contribution, pending a fuller literature comparison,
and the classical finite-orbit input is credited as classical. Nothing here is machine-checked
in a proof assistant, nothing has been refereed, and testing 26 instances does not establish the
theorem. See `docs/CLAIM_LEDGER.md` for the statement-by-statement ledger and the ten open
obligations.

## 9. Open items on the Zenodo record

Neither affects this repository; both are for the author to act on at Zenodo.

| item | action |
|---|---|
| no *related identifiers* are set on the record | add **continues** -> doi:10.5281/zenodo.24046651 and *is supplemented by* -> the repository URL |
| the deposit carries `main.pdf` only | optionally publish a new version adding `main.tex`, `references.bib` and a zip of `scripts/`+`certificates/`+`results/`; a new version DOI would be minted under the same concept DOI |
