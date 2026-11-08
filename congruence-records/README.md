# Odd/odd records for a relative approximation error

Companion work to the 2026-08 note in the parent repository. It proves the two completeness
conjectures that note left open, adds a third slope, and corrects one assertion there.

> E. De Jesús, *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
> Classifications and an Exact Certificate*, 2026.
> ORCID [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143).
> Zenodo (2026). doi:[10.5281/zenodo.24046651](https://doi.org/10.5281/zenodo.24046651) — the version DOI of the deposit, published
> 2026-11-08, CC BY 4.0. Concept DOI (all versions): [10.5281/zenodo.24046650](https://doi.org/10.5281/zenodo.24046650).
> Release tag: `congruence-records-v1.0.0`.

| | |
|---|---|
| the note | [`paper/congruence_records_note.pdf`](paper/congruence_records_note.pdf) · [`.tex`](paper/congruence_records_note.tex) |
| the certificate | [`certificate/`](certificate/) — programs, instructions, captured outputs |
| the data | [`tables/`](tables/) — per-orbit classification and exclusion witnesses, CSV and LaTeX |
| the paperwork | [`docs/`](docs/) — changelog, release manifest, review summary, Zenodo metadata, licence inventory, status of the earlier note |

## The problem

For `alpha > 1` and positive **odd** integers `m, k`,

```
H   = m*alpha + k                      (height, h = H/2)
eps = |m*alpha - k| / (m*alpha + k)    (relative error)
```

A state is a **strict chronological record** if its `eps` is strictly smaller than that of
every admissible state of strictly smaller height. The note classifies the strict records
completely at three slopes.

## Results

| slope | strict records | defect cycle |
|---|---|---|
| `phi` | `(F_{3j+1}, F_{3j+2})` together with `(L_{6j+4}, L_{6j+5})`, merged by height | `(-1, +1, -5)` |
| `1+sqrt(3)` | three orbits of `[[3,4],[8,11]]` seeded at `(1,1)`, `(1,3)`, `(5,13)` | `(-3, +1, -11)` |
| `sqrt(3)` | the orbit of `[[2,1],[3,2]]` seeded at `(1,1)`; `h^2 eps = 1/2` exactly | `(-2)` |

The norm cutoff that the 2026-08 note **assumed** for `phi` and `1+sqrt(3)` is **derived**:
`|N| <= 18`, `204`, `27`. At `sqrt(3)` the companion family `(m,k) -> (k,3m)` has **exactly**
equal error at `sqrt(3)` times the height, so it consists of weak records that are never
strict.

## Reproducing

Python ≥ 3.10, standard library only; no third-party packages, no network.

```sh
cd certificate
python3 certificate.py    > outputs/certificate_output.txt   # the proof certificate
python3 tail_table.py     > outputs/tail_table_output.txt    # the finite-check table (§7)
python3 hypotheses.py     > outputs/hypotheses_output.txt    # H1/H3 side checks
python3 tables.py                                            # writes ../tables/
python3 verify_records.py > outputs/verify_output.txt        # 31 checks; "VERIFY PASSED"
cd .. && sha256sum -c SHA256SUMS   # covers the whole congruence-records/ folder
```

The shipped `certificate/outputs/` were captured from a clean extraction. Building the note
needs `tables/` to exist, since the appendix `\input`s it:

```sh
cd paper && latexmk -pdf congruence_records_note.tex
```

## Status

* The three classifications are **proved**, with the finite content isolated in `certificate/`.
* The certificate is **exact arithmetic**, not formal verification: no proof assistant is
  involved, and the note has **not** been refereed.
* **Not claimed:** a uniform theorem for general quadratic slopes and congruence classes; a
  classification of all weak records; novelty relative to the odd–odd continued fraction
  literature. See §11 and §12 of the note.
* The deposited file is the PDF only; the record links here for the LaTeX source, the
  certificate and the data. See [`docs/REVIEW_SUMMARY.md`](docs/REVIEW_SUMMARY.md) §6 for the
  remaining open items.

## Relationship to the 2026-08 note

`../paper/oscillator_records.{tex,pdf}` is the deposited baseline
(doi:[10.5281/zenodo.21796640](https://doi.org/10.5281/zenodo.21796640)) and is left
byte-identical. Its Conjectures 5.11 and 5.13 are resolved here; its Observations 5.9 and 5.12
overstate the height period, which is corrected here. Details:
[`docs/EARLIER_NOTE_STATUS.md`](docs/EARLIER_NOTE_STATUS.md).

## Licence

Note (`paper/`) and documentation (`docs/`): CC BY 4.0.
Code (`certificate/`) and data (`tables/`): MIT, see `../LICENSE`.
