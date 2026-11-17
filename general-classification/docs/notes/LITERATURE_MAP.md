# Literature map: what is classical, what is a short corollary, what is new

Internal, 16 November 2026. Companion to `THEOREM_AND_PROOF.md`.
Searches were run on 16 Nov 2026; the four-way classification the brief asks for is applied to
each item. **A failed search is not evidence of novelty** and is not used as such below.

---

## 1. Available verbatim (classical; used as a black box)

**1.1 Finiteness of the orbits of a given value under the automorph group, and an explicit
bounded region containing a representative of each.** This is the reduction theory of the
generalised Pell equation `Q(m,k) = n` for an indefinite integral binary quadratic form
(Lagrange/Gauss; textbook form in the Stanford Math 154 handout *Generalized Pell equation*,
Thms 1.1 and 2.1, which the published note already cites). Mapping: our `Q = Ak²+Bmk+Cm²` is
the form, `X₀` of §2 is its proper automorph from `T² − ΔU² = 4`, and Prop 5.1 is Thm 2.1's
box written in the `(η, ξ)` embedding. **No class-number or principal-ideal input is used**;
the published note's earlier PID framing was unnecessary and is not reinstated.

**1.2 The automorph group of an indefinite form is `{±1} × ⟨X₀⟩`.** Classical. We use only
the proper part `⟨X₀⟩` (Remark 2.2), and we must keep the `−I` translate of each representative
as a *separate* orbit because `−I ∉ ⟨P⟩` and `−I` need not preserve `R`.

**1.3 Klein sails and best approximations — with two corrections to the mapping.** In the
geometric (Klein) picture the best rational approximations of a real number are exactly the
lattice points on the sails of the corresponding cone, with the unit group acting on the sail.
Two things must be said carefully about how our setting maps onto it.

*(i) The admissible set is a union of cosets, not generally a sublattice.* `R ⊆ (Z/M)²` is an
arbitrary nonempty subset, so `{(m,k) : (m,k) mod M ∈ R}` is a **union of `|R|` cosets** of the
sublattice `MZ²`; it is a sublattice only when `R` is a subgroup containing `(0,0)`. What our
`⟨P⟩` is, correctly stated: `P ≡ I (mod M)` makes `⟨P⟩` a finite-index subgroup of the proper
automorph group that fixes **every** coset individually, which is why each admissible coset is
`⟨P⟩`-invariant and the orbit bookkeeping goes through. The sail picture then applies coset by
coset, not to a single sublattice. An earlier version of this file said "sublattice"; that is
**withdrawn**.

*(ii) The height differs.* Our order is by `H = mα + k`; the sail/best-approximation picture
orders by the denominator. So even for a single coset the two selections are not the same
ordering, and Proposition 0.1 is the only bridge established here — in one direction, and it
needs the explicit argument given there rather than a citation.

With those two qualifications, 1.3 is the classical backbone of stages A–D and is where the
*finiteness and periodicity* come from. See Karpenkov, *Geometry of Continued Fractions*, and
the arXiv preprints below. **It does not supply the record criterion**: see §3.1.

**1.4 Lagrange's theorem (periodicity of the continued fraction of a quadratic irrational)**
is the shadow of 1.1–1.3 and is not used directly: nothing here passes through the continued
fraction of `α`.

---

## 2. Short corollaries of classical material

**2.1 Proposition 0.1** (every congruence-restricted classical best approximation is an
`ε`-record). One line from `ε = |ξ|/H` once `|ξ|` decreases and `H` increases. **The notion of
"best approximation" here is the one defined in §0 — running minima of `|ξ|` among admissible
states listed by increasing `H`** — and not the denominator-ordered notion of the cited parity
papers. Relating it to the sail vertices, or to Kim–Lee–Liao's Definition 1.1, needs a separate
bridge between the two orders, which is **not** supplied here; the measurement below compares
the two sets as computed under our own height order. Verified, with
explicit extra records at `φ`, `1+√3`, `√2`, `3x²−x−1`, `√6 mod 3`, and with equality below the
tested cap at `√3` (`lit_bridge` L2).

**2.2 The `tanh` identity** `ε = |tanh(½ log(k/(mα)))|`. Immediate, but it is the statement
that identifies the objective: records minimise the **multiplicative** error `|log(k/m) − log α|`
under the weighted height `mα+k`. This places the problem in relative/multiplicative
approximation rather than in the `|qx − p|`-with-height-`q` tradition.

**2.3 Corollary 7.1** (`H²ε → 2α|Q|/√Δ` along a fixed-defect orbit) is the published note's
accumulation corollary, re-derived in the general normalisation.

---

## 3. New effective formulations of classical structure (this round)

**3.1 The objective is not any of the standard ones, and no transfer may be assumed.**
* *Best `1`-rational approximation* (Kim–Lee–Liao, *Odd–odd continued fraction algorithm*,
  Monatsh. Math. **198** (2022) 323–344, Def. 1.1 and Thm 1.2; and *Diophantine approximation
  by rational numbers of certain parity types*, Mathematika **71** (2025) e12285): the
  objective is `|qx − p|` ordered by `q`, with `p,q` odd and coprime. Our objective is
  `|mα − k|/(mα + k)` ordered by `mα + k`, with no coprimality. The published note's witness
  stands and is reproduced here: at `φ`, `(7,11)` is a strict `ε`-record while
  `|3φ−5| < |7φ−11|` with `3 < 7`, so `11/7` is not a best `1`-rational approximation.
* *Hurwitz-type theorems with congruence conditions* (Hartman; Koksma 1951; Uchiyama; Elsner,
  Fibonacci Quart. **38** (2000) 24–33): these bound an approximation constant; they do not
  enumerate a record set. Elsner's Thm 1.1 needs the modulus to have an odd prime divisor and
  his Cor. 1.1 **fails** for modulus `2` with `h = 1`, i.e. exactly the odd/odd class, with
  witness `ξ = 12 + √145`. So the odd/odd case is the acknowledged exceptional case of that
  line — a point in favour of treating it directly, as here.
* *Intrinsic approximation on the circle* (Cha–Kim, Ann. Inst. Fourier **73** (2023) 101–161):
  different space, different height, asymptotic spectrum rather than a record list. No
  reduction in either direction is claimed.

**3.2 Theorem 4.1 (the cutoff) in its general form.** The inequality
`|Q_{B*}| < |Q_A|(H_C/H_A)²(1 + θ_A)` with no sign hypotheses, and its certified tail bound,
is an effective statement that I have not found in the above sources, and it is the step that
makes the infinite problem finite. Classical reduction theory gives finiteness *at a given
defect*; it does not bound the defect of a record.

**3.3 The congruence bookkeeping as a finite-index subgroup acting on a sublattice**
(Lemma 2.1, Prop 5.2) is classical in spirit (1.3) but the *effective* form — enumerate in the
fundamental domain of `λ`, then split into the `j` translates and keep the admissible ones — is
what makes the cost `O(λ·B)` rather than `O(λ^j·B)`, and is the practical content.

---

## 4. Genuinely unproved extensions / unsettled questions

0. **The `H`-order versus the denominator order.** Converting between "running minima of
   `|ξ|` ordered by `H`" and the classical "ordered by `q`" notion is an unresolved bridge, and
   until it is supplied no statement here may be read as a claim about best `1`-rational
   approximations in the sense of Kim–Lee–Liao, Definition 1.1.
1. **Is the objective itself new?** Unsettled. Targeted searches for the relative error
   `|mα−k|/(mα+k)` ordered by `mα+k`, with congruence restrictions, returned nothing matching;
   that is not evidence of novelty. The honest statement: the objective is a *weighted,
   multiplicative-metric* best-approximation problem on a congruence sublattice, and such
   problems are a recognised family (1.3, 3.1), so a prior treatment is plausible and has not
   been excluded. The specific literature to read next: Karpenkov's sail machinery for
   sublattices, and the "best approximation with respect to a general norm/weight" line.
2. **Does the record criterion have a sail-theoretic description?** Prop 0.1 gives only an
   inclusion. A description of the extra records as a secondary structure on the sail (they are
   the points where `|ξ|` increases but `H` increases faster) is not formulated here.
3. **Lagrange-spectrum analogue.** The accumulation values `2α|Q|/√Δ` at records are computed,
   but the envelope of `H ↦ H²ε` *between* records — the analogue of a Lagrange/Markov
   spectrum for this objective — is untouched, in this round and in the published note.
4. **Non-quadratic `α`.** Outside the method entirely.

---

## Sources consulted in this round

- [Geometry of Continued Fractions (Karpenkov) — overview](https://www.academia.edu/15076616/Geometry_of_Continued_Fractions)
- [Rational approximations, multidimensional continued fractions and lattice reduction (arXiv:2303.07777)](https://arxiv.org/pdf/2303.07777)
- [Constructing multidimensional periodic continued fractions in the sense of Klein (arXiv:math/0411031)](https://arxiv.org/pdf/math/0411031)
- [Rational approximation of the maximal commutative subgroups of GL(n,R) (Karpenkov)](http://pcwww.liv.ac.uk/~karpenk/mytexts/ok13_p09.pdf)
- [Diophantine approximation by rational numbers of certain parity types (arXiv:2403.12341)](https://arxiv.org/pdf/2403.12341)
- [The Arithmetic of Binary Quadratic Forms (Bonn, bachelor thesis notes)](https://www.math.uni-bonn.de/people/toma/notes/BA-korrigiert.pdf)
- [Reduction of binary quadratic forms (ETH notes)](https://metaphor.ethz.ch/x/2021/hs/401-3110-71L/ex/Eleventh.pdf)
- Cited from the published note and not re-fetched: the Stanford Math 154 *Generalized Pell
  equation* handout; Kim–Lee–Liao (2022, 2025); Elsner (2000); Cha–Kim (2023).
