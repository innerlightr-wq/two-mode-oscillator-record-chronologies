"""gq.py -- independent exact arithmetic and general machinery for the
congruence-restricted relative-error record problem.

Written from scratch for this round.  It deliberately shares no code with
`congruence-records/certificate/quad.py`, so that the regression controls are
an independent check of the published classifications and not a re-run of the
same arithmetic.

GENERAL SETTING (no monicity, no sign hypotheses)
-------------------------------------------------
A primitive integral polynomial  A x^2 + B x + C  with A > 0 and
Delta = B^2 - 4AC > 0 not a square; a choice of root

        alpha = (-B + s*sqrt(Delta)) / (2A),     s = +1 or -1,
        alpha' = (-B - s*sqrt(Delta)) / (2A),

required only to satisfy alpha > 0 and alpha irrational.  alpha may be < 1,
may be the smaller root, alpha' may be positive, and alpha need not be an
algebraic integer.

States are pairs of POSITIVE integers (m,k) with (m mod M, k mod M) in R.
No coprimality is imposed.

        H(m,k) = m*alpha + k  > 0,
        eps(m,k) = |m*alpha - k| / (m*alpha + k)  in (0,1),
        xi = k - m*alpha,  eta = k - m*alpha',
        Q(m,k) = A*k^2 + B*m*k + C*m^2 = A*xi*eta   (the integral defect).

Everything below is exact: elements of Q(sqrt(Delta)) are pairs of Fractions
and every sign is decided by an integer comparison.  Floats appear only in
printed diagnostics.
"""
from fractions import Fraction as Fr
from math import isqrt, gcd


# --------------------------------------------------------------- arithmetic
class Surd:
    """p + q*sqrt(D) with p,q rational and D a fixed positive non-square."""
    __slots__ = ('p', 'q', 'D')

    def __init__(self, p, q, D):
        self.p = Fr(p); self.q = Fr(q); self.D = D

    @staticmethod
    def of(x, D):
        return x if isinstance(x, Surd) else Surd(x, 0, D)

    def __repr__(self):
        return f'({self.p}+{self.q}r{self.D})'

    def __add__(s, o):
        o = Surd.of(o, s.D); return Surd(s.p + o.p, s.q + o.q, s.D)
    __radd__ = __add__

    def __neg__(s):
        return Surd(-s.p, -s.q, s.D)

    def __sub__(s, o):
        return s + (-Surd.of(o, s.D))

    def __rsub__(s, o):
        return Surd.of(o, s.D) + (-s)

    def __mul__(s, o):
        o = Surd.of(o, s.D)
        return Surd(s.p * o.p + s.D * s.q * o.q, s.p * o.q + s.q * o.p, s.D)
    __rmul__ = __mul__

    def inv(s):
        d = s.p * s.p - s.D * s.q * s.q
        assert d != 0, 'zero divisor'
        return Surd(s.p / d, -s.q / d, s.D)

    def __truediv__(s, o):
        return s * Surd.of(o, s.D).inv()

    def __rtruediv__(s, o):
        return Surd.of(o, s.D) * s.inv()

    def conj(s):
        return Surd(s.p, -s.q, s.D)

    def norm(s):
        return s.p * s.p - s.D * s.q * s.q

    def sign(s):
        """exact sign of p + q*sqrt(D), by integer comparison only."""
        if s.q == 0:
            return (s.p > 0) - (s.p < 0)
        if s.p == 0:
            return (s.q > 0) - (s.q < 0)
        sp = (s.p > 0) - (s.p < 0)
        sq = (s.q > 0) - (s.q < 0)
        if sp == sq:
            return sp
        # opposite signs: compare p^2 against D q^2
        a = s.p * s.p
        b = s.D * s.q * s.q
        if a == b:
            return 0            # impossible for D non-square unless p=q=0
        return sp if a > b else sq

    def __eq__(s, o):
        o = Surd.of(o, s.D); return s.p == o.p and s.q == o.q

    def __hash__(s):
        return hash((s.p, s.q, s.D))

    def cmp(s, o):
        return (s - Surd.of(o, s.D)).sign()

    def __lt__(s, o): return s.cmp(o) < 0
    def __le__(s, o): return s.cmp(o) <= 0
    def __gt__(s, o): return s.cmp(o) > 0
    def __ge__(s, o): return s.cmp(o) >= 0

    def pow(s, n):
        assert n >= 0
        r = Surd(1, 0, s.D); b = s
        while n:
            if n & 1: r = r * b
            b = b * b; n >>= 1
        return r

    _rtcache = {}

    def approx(s, bits=200):
        """exact rational approximation of p + q*sqrt(D) (for sort keys and
        display only; never used in a decision)."""
        key = (s.D, bits)
        r = Surd._rtcache.get(key)
        if r is None:
            sc = 1 << bits
            r = Fr(isqrt(s.D * sc * sc), sc)
            Surd._rtcache[key] = r
        return s.p + s.q * r

    def f(s):
        a = s.approx()
        try:
            return float(a)
        except OverflowError:
            return float('inf') if a > 0 else float('-inf')


def floor_int(x):
    """largest integer n with n <= x, exactly (x a Surd)."""
    a, b, D = x.p, x.q, x.D
    c = a.denominator * b.denominator
    ai = int(a * c); bi = int(b * c)          # x = (ai + bi*sqrt(D))/c, c > 0
    assert c > 0
    def le(n):          # n <= x  <=>  ai - c*n + bi*sqrt(D) >= 0
        return sgn_ab(ai - c * n, bi, D) >= 0
    n = int(x.f()) if abs(x.f()) < 1e17 else 0
    if not le(n):
        hi, lo = n, n - 1
        step = 1
        while not le(lo):
            hi = lo; lo -= step; step *= 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if le(mid): lo = mid
            else: hi = mid
        return lo
    lo, hi = n, n + 1
    step = 1
    while le(hi):
        lo = hi; hi += step; step *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if le(mid): lo = mid
        else: hi = mid
    return lo


# ------------------------------------------------------------------- setup
def squarefree_part(n):
    """n = f^2 * d with d squarefree; return (d, f)."""
    assert n > 0
    d, f, p = n, 1, 2
    while p * p <= d:
        while d % (p * p) == 0:
            d //= p * p; f *= p
        p += 1
    return d, f


class Setup:
    """A problem instance (A,B,C,s,M,R)."""

    def __init__(self, A, B, C, s, M, R, name=''):
        assert A > 0 and s in (1, -1)
        g = gcd(gcd(A, B), C)
        assert g == 1, f'minimal polynomial not primitive (gcd {g})'
        Delta = B * B - 4 * A * C
        assert Delta > 0 and isqrt(Delta) ** 2 != Delta, 'not a real quadratic irrational'
        self.A, self.B, self.C, self.s = A, B, C, s
        self.Delta = Delta
        d, fsq = squarefree_part(Delta)
        self.D = d                    # ambient field Q(sqrt(D)), D squarefree
        self.rt = Surd(0, fsq, d)     # = sqrt(Delta)
        self.alpha = (Surd(-B, 0, d) + s * self.rt) / (2 * A)
        self.alphap = (Surd(-B, 0, d) - s * self.rt) / (2 * A)
        assert self.alpha.sign() > 0, 'alpha must be positive'
        self.dd = self.alpha - self.alphap          # = s*sqrt(Delta)/A
        self.M, self.R = M, frozenset((a % M, b % M) for a, b in R)
        assert self.R, 'R must be nonempty'
        self.name = name or f'({A},{B},{C};s={s})'

    # --- basic quantities (exact)
    def Qf(self, m, k):
        return self.A * k * k + self.B * m * k + self.C * m * m

    def xi(self, m, k):
        return Surd(k, 0, self.D) - m * self.alpha

    def eta(self, m, k):
        return Surd(k, 0, self.D) - m * self.alphap

    def H(self, m, k):
        return m * self.alpha + Surd(k, 0, self.D)

    def admissible(self, m, k):
        return m > 0 and k > 0 and (m % self.M, k % self.M) in self.R

    def eps_num_den(self, m, k):
        """eps = |xi| / H as an exact pair of Surds with positive denominator."""
        x = self.xi(m, k)
        return (x if x.sign() > 0 else -x), self.H(m, k)

    def eps_lt(self, s1, s2):
        """exact test eps(s1) < eps(s2)."""
        n1, d1 = self.eps_num_den(*s1)
        n2, d2 = self.eps_num_den(*s2)
        return (n1 * d2 - n2 * d1).sign() < 0

    def eps_cmp(self, s1, s2):
        n1, d1 = self.eps_num_den(*s1)
        n2, d2 = self.eps_num_den(*s2)
        return (n1 * d2 - n2 * d1).sign()

    def H_cmp(self, s1, s2):
        return (self.H(*s1) - self.H(*s2)).sign()

    # --- the automorph group of the form Q
    def pell4(self):
        """least T,U > 0 with T^2 - Delta*U^2 = 4."""
        De = self.Delta
        U = 1
        while True:
            v = De * U * U + 4
            T = isqrt(v)
            if T * T == v:
                return T, U
            U += 1

    def automorph(self):
        """the proper automorph of Q = A k^2 + B m k + C m^2, acting on the
        column (m,k).  Derived from T^2 - Delta U^2 = 4:

            k -> ((T - B U)/2) k - C U m,     m -> A U k + ((T + B U)/2) m.

        Returns the 2x2 integer matrix in (m,k) coordinates, i.e.
        (m,k) -> (M00 m + M01 k, M10 m + M11 k)."""
        T, U = self.pell4()
        A, B, C = self.A, self.B, self.C
        assert (T - B * U) % 2 == 0, 'automorph not integral'
        a = (T - B * U) // 2      # coefficient of k in new k
        b = -C * U                # coefficient of m in new k
        c = A * U                 # coefficient of k in new m
        d = (T + B * U) // 2      # coefficient of m in new m
        # in (m,k) coordinates:
        return ((d, c), (b, a))

    @staticmethod
    def matmul(X, Y):
        return (((X[0][0] * Y[0][0] + X[0][1] * Y[1][0]),
                 (X[0][0] * Y[0][1] + X[0][1] * Y[1][1])),
                ((X[1][0] * Y[0][0] + X[1][1] * Y[1][0]),
                 (X[1][0] * Y[0][1] + X[1][1] * Y[1][1])))

    @staticmethod
    def matapply(X, v):
        m, k = v
        return (X[0][0] * m + X[0][1] * k, X[1][0] * m + X[1][1] * k)

    @staticmethod
    def matinv(X):
        (a, b), (c, d) = X
        det = a * d - b * c
        assert det in (1, -1), f'not unimodular: det={det}'
        return ((d // det, -b // det), (-c // det, a // det))

    def eta_multiplier(self, X):
        """the factor by which eta is multiplied by the matrix X (a Surd)."""
        # eta is linear in (m,k): eta(X v) = lam * eta(v) for an automorph
        e1 = self.eta(*self.matapply(X, (1, 0)))
        e0 = self.eta(1, 0)
        lam = e1 / e0
        # cross-check on a second vector
        e1b = self.eta(*self.matapply(X, (0, 1)))
        e0b = self.eta(0, 1)
        assert e1b == lam * e0b, 'X is not an eta-eigenvector map'
        return lam

    def rho_matrix(self, extra_positive=False):
        """A power P of the proper automorph with
             (1) P == I  (mod M), so every residue class is preserved;
             (2) eta -> rho*eta with rho > 1 (expanding), so xi -> xi/rho;
             (3) optionally all entries of P positive.
        NOTE (3) is NOT always achievable: when alpha' > 0 the two eigen-
        directions (1,alpha) and (1,alpha') both lie in the open positive
        quadrant, the limit of P^n/rho^n is proportional to (1,alpha) times the
        left eigenvector (-alpha',1), which has a negative entry, so no power of
        the automorph is entrywise positive and the positive quadrant is NOT
        forward invariant.  Hence extra_positive defaults to False.
        Returns (P, rho, j) with rho a Surd."""
        X0 = self.automorph()
        lam = self.eta_multiplier(X0)
        if not (lam.sign() > 0 and lam > Surd(1, 0, self.D)):
            X0 = self.matinv(X0)
            lam = self.eta_multiplier(X0)
        assert lam > Surd(1, 0, self.D), f'no expanding automorph found ({lam.f()})'
        I = ((1, 0), (0, 1))
        X, j = X0, 1
        while True:
            ok_mod = all(X[i][l] % self.M == I[i][l] % self.M
                         for i in range(2) for l in range(2))
            ok_pos = (not extra_positive) or all(X[i][l] > 0 for i in range(2) for l in range(2))
            if ok_mod and ok_pos:
                return X, self.eta_multiplier(X), j
            X = self.matmul(X, X0); j += 1
            assert j <= 4000, 'no admissible automorph power found'


# ------------------------------------------------------- ground truth: brute
def enumerate_states(S, Hcap):
    """all admissible (m,k) with H = m*alpha + k <= Hcap (Hcap an int or Fr)."""
    out = []
    a = S.alpha
    m = 1
    while True:
        if (m * a - Hcap).sign() >= 0:
            break
        # k <= Hcap - m*alpha
        rem = Surd(Hcap, 0, S.D) - m * a
        kmax = 0
        # integer part of rem (rem > 0 here)
        lo, hi = 0, 1
        while (Surd(hi, 0, S.D) - rem).sign() <= 0:
            hi *= 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if (Surd(mid, 0, S.D) - rem).sign() <= 0:
                lo = mid
            else:
                hi = mid
        kmax = lo
        for k in range(1, kmax + 1):
            if (m % S.M, k % S.M) in S.R:
                out.append((m, k))
        m += 1
    return out


def sort_by_height(S, states):
    """sort exactly: float presort, then verify every adjacent pair exactly."""
    states = sorted(states, key=lambda v: S.H(*v).f())
    for i in range(len(states) - 1):
        c = S.H_cmp(states[i], states[i + 1])
        assert c < 0, f'height order not strict/correct at {states[i]},{states[i+1]} (cmp {c})'
    return states


def brute_records(S, Hcap):
    """exact strict records with H <= Hcap, plus the weak-but-not-strict ties."""
    st = sort_by_height(S, enumerate_states(S, Hcap))
    strict, weak_ties = [], []
    best = None            # (num, den) of the running minimum
    for v in st:
        n, d = S.eps_num_den(*v)
        if best is None:
            strict.append(v); best = (n, d); continue
        c = (n * best[1] - best[0] * d).sign()
        if c < 0:
            strict.append(v); best = (n, d)
        elif c == 0:
            weak_ties.append(v)
    return strict, weak_ties, len(st)


# ------------------------------------------- fast integer-only comparators
# Every state quantity lies in Z + Z*sqrt(Delta) after clearing 2A:
#     2A*xi = X - s*m*sqrt(Delta),   X = 2Ak + Bm
#     2A*H  = W + s*m*sqrt(Delta),   W = 2Ak - Bm      (H > 0 for m,k > 0)
# so   eps = |X - s m sqrt(Delta)| / (W + s m sqrt(Delta)).

def sgn_ab(a, b, Delta):
    """exact sign of a + b*sqrt(Delta) for integers a,b."""
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    aa, bb = a * a, Delta * b * b
    if aa == bb:
        return 0
    return ((a > 0) - (a < 0)) if aa > bb else ((b > 0) - (b < 0))


class Fast:
    """integer-only comparators for one Setup."""

    def __init__(self, S):
        self.A, self.B, self.s, self.De = S.A, S.B, S.s, S.Delta

    def h_cmp(self, v1, v2):
        dm = v1[0] - v2[0]
        P = -self.B * dm + 2 * self.A * (v1[1] - v2[1])
        return sgn_ab(P, self.s * dm, self.De)

    def xi_ab(self, m, k):
        return 2 * self.A * k + self.B * m, -self.s * m

    def h_ab(self, m, k):
        return 2 * self.A * k - self.B * m, self.s * m

    def absxi_ab(self, m, k):
        a, b = self.xi_ab(m, k)
        return (a, b) if sgn_ab(a, b, self.De) > 0 else (-a, -b)

    def eps_cmp(self, v1, v2):
        a1, b1 = self.absxi_ab(*v1); c2, d2 = self.h_ab(*v2)
        a2, b2 = self.absxi_ab(*v2); c1, d1 = self.h_ab(*v1)
        p = a1 * c2 + self.De * b1 * d2 - (a2 * c1 + self.De * b2 * d1)
        q = a1 * d2 + b1 * c2 - (a2 * d1 + b2 * c1)
        return sgn_ab(p, q, self.De)


def kmax_for(S, m, Hcap):
    """largest integer k >= 1 with m*alpha + k <= Hcap, or 0 if none."""
    A, B, s, De = S.A, S.B, S.s, S.Delta
    def ok(k):
        Z = 2 * A * Hcap - 2 * A * k + B * m
        return sgn_ab(Z, -s * m, De) >= 0
    if not ok(1):
        return 0
    lo, hi = 1, 2
    while ok(hi):
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo


def brute_records_fast(S, Hcap, verify_order=True):
    """exact strict records with H <= Hcap; integer arithmetic only.
    Returns (strict, weak_ties, n_states)."""
    F = Fast(S)
    states = []
    m = 1
    while True:
        km = kmax_for(S, m, Hcap)
        if km == 0:
            break
        for k in range(1, km + 1):
            if (m % S.M, k % S.M) in S.R:
                states.append((m, k))
        m += 1
    states = sort_heights(S, states)      # approximate sort, exactly verified,
                                          # with a guaranteed exact fallback (O2)
    strict, ties = [], []
    best = None
    for v in states:
        if best is None:
            strict.append(v); best = v; continue
        c = F.eps_cmp(v, best)
        if c < 0:
            strict.append(v); best = v
        elif c == 0:
            ties.append(v)
    return strict, ties, len(states)


# ================================================================ STAGE A/B/C
# The cutoff, in the general form derived in this round.  For any admissible
# comparison family F = {A_1 < A_2 < ... } (ordered by height, heights -> oo)
# and any strict record B with H_{A_i} < H_B <= H_{A_{i+1}}:
#
#       |Q_B| < |Q_{A_i}| * (H_{A_{i+1}}/H_{A_i})^2 * (1 + theta_i),
#       theta_i = (B*Q_{A_i} + |B*Q_{A_i}|) / (2*alpha*A^2*eta_{A_i}^2)
#               = 2*max(u_i, 0),     u = B*Q/(2*alpha*A^2*eta^2).
#
# Derivation (no sign hypotheses):  with z = xi/H, Q = H^2 z (A*dd - B z)/(2 alpha)
# so |Q| = H^2 eps (A|dd| + |B| eps)/(2 alpha) at worst, A|dd| = sqrt(Delta);
# eps_B < eps_A and x -> x(sqrt(Delta) + |B| x) increasing give
#       |Q_B| < H_C^2 eps_A (sqrt(Delta) + |B| eps_A)/(2 alpha),
# and eps_A = |Q_A| sqrt(Delta)/G_A, H_A^2 = G_A^2/(A^2 eta_A^2 * Delta),
# G_A = 2 alpha A^2 eta_A^2 + B Q_A, reduce this to the displayed form.

def orbit_forward(S, P, v, n):
    out = [v]
    for _ in range(n):
        v = S.matapply(P, v)
        out.append(v)
    return out


def norm_rep(S, P, rho, v):
    """move v along its P-orbit until |eta| in [1, rho); returns (rep, shift)."""
    one = Surd(1, 0, S.D)
    Pi = S.matinv(P)
    w, sh = v, 0
    for _ in range(10000):
        e = S.eta(*w)
        ae = e if e.sign() > 0 else -e
        if (ae - one).sign() < 0:
            w = S.matapply(P, w); sh += 1
        elif (ae - rho).sign() >= 0:
            w = S.matapply(Pi, w); sh -= 1
        else:
            return w, sh
    raise AssertionError('normalisation did not terminate')


def theta_of(S, v):
    """theta = 2*max(u,0) with u = B*Q/(2*alpha*A^2*eta^2)."""
    Q = S.Qf(*v)
    e = S.eta(*v)
    Y = (S.A ** 2) * e * e
    u = Surd(S.B * Q, 0, S.D) / (2 * S.alpha * Y)
    return 2 * u if u.sign() > 0 else Surd(0, 0, S.D)


def u_of(S, v):
    Q = S.Qf(*v)
    e = S.eta(*v)
    Y = (S.A ** 2) * e * e
    return Surd(S.B * Q, 0, S.D) / (2 * S.alpha * Y)


def F_pair(S, vA, vC):
    """the cutoff functional for a consecutive family pair (A below, C above)."""
    QA = abs(S.Qf(*vA))
    r = S.H(*vC) / S.H(*vA)
    return QA * r * r * (Surd(1, 0, S.D) + theta_of(S, vA))


def cutoff(S, P, rho, seeds, periods=14, tail_from=6, verbose=False):
    """B_cut for the comparison family generated by `seeds` (one P-orbit each).

    Returns (Bcut:int, data) where data records the exact maximum, the pair
    attaining it, and the certified tail bound.  Every comparison is exact."""
    F = Fast(S)
    one = Surd(1, 0, S.D)
    # positive tails of each seed orbit, advanced `periods` times
    fam, dropped = [], []
    for sd in seeds:
        v = sd
        for _ in range(200):
            if v[0] > 0 and v[1] > 0:
                break
            v = S.matapply(P, v)
        if not (v[0] > 0 and v[1] > 0):
            # forward orbit never enters the positive quadrant.  This happens
            # exactly when alpha' > 0 and the state lies beyond the (1,alpha')
            # eigendirection: such an orbit's positive states run BACKWARD, its
            # eps tends to a positive constant, and it cannot serve as a ladder.
            dropped.append(sd)
            continue
        fam.append(orbit_forward(S, P, v, periods))
    assert fam, 'every candidate seed is in the backward (alpha\'>0) sector'
    members = [(w, i, p) for i, orb in enumerate(fam) for p, w in enumerate(orb)]
    members = [x for x in members if x[0][0] > 0 and x[0][1] > 0]
    order = {v: i for i, v in enumerate(sort_heights(S, [x[0] for x in members]))}
    members.sort(key=lambda x: order[x[0]])
    best, bestpair = None, None
    for i in range(len(members) - 1):
        vA, vC = members[i][0], members[i + 1][0]
        if members[i][2] >= periods - 2:
            continue
        f = F_pair(S, vA, vC)
        if best is None or (f - best).sign() > 0:
            best, bestpair = f, (vA, vC)
    # certified tail bound: for each consecutive pair type at period >= tail_from
    tails = []
    for i in range(len(members) - 1):
        if members[i][2] != tail_from:
            continue
        vA, vC = members[i][0], members[i + 1][0]
        QA = abs(S.Qf(*vA))
        eA, eC = S.eta(*vA), S.eta(*vC)
        r = eC / eA
        if r.sign() < 0:
            r = -r
        uA, uC = u_of(S, vA), u_of(S, vC)
        w = max((uA if uA.sign() > 0 else -uA), (uC if uC.sign() > 0 else -uC))
        assert (w - one).sign() < 0, 'tail bound needs |u| < 1'
        bnd = QA * r * r * ((one + w) / (one - w)) * ((one + w) / (one - w)) * (one + 2 * w)
        tails.append((bnd, vA, vC))
    assert tails, 'no tail pairs found; increase periods'
    tmax = max(tails, key=lambda x: x[0].f())
    allmax = best if (best - tmax[0]).sign() > 0 else tmax[0]
    if (best - tmax[0]).sign() <= 0:
        bestpair = (tmax[1], tmax[2])
    # floor of allmax as an integer
    Bcut = floor_int(allmax)   # |Q_B| < max  =>  |Q_B| <= floor(max)
    if verbose:
        print(f'    cutoff: max F = {allmax.f():.6f} at {bestpair}, tail <= {tmax[0].f():.6f}'
              f'  => |Q_B| <= {Bcut}')
    return Bcut, dict(maxF=allmax, pair=bestpair, tail=tmax[0], nfam=len(members),
                      dropped=dropped)


# ================================================================= STAGE D/E
def enumerate_orbits(S, P, rho, Bmax, box_limit=4 * 10 ** 7):
    """every P-orbit of states with 0 < |Q| <= Bmax, admissible residue,
    by the classical reduction box:  normalise |eta| in [1,rho), then
    |xi| = |Q|/(A|eta|) <= Bmax/A, and m = (eta-xi)/dd, k = xi + m*alpha are
    bounded.  Imprimitive orbits are retained.  No PID hypothesis is used."""
    one = Surd(1, 0, S.D)
    dd = S.dd
    addf = abs(dd.f())
    mb = int((rho.f() + Bmax / S.A) / addf) + 2
    kb = int(Bmax / S.A + mb * S.alpha.f()) + 2
    if (2 * mb + 1) * (2 * kb + 1) > box_limit:
        raise MemoryError(f'reduction box {(2*mb+1)}x{(2*kb+1)} exceeds limit')
    out = []
    for m in range(-mb, mb + 1):
        for k in range(-kb, kb + 1):
            Q = S.Qf(m, k)
            if Q == 0 or abs(Q) > Bmax:
                continue
            if (m % S.M, k % S.M) not in S.R:
                continue
            e = S.eta(m, k)
            ae = e if e.sign() > 0 else -e
            if (ae - one).sign() < 0 or (ae - rho).sign() >= 0:
                continue
            out.append(((m, k), Q))
    return out, (mb, kb)


def first_positive(S, P, v, limit=400):
    w = v
    for p in range(limit):
        if w[0] > 0 and w[1] > 0:
            return w, p
        w = S.matapply(P, w)
    return None, None


def classify(S, P, rho, Bcut, p_star=6, verbose=False):
    """Decide, for every orbit with |Q| <= Bcut, whether its late states are
    strict records, permanent ties, or excluded.

    Pruning lemma used here (proved this round): if V blocks a record B, i.e.
    H_V < H_B and eps_V <= eps_B, then
        |Q_V| <= |Q_B| * (sqrt(Delta) + |B|eps_B) / (sqrt(Delta) - |B|eps_B),
    because |Q| = H^2 eps (A|dd| - B z)/(2 alpha) with A|dd| = sqrt(Delta) and
    |z| = eps.  So only orbits of comparable defect can block, and the
    competitor set is pruned per candidate instead of globally.

    Returns (verdicts, cand, comp, box, j)."""
    F = Fast(S)
    comp_raw, box, j, nclass = enumerate_orbits2(S, P, rho, Bcut)
    comp = []
    for rep, Q in comp_raw:
        pv, p0 = first_positive(S, P, rep)
        if pv is None:
            continue                      # backward (alpha'>0) sector
        comp.append(dict(rep=rep, Q=Q, pos=pv, p0=p0))
    # precompute states for a window of periods
    LO, HI = max(0, p_star - 4), p_star + 3
    for o in comp:
        o['st'] = {}
        w = o['pos']
        for q in range(0, HI + 1):
            if q >= LO:
                o['st'][q] = w
            w = S.matapply(P, w)
    cand = [c for c in comp if abs(c['Q']) <= Bcut]
    verdicts = {}
    for ci, c in enumerate(cand):
        res = {'beats': True, 'tie_with': None, 'lost_to': None}
        qB = abs(c['Q'])
        for p in (p_star, p_star + 1, p_star + 2):
            vB = c['st'][p]
            if vB[0] <= 0 or vB[1] <= 0:
                res['beats'] = False; res['lost_to'] = 'not positive yet'; break
            n, d = S.eps_num_den(*vB)
            lim = Bcomp_from(S, qB, (n, d)) if S.B != 0 else qB
            for o in comp:
                if abs(o['Q']) > lim:
                    continue
                # minimal-eps competitor below H_B (the definition of blocking);
                # the largest-period rule is equivalent only on the G > 0 branch
                best = None
                for q in range(LO, p + 3):
                    w = o['st'].get(q)
                    if w is None or w[0] <= 0 or w[1] <= 0:
                        continue
                    if F.h_cmp(w, vB) < 0 and (best is None or F.eps_cmp(w, best) < 0):
                        best = w
                if best is None:
                    continue
                c2 = F.eps_cmp(vB, best)
                if c2 > 0:
                    # a strict loss is decisive and overrides any tie found
                    res['beats'] = False
                    res['lost_to'] = (o['rep'], o['Q'], best)
                    break
                if c2 == 0:
                    # record the tie but KEEP SCANNING: a later strict loss
                    # means the orbit is excluded, not a permanent tie.
                    res['beats'] = False
                    if res['tie_with'] is None:
                        res['tie_with'] = (o['rep'], o['Q'], best)
            if res['lost_to'] is not None:
                res['tie_with'] = None
                break
        verdicts[ci] = res
    return verdicts, cand, comp, box, j


def matpow(S, P, n):
    assert n >= 0
    R = ((1, 0), (0, 1))
    B = P
    while n:
        if n & 1: R = S.matmul(R, B)
        B = S.matmul(B, B); n >>= 1
    return R


def Bcomp_from(S, Bcut, eps0_num_den):
    """blockers of a record B satisfy |Q_V| <= |Q_B|*(rtD+|B|eps)/(rtD-|B|eps).
    Pass eps0 as an upper bound (num,den) Surds on eps_B in the regime used."""
    n, d = eps0_num_den
    rt = S.rt
    num = rt * d + abs(S.B) * n
    den = rt * d - abs(S.B) * n
    assert den.sign() > 0, 'eps too large for the blocker bound'
    val = Surd(Bcut, 0, S.D) * num / den
    return max(Bcut, floor_int(val))


def orbit_key(S, P, rho, v):
    rep, _ = norm_rep(S, P, rho, v)
    return rep


def auto_family(S, P, rho, Hseed=400, Dlist=None, periods=8, verbose=False):
    """Choose a comparison family: all admissible orbits of defect |Q| <= D
    met below height Hseed, for the D minimising the resulting cutoff.
    Returns (Bcut, seeds, D, info)."""
    states = []
    m = 1
    while True:
        km = kmax_for(S, m, Hseed)
        if km == 0:
            break
        for k in range(1, km + 1):
            if (m % S.M, k % S.M) in S.R:
                states.append((m, k))
        m += 1
    reps = {}
    for v in states:
        r = orbit_key(S, P, rho, v)
        reps.setdefault(r, abs(S.Qf(*v)))
    if not reps:
        raise AssertionError('no admissible state below Hseed')
    if Dlist is None:
        qs = sorted(set(reps.values()))
        Dlist = qs[:8]            # the 8 smallest distinct defect bounds
    best = None
    for D in Dlist:
        sd = [r for r, q in reps.items() if q <= D]
        if not sd:
            continue
        try:
            Bc, info = cutoff(S, P, rho, sd, periods=periods)
        except AssertionError:
            continue
        if best is None or Bc < best[0]:
            best = (Bc, sd, D, info)
        if verbose:
            print(f'      D={D:<8d} family size {len(sd):3d}  ->  cutoff {Bc}')
    assert best is not None, 'no usable family'
    return best


def fundamental_expander(S):
    """the proper automorph X0 oriented so that eta -> lam*eta with lam > 1."""
    X0 = S.automorph()
    lam = S.eta_multiplier(X0)
    if not (lam.sign() > 0 and lam > Surd(1, 0, S.D)):
        X0 = S.matinv(X0)
        lam = S.eta_multiplier(X0)
    assert lam > Surd(1, 0, S.D)
    return X0, lam


def enumerate_orbits2(S, P, rho, Bmax, box_limit=2 * 10 ** 8):
    """Same as enumerate_orbits but the reduction box uses the FUNDAMENTAL
    automorph multiplier lam (not rho = lam^j), so its size is O(lam + Bmax)
    instead of O(rho + Bmax).  Each lam-class is then split into the j
    P-orbits it contains, and only the admissible ones are kept.

    This is what makes instances with a large class-fixing index j tractable:
    the fundamental domain has size lam, while rho = lam^j."""
    X0, lam = fundamental_expander(S)
    one = Surd(1, 0, S.D)
    # j = index with P = X0^j
    j, Y = 1, X0
    while Y != P:
        Y = S.matmul(Y, X0); j += 1
        assert j <= 5000, 'P is not a power of the fundamental automorph'
    addf = abs(S.dd.f())
    mb = int((lam.f() + Bmax / S.A) / addf) + 2
    kb = int(Bmax / S.A + mb * S.alpha.f()) + 2
    if (2 * mb + 1) * (2 * kb + 1) > box_limit:
        raise MemoryError(f'reduction box {(2*mb+1)}x{(2*kb+1)} exceeds limit')
    classes = []
    for m in range(-mb, mb + 1):
        for k in range(-kb, kb + 1):
            Q = S.Qf(m, k)
            if Q == 0 or abs(Q) > Bmax:
                continue
            e = S.eta(m, k)
            ae = e if e.sign() > 0 else -e
            if (ae - one).sign() < 0 or (ae - lam).sign() >= 0:
                continue
            classes.append(((m, k), Q))
    out = []
    for rep, Q in classes:
        w = rep
        for p in range(j):
            if (w[0] % S.M, w[1] % S.M) in S.R:
                out.append((w, Q))
            w = S.matapply(X0, w)
    return out, (mb, kb), j, len(classes)


def auto_family2(S, P, rho, Dlist=None, periods=8, verbose=False):
    """Choose the comparison family as *all* admissible orbits of defect
    |Q| <= D, enumerated through the fundamental-domain box (so no brute-force
    height search is needed), for the smallest D that is SELF-CONSISTENT:

        cutoff(family of defect <= D)  <=  D.

    Self-consistency means the record orbits are already inside the family's
    defect range, so the enumeration needed for the classification is exactly
    the family itself.  Returns (Bcut, seeds, D, info, selfconsistent)."""
    if Dlist is None:
        Dlist = [1, 2, 3, 5, 8, 13, 20, 30, 50, 80, 130, 200, 320, 500, 800,
                 1300, 2000, 3200, 5000, 8000, 13000, 20000]
    best = None
    for D in Dlist:
        try:
            orbs, box, j, nc = enumerate_orbits2(S, P, rho, D)
        except MemoryError:
            break
        seeds = [rep for rep, Q in orbs]
        if not seeds:
            continue
        try:
            Bc, info = cutoff(S, P, rho, seeds, periods=periods)
        except AssertionError as e:
            if verbose: print(f'      D={D}: {e}')
            continue
        sc = Bc <= D
        if verbose:
            print(f'      D={D:<6d} orbits {len(seeds):4d} (fwd-positive '
                  f'{len(seeds)-len(info["dropped"]):4d})  cutoff {Bc:<12d}'
                  f'{"  SELF-CONSISTENT" if sc else ""}')
        if best is None or Bc < best[0]:
            best = (Bc, seeds, D, info, sc)
        if sc:
            return (Bc, seeds, D, info, True)
    assert best is not None, 'no usable family at any tested D'
    return best + () if len(best) == 5 else best


# ================================================== STAGE E, certified tail
# Along a P-orbit the defect Q is CONSTANT (P is a proper automorph), so every
# comparison below has constant right-hand side and no parity bookkeeping.
#
# (E1) eps strictly decreases along every orbit, unconditionally:
#      with A = B the same orbit and offset 1, Gamma = |Q| r^2 (rho^2 - 1) > 0
#      and the right-hand side B(|Q|Q - |Q|Q) = 0, so the criterion holds.
# (E2) eps_B < eps_A  <=>  2 alpha A^2 Gamma > B(|Q_A| Q_B - |Q_B| Q_A), with
#      Gamma = rho^{2(p-d)} Gamma_d, Gamma_d = |Q_A| r_B^2 rho^{2d} - |Q_B| r_A^2.
#      Hence one exact sign per (pair, d), certified once
#           2 alpha A^2 rho^{2(p-d)} |Gamma_d| > |RHS|.
#      If Gamma_d = 0 the verdict is the constant sign of -RHS (three-way; for
#      B = 0 it is EXACT EQUALITY at every period).
# (E3) sign(H_B - H_A) = sign(rho^q U + V) with A at period q, B at q+d,
#      U = 2 alpha A^2 r_A r_B rho^d (r_B rho^d - r_A),  V = B(Q_B r_A - Q_A r_B rho^d),
#      so one exact sign per (pair, d), certified once rho^q |U| > |V|.
# (E4) With all representatives normalised to |eta| in [1, rho), period p-1 of
#      any orbit precedes period p of any other in |eta|; with (E1) and (E3)
#      this forces the binding competitor to sit at offset d in {0,1}.

def _absS(x):
    return x if x.sign() > 0 else -x


def certify_tail(S, P, rho, comp, dmax=1, pmax=400):
    """Compute a period p_cert such that for every ordered pair of
    forward-positive orbits and every offset d <= dmax, both the eps comparison
    (E2) and the height comparison (E3) have their sign fixed for all p >= p_cert.
    Returns (p_cert, detail)."""
    one = Surd(1, 0, S.D)
    A2 = S.A ** 2
    reps = []
    for o in comp:
        r, _ = norm_rep(S, P, rho, o['pos'])
        e = S.eta(*r)
        reps.append(dict(o=o, r=_absS(e), Q=o['Q']))
    pcert = 0
    worst = None
    for a in reps:
        for b in reps:
            for d in range(0, dmax + 1):
                QA, QB = a['Q'], b['Q']
                rA, rB = a['r'], b['r']
                # ---- (E2)   eps_B < eps_A  <=>  |Q_A| G_B - |Q_B| G_A > 0
                #          <=>  2 alpha A^2 Gamma > B(|Q_B| Q_A - |Q_A| Q_B)
                # (the right-hand side is B(|Q_B|Q_A - |Q_A|Q_B); an earlier
                #  write-up displayed its negative -- see review item R1.)
                Gd = abs(QA) * rB * rB * rho.pow(2 * d) - abs(QB) * rA * rA
                rhs = S.B * (abs(QB) * QA - abs(QA) * QB)
                if Gd.sign() != 0:
                    need = Surd(abs(rhs), 0, S.D)
                    p = d
                    while p <= pmax:
                        lhs = 2 * S.alpha * A2 * rho.pow(2 * (p - d)) * _absS(Gd)
                        if (lhs - need).sign() > 0:
                            break
                        p += 1
                    assert p <= pmax, 'eps threshold did not certify'
                    if p > pcert:
                        pcert, worst = p, ('eps', a['o']['pos'], b['o']['pos'], d)
                # ---- (E3)
                U = 2 * S.alpha * A2 * rA * rB * rho.pow(d) * (rB * rho.pow(d) - rA)
                V = Surd(S.B, 0, S.D) * (Surd(QB, 0, S.D) * rA
                                         - Surd(QA, 0, S.D) * rB * rho.pow(d))
                if U.sign() == 0:
                    assert V.sign() == 0, 'U = 0 with V != 0: inconsistent data'
                    continue
                # sgn(H_B - H_A) = sgn(rho^{2q} U + V): clearing the positive
                # factor A^2 dd r_A r_B rho^{q+d} leaves rho^{2q} U + V, not
                # rho^q U + V (review item R3).
                q = 0
                while q <= pmax:
                    if (rho.pow(2 * q) * _absS(U) - _absS(V)).sign() > 0:
                        break
                    q += 1
                assert q <= pmax, 'height threshold did not certify'
                if q + d > pcert:
                    pcert, worst = q + d, ('height', a['o']['pos'], b['o']['pos'], d)
    return pcert, worst


def dstar_and_noblock(S, rho, Bcomp, pmax=400):
    """The correct offset bound: a competitor can only BLOCK (have eps <= eps_B
    at a lower height); BINDING offsets are unbounded when alpha' > 0, but
    blocking offsets are not.

    With eps = |Q| sqrt(Delta)/G, G = 2 alpha A^2 eta^2 + B Q > 0 on the branch,
    A at level L-d and B at level L satisfy eps_A > eps_B as soon as
        |Q_A| G_B > |Q_B| G_A,
    and using r_A < rho, r_B >= 1 it suffices that
        2 alpha A^2 rho^{2L} ( |Q_A| - |Q_B| rho^{2-2d} )
              >  |Q_A| |B Q_B| + |Q_B| |B Q_A| .
    The bracket is positive for every pair with |Q| <= Bcomp once
    rho^{2d-2} > Bcomp, which defines d_star; the additive part then fixes a
    level threshold p_noblock, both monotone.  So for d > d_star no competitor
    can block, independently of the height relation, and only d <= d_star needs
    the Gamma_d thresholds.

    Returns (d_star, p_noblock)."""
    one = Surd(1, 0, S.D)
    d = 1
    while d <= pmax:
        if (rho.pow(2 * d - 2) - Surd(Bcomp, 0, S.D)).sign() > 0:
            break
        d += 1
    assert d <= pmax, 'd_star did not terminate'
    dstar = d
    # worst case over pairs: |Q_A| = 1, |Q_B| = Bcomp, d = dstar + 1
    QA, QB = 1, Bcomp
    dd1 = dstar + 1
    brack = Surd(QA, 0, S.D) - Surd(QB, 0, S.D) / rho.pow(2 * dd1 - 2)
    assert brack.sign() > 0, 'd_star bracket not positive'
    rhs = Surd(QA * abs(S.B) * QB + QB * abs(S.B) * QA, 0, S.D)
    L = 0
    while L <= pmax:
        lhs = 2 * S.alpha * Surd(S.A ** 2, 0, S.D) * rho.pow(2 * L) * brack
        if (lhs - rhs).sign() > 0:
            break
        L += 1
    assert L <= pmax, 'p_noblock did not terminate'
    return dstar, L


def eps0_threshold(S):
    """The starting error threshold: eps_0 < min(1, sqrt(Delta)/(2|B|)), with the
    second constraint omitted when B = 0.  Returns the threshold as a Surd.

    Two consequences, both used below.
    (a)  eps < sqrt(Delta)/|B|  =>  eta*(alpha-alpha') > 0  =>  G > 0.
         Indeed eta = (H dd - (B/A) xi)/(2 alpha) and |xi| = eps H give
         eta*dd >= H|dd|(|dd| - |B|eps/A)/(2 alpha) > 0 iff eps < A|dd|/|B|
         = sqrt(Delta)/|B|.  So the whole G < 0 branch -- on which eps
         INCREASES along an orbit (review item R2) -- is excluded from the tail
         analysis, and Lemma 6.1 applies to everything that remains.
    (b)  Lemma 5.4 then gives the uniform blocker bound
         |Q_V| <= |Q_B| (sqrt(D)+|B|eps)/(sqrt(D)-|B|eps) <= 3 |Q_B|,
         so B_comp = 3 B_cut is always safe.
    """
    one = Surd(1, 0, S.D)
    if S.B == 0:
        return one
    t = S.rt / Surd(2 * abs(S.B), 0, S.D)
    return t if t.cmp(one) < 0 else one


def eps_lt_threshold(S, v, thr):
    """exact test eps(v) < thr, thr a Surd."""
    n, d = S.eps_num_den(*v)
    return (n - thr * d).sign() < 0


def find_eps0_state(S, P, seeds, thr, maxsteps=200):
    """An admissible state with eps < thr, chosen to maximise eps over an
    EXPLICIT FINITE candidate family: the first state of each family seed's
    forward tail that falls below thr.  (There is no claim of a global maximum
    over all admissible states, and none is needed -- for the theorem ANY
    computable admissible w with eps(w) < thr suffices.  A larger eps_0 merely
    gives a smaller Ystar and so a shallower cutoff level.)  Existence is
    guaranteed because eps -> 0 along every forward tail."""
    F = Fast(S)
    best = None
    for sd in seeds:
        w = sd
        for _ in range(maxsteps):
            if w[0] > 0 and w[1] > 0 and eps_lt_threshold(S, w, thr):
                if best is None or F.eps_cmp(w, best) > 0:
                    best = w
                break
            w = S.matapply(P, w)
    return best


def sort_heights(S, states, _force_key_failure=False):
    """Sort admissible states by height, with a GUARANTEED exact fallback.

    Attempt the approximate-key sort and verify every adjacent pair exactly;
    if key generation raises, or if any adjacent pair fails, redo the sort with
    the exact algebraic comparator.  This establishes termination with a
    correctly ordered list for every input, which verification alone does not
    (review item O2).  Returns (list) and records whether the fallback fired in
    S.last_sort_fallback."""
    import functools
    F = Fast(S)
    S.last_sort_fallback = False
    if not _force_key_failure:
        try:
            af = S.alpha.f()
            if af != af or af in (float('inf'), float('-inf')):
                raise ValueError('degenerate alpha key')
            out = sorted(states, key=lambda v: v[0] * af + v[1])
            if all(F.h_cmp(out[i], out[i + 1]) < 0 for i in range(len(out) - 1)):
                return out
        except Exception:
            pass
    S.last_sort_fallback = True
    out = sorted(states, key=functools.cmp_to_key(F.h_cmp))
    assert all(F.h_cmp(out[i], out[i + 1]) < 0 for i in range(len(out) - 1)), \
        'exact comparator sort failed: states are not pairwise distinct in height'
    return out


def eps0_level_cutoff(S, Q, eps_num, eps_den):
    """On the G > 0 branch, with eps_0 = eps(w) = eps_num/eps_den the ATTAINED
    error of the chosen comparison state (not the bound),

        eps >= eps_0   <=>   Y := A^2 eta^2  <=  Ystar
        Ystar = ( |Q| sqrt(Delta) * eps_den / eps_num  -  B Q ) / (2 alpha).

    States with Y <= Ystar have eps >= eps_0, so they are neither records above
    H(w) nor blockers of one: an explicit BACKWARD-LEVEL cutoff on the G > 0
    branch, where the floor eps >= sqrt(Delta)/|B| does NOT apply (review O1).

    The attained eps_0 matters: it is STRICTLY below min(1, sqrt(Delta)/(2|B|)),
    and that strictness is exactly what makes Ystar strictly exceed the height
    minimum Y_min = B Q/(2 alpha) when B Q > 0, so the height is strictly
    increasing on the surviving region Y > Ystar.  Taking eps_0 to be the bound
    itself gives Ystar = Y_min and loses the strictness."""
    return (Surd(abs(Q), 0, S.D) * S.rt * eps_den / eps_num
            - Surd(S.B * Q, 0, S.D)) / (2 * S.alpha)


def level_cutoff_search(S, rho, r, Ystar, cap=4000):
    """The exact two-sided expanding search for the backward-level cutoff.

    With Y_L = A^2 r^2 rho^{2L} and rho > 1, Y_L is strictly increasing in L,
    Y_L -> 0 as L -> -infinity and Y_L -> +infinity as L -> +infinity.  Since
    Ystar is finite and positive, there is a UNIQUE integer L* with

            Y_{L*}  <=  Ystar  <  Y_{L*+1} ,

    and an expanding search in both directions locates it in finitely many
    steps.  Those two inequalities are the whole certificate: by monotonicity
    they prove the exclusion for EVERY level L <= L*, with no logarithm, no
    rounding and no appeal to a window that happened to be wide enough.  The
    orbit list is finite, so all such searches terminate -- which is the
    universal termination argument.

    Returns (Lstar, Y_at_Lstar, Y_at_Lstar_plus_1)."""
    A2 = Surd(S.A ** 2, 0, S.D)
    base = A2 * r * r
    def Y(L):
        return base * rho.pow(L * 2) if L >= 0 else base / rho.pow(-L * 2)
    assert Ystar.sign() > 0, 'Ystar must be positive'
    L = 0
    if (Y(L) - Ystar).sign() <= 0:
        step = 1
        while (Y(L + step) - Ystar).sign() <= 0:
            L += step
            step *= 2
            assert L <= cap, 'cutoff search diverged upward'
        while (Y(L + 1) - Ystar).sign() <= 0:
            L += 1
    else:
        step = 1
        while (Y(L) - Ystar).sign() > 0:
            L -= step
            step *= 2
            assert L >= -cap, 'cutoff search diverged downward'
        while (Y(L) - Ystar).sign() > 0:
            L -= 1
        # now Y(L) <= Ystar; climb back to the largest such L
        while (Y(L + 1) - Ystar).sign() <= 0:
            L += 1
    lo, hi = Y(L), Y(L + 1)
    assert (lo - Ystar).sign() <= 0 and (hi - Ystar).sign() > 0, \
        'the two witness inequalities do not hold'
    return L, lo, hi
