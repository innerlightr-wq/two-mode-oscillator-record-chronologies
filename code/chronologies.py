"""
Interior balance-record chronologies for additional frequency ratios.

alpha = (p + q*sqrt(d))/r  (quadratic case, q>0)  or  p/r (rational, q=0)
Defect (quadratic case): alpha is the root of x^2 - t x - s = 0, and
    N(m,k) = k^2 - t*k*m - s*m^2   (integer norm form; for sqrt2: k^2-2m^2).

Exact ordering and exact eps comparisons throughout (integer pairs in Z[sqrt d],
or plain integers for rational / high-precision-rational alpha).
"""
import math, csv
from math import isqrt, gcd
from fractions import Fraction

def sgn2(a, b, d):
    if a == 0 and b == 0: return 0
    if a >= 0 and b >= 0: return 1
    if a <= 0 and b <= 0: return -1
    if a > 0:
        l, r = a*a, d*b*b
        return 1 if l > r else (-1 if l < r else 0)
    l, r = d*b*b, a*a
    return 1 if l > r else (-1 if l < r else 0)

def qmul(x, y, d):
    return (x[0]*y[0] + d*x[1]*y[1], x[0]*y[1] + x[1]*y[0])

def quad_record_scan(p, q, r, d, t, s, U, name, prune_M=None, Qmax=200):
    """Brute-force all odd (m,k) with u = m*alpha + k <= U; exact scan.
    Optionally extend with pruned candidates m <= prune_M, |N| <= Qmax."""
    af = (p + q*math.sqrt(d))/r
    states = []
    m = 1
    while m*af < U + 1:
        # exact: m*alpha < U  <=>  m p - U r + m q sqrt(d) < 0
        if sgn2(m*p - U*r, m*q, d) >= 0: break
        k = 1
        while True:
            # u <= U  <=>  (m p + k r - U r) + m q sqrt(d) <= 0
            if sgn2(m*p + k*r - U*r, m*q, d) <= 0:
                states.append((m, k)); k += 2
            else:
                break
        m += 2
    if prune_M:
        seen = set(states)
        for m in range(1, prune_M+1, 2):
            # k0 ~ m*alpha
            k0 = int(m*af)
            for k in range(max(1, k0-4), k0+6):
                if k % 2 == 1 and (m, k) not in seen:
                    N = k*k - t*k*m - s*m*m
                    if abs(N) <= Qmax and gcd(m, k) == 1:
                        states.append((m, k)); seen.add((m, k))
    # sort by u exactly: r*u = (m p + k r) + m q sqrt(d)
    states.sort(key=lambda mk: mk[0]*af + mk[1])
    for i in range(len(states)-1):
        m1,k1 = states[i]; m2,k2 = states[i+1]
        c = sgn2((m1-m2)*p + (k1-k2)*r, (m1-m2)*q, d)
        assert c <= 0
        if c == 0: assert (m1,k1) == (m2,k2)
    # record scan: eps = |m alpha - k| / (m alpha + k); scaled by r both.
    recs = []
    best = None   # (num_pair, u_pair) ints in Z[sqrt d]
    for m, k in states:
        u = (m*p + k*r, m*q)
        nraw = (m*p - k*r, m*q)
        sg = sgn2(*nraw, d)
        if sg == 0:
            num = (0, 0)   # exact zero
        else:
            num = (sg*nraw[0], sg*nraw[1])
        if best is None:
            better = True
        else:
            lhs = qmul(num, best[1], d)
            rhs = qmul(best[0], u, d)
            better = sgn2(lhs[0]-rhs[0], lhs[1]-rhs[1], d) < 0
        if better:
            N = k*k - t*k*m - s*m*m
            hf = (m*af + k)/2
            ef = abs(m*af - k)/(m*af + k)
            recs.append((m, k, N, hf, ef))
            best = (num, u)
            if num == (0, 0):
                break   # chronology terminates
    print(f"[{name}] states={len(states)}  records:")
    for m,k,N,hf,ef in recs:
        print(f"    (m,k)=({m},{k})  N={N:>6}  h={hf:.6f}  eps={ef:.6e}")
    return recs

def rational_record_scan(P, R, U, name):
    """alpha = P/R (>1).  Exact integer arithmetic; height ties handled."""
    states = []
    m = 1
    while m*P < U*R:
        k = 1
        while m*P + k*R <= U*R:
            states.append((m, k)); k += 2
        m += 2
    states.sort(key=lambda mk: mk[0]*P + mk[1]*R)   # exact integer key
    recs = []
    best = None   # (num, u) ints, eps = num/u with num=|mP-kR| (scaled by R both)
    i, n = 0, len(states)
    while i < n:
        j = i
        u0 = states[i][0]*P + states[i][1]*R
        while j+1 < n and states[j+1][0]*P + states[j+1][1]*R == u0:
            j += 1
        group = states[i:j+1]
        gm = min(group, key=lambda mk: abs(mk[0]*P - mk[1]*R))
        num = abs(gm[0]*P - gm[1]*R); u = gm[0]*P + gm[1]*R
        if best is None or num*best[1] < best[0]*u:
            winners = [mk for mk in group if abs(mk[0]*P - mk[1]*R)*u == num*(mk[0]*P + mk[1]*R)]
            for m, k in winners:
                N = num if (m,k)==gm else abs(m*P-k*R)
                hf = (m*P/R + k)/2
                ef = abs(m*P/R - k)/(m*P/R + k)
                recs.append((m, k, abs(m*P-k*R), hf, ef))
            best = (num, u)
            if num == 0:
                break
        i = j + 1
    print(f"[{name}] states={len(states)}  records:")
    for m,k,N,hf,ef in recs:
        print(f"    (m,k)=({m},{k})  |Pm-Rk|={N:>4}  h={hf:.6f}  eps={ef:.6e}")
    return recs

def hp_const(name, digits):
    """High-precision Fraction for e or pi (digits-decimal accuracy)."""
    scale = 10**(digits+10)
    if name == "e":
        # series sum 1/n!
        term = scale; total = 0; nfac = 1; nn = 0
        while term:
            total += term
            nn += 1
            term = term // nn if nn > 1 else scale  # careful: rebuild
        # redo cleanly
        total = 0; term = scale; nn = 0
        while term:
            total += term; nn += 1; term //= nn
        return Fraction(total, scale)
    if name == "pi":
        # Chudnovsky via integer arithmetic (few terms suffice)
        # use Machin-like: pi = 16 atan(1/5) - 4 atan(1/239)
        def atan_inv(x):
            # atan(1/x)*scale
            total = 0; termnum = scale // x; k = 0; xsq = x*x
            while termnum:
                total += termnum // (2*k+1) * (1 if k % 2 == 0 else -1)
                termnum //= xsq; k += 1
            return total
        val = 16*atan_inv(5) - 4*atan_inv(239)
        return Fraction(val, scale)
    raise ValueError

def real_record_scan(alpha, U, name):
    """alpha: Fraction surrogate; exact scan wrt the surrogate."""
    P, R = alpha.numerator, alpha.denominator
    af = P / R
    states = []
    m = 1
    while m*af < U + 1:
        if m*P >= U*R: break
        k = 1
        while m*P + k*R <= U*R:
            states.append((m, k)); k += 2
        m += 2
    states.sort(key=lambda mk: mk[0]*P + mk[1]*R)
    recs = []
    best = None
    for m, k in states:
        num = abs(m*P - k*R); u = m*P + k*R
        if best is None or num*best[1] < best[0]*u:
            hf = (m*af + k)/2; ef = abs(m*af - k)/(m*af + k)
            recs.append((m, k, hf, ef))
            best = (num, u)
    print(f"[{name}] states={len(states)}  records:")
    for m,k,hf,ef in recs:
        print(f"    (m,k)=({m},{k})  h={hf:.6f}  eps={ef:.6e}")
    return recs

def write_csv(fn, rows, header):
    with open(fn, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header)
        for row in rows: w.writerow(row)

if __name__ == "__main__":
    print("="*72)
    # sqrt2 cross-check against audited chronology
    r2 = quad_record_scan(0,1,1,2, 0,2, 800, "sqrt2 (cross-check)")
    assert [(m,k) for m,k,*_ in r2][:6] == [(1,1),(3,5),(5,7),(19,27),(29,41),(111,157)]
    print("[sqrt2] matches audited P/S chronology: True")

    print("="*72)
    phi = quad_record_scan(1,1,2,5, 1,1, 1500, "phi", prune_M=3_000_000, Qmax=200)
    write_csv("chron_phi.csv",
              [(j,m,k,N,f"{h:.10f}",f"{e:.10e}") for j,(m,k,N,h,e) in enumerate(phi)],
              ["j","m","k","N=k2-km-m2","h","eps_bal"])

    print("="*72)
    s3 = quad_record_scan(1,1,1,3, 2,2, 1500, "1+sqrt3", prune_M=3_000_000, Qmax=200)
    write_csv("chron_1plus_sqrt3.csv",
              [(j,m,k,N,f"{h:.10f}",f"{e:.10e}") for j,(m,k,N,h,e) in enumerate(s3)],
              ["j","m","k","N=k2-2km-2m2","h","eps_bal"])

    print("="*72)
    r32 = rational_record_scan(3,2, 400, "3/2")
    write_csv("chron_rational_3_2.csv",
              [(j,m,k,N,f"{h:.10f}",f"{e:.10e}") for j,(m,k,N,h,e) in enumerate(r32)],
              ["j","m","k","|3m-2k|","h","eps_bal"])
    r53 = rational_record_scan(5,3, 400, "5/3")
    write_csv("chron_rational_5_3.csv",
              [(j,m,k,N,f"{h:.10f}",f"{e:.10e}") for j,(m,k,N,h,e) in enumerate(r53)],
              ["j","m","k","|5m-3k|","h","eps_bal"])

    print("="*72)
    e60 = hp_const("e", 60); e120 = hp_const("e", 120)
    re1 = real_record_scan(e60, 3000, "e (60d)")
    re2 = real_record_scan(e120, 3000, "e (120d)")
    print("[e] 60-digit and 120-digit surrogates give identical records:",
          [(m,k) for m,k,*_ in re1] == [(m,k) for m,k,*_ in re2])
    write_csv("chron_e.csv",
              [(j,m,k,f"{h:.10f}",f"{e:.10e}") for j,(m,k,h,e) in enumerate(re1)],
              ["j","m","k","h","eps_bal"])

    pi60 = hp_const("pi", 60); pi120 = hp_const("pi", 120)
    rp1 = real_record_scan(pi60, 3000, "pi (60d)")
    rp2 = real_record_scan(pi120, 3000, "pi (120d)")
    print("[pi] 60-digit and 120-digit surrogates give identical records:",
          [(m,k) for m,k,*_ in rp1] == [(m,k) for m,k,*_ in rp2])
    write_csv("chron_pi.csv",
              [(j,m,k,f"{h:.10f}",f"{e:.10e}") for j,(m,k,h,e) in enumerate(rp1)],
              ["j","m","k","h","eps_bal"])
