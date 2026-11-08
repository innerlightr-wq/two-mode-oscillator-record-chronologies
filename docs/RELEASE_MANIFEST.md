# Release manifest — `companion-1.0.0-rc1`

Release candidate for the companion technical note. **Nothing here has been published, pushed
or deposited.** Prepared 2026-11-07.

---

## 1. Identity

| field | value |
|---|---|
| manuscript | *Odd/Odd Records for a Relative Approximation Error: Three Quadratic Classifications and an Exact Certificate* |
| manuscript version | `1.0.0` (release candidate 1) |
| certificate bundle version | `1.0.0`, derived from internal package v3 |
| author | Elias De Jesús, ORCID 0009-0007-0190-9143 |
| branch | `companion-odd-odd-records` |
| source baseline | commit `10ea1c62c6866990ded0a85a531883841d38d034` ("Update README.md"), clean tree |
| DOI | **none** — not deposited; see `docs/ZENODO_METADATA.md` |

## 2. Source baseline, unchanged by this release

These files are byte-identical to the deposited 2026-08 version and are **not** touched:

```
f36c23ab099a7a0bca1e68dfe699ea02e15ef6e767bbc52428a77b272da247b3  paper/oscillator_records.pdf
6b616f79602393fd4560c0adbc2f789f47e9c8b13ca771ebe9d6f70e599295cd  paper/oscillator_records.tex
```

What has changed about their *claims* is recorded in `docs/EARLIER_NOTE_STATUS.md`.
`code/`, `data/`, `docs/REPORT.md`, `LICENSE`, `CITATION.cff`, `SHA256SUMS` and `VERSIONS.txt`
are also unchanged.

## 3. Release artefacts and their hashes

```
4dcd3d6ddb21b9dbb68da359b772119ce9739e085960cb34b693d9af97ce0d20  paper/congruence_records_note.pdf   (16 pp., 324169 bytes)
35c15dcea91fa11ef126fc8d612e8ac555ffeb5d4daed38410ec6d8c0f579122  paper/congruence_records_note.tex
66148c9c481fad892c9e4cd98bb8be6108a05aa0456b4039f392079c52ceb4a8  README.md                           (updated)
1d0957a464499b4dc319fd91168bb74118c0eefc1472a276c7c53d8f57a427dd  docs/CHANGELOG.md
f04eac2b4a6fc1ee46a0f3d88cfafb93d1f01086a348659c47eaa7f0f5c88cc8  docs/EARLIER_NOTE_STATUS.md
b8235604ed8bcd1300b5be08c3adb131fcb575e56fc8f2d0d469a75503b27806  docs/LICENSE_AND_SOURCE_INVENTORY.md
27c7804338852188434a7a7708f89185445888afe84b214ab589a885a4671fa5  docs/REVIEW_SUMMARY.md
c3bb5b5a63774bac9a1dfbf43cb6ba08a1bc95141d77341e117b4e8fda42f797  docs/ZENODO_METADATA.md
374bf36f8f39d0665ac7661e8008427d331ef5046e29294e5fa340ccec1e8dca  certificate/SHA256SUMS
```

The 24 files of the certificate bundle are hashed individually in `certificate/SHA256SUMS`;
verify with `sha256sum -c SHA256SUMS` from inside `certificate/`. (This manifest is not listed
in its own hash table, and `docs/RELEASE_MANIFEST.md` is not self-hashed.)

A packaged copy of the bundle, built with `zip -r -X certificate-bundle-1.0.0.zip certificate`
excluding `__pycache__`, has sha256

```
ed22240048bf1f642ee14404b8f138c6715e43314f704c8d6c86c54afc158cc7  certificate-bundle-1.0.0.zip
```

It is held outside the repository (it is a build product of `certificate/`, which is committed
in full) and is the third file to upload at deposit.

## 4. Build of the manuscript

```sh
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error congruence_records_note.tex
```

Toolchain: TeX Live `pdflatex` with `latexmk`; packages `amsmath`, `amsthm`, `amssymb`,
`geometry`, `booktabs`, `longtable`, `array`, `hyperref`, `microtype`. The bibliography is a
`thebibliography` environment inside the `.tex`; no `.bib` file and no BibTeX run is needed.
The appendix `\input`s `../certificate/tables/classification.tex` and
`../certificate/tables/exclusions_summary.tex`, so those must exist; regenerate them with
`python3 certificate/tables.py`.

**Outcome:** exit 0; 16 pages; **zero** overfull or underfull `\hbox` warnings, zero hyperref
warnings, zero undefined references or citations. Rendered pages were inspected individually;
the two 74-row and 67-row appendix tables paginate as `longtable` and are not clipped.

Build artefacts (`.aux`, `.log`, `.out`, `.fls`, `.fdb_latexmk`) are **not** committed.

## 5. Verification of the certificate — clean-extraction run

Procedure: the 14 bundle source files were copied into an empty directory containing no
`__pycache__` and no `tables/`; the five programs were then run in that directory, their
`stdout`+`stderr` captured, and the resulting `outputs/` and regenerated `tables/` compared
against the committed copies. They are byte-identical.

Environment: `certificate/outputs/ENVIRONMENT.txt` —
Linux 7.2.5-3-omarchy x86_64, Python 3.14.7, standard library only, no network.

| command | exit | wall | outcome |
|---|---|---|---|
| `python3 certificate.py` | 0 | 4 s | cutoffs 18 / 204 / 27; orbits 4 / 64 / 6; classification 1+1 / 3 / 1+1 strict-or-alternating; checks (S), (W1), (W2), (W3′), (R) all true; `U = 0` found 0 times |
| `python3 tail_table.py` | 0 | 2 s | `p0` = 2 / 2 / 3; largest pre-tail `H` = 22.3262 / 301.2628 / 45.5167; caps 23 / 302 / 46; states 41 / 4173 / 152 |
| `python3 hypotheses.py` | 0 | 0 s | H1 minimal admissible unit power 3 / 2 / 1, matching `rho`; H3 box bounds well inside the boxes actually searched |
| `python3 tables.py` | 0 | 0 s | 74 classification rows, 67 exclusion rows |
| `python3 verify_records.py` | 0 | 317 s | **28 `[PASS]`, `VERIFY PASSED`** |

The 28 checks are C1–C10 over the three slopes plus C7 (the `phi` tie). Captured outputs:
`certificate/outputs/{certificate,tail_table,hypotheses,tables,verify}_output.txt`.

## 6. Diff summary against the source baseline

Added, nothing removed, nothing in `paper/oscillator_records.*` or `code/` or `data/` modified:

```
 README.md                                  | modified (companion section; conjecture numbering 5.11/5.13; truncated sentence completed; licence paragraph)
 docs/CHANGELOG.md                          | new
 docs/EARLIER_NOTE_STATUS.md                | new
 docs/LICENSE_AND_SOURCE_INVENTORY.md       | new
 docs/RELEASE_MANIFEST.md                   | new (this file)
 docs/REVIEW_SUMMARY.md                     | new
 docs/ZENODO_METADATA.md                    | new
 paper/congruence_records_note.tex          | new
 paper/congruence_records_note.pdf          | new
 certificate/                               | new (24 files)
```

## 7. What is left to do before deposit

Mathematical: nothing is blocking. Administrative, all for the author:

1. `CITATION.cff` DOI placeholder (open item **O-1**).
2. `LICENSE` scope line (open item **O-2**).
3. Zenodo upload, publication date, DOI — `docs/ZENODO_METADATA.md`.
4. After the DOI exists: update `README.md`, this manifest and `CITATION.cff`, then tag.
