# Zenodo deposit metadata (prepared; **not** deposited)

Everything below is ready to paste into the Zenodo deposition form. No DOI has been reserved
and no upload has been made. Fields that require a DOI or a date that does not yet exist are
marked `TO BE SET AT DEPOSIT`.

---

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

**Publication date:** `TO BE SET AT DEPOSIT`

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
| continues | `10.5281/zenodo.21796640` | the author's earlier note, whose Conjectures 5.11 and 5.13 this resolves |
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

0. Push the branch and publish the GitHub release `congruence-records-v1.0.0`, so the
   related identifier above resolves.
1. Decide whether to reserve a DOI before upload or accept the minted one.
2. Set the publication date.
3. Upload the three files, paste the fields above, add the related identifiers.
4. Publish, then record the **version** DOI and the **concept** DOI separately.
5. Update `CITATION.cff` — it currently holds the placeholder
   `doi: "10.5281/zenodo.XXXXXXXX"` (open item O-1).
6. Update `README.md` and `RELEASE_MANIFEST.md` with the minted DOI, and tag the commit.
