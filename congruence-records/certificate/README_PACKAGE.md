# Proof package v3: congruence-restricted record chronologies (2026-11-07)

Third freeze.  **v3 exists because an independent re-audit of v2 found three further defects;
all three are repaired here.**  Lineage, all retained as audited baselines:

| version | sha256 | status |
|---|---|---|
| v1 | `a9fda5b01a6cca673b225bd67c5adce86535df856a4da38d2812e08758510eaf` | audited; 6 material defects (F1-F7) |
| v2 | `10ca883566637cc4bcd80c8e4a0f050214c949e44e91d7033d964319122d36bf` | F1-F7 repaired; re-audited; 3 defects (R1-R3) |
| **v3** | this archive | R1-R3 repaired |

Local, unpublished.  Source repository `two-mode-oscillator-record-chronologies` untouched at
commit `10ea1c6`, clean tree.

## Exact verification command and environment

```sh
python3 verify_records.py      # OUTPUT_verify_records.txt -> 28 [PASS], "VERIFY PASSED"
python3 certificate.py         # OUTPUT_certificate.txt
```

Standard library only; no network; no data files read at runtime.  Every ordering and comparison
is an exact sign test in Z[sqrt D]; floats are display and presort keys only, and the two places
an earlier version let a float into a decision (the C10 comparison, the C5 box size) now use
exact enclosures.

## What changed from v2

| re-audit finding | repair |
|---|---|
| **R1** the cutoff sampled six ladder states and justified it with "F is monotone in Y", which is **false** -- at phi the n = -1 branch increases while the n = +1 branch decreases | replaced by the audit's **sign-separated proof**.  phi, n = -1: F = R^2(1-u/R^2)^2(1+2u)/(1+u)^2 **< R^2 = 17.9442719100** since both correction factors are < 1; phi, n = +1: F = R^2(1+u/R^2)^2/(1-u)^2 is increasing in u, hence maximal at the first positive-norm predecessor Y = phi^8, giving **18.1960225537**; 1+sqrt(3): increasing in u, maximal at the first ladder state, **204.5520518132**; sqrt(3): t = 0 gives F = L R^2 **identically**, 27.8564064606.  Bounds **18 / 204 / 27 unchanged**; `cutoff` now evaluates only the proved endpoints |
| **R2** C2 had branches for phi and 1+sqrt(3) only, so for sqrt(3) it asserted **nothing** and printed PASS (the audit confirmed it passed when fed an invalid norm) | explicit sqrt(3) branch asserting **k^2 - 3m^2 = 6 (mod 8)**, plus an else-branch that fails rather than silently passing for any future slope.  Negative control run here: corrupting the norm makes C2 **FAIL**, as it must |
| **R3** superseded code and wording | `orbits.decide` and `sigma_gt` **deleted** (they mislabelled the sqrt(3) companion; `certificate.classify` is authoritative); `cmp_frac` now imported in `certificate.py`; section 4 rewritten with no trace of the old formula, the cutoff 23, the norm-19 window, or the count 63; exclusion counts corrected to **2 / 61 / 4** at cutoffs 18 / 204 / 27; the Gamma = 0 rule is now explicit wherever section 5's leading-score conditions are used, and the closing proof sentence no longer says "records in every period" (the phi Lucas family is **alternating**); `THEOREM_TARGET.md` no longer calls V constant in q, and its scope is narrowed -- see below; references to files not shipped in the package removed |

The re-audit's scripts (`audit_v2_checks.py`, `cutoff_endpoints.py`, `remaining_checks.py`) were
run against v2 and reproduced every finding before anything was changed.

## Two separate verdicts

**(1) The three classifications** -- Theorems A (phi), B (1+sqrt3), C (sqrt3, **strict** records).
Both independent audits recover exactly these families.

| slope | cutoff | orbits | strict | alternating | permanent equality | excluded |
|---|---|---|---|---|---|---|
| phi | 18 | 4 | N = -1 | N = +5 (Lucas, records every other period) | -- | 2 |
| 1+sqrt(3) | 204 | 64 | N = -3, +1, -11 | -- | -- | 61 |
| sqrt(3) | 27 | 6 | N = -2 | -- | N = +6 (eps exactly equal forever) | 4 |

Note the labels are the **normalised representative's** norm; at phi the actual winning Lucas
states have N = -5 and the unit family's norm alternates, since Norm(rho) = Norm(phi^3) = -1.

**(2) The proposed uniform theorem** (`THEOREM_TARGET.md`) -- **not** claimed proved, and its
scope is now stated narrowly.  The arguments use **t >= 0 and alpha' < 0**, and section 1's
imprimitivity reduction is **specific to odd/odd**: primitive residues do not give primitive
states.  At alpha = sqrt(6) with (m,k) = (1,1) mod 3, the state (4,10) is a strict record in the
class although gcd = 2, and its reduction (2,5) leaves the class (verified here).  Odd/odd is
special because the gcd is odd.  Existence of *some* known-norm seed is easy (a CRT construction
supplied by the audit); a prescribed or minimal |L| is the hard part, and L = 1, 1, 2 here were
found by inspection.

## Files

Proof-bearing: `certificate.py`, `orbits.py`, `setups.py`, `quad.py`, `verify_records.py`.
Required by C8/C9: `brute.py`, `candidates.py`.  Not proof-bearing: `hypotheses.py`.
Documents: `PROOF_OR_OBSTRUCTION.md`, `THEOREM_TARGET.md`.  Output: `OUTPUT_*.txt`.

## Known limitations

* Theorem B is computer-assisted in a way Theorem A is not: 61 exclusions at |N| <= 204 against
  2 at |N| <= 18.
* The uniform theorem is unproved, with the scope caveats above.
* Novelty unresolved: Kim-Lee-Liao solve the second-kind odd/odd problem (strictly smaller record
  set); Elsner's congruence-restricted Hurwitz theory explicitly excludes s = 2; Cha-Kim concerns
  the Lagrange spectrum of S^1.  No systematic search was run.
* Both audits reuse this package's `quad.py` arithmetic; they are logical/code audits, not formal
  verification.  No Lean proof exists.
