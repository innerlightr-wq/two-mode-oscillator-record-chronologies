# Status of the baseline note after the companion note

**The baseline note is not modified.** `paper/oscillator_records.tex` and
`paper/oscillator_records.pdf` are byte-identical to the deposited version and remain the
historical record that both certificate audits were run against. This file says what has since
changed about its *claims*; it does not change the document.

Pinned baseline:

```
deposit            E. De Jesús, "Boundary and Interior Record Chronologies for the
                   Two-Mode Oscillator Spectrum", Zenodo, 2026-08-04
                   version DOI  10.5281/zenodo.21796640
                   concept DOI  10.5281/zenodo.21796540
repository commit  10ea1c62c6866990ded0a85a531883841d38d034
oscillator_records.pdf  sha256 f36c23ab099a7a0bca1e68dfe699ea02e15ef6e767bbc52428a77b272da247b3
oscillator_records.tex  sha256 6b616f79602393fd4560c0adbc2f789f47e9c8b13ca771ebe9d6f70e599295cd
```

Numbering below is that of the **pinned PDF**. The repository `README.md` previously referred
to the two completeness conjectures as "Conjectures 5.8, 5.10"; that was a `README.md` error
and has been corrected in this release. The PDF prints Conjecture 5.11 and Conjecture 5.13.

---

## 1. Statements now proved

| baseline statement | label there | status now |
|---|---|---|
| **Conjecture 5.11** (`phi`-completeness) | conjectural | **proved** — Theorem A of the companion note |
| **Conjecture 5.13** (`1+sqrt(3)`-completeness) | conjectural | **proved** — Theorem B |
| **Observation 5.9** (`phi` chronology, record list and defect cycle) | computationally verified | the record list and the cycle `(-1,+1,-5)` are **proved** |
| **Observation 5.12** (`1+sqrt(3)` chronology, record list and defect cycle) | computationally verified | the record list and the cycle `(-3,+1,-11)` are **proved** |
| **Remark 5.10** (asymptotically degenerate competition) | observed pattern, explicitly "not a proved theorem" | the selection rule — odd Lucas pairs with `n = 4 (mod 6)`, i.e. `N = -5` — is **proved**, Theorem 8.4 |
| the pruned `|N| <= 200` scan range for `phi` and `1+sqrt(3)`, which Section 6 labels computational "precisely because the analogous bound is Conjectures 5.11–5.13" | assumption | the cutoff is now **derived**: `|N| <= 18` at `phi`, `|N| <= 204` at `1+sqrt(3)` (Theorem 4.1) |

## 2. Statement corrected

**Observation 5.9** ("…with three records per multiplicative period `phi^6` in height") and
**Observation 5.12** ("…with three records per multiplicative period `(2+sqrt(3))^2 = 7+4sqrt(3)`
in height") both treat the height as scaling exactly by the unit.

It does not. From `H = G/(D0*eta)` with `G = 2*alpha*eta^2 - t*N`,

```
H_next - rho*H = t*N*(rho - delta/rho) / (D0*eta),
```

which vanishes only when `t*N = 0`. Both slopes have `t > 0`, and exact witnesses are

```
H(7,19)  - rho     * H(1,1) = -8*sqrt(3)        (1+sqrt(3), rho = 7+4sqrt(3))
H(13,21) - phi^6   * H(1,1) = 4 - 4*sqrt(5)     (phi)
```

What survives is the limit: `H_next/H -> rho` along each orbit, since `eta -> infinity`.

**Scope of the correction.** This affects the *exactness of the height period*, not the record
lists, not the defect cycles, and not the observed counts, all of which are proved in the
companion note. The companion note deliberately does **not** assert that every sufficiently
large multiplicative height window contains exactly three records; that is a statement about
how three orbits with different multiplicative phases interleave, and it is not proved here.

At `alpha = sqrt(3)`, where `t = 0`, the height period `2+sqrt(3)` **is** exact — see
Theorem C. That slope does not appear in the baseline note.

## 3. Statement withdrawn during this work (never in the baseline note)

An identification of these records with ordinary first-kind Diophantine approximation was
proposed and then **withdrawn**; it is not resurrected anywhere in the companion note. The
reason: `eps(r) = |m*alpha-k|/(m*alpha+k)` and `|alpha - k/m|` order the two sides of `alpha`
differently. Absolute error ties at the arithmetic mean of a pair of approximants on opposite
sides, `eps` ties at the geometric mean, and for `alpha = sqrt(11)-2 = 1.316624790…` the two
means `1.290994449…` and `1.333333333…` bracket `alpha` from opposite sides.

## 4. What remains open from the baseline programme

* The baseline's `alpha = e` and `alpha = pi` chronologies (Observation 5.18) are unaffected
  and remain computational: the companion note's method is specific to quadratic `alpha`.
* A uniform theorem covering arbitrary quadratic slopes and congruence classes is **not**
  proved; see Section 12 of the companion note for the three places the present argument uses
  `t >= 0`, `alpha' < 0` and the odd/odd class.
* Novelty relative to the odd–odd continued fraction literature is **unresolved**; Section 11
  records only the comparisons that were actually made.
