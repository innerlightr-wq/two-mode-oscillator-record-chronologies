# Review summary — companion note release candidate `congruence-records-v1.0.0` (rc2)

For a reviewer deciding whether this is ready to deposit. Written to be read before the note.

---

## 1. What is claimed, and how strongly

| # | claim | strength | where |
|---|---|---|---|
| T-A | At `alpha = phi` the strict records are exactly `(F_{3j+1}, F_{3j+2})` together with `(L_{6j+4}, L_{6j+5})`, merged by height, defect cycle `(-1,+1,-5)` | **theorem** | note Thm 8.1 |
| T-B | At `alpha = 1+sqrt(3)` the strict records are exactly the three orbits of `[[3,4],[8,11]]` seeded at `(1,1)`, `(1,3)`, `(5,13)`, defects `-3, +1, -11` | **theorem** | note Thm 8.2 |
| T-C1 | At `alpha = sqrt(3)` the strict records are exactly the orbit of `(1,1)` under `[[2,1],[3,2]]`, defect `-2`, with `h^2 eps = 1/2` exactly | **theorem** | note Thm 8.3(i) |
| T-C2 | The companion family `(k, 3m)` has `eps` **exactly** equal to that of `(m,k)` at `sqrt(3)` times the height; these are weak records, never strict | **theorem** | note Thm 8.3(ii) |
| T-D | The norm cutoff `|N| <= 18 / 204 / 27` follows from height comparisons alone | **theorem** | note Thm 4.1 |
| T-E | The `phi` Fibonacci/Lucas competition is an exact tie at leading order, decided by `N_B = -5 N_A`; the Lucas state wins iff `n` is even | **theorem** | note Thm 8.4 |
| L-1 | Classification of all **weak** records | **not claimed**. T-C2 exhibits one infinite non-strict family; imprimitive weak records are not treated | note Def. 1.1 and §8 |
| L-2 | A uniform theorem for general quadratic `alpha` and general congruence classes | **not claimed**; three obstructions stated | note §12 |
| L-3 | Novelty relative to Kim–Lee–Liao / Elsner / Cha–Kim | **unresolved**. Only the comparisons actually made are reported; no systematic search was run | note §11 |
| L-4 | Any count of records per multiplicative height window | **explicitly not asserted** | note §9 |

## 2. What the proof depends on computationally

The argument is finite-plus-infinite: an exact certificate decides everything from a computed
period onward, and an unpruned enumeration covers everything below it. The two halves meet at:

| slope | finite region covered by unpruned enumeration | states enumerated | orbits classified | exclusions decided by exact sign |
|---|---|---|---|---|
| `phi` | `H <= 23` | 41 | 4 | 2 |
| `1+sqrt(3)` | `H <= 302` | 4173 | 64 | 61 |
| `sqrt(3)` | `H <= 46` | 152 | 6 | 4 |

So **Theorem B is computer-assisted in a way Theorem A is not**: 61 exclusions at `|N| <= 204`
against 2 at `|N| <= 18`. A reader who wants to check Theorem A by hand can; Theorem B realistically
requires running `tables.py` and checking rows. Appendix A of the note prints every row with
its orbit ID, its competitor's ID, the offset, the certified period `P` and both states at
`p = P`, so each row is independently re-derivable from Propositions 6.1–6.3 without re-running
a search — and check C11 does exactly that re-derivation for all 67 rows at twelve consecutive
periods.

Everything else is proved in closed form: the master identities, the imprimitivity reduction,
the cutoff, the bounded-rectangle enumeration, error monotonicity along orbits, the
`d in {0,1}` window, and the `Gamma_d = 0` three-way rule.

## 3. Verification status — read this before calling anything "verified"

* The certificate is **exact arithmetic in `Z[sqrt D]`**, with every ordering and comparison
  decided by integer sign tests. Floats are presort keys (with the sorted order re-verified
  exactly afterwards) and display.
* It is **not formally verified**. There is no proof-assistant development of any kind.
* The note has **not been refereed** and no human other than the author has reviewed it.
* Two adversarial audits of earlier bundle versions were run with an automated reviewer. They
  re-derived the classifications through separate orbit enumeration and tail logic, and they
  found real defects, listed in `CHANGELOG.md`. They **re-used this bundle's `quad.py`**,
  so they are independent in logic and control flow but not in the underlying arithmetic
  implementation.
* Clean-extraction run, this release: `verify_records.py` reports **31 `[PASS]`, 0 `[FAIL]`**
  and `VERIFY PASSED`, exit 0. Outputs in `../certificate/outputs/`.

## 4. The defects that were found and fixed (what a reviewer should spot-check)

Listed because each one was a claim that looked right and was not. Details in
`CHANGELOG.md` and `../certificate/README_PACKAGE.md`.

**Found in the pre-upload review of rc1, after the note was first compiled** — these are the
freshest and deserve the closest look:

0a. **Proposition 7.2 had no hypotheses and is false before the tail.** Exact search found 13
    violating pairs at `1+sqrt(3)`, all at `p = 0`; witness `B = (7,1)` with the defect-`+193`
    orbit's first positive state `(1,15)` sitting below it at period 1. The proposition now
    requires `p >= p0` with both hypotheses named, and Remark 7.3 prints the witness. The
    region containing every violation is inside the enumerated segment, so no bound moved.
0b. **The appendix was not re-derivable.** `N_rep` is not a unique orbit label — `-143` names
    four distinct orbits at `1+sqrt(3)` — and the reported period ignored the ordering
    threshold. An independent audit scored **66 of 67 rows unusable as stated**. Rows now
    carry orbit IDs, printed states, and a period that accounts for all three constraints,
    and check C11 re-derives every row.
0c. The weak-record definition was self-contradictory; the cutoff asserted `0 < u < 1` where
    `u = 0` (at `sqrt(3)`, `t = 0`); Theorem C(ii) never showed the companion precedes the
    next strict record. All three repaired.

Earlier rounds:

1. **The cutoff proof was wrong twice** before reaching its present form. The second version
   asserted that `F` is monotone in `Y`; at `phi` the two sign branches move in opposite
   directions. The *bounds* never changed — only the proof. Check Theorem 4.1 and
   Remark 4.2 carefully.
2. **A threshold had the wrong period coordinate**, producing 51 wrong predictions at
   `1+sqrt(3)`. The error and ordering thresholds still use different coordinates (`p` vs `q`),
   converted by `+d`. Check Section 6's closing paragraph and `tail_table.py`.
3. **Strict versus weak was not implemented at all** in an early version, which labelled the
   `sqrt(3)` norm-`+6` companion a strict record. That family is now Theorem 8.3(ii).
4. **A verifier check was vacuous** at `sqrt(3)` and printed `PASS`. Confirmed by a negative
   control; now asserts `k^2 - 3m^2 = 6 (mod 8)` and fails for an unhandled slope.
5. **`eta`-order is not height-order** across different defects. An early argument assumed it.
   Remark 2.2 of the note gives the counterexample `(3,1)` versus `(1,3)` at `phi`.
6. **The first-kind identification was withdrawn** and must not be reintroduced; see
   `EARLIER_NOTE_STATUS.md` §3.

## 5. Limitations the note states about itself

* No uniform theorem (§12), with an explicit counterexample to the naive generalisation of the
  imprimitivity step (`alpha = sqrt(6)`, class `(1,1) mod 3`, state `(4,10)`).
* The existence of a comparison ladder of *prescribed* norm is unproved; `L = 1, 1, 2` were
  found by inspection. A CRT construction gives *some* seed of computable norm, not a minimal one.
* Novelty unresolved (§11). In particular the note does **not** claim that its classifications
  fail to follow from Kim–Lee–Liao's machinery; it claims only that the objectives differ and
  that no reduction in either direction has been given. The concrete separation offered is one
  example: `11/7` is a strict record here and is not a best 1-rational approximation of `phi`.
* The Elsner comparison establishes that the odd/odd class is the acknowledged exceptional case
  of congruence-restricted Hurwitz theory (his Corollary 1.1 fails at `s = 2`, `h = 1`, witness
  `12 + sqrt(145)`); it does not establish that the present record set is new.

## 6. Blockers for deposit

| id | item | owner |
|---|---|---|
| **O-1** | `CITATION.cff` holds `doi: "10.5281/zenodo.XXXXXXXX"`, disagreeing with the `10.5281/zenodo.21796640` in `README.md`. It cannot be resolved from inside the repository — whether that is the concept or the version DOI is not determinable here. **Not guessed.** | author |
| **O-2** | `LICENSE` header scopes MIT to "code/ and data/"; `certificate/` is new MIT code and is not named. | author |
| **O-3** | Root `SHA256SUMS` covers the baseline files only; the release list is in `RELEASE_MANIFEST.md` rather than overwriting it. | author |
| **O-4** | Publication date, DOI reservation, and the upload itself. | author |

No blocker is mathematical.

## 7. One-line verdict

The three classifications are proved and exactly certified, the earlier note's two conjectures
are resolved and one of its assertions is corrected; the uniform theorem and the novelty
question are open and are presented as open.
