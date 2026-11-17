# Zenodo metadata — as deposited

**Deposited 2026-11-17 under CC BY 4.0.** Version DOI **10.5281/zenodo.24297228**, concept DOI
**10.5281/zenodo.24297227**. The fields below record what the deposit carries; they were
drafted as suggestions before upload and have been reconciled against the live record.

---

## Core fields

| field | value |
|---|---|
| Resource type | Publication → Technical note *(as deposited)* |
| Title | **An Effective Classification of Congruence-Restricted Quadratic Relative-Error Records** |
| Author | De Jesús, Elias |
| Affiliation | Independent Researcher |
| ORCID | 0009-0007-0190-9143 |
| Contact | dejesuselias10@gmail.com |
| Publication date | 2026-11-17 |
| Version | not set on the record; the repository release tag is `general-classification-v1.0.0` |
| Language | English |
| Version DOI | **10.5281/zenodo.24297228** |
| Concept DOI | **10.5281/zenodo.24297227** |

## Description (for the Zenodo abstract field)

> Let α > 0 be a real quadratic irrational, given as either root of a primitive integral
> quadratic Ax² + Bx + C with A > 0 and nonsquare discriminant Δ = B² − 4AC. For pairs of
> positive integers (m,k) whose residue (m,k) mod M lies in a prescribed nonempty set
> R ⊆ (Z/MZ)², order the pairs by the weighted height H = mα + k and measure them by the
> relative error ε = |mα − k|/(mα + k). A pair is a strict record if its error is smaller than
> at every admissible pair of smaller height.
>
> This note proves that the strict records always form a finite, explicitly decided part
> together with finitely many certified forward orbits of one integral matrix, each starting at
> a computed level, and gives a terminating algorithm that outputs this data with an exact
> certificate. No coprimality restriction is imposed on the admissible pairs, and no sign or
> monicity hypothesis on the polynomial: α may be the
> smaller root, its conjugate may be positive, α may be less than 1, A may exceed 1, R may be
> any union of residue classes, and imprimitive records occur and are classified. The mechanism
> is the proper automorph of the integral defect form Q = Ak² + Bmk + Cm²: a power P of it fixes
> every residue class modulo M and preserves Q, an explicit cutoff bounds |Q| on records,
> classical reduction theory of indefinite binary quadratic forms makes the surviving orbits
> finite, and finitely many exact comparisons decide each orbit's tail. Two phenomena absent
> from the monic negative-conjugate case are isolated: when the conjugate is positive the
> positive cone is not forward invariant and the height is not monotone along an orbit, and the
> backward exclusion then splits into two cases with different certificates.
>
> A separate negative result is isolated: a strict record need not be a vertex of the convex
> hull of the admissible points of its cone (Prop. 2.7), so the records cannot in general be read off a
> Klein/Arnold sail. The witness is exact — at α = 2+√2, M = 3, R = {(1,1)} the record (7,25)
> lies strictly inside the triangle spanned by the admissible cone points (1,4), (31,106) and
> (1,7). That refutes this one geometric reduction and rules out no other.
>
> What is classical here and what is proposed is separated explicitly. That all sufficiently
> late records lie in finitely many automorph orbits follows from classical reduction theory
> once the defect is bounded, and no novelty is claimed for it. Determining which orbit tails
> are records, at which level each begins, and certifying that the finitely many exceptions are
> completely enumerated, does not. The effectiveness, generality and certificate-completeness
> claims are offered as a proposed contribution pending a fuller comparison with the
> congruence-restricted approximation literature.
>
> The note generalises three worked classifications (α = φ, 1+√3, √3, with both coordinates
> odd) from the author's earlier note, which were proved one slope at a time under five
> hypotheses that are all removed here. Computations are used only to instantiate and audit the
> proof, not to establish it; all arithmetic is exact. The accompanying archive contains the
> algorithm, an independent certificate checker, 26 certificates, regression controls, and
> hashes.
>
> This technical note forms part of an ongoing research program. Independent verification,
> corrections, related references, and suggestions for extensions are welcome.

## Keywords

`Diophantine approximation`, `quadratic irrationals`, `record sequences`,
`congruence conditions`, `binary quadratic forms`, `Pell equation`, `automorph group`,
`reduction theory`, `relative error`, `exact arithmetic`, `certificates`, `effective algorithms`,
`Klein sail`, `convex hull`, `best approximation`

## Related identifiers

| relation | identifier | note |
|---|---|---|
| *is new version of* / *continues* | 10.5281/zenodo.24046651 | *Odd/Odd Records for a Relative Approximation Error: Three Quadratic Classifications and an Exact Certificate* — this note generalises its three theorems. Use the **version** DOI; the concept DOI is 10.5281/zenodo.24046650. Choose **continues** rather than *is new version of* if it should be a separate record rather than a new version of that one. |
| *references* | 10.5281/zenodo.21796640 | *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum* (baseline; concept DOI 10.5281/zenodo.21796540) |
| *is supplemented by* | https://github.com/innerlightr-wq/two-mode-oscillator-record-chronologies | supporting repository |

**Accurate relationship, stated plainly:** this is a *generalisation*, not a correction, of
doi:10.5281/zenodo.24046651. That note's three theorems remain true as stated and are
reproduced here as controls. What is new is that the five hypotheses it used (`B ≤ 0`,
`α' < 0`, `α > 1`, `A = 1`, the odd/odd class) are removed, and that the classification is
proved for arbitrary admissible input rather than slope by slope. Several statements in the
working notes behind that programme were found to be false in the general setting and are
recorded as explicit warnings in §§6–12 of the present note; none of them affects the three
published classifications.

## Licensing — as applied

The Zenodo record carries **CC BY 4.0** (`license.id = cc-by-4.0`), matching the established
pattern in this programme: CC BY 4.0 for the note, MIT for the code. In the repository, the
note and documentation under `general-classification/paper/` and `general-classification/docs/`
are CC BY 4.0; the code under `general-classification/scripts/` and the certificates and logs
under `certificates/` and `results/` are MIT, per the repository `LICENSE` and `CITATION.cff`
(`license: [MIT, CC-BY-4.0]`).

## Files — what the deposit actually contains

The record carries **`main.pdf` only** (518356 bytes, `sha256
588bbb003bd8b8444d69d4bf40fa241b8e84d70dfef61cb757468725746dd7ba`, byte-identical to
`general-classification/paper/main.pdf`). The LaTeX source, the code, the 26 certificates, the
logs and these documents are in this repository and **not** in the deposit.

Two things remain open on the Zenodo record itself, neither affecting the repository:

| open item | what to do on Zenodo |
|---|---|
| no *related identifiers* are set | add **continues** → doi:10.5281/zenodo.24046651, and *is supplemented by* → the repository URL |
| source and archive are not deposited | optionally publish a new version adding `main.tex`, `references.bib` and a zip of `scripts/`+`certificates/`+`results/`; that would mint a new version DOI under the same concept DOI |
