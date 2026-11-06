"""1단원 실험: 부동소수점과 오차"""
import math
import sys

import numpy as np


def section(title):
    print(f"\n=== {title} ===")


# 실험 1: 0.1 + 0.2
section("실험 1: 0.1 + 0.2")
print("0.1 + 0.2        =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3 :", 0.1 + 0.2 == 0.3)
print("0.1 을 50자리로   =", f"{0.1:.50f}")
print("isclose 로 비교   :", math.isclose(0.1 + 0.2, 0.3))


# 실험 2: 기계 엡실론을 직접 찾기
section("실험 2: 기계 엡실론")
eps = 1.0
while 1.0 + eps / 2 > 1.0:
    eps /= 2
print("직접 찾은 eps  =", eps)
print("numpy가 아는 eps =", np.finfo(float).eps)
print("sys.float_info.epsilon =", sys.float_info.epsilon)


# 실험 3: 오차의 누적
section("실험 3: 0.1을 반복해서 더하기")
for n in (10, 1_000, 1_000_000):
    s = 0.0
    for _ in range(n):
        s += 0.1
    exact = n * 0.1
    print(f"n={n:>9,}  합={s!r:<24} 기대값={exact!r:<24} 오차={abs(s - exact):.3e}")
print("math.fsum (정밀 합산) n=1,000,000:", math.fsum([0.1] * 1_000_000))


# 실험 4: 상쇄 (catastrophic cancellation)
section("실험 4: (1 - cos x) / x^2, 참값은 x->0 에서 0.5")
print(f"{'x':>10} {'나쁜 식':>22} {'좋은 식':>22}")
for k in range(1, 10):
    x = 10.0 ** (-k)
    bad = (1 - math.cos(x)) / x**2
    good = 2 * math.sin(x / 2) ** 2 / x**2
    print(f"{x:>10.0e} {bad:>22.15f} {good:>22.15f}")


# 실험 5: 큰 수 + 작은 수
section("실험 5: 큰 수에 작은 수 더하기")
big = 1e16
print("1e16 + 1 == 1e16 :", big + 1 == big)
print("1e16 + 2 == 1e16 :", big + 2 == big)
print("(왜 +1은 사라지고 +2는 살아남을까? float64 간격을 생각해 보세요)")
print("np.spacing(1e16) =", np.spacing(1e16))
