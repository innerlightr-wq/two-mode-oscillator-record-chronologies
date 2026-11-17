# An Effective Classification of Congruence-Restricted Quadratic Relative-Error Records

Technical note (note 3 of this repository) and its reproducibility material.

> E. De Jesús, *An Effective Classification of Congruence-Restricted Quadratic
> Relative-Error Records*. Zenodo (2026).
> doi:[10.5281/zenodo.24297228](https://doi.org/10.5281/zenodo.24297228) ·
> concept DOI (all versions)
> [10.5281/zenodo.24297227](https://doi.org/10.5281/zenodo.24297227) ·
> deposited 2026-11-17, CC BY 4.0 · release tag `general-classification-v1.0.0`

Author: Elias De Jesús, Independent Researcher — ORCID
[0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143) —
`dejesuselias10@gmail.com`

`paper/main.pdf` here is **byte-identical to the deposited file**
(`sha256 588bbb003bd8b8444d69d4bf40fa241b8e84d70dfef61cb757468725746dd7ba`), so the DOI is
recorded in this README and in the metadata rather than stamped into the PDF. The deposit
contains the PDF only; the LaTeX source, the code, the 26 certificates and the logs are here.

---

## The theorem, in scope

Let `A,B,C` be coprime integers with `A > 0` and `Δ = B² − 4AC > 0` not a perfect square. For a
sign `s ∈ {±1}` put `α = (−B + s√Δ)/(2A)` and require only `α > 0`; let `α'` be the conjugate.
Fix `M ≥ 1` and a **nonempty** `R ⊆ (Z/MZ)²`. The admissible states are the pairs of positive
integers `(m,k)` with `(m mod M, k mod M) ∈ R` — **no coprimality is imposed**. Put

```
H(m,k) = mα + k,    ε(m,k) = |mα − k| / (mα + k),    Q(m,k) = Ak² + Bmk + Cm².
```

A state is a **strict record** if its `ε` is strictly smaller than at every admissible state of
smaller `H`. Because `α` is irrational, distinct states have distinct `H`, so `H` is a strict
total order and the running minimum of `ε` is well defined.

**Theorem (§3 of the note).** There is an algorithm which, on input `(A,B,C,s,M,R)`, terminates
and outputs: a matrix `P ∈ SL₂(Z)` with `P ≡ I (mod M)` preserving `Q` and `gcd` and scaling `η`
by `ρ > 1`; a comparison state `w` with attained error `ε_w < ε̄ = min(1, √Δ/(2|B|))`; integers
`B_cut ≤ B_comp` and a finite list of `⟨P⟩`-orbits containing every admissible state with
`|Q| ≤ B_comp`; per orbit a cutoff level `L*ᵢ` with two exact witnesses and a tail-start level
`Tᵢ > L*ᵢ`; a verdict in `{record, tie, excluded}` correct at every level `L ≥ Tᵢ`; and the exact
record set of the finite region `H ≤ H(w)` together with the exact verdict at each level
`L*ᵢ < L < Tᵢ`. The strict records are exactly the finite part plus the complete forward orbits
of the seeds `P^{Tᵢ}(repᵢ)` of the orbits verdicted *record*.

**In scope:** either root; `α'` of either sign; `α ≷ 1`; nonmonic (`A > 1`); any nonempty `R`,
including unions of residue classes; imprimitive states, which do occur as records.
**Out of scope:** a complete classification of *weak* records (ties are detected and the
certified tie families are reported, but not classified exhaustively); any `α` of degree > 2;
any bound on the running time.

**What is classical, what is proposed.** That all sufficiently late records lie in finitely many
automorph orbits follows from the classical reduction theory of indefinite binary quadratic
forms once the defect is bounded, and no novelty is claimed for it; the Pell solution, the proper
automorph, `Q`-invariance and the reduction box are classical inputs used as such. Determining
*which* orbit tails are records, at *which* level each begins, and certifying that the finitely
many exceptions are completely enumerated, does not follow from that. The *proposed*
contribution — effectiveness, generality, and certificate completeness — is stated as such in §1
and is pending a fuller literature comparison; §17 item 6 distinguishes the nearest works
consulted individually. Corrections of that reading are invited.

**One negative result worth isolating.** Proposition 2.7: a strict record need not be a vertex of
the convex hull of the admissible points of its cone. At `α = 2+√2`, `M = 3`, `R = {(1,1)}` the
record `(7,25)` lies strictly inside the triangle spanned by the admissible cone points `(1,4)`,
`(31,106)`, `(1,7)`, with barycentric coordinates `3/5, 1/5, 1/5`. So the natural
"read the records off a Klein/Arnold sail" reduction fails. This refutes that one reduction only;
it rules out no other geometric description, and establishes no novelty by itself.

## Files

| path | content |
|---|---|
| `paper/main.pdf` | the note (22 pp), byte-identical to the deposited file |
| `paper/main.tex` | its LaTeX source: proof, worked example, stress examples, reproducibility, crosswalk |
| `paper/references.bib` | bibliography source, mirroring the inline `thebibliography` in `main.tex` |
| `scripts/` | the algorithm (`gq.py`, `emit.py`), the independent checker (`check.py`) and the verifier suites |
| `certificates/` | the 26 machine-readable certificates, one per instance |
| `results/` | the complete logs of every run quoted below |
| `docs/CLAIM_LEDGER.md` | every substantive statement, its proof location, its computational support, its limitations |
| `docs/RELEASE_MANIFEST.md` | identity, DOIs, artefacts and per-file hashes for this release |
| `docs/ZENODO_METADATA.md` | the deposit metadata, with the assigned DOIs |
| `docs/PROVENANCE.txt` | source folder, repository state at draft time, and `sha256` for every archived file |
| `docs/notes/` | the working proof and audit notes this note consolidates |
| `SHA256SUMS` | hashes for every file in this folder |

## Reproducing the computations

Requires Python 3.11+ and **no third-party packages**. From this folder:

```
python3 scripts/emit.py            # regenerate all 26 certificates into certificates/
python3 scripts/check.py           # audit every certificate (independent checker)
python3 scripts/check.py control_phi   # audit one certificate, verbose per-check output
python3 scripts/qr_general.py      # classifier-side suite
python3 scripts/lit_bridge.py      # objective-comparison checks
python3 scripts/review3.py         # regression controls (third review)
python3 scripts/review4.py         # regression controls (fourth review)
python3 scripts/review5.py         # regression controls (fifth review)
python3 scripts/review6_sail.py    # the exact counterexample of Prop. 2.7
```

The bundle is self-contained: `emit.py` run here regenerates all 26 certificates
byte-identically (verified by `sha256` before and after), and `check.py` run here
reproduces the 1707/1707 audit exactly. `emit.py` writes into `certificates/`; `check.py` only
reads. Both are pure Python and
deterministic. `emit.py` takes a few minutes for all 26 instances; `check.py` takes longer
(tens of minutes) because its checks are deliberately unpruned.

### Results obtained, on the certificates in `certificates/`

| run | result | log |
|---|---|---|
| `check.py`, all 26 certificates | **1707/1707** exact checks, 0 failures | `results/check_v8.log` |
| the same, re-run **inside the frozen bundle** | **1707/1707**, 0 failures | `results/check_archive.log` |
| `emit.py` **inside the frozen bundle** | 26 certificates, **byte-identical** to the frozen ones | `results/emit_archive.log` |
| `qr_general.py` | 98/98, 0 failures | `results/qr_general2.log` |
| `lit_bridge.py` | 14/14, 0 failures | `results/lit_bridge.log` |
| `review3.py` | 25/25, 0 failures | `results/review3.log` |
| `review4.py` | 14/14, 0 failures | `results/review4.log` |
| `review5.py` | 14/14, 0 failures | `results/review5.log` |
| `review6_sail.py` | 14/14, 0 failures | `results/review6_sail.log` |


### What the computations do and do not establish

The theorem and every lemma are proved for arbitrary admissible input. The computations
instantiate the algorithm on 26 inputs, emit a certificate per input, and audit those
certificates with a checker that shares no code, no data representation and no decision routine
with the classifier and that does not use the blocker bound. Nothing universal is inferred from
them, and nothing here is machine-checked in a proof assistant or refereed.

## Relationship to previous work

This note generalises the three worked classifications (`φ`, `1+√3`, `√3`, odd/odd) of

> E. De Jesús, *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
> Classifications and an Exact Certificate*, Zenodo 2026,
> [doi:10.5281/zenodo.24046651](https://doi.org/10.5281/zenodo.24046651)
> (concept DOI 10.5281/zenodo.24046650),

which proved them one slope at a time under `B ≤ 0`, `α' < 0`, `α > 1`, `A = 1` and the specific
odd/odd class. All five hypotheses are removed here. The baseline is

> E. De Jesús, *Boundary and Interior Record Chronologies for the Two-Mode Oscillator Spectrum*,
> Zenodo 2026, [doi:10.5281/zenodo.21796640](https://doi.org/10.5281/zenodo.21796640)
> (concept DOI 10.5281/zenodo.21796540).

The supporting repository is
[`innerlightr-wq/two-mode-oscillator-record-chronologies`](https://github.com/innerlightr-wq/two-mode-oscillator-record-chronologies).
Nothing in that repository was modified in preparing this draft; its state is recorded in
`docs/PROVENANCE.txt`.

## Open engagement

This technical note forms part of an ongoing research program. Independent verification,
corrections, related references, and suggestions for extensions are welcome. In particular,
feedback on the universal scope of the classification, the certificate completeness conditions,
and connections with congruence-restricted approximation theory would be valuable.

## Licensing

Not yet fixed for this deposit. The established pattern in this programme — recorded in
`congruence-records/docs/ZENODO_METADATA.md` of the supporting repository — is **CC BY 4.0 for
the note and MIT for the accompanying code bundle**. That pairing is proposed here and is
flagged for confirmation at the upload stage; see `ZENODO_METADATA.md`.
