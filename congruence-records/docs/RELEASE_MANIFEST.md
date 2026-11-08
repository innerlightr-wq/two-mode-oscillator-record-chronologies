# Release manifest — `congruence-records-v1.0.0`

The companion technical note and its certificate. The note is **deposited** at
doi:10.5281/zenodo.24046651 (2026-11-08); this repository holds the source, the
certificate and the data that the deposit does not. Prepared 2026-11-07.

---

## 1. Identity

| field | value |
|---|---|
| manuscript | *Odd/Odd Records for a Relative Approximation Error: Three Quadratic Classifications and an Exact Certificate* |
| manuscript version | `1.0.0` (rc1 superseded before deposit, see `CHANGELOG.md`) |
| certificate bundle version | `1.0.0`, derived from internal package v3 |
| author | Elias De Jesús, ORCID 0009-0007-0190-9143 |
| branch | `companion-odd-odd-records` |
| release tag | `congruence-records-v1.0.0` |
| release commit | not quoted here — a commit hash covers this file, so it cannot name itself. Resolve it with `git rev-parse congruence-records-v1.0.0^{commit}`, and cite the **tag** rather than the branch. |
| folder | `congruence-records/` (self-contained: `paper/`, `certificate/`, `tables/`, `docs/`) |
| source baseline | commit `10ea1c62c6866990ded0a85a531883841d38d034` ("Update README.md"), clean tree |
| DOI (version) | **10.5281/zenodo.24046651** — deposited 2026-11-08, CC BY 4.0 |
| DOI (concept) | 10.5281/zenodo.24046650 — resolves to the latest version |
| deposited file | `congruence_records_note.pdf`, 331326 bytes, md5 `45f52bbe39ba3bef82c064060c5d56e1` — **byte-identical to the PDF in this release** |

## 2. Source baseline, unchanged by this release

These files are byte-identical to the deposited 2026-08 version and are **not** touched:

```
f36c23ab099a7a0bca1e68dfe699ea02e15ef6e767bbc52428a77b272da247b3  paper/oscillator_records.pdf
6b616f79602393fd4560c0adbc2f789f47e9c8b13ca771ebe9d6f70e599295cd  paper/oscillator_records.tex
```

What has changed about their *claims* is recorded in `EARLIER_NOTE_STATUS.md`.
`code/`, `data/`, `docs/REPORT.md`, `LICENSE`, `CITATION.cff`, `SHA256SUMS` and `VERSIONS.txt`
are also unchanged.

## 3. Release artefacts and their hashes

Paths are relative to the repository root.

```
8aba33a7c5bb967dd5f6b3c142e593fb247a38636f1bd2c1a1704fb3c83ddf6f  congruence-records/paper/congruence_records_note.pdf   (17 pp., 331326 bytes)
2c142aeef418a4db9e175d0efa08ba974b1da1f8a9ed024f5f5bba638befed9d  congruence-records/paper/congruence_records_note.tex
121dd3c9482892bc717dfc3fd2e48c851871b8f40b6b1ff05b72d8ca6a1158e1  congruence-records/README.md
62cc4bf9d8a2e20991ace26b03d7d1271e0566a51806915b7a741a843907fa68  README.md                                             (updated: introduces both notes)
```

`congruence-records/SHA256SUMS` hashes all **33** files of the companion folder individually,
with paths relative to that folder. Verify with

```sh
cd congruence-records && sha256sum -c SHA256SUMS
```

It is not self-hashed. It *does* cover this manifest, so `SHA256SUMS` is regenerated last;
its own hash is therefore not quoted here, to avoid a circular reference.

A frozen archive of the whole folder is built, **after** the seal above, with

```sh
zip -r -X congruence-records-v1.0.0.zip congruence-records
```

Its sha256 is recorded at the repository root in `congruence-records-v1.0.0.zip.sha256`,
outside the folder, because the archive contains `SHA256SUMS` and so cannot be hashed from
inside it. The archive is the third file to upload at deposit; it is not committed, since the
folder itself is.

## 4. Build of the manuscript

```sh
cd congruence-records/paper
latexmk -pdf -interaction=nonstopmode -halt-on-error congruence_records_note.tex
```

Toolchain: TeX Live `pdflatex` with `latexmk`; packages `amsmath`, `amsthm`, `amssymb`,
`geometry`, `booktabs`, `longtable`, `array`, `hyperref`, `microtype`. The bibliography is a
`thebibliography` environment inside the `.tex`; no `.bib` file and no BibTeX run is needed.
The appendix `\input`s `../tables/classification.tex` and `../tables/exclusions_summary.tex`,
so those must exist; regenerate them with `python3 certificate/tables.py`.

**Outcome:** exit 0; 17 pages; **zero** overfull or underfull `\hbox` warnings, zero hyperref
warnings, zero undefined references or citations. Rendered pages were inspected individually;
the two 74-row and 67-row appendix tables paginate as `longtable` and are not clipped.

Build artefacts (`.aux`, `.log`, `.out`, `.fls`, `.fdb_latexmk`) are **not** committed.

## 5. Verification of the certificate — clean-extraction run

Procedure: the 15 bundle source files were copied into a fresh `certificate/` beside an
empty `tables/`, with no `__pycache__`; the five programs were then run in that directory, their
`stdout`+`stderr` captured, and the resulting `outputs/` and regenerated `tables/` compared
against the committed copies. They are byte-identical.

Environment: `certificate/outputs/ENVIRONMENT.txt` —
Linux 7.2.5-3-omarchy x86_64, Python 3.14.7, standard library only, no network.

| command | exit | wall | outcome |
|---|---|---|---|
| `python3 certificate.py` | 0 | 3 s | cutoffs 18 / 204 / 27; orbits 4 / 64 / 6; classification 1+1 / 3 / 1+1 strict-or-alternating; checks (S), (W1), (W2), (W3′), (R) all true; `U = 0` found 0 times |
| `python3 tail_table.py` | 0 | 2 s | `p0` = 2 / 2 / 3; largest pre-tail `H` = 22.3262 / 301.2628 / 45.5167; caps 23 / 302 / 46; states 41 / 4173 / 152 |
| `python3 hypotheses.py` | 0 | 0 s | H1 minimal admissible unit power 3 / 2 / 1, matching `rho`; H3 box bounds well inside the boxes actually searched |
| `python3 tables.py` | 0 | 1 s | 74 classification rows, 67 exclusion rows, every exclusion re-verified at `P`, `P+1`, `P+2` before emission |
| `python3 verify_records.py` | 0 | 313 s | **31 `[PASS]`, 0 `[FAIL]`, `VERIFY PASSED`** |

The 31 checks are C1–C11 over the three slopes plus C7 (the `phi` tie); C11 re-derives all
67 exclusion rows from the orbit each names and tests them at twelve consecutive periods. Captured outputs:
`certificate/outputs/{certificate,tail_table,hypotheses,tables,verify}_output.txt`.

## 6. Diff summary against the source baseline

Nothing in `paper/oscillator_records.*`, `code/`, `data/`, `docs/REPORT.md`, `LICENSE`,
`CITATION.cff`, root `SHA256SUMS` or `VERSIONS.txt` is modified.

```
 README.md                                            | modified (introduces both notes; conjecture numbering 5.11/5.13; truncated sentence completed; licence paragraph)
 .gitignore                                           | new
 congruence-records/README.md                         | new
 congruence-records/SHA256SUMS                        | new (38 files)
 congruence-records/paper/congruence_records_note.tex | new
 congruence-records/paper/congruence_records_note.pdf | new
 congruence-records/certificate/                      | new (15 programs and documents + outputs/)
 congruence-records/tables/                           | new (4 files)
 congruence-records/docs/                             | new (6 files)
```

In rc2 the companion material moved from the repository root into `congruence-records/`, and
`tables/` moved out of `certificate/` to sit beside it.

## 7. What is left to do before deposit

Mathematical: nothing is blocking. Administrative, all for the author:

1. `CITATION.cff` DOI placeholder (open item **O-1**).
2. `LICENSE` scope line (open item **O-2**).
3. Zenodo upload, publication date, DOI — `ZENODO_METADATA.md`.
4. After the DOI exists: update `README.md`, this manifest and `CITATION.cff`.
5. The commit is tagged `congruence-records-v1.0.0`; publish it as a GitHub release and cite
   that tag, not the branch, for the computations behind the published claims.
