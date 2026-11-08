"""Exact arithmetic in Z[sqrt(D)] and exact sign/ordering tests.  No floating point.

Elements are pairs (a, b) meaning a + b*sqrt(D) with a, b integers (or Fractions).
Every comparison below is decided by integer arithmetic alone.
"""
from fractions import Fraction

class Q:
    """a + b*sqrt(D), exact."""
    __slots__ = ("a", "b", "D")
    def __init__(self, a, b, D):
        self.a = Fraction(a); self.b = Fraction(b); self.D = D
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b, s.D)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b, s.D)
    def __neg__(s):    return Q(-s.a, -s.b, s.D)
    def __mul__(s, o):
        if isinstance(o, Q):
            assert s.D == o.D
            return Q(s.a*o.a + s.D*s.b*o.b, s.a*o.b + s.b*o.a, s.D)
        return Q(s.a*o, s.b*o, s.D)
    def conj(s): return Q(s.a, -s.b, s.D)
    def norm(s): return s.a*s.a - s.D*s.b*s.b
    def sign(s):
        """Exact sign of a + b*sqrt(D), by integer reasoning only."""
        a, b, D = s.a, s.b, s.D
        if a == 0 and b == 0: return 0
        if a >= 0 and b >= 0: return 1
        if a <= 0 and b <= 0: return -1
        # opposite signs: compare a^2 with D*b^2
        lhs, rhs = a*a, D*b*b
        if a > 0:                 # a > 0 > b : positive iff a^2 > D b^2
            return 1 if lhs > rhs else (0 if lhs == rhs else -1)
        else:                     # a < 0 < b : positive iff D b^2 > a^2
            return 1 if rhs > lhs else (0 if rhs == lhs else -1)
    def __abs__(s): return s if s.sign() >= 0 else -s
    def cmp(s, o):
        d = (s - o).sign()
        return d
    def __repr__(s): return "(%s + %s*sqrt%d)" % (s.a, s.b, s.D)

def cmp_frac(n1, d1, n2, d2):
    """Compare n1/d1 vs n2/d2 for Q elements with d1, d2 > 0.  Returns -1, 0, 1."""
    assert d1.sign() > 0 and d2.sign() > 0
    return (n1*d2 - n2*d1).sign()
