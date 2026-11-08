"""The two slopes, as exact data.  Nothing here is numerical.

alpha > 1 quadratic with minimal polynomial x^2 - t x - s, conjugate alpha'.
State (m, k), m and k positive odd.  Height h = (m alpha + k)/2.
Balance error eps = |m alpha - k| / (m alpha + k).
Defect N(m, k) = k^2 - t k m - s m^2 = (k - m alpha)(k - m alpha').

phi:      t = 1, s = 1, alpha = (1+sqrt5)/2,  N = k^2 - km - m^2
1+sqrt3:  t = 2, s = 2, alpha = 1 + sqrt3,    N = k^2 - 2km - 2m^2
"""
from fractions import Fraction
from quad import Q

class Setup:
    def __init__(self, name, D, t, s, a_num_a, a_num_b, a_den):
        self.name=name; self.D=D; self.t=t; self.s=s
        # alpha = (a_num_a + a_num_b*sqrt(D)) / a_den
        self.an_a=Fraction(a_num_a); self.an_b=Fraction(a_num_b); self.ad=Fraction(a_den)
    def alpha(self):
        return Q(self.an_a/self.ad, self.an_b/self.ad, self.D)
    def N(self, m, k):
        return k*k - self.t*k*m - self.s*m*m
    def num_err(self, m, k):
        """m*alpha - k as an exact Q element."""
        al = self.alpha()
        return Q(al.a*m - k, al.b*m, self.D)
    def den_err(self, m, k):
        """m*alpha + k."""
        al = self.alpha()
        return Q(al.a*m + k, al.b*m, self.D)
    def height2(self, m, k):
        """2h = m*alpha + k (ordering by 2h is ordering by h)."""
        return self.den_err(m, k)
    def eta(self, m, k):
        """k - m*alpha' , the large conjugate factor; N = (k - m alpha)(k - m alpha')."""
        al = self.alpha()
        ap = Q(al.a, -al.b, self.D)          # alpha' = conj(alpha)
        return Q(k - ap.a*m, -ap.b*m, self.D)
    def eps_parts(self, m, k):
        """eps = |num| / den, both exact; den > 0."""
        return abs(self.num_err(m, k)), self.den_err(m, k)

PHI  = Setup("phi",      5, 1, 1, 1, 1, 2)
S3   = Setup("1+sqrt3",  3, 2, 2, 1, 1, 1)
SQ3  = Setup("sqrt3",    3, 0, 3, 0, 1, 1)      # alpha = sqrt3, t = 0: eps = |N|/(2h)^2 EXACTLY

# Per-setup lattice data for the orbit machinery.
#   eta = a + b*w  with w = phi or sqrt(D);  (m,k) recovered by MK; admissibility by ADM;
#   RHO = the least unit > 1 preserving ADM.
# phi      : eta = (k-m) + m phi,  a even, b odd,  rho = phi^3 = 1 + 2 phi
# 1+sqrt3  : eta = (k-m) + m sqrt3, a even, b odd, rho = (2+sqrt3)^2 = 7 + 4 sqrt3
# sqrt3    : eta = k + m sqrt3,     a odd,  b odd, rho = 2 + sqrt3
LATTICE = {
  "phi":     dict(MK=lambda a,b:(b,a+b), ADM=lambda a,b: a%2==0 and b%2!=0, RHO=(1,2),
                  NORM=lambda a,b: a*a+a*b-b*b, ETA_L=(0,1), L=1),
  "1+sqrt3": dict(MK=lambda a,b:(b,a+b), ADM=lambda a,b: a%2==0 and b%2!=0, RHO=(7,4),
                  NORM=lambda a,b: a*a-3*b*b,   ETA_L=(2,1), L=1),
  "sqrt3":   dict(MK=lambda a,b:(b,a),   ADM=lambda a,b: a%2!=0 and b%2!=0, RHO=(2,1),
                  NORM=lambda a,b: a*a-3*b*b,   ETA_L=(1,1), L=2),
}
