# Zenodo deposit — **DEPOSITED 2026-11-08**

| | |
|---|---|
| version DOI | **%s** — cite this when a result depends on the exact files |
| concept DOI | %s — always resolves to the latest version |
| record | https://zenodo.org/records/24046651 |
| published | 2026-11-08 |
| licence | CC BY 4.0 |
| resource type | Technical note |
| creator | De Jesus, Elias — ORCID 0009-0007-0190-9143 |
| file deposited | `congruence_records_note.pdf`, 331326 bytes, md5 `45f52bbe39ba3bef82c064060c5d56e1` |

The deposited PDF was checked against this repository and is **byte-identical** to
`../paper/congruence_records_note.pdf` at tag `congruence-records-v1.0.0` — that is, it is the
corrected build, with all five pre-upload repairs of `CHANGELOG.md` rc2 included.

## What the deposit does *not* contain

Verified against the Zenodo API on 2026-11-08:

1. **Only the PDF was uploaded.** The LaTeX source and the certificate archive were not. They
   live here and in the tagged GitHub release; the deposit alone is not reproducible.
2. **No related identifiers were set.** The record does not link to the repository, to the
   baseline note, or to the literature.

Neither is an error in the note. Both are worth fixing with a **new version** of the record,
which keeps the concept DOI %s and mints a fresh version DOI; the
existing version DOI %s stays valid and keeps pointing at the PDF
as cited. The fields below are what to use when doing that.

## Core fields

**Resource type:** Publication → Technical note

**Title**

```
Odd/Odd Records for a Relative Approximation Error: Three Quadratic Classifications and an Exact Certificate
```

**Authors**

| name | ORCID | affiliation |
|---|---|---|
| De Jesús, Elias | 0009-0007-0190-9143 | *(leave blank — no affiliation to declare)* |

**Publication date:** 2026-11-08 (as deposited)

**Language:** eng

**Version:** `1.0.0` (matching the GitHub tag `congruence-records-v1.0.0`)

**Description / abstract**

```
For a quadratic irrational alpha > 1 and positive odd integers m, k, set H = m*alpha + k and
eps = |m*alpha - k| / (m*alpha + k). A state (m,k) is a strict chronological record if eps is
smaller than at every admissible state of smaller H. This note classifies the strict records
completely for alpha = phi, alpha = 1 + sqrt(3) and alpha = sqrt(3). In each case they form a
finite explicit union of orbits of a single unimodular matrix, with signed defect cycles
(-1, +1, -5), (-3, +1, -11) and (-2) respectively.

The proofs rest on two exact identities that make eps a function of the integral defect
N = k^2 - t*k*m - s*m^2 and the conjugate factor eta alone; on a norm cutoff |N| <= 18, 204, 27
derived from heights by a sign-separated argument; on a bounded-rectangle enumeration of the
surviving unit orbits that uses no unique-factorisation hypothesis; and on a finite exact
certificate that decides every remaining comparison of error and of height. Two phenomena are
isolated: at phi the competition between the Fibonacci and the Lucas ladder is a genuine tie at
leading order, decided by the integer identity N_B = -5 N_A; and at sqrt(3) a companion family
has exactly equal error at larger height, so it is excluded by equality rather than by loss.

The results resolve two conjectures of the author's earlier note (doi:10.5281/zenodo.21796640)
and correct one assertion there about exact multiplicativity of the height period. A
standalone, exact-arithmetic certificate bundle accompanies the note. The work is not formally
verified in a proof assistant and has not been refereed, and the uniform generalisation to
arbitrary quadratic slopes and congruence classes is left open.
```

**Keywords**

```
Diophantine approximation
quadratic irrationals
congruence conditions
record sequences
Pell equation
unit orbits
golden ratio
Fibonacci and Lucas numbers
exact arithmetic
reproducibility
```

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) — for the note.
The accompanying certificate bundle is MIT; see `LICENSE_AND_SOURCE_INVENTORY.md`.

**Subjects (optional, MSC 2020):** 11J04 (homogeneous approximation to one number),
11J70 (continued fractions and generalizations), 11D09 (quadratic and bilinear Diophantine
equations). These three are the classifications carried by the cited literature
(Elsner 2000 carries 11J04 and 11J70); they have not been assigned by a cataloguer.

---

## Related identifiers

Only identifiers confirmed from the sources themselves are listed.

| relation | identifier | what it is |
|---|---|---|
| continues | `10.5281/zenodo.21796640` | the author's earlier note (version DOI; its concept DOI is `10.5281/zenodo.21796540`), whose Conjectures 5.11 and 5.13 this resolves |
| is supplemented by | `https://github.com/innerlightr-wq/two-mode-oscillator-record-chronologies/releases/tag/congruence-records-v1.0.0` | the tagged release holding the source, the certificate bundle and the outputs. Cite the **tag**, not the branch: Zenodo's own guidance is to pin a version when reproducibility depends on the exact files. |
| references | `10.5802/aif.3522` | Cha & Kim, Ann. Inst. Fourier 73 (2023) 101–161 |
| references | `10.1007/s00605-022-01704-2` | Kim, Lee & Liao, Monatsh. Math. 198 (2022) 323–344 |
| references | `10.1112/mtk.12285` | Kim, Lee & Liao, Mathematika 71 (2025) e12285 |
| references | `arXiv:2002.06310` | author version of Kim–Lee–Liao 2022, the version actually read |
| references | `arXiv:2403.12341` | author version of Kim–Lee–Liao 2025, the version actually read |

Not listed as a related identifier because it has no DOI: Elsner, *Fibonacci Quarterly* 38
(2000), no. 1, read at `https://www.fq.math.ca/Scanned/38-1/elsner.pdf`. It is cited in the
bibliography.

---

## Files to upload

| file | source path |
|---|---|
| `congruence_records_note.pdf` | `congruence-records/paper/congruence_records_note.pdf` |
| `congruence_records_note.tex` | `congruence-records/paper/congruence_records_note.tex` |
| `congruence-records-v1.0.0.zip` | the frozen `congruence-records/` folder — see `RELEASE_MANIFEST.md` |

---

## Remaining steps, to be done by the author

The deposit exists; what is left is completing it.

1. Push the branch and publish the GitHub release `congruence-records-v1.0.0`, so the
   repository related identifier resolves.
2. On the Zenodo record, choose **New version** and add the two missing files:
   `congruence_records_note.tex` and `congruence-records-v1.0.0.zip` (its sha256 is recorded
   at the repository root in `congruence-records-v1.0.0.zip.sha256`). Keep the PDF unchanged.
3. Add the related identifiers from the table above.
4. Record the new version DOI here and in `RELEASE_MANIFEST.md`; the concept DOI
   10.5281/zenodo.24046650 does not change, and the existing version DOI
   10.5281/zenodo.24046651 remains valid for anyone who already cited it.

`CITATION.cff` is **done** — open item O-1 is resolved, with both notes' version and concept
DOIs verified against the Zenodo API rather than inferred.
