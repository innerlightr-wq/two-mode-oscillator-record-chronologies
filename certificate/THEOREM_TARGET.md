# The general theorem, as a target to prove -- not as something three examples establish

Three worked slopes are three worked slopes.  This file states what a general theorem would
have to say, what is already in hand, and what is missing, so that the gap is visible rather
than implied.

## Target statement

> **Target.**  Let alpha > 1 be a quadratic irrational with minimal polynomial x^2 - tx - s,
> conjugate alpha', Delta = t^2 + 4s, and let C be a primitive congruence class condition on
> (m,k) (here: both odd).  Suppose the hypotheses H1-H4 below hold.  Then the **strict** records
> of eps = |m alpha - k|/(m alpha + k), ordered by h = (m alpha + k)/2, form **finitely many
> unit-orbit tails beyond an effectively computable height**, and a finite exact certificate
> determines (a) those tails, (b) every initial exception, and (c) every equality case.

The "equality case" clause is not decoration: at alpha = sqrt(3) the norm-6 companion family
has **permanently identical** eps to the norm -2 record ladder, so it supplies
weak records forever and is excluded only by strictness.  A statement omitting (c) would be
false as an "and nothing else" claim about weak records.

## The four things it must deliver, and their present status

**H1 -- an admissible comparison ladder.**  A unit power rho preserving the class C and
primitivity, plus one admissible primitive state of known norm L on which to anchor the cutoff.
*Status: **PROVED effectively**.*  u acts on O = Z + Zw by U in GL_2(Z); mod M,
U lies in the finite group GL_2(Z/M), so U^j = I mod M for some j <= |GL_2(Z/M)|, and
multiplication by u^j is then the identity mod M -- preserving every congruence class,
primitivity, and (for Norm(u^j) = +1) the norm.  For odd/odd, M = 2 and j <= 6.  The minimal
admissible power may be smaller than the order of U, since the class need only be fixed.  rho is the least power of the
fundamental unit acting trivially on C inside (O/2)^*, computed case by case:
phi -> phi^3, 1+sqrt(3) -> (2+sqrt3)^2, sqrt(3) -> 2+sqrt3.  **Norm one is not required**: sqrt(3) has no norm +-1 admissible state at all and the method still runs with
L = 2.  What is missing is a general construction of (rho, L) from (alpha, C) -- a statement
about the image of the unit group in (O/2)^* together with the norms represented in C.

**H2 -- an effective norm bound, with the initial range handled.**  *Status: proved, conditional
on H1 -- but the proof had to be replaced.*  The first version bounded |N| via an eta-bracket
justified by a fixed-N derivative of the height, which orders nothing across norms (external
audit F1).  The correct argument works entirely with heights: with eps_B < eps_A and
H_B <= H_C,

> |N_B| < H_C^2 eps_A (dd + t eps_A)/(2 alpha) = L (H_C/H_A)^2 (dd + t eps_A)/(dd + t sign(n) eps_A),

evaluated exactly at the first ladder states.  This gives **18, 204, 27** in the three cases,
sharpening the phi bound from the 23 the earlier argument produced.  The "initial range" is exactly the states below
the first ladder member, which must go into the finite check.

**H3 -- complete orbit enumeration.**  *Status: **PROVED, with no PID or class-number
hypothesis**.*  Reduce eta into [1, rho); then |xi| = |N|/eta <= B automatically,
so (eta, xi) lies in [1, rho) x [-B, B] and m = (eta - xi)/sqrtDelta,
k = (alpha eta - alpha' xi)/sqrtDelta are explicitly bounded.  An exhaustive search over that
box finds every orbit.  My earlier PID framing was unnecessary; unique factorisation appears in
the write-up only to *describe* orbits.  This is the classical generalized-Pell reduction
(*Generalized Pell equation*, Math 154 handout, Stanford University, Thms 1.1 and 2.1; the handout carries no printed author line).  Reduced representatives with
negative coordinates must be kept -- their forward orbit enters the positive region later.

**H4 -- a certified chronology.**  Height ordering, error comparisons, permanent ties, and the
threshold beyond which the pattern repeats under rho.  *Status: assembled, with the pieces now
stated separately rather than bundled:*

* **(W1)** eps strictly decreasing along each orbit;
* **(W2)** representatives normalised into [1, rho), which is what forces the relevant period
  offset into {0,1};
* **(W3')** a pairwise certified cross-orbit height ordering.  The naive version
  (eta-ordering = h-ordering where 2 alpha eta^2 > t|N|) is a fixed-N derivative and is
  **insufficient across norms** -- see section 5 of PROOF_OR_OBSTRUCTION.md for an exact counterexample at phi.  The
  certificate instead decides sign(h_B - h_A) = sign(rho^{2q} U - V) with U constant in q and V = delta^q t(delta^d N_B rA - N_A rB rho^d) parity-dependent when
  delta = -1 (external v2 audit R3);
* **(CRIT)** eps_B < eps_A iff 2 alpha Gamma > t(|N_A| N_B - |N_B| N_A), with
  Gamma_d = |N_A| rB^2 rho^{2d} - |N_B| rA^2 constant in the period, so one exact sign per
  (pair, d) once rho^{2p-2d}|Gamma_d| strictly dominates the bounded right side -- the
  threshold starts at p = d with factor rho^0 = 1, and an earlier implementation
  pre-multiplied by rho^{2d}, mispredicting 51 comparisons at 1+sqrt(3) (audit F2).  The two
  threshold functions use different period coordinates (q = p - d), so combining them needs
  max(P_error, Q_order + d) (audit F3).  When **Gamma_d = 0** the comparison is the integer
  condition in the norms alone, with a **three-way** outcome: for t = 0 it is exact EQUALITY,
  not a loss, which is what the sqrt(3) companion family realises (audit F4).

## Corollary that comes with it

    h^2 eps = alpha|N|/(2 sqrtDelta) - t N|N|/(4 sqrtDelta eta^2)  ->  alpha|N|/(2 sqrtDelta),

so once the surviving families are known their accumulation values follow immediately.  Note these are values **at** records, not the staircase envelope.

## What would make this a theorem rather than a programme

**H1-H4 are proved in the setting actually used, which is narrower than "a general monic
quadratic with a general congruence class"** -- an earlier draft of this file claimed the wider
scope, and that is withdrawn (external v2 audit R7).  The proofs use:

* **t >= 0 and alpha' < 0**, so that eta > 0 on positive states and x -> x(D0 + t x) is
  increasing.  Other sign patterns need explicit changes.
* **the odd/odd class specifically** in section 1's reduction.  Primitive *residues* do not give
  primitive *states*: at alpha = sqrt(6) with the class (m,k) = (1,1) mod 3, the state (4,10) is
  a strict record in the class although gcd = 2, and its reduction (2,5) leaves the class
  (verified).  Odd/odd is special because the gcd is odd, so dividing it preserves the class.
  A general statement must either quantify over primitive states or keep imprimitive
  bounded-norm orbits.

With that scope fixed, what remains is:

1. **Assemble it uniformly.**  Each piece is proved for a general monic quadratic with a general
   mod-M class, but the write-up above still reasons through three worked slopes.  A uniform
   statement needs the quantifiers put in order and the finite-check region described in general
   (it is "everything below the max of the cutoff, Gamma-decidedness and ordering thresholds",
   all three of which are explicit functions of (alpha, C, L, rho)).
2. **Decide which (alpha, C) admit a ladder at all.**  H1 produces rho; it does **not** produce
   an admissible state of known norm L to anchor the cutoff on.  **Existence is easier than I
   claimed**: for an ordinary residue pair (a,b) mod M, some positive primitive seed exists iff
   gcd(a,b,M) = 1 -- pick positive m = a mod M, let P be the product of primes dividing m but
   not M, and use CRT to choose positive k = b mod M with k = 1 mod P; common primes of m and M
   cannot divide b, so gcd(m,k) = 1, and a large enough k makes eta positive.  Its norm is
   nonzero and computable (construction supplied by the external audit).  What remains hard is
   a **prescribed or minimal** |L|, which is a different question; the three cases here use
   L = 1, 1, 2 found by inspection.

So the honest status is **three theorems plus a method whose every lemma is proved**, needing
assembly and the ladder-existence input.  That is a better position than the previous round
claimed, and the credit for the finiteness machinery belongs to the classical generalized-Pell
theory, not here; what is specific to this work is the chronology, the equality mechanisms and
the effective certificate for this error and height.
