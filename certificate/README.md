# Certificate bundle — odd/odd records for a relative approximation error

Reproducibility bundle for the technical note

> E. De Jesús, *Odd/Odd Records for a Relative Approximation Error: Three Quadratic
> Classifications and an Exact Certificate*, 2026.
> ORCID: [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143)
> Source: `paper/congruence_records_note.tex`, PDF: `paper/congruence_records_note.pdf`.

The bundle is **self-contained**: Python standard library only, no third-party packages, no
network access, no data files read at runtime. Everything is recomputed from the definitions.

## Problem

For `alpha > 1` and positive **odd** integers `m, k`,

```
H = m*alpha + k          (height; h = H/2)
eps = |m*alpha - k| / (m*alpha + k)       (relative error)
```

A state is a **strict chronological record** if its `eps` is strictly smaller than that of
every admissible state of strictly smaller height. The bundle proves, with an exact finite
certificate, the complete strict-record classification at `alpha = phi`, `alpha = 1 + sqrt(3)`
and `alpha = sqrt(3)`.

## Exact commands

Run from this directory. Wall-clock figures are from the machine recorded in
`outputs/ENVIRONMENT.txt`.

```sh
python3 certificate.py    > outputs/certificate_output.txt     # ~4 s    the proof certificate
python3 verify_records.py > outputs/verify_output.txt          # ~5 min  28 independent checks
python3 tail_table.py     > outputs/tail_table_output.txt      # ~2 s    Section 7 finite-check table
python3 hypotheses.py     > outputs/hypotheses_output.txt      # ~1 s    H1/H3 side checks
python3 tables.py                                              # ~1 s    regenerates tables/
```

`verify_records.py` prints one `[PASS]`/`[FAIL]` line per check and ends with `VERIFY PASSED`;
it exits non-zero on any failure. The shipped `outputs/` were captured by running the four
programs in a **clean extraction** of this bundle (an empty directory holding only the files
listed below, with no `__pycache__` and no pre-existing `tables/`).

To check file integrity:

```sh
sha256sum -c SHA256SUMS
```

## Files

| file | role |
|---|---|
| `quad.py` | exact arithmetic in `Z[sqrt D]`: integer-only sign tests, comparison of fractions |
| `setups.py` | the three slopes, the defect form `N`, the admissible lattice and the admissible unit |
| `orbits.py` | bounded-rectangle enumeration of admissible primitive unit orbits |
| `certificate.py` | **proof-bearing**: cutoff, `Gamma_d`, the tie rule, the `U`/`V` height order, the four-way classification |
| `verify_records.py` | **independent verifier**: 28 checks C1–C10 across the three slopes |
| `brute.py` | independent unpruned enumeration, written from the problem statement only |
| `candidates.py` | justified-pruned scan (solves for `k` from `N`), cross-checked against `brute.py` |
| `tail_table.py` | the finite-check table of Section 7 of the note |
| `tables.py` | emits `tables/` (per-orbit classification and exclusion witnesses) |
| `hypotheses.py` | side checks of H1 (admissible unit power) and H3 (box bounds); **not** proof-bearing |
| `PROOF_OR_OBSTRUCTION.md` | the proofs, sections 0–8 |
| `THEOREM_TARGET.md` | the proposed uniform theorem, **stated as a target, not proved**, with its scope restrictions |
| `README_PACKAGE.md` | audit lineage v1 → v2 → v3 and what each re-audit changed |
| `tables/` | `classification.csv/.tex`, `exclusions.csv/.tex` (74 and 67 rows) |
| `outputs/` | captured outputs of the clean-extraction run, plus `ENVIRONMENT.txt` |

## Results

| slope | cutoff \|N\| | orbits | strict | alternating | permanent equality | excluded |
|---|---|---|---|---|---|---|
| `phi` | 18 | 4 | 1 (`N = -1`) | 1 (`N_rep = +5`, Lucas) | 0 | 2 |
| `1+sqrt(3)` | 204 | 64 | 3 (`N = -3, +1, -11`) | 0 | 0 | 61 |
| `sqrt(3)` | 27 | 6 | 1 (`N = -2`) | 0 | 1 (`N_rep = +6`) | 4 |

Labels are the **normalised representative's** signed norm. At `phi` the admissible unit is
`rho = phi^3` with `Norm(rho) = -1`, so the norm alternates along an orbit: the Lucas states
that actually record have `N = -5`, reached at the other period parity.

## What is and is not established

* The three classifications are **proved**, with the finite content isolated here.
* The verification is **exact arithmetic, not formal verification**: there is no proof-assistant
  development, and the note has not been refereed.
* The proposed **uniform theorem** (`THEOREM_TARGET.md`) is **not** proved. Its three
  obstructions are stated there: sign conditions (`t >= 0`, `alpha' < 0`), the odd/odd-specific
  imprimitivity reduction (counterexample at `alpha = sqrt(6)`), and the existence of a
  comparison ladder of prescribed norm.
* **Novelty is unresolved.** See Section 11 of the note for the comparisons actually made with
  Kim–Lee–Liao, Elsner and Cha–Kim. No systematic literature search was performed.

## License

MIT (same as `code/` and `data/` of the parent repository; see `../LICENSE`).
