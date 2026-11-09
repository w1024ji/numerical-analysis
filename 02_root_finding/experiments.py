"""2단원 실험: 근 찾기. 실행하면 figures/ 폴더에 그래프가 저장됩니다.

    python 02_root_finding/experiments.py
"""
import math
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common_plot import save  # noqa: E402
from rootfinding import bisection, fixed_point, newton, secant, estimate_order  # noqa: E402

HERE = __file__


def section(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------- 실험 1
section("실험 1: 이분법으로 sqrt(2) 찾기 (f(x) = x^2 - 2, 구간 [0, 2])")
f = lambda x: x**2 - 2
root, hist = bisection(f, 0, 2, tol=1e-10)
print(f"{'n':>3} {'중점 c_n':>20} {'|c_n - sqrt2|':>16} {'구간 절반 길이':>16}")
for n, c in enumerate(hist[:12], start=1):
    print(f"{n:>3} {c:>20.15f} {abs(c - math.sqrt(2)):>16.3e} {2 / 2**n:>16.3e}")
print(f"... 총 {len(hist)}번 반복해서 {root:.12f}")
print("이론상 필요한 횟수 n >= log2((b-a)/tol) =", math.ceil(math.log2(2 / 1e-10)))

# 그림 1: 이분법 단계별 구간
fig, ax = plt.subplots(figsize=(8, 4.5))
xs = np.linspace(0, 2, 300)
ax.plot(xs, f(xs), "k-", lw=2, label=r"$f(x)=x^2-2$")
ax.axhline(0, color="gray", lw=1)
a, b = 0.0, 2.0
colors = plt.cm.viridis(np.linspace(0, 0.85, 5))
for k in range(5):
    y = -1.6 - 0.45 * k
    ax.plot([a, b], [y, y], "-", color=colors[k], lw=6, solid_capstyle="butt")
    ax.text(2.03, y, f"구간 {k}  길이 {b - a:.3f}", va="center", fontsize=9)
    c = (a + b) / 2
    ax.plot([c], [y], "wo", ms=5, mec="k")
    if f(a) * f(c) < 0:
        b = c
    else:
        a = c
ax.plot([math.sqrt(2)], [0], "r*", ms=15, label=r"참값 $\sqrt{2}$")
ax.set_xlim(-0.1, 3.0)
ax.set_xlabel("x")
ax.set_title("이분법: 매 단계 구간이 절반으로 줄어든다 (흰 점 = 중점)")
ax.legend(loc="upper left")
save(fig, HERE, "02_bisection_steps.png")

# ---------------------------------------------------------------- 실험 2
section("실험 2: 고정점 반복  x = cos(x)")
root_fp, hist_fp = fixed_point(math.cos, 1.0, tol=1e-12)
r = 0.7390851332151607  # cos(x) = x 의 근 (참값, 충분히 정밀하게 알려진 값)
print(f"수렴한 값 {root_fp:.15f}, 반복 {len(hist_fp) - 1}번")
errs = [abs(x - r) for x in hist_fp[:10]]
print("연속 오차 비 e_{n+1}/e_n :", [f"{errs[i + 1] / errs[i]:.3f}" for i in range(len(errs) - 1)])
print("  → 비가 약 |g'(r)| = |sin r| =", f"{abs(math.sin(r)):.3f}", "로 일정하다. (선형 수렴)")


def cobweb(ax, g, x0, n, lo, hi, title):
    xs = np.linspace(lo, hi, 300)
    ax.plot(xs, g(xs), "b-", lw=2, label="y = g(x)")
    ax.plot(xs, xs, "k--", lw=1, label="y = x")
    x = x0
    for _ in range(n):
        y = g(x)
        ax.plot([x, x], [x, y], "r-", lw=1)   # 세로: x -> g(x)
        ax.plot([x, y], [y, y], "r-", lw=1)   # 가로: y 를 다음 x 로
        x = y
    ax.plot([x0], [x0], "go")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_title(title)
    ax.legend(loc="upper left")


fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
cobweb(axes[0], np.cos, 0.1, 12, 0, 1.2, "수렴: g(x)=cos x,  |g'| 약 0.67 < 1")
cobweb(axes[1], lambda x: 2.5 - 1.5 * x, 1.1, 7, 0.0, 2.2, "발산: g(x)=2.5-1.5x,  |g'|=1.5 > 1")
save(fig, HERE, "02_cobweb.png")

# ---------------------------------------------------------------- 실험 3
section("실험 3: 뉴턴법으로 sqrt(2) 찾기")
df = lambda x: 2 * x
root_n, hist_n = newton(f, df, 2.0, tol=1e-15)
print(f"{'n':>2} {'x_n':>22} {'|x_n - sqrt2|':>16}")
for n, x in enumerate(hist_n):
    print(f"{n:>2} {x:>22.16f} {abs(x - math.sqrt(2)):>16.3e}")
print("→ 오차가 0.5858 → 8.6e-2 → 2.5e-3 → 2.1e-6 → 1.6e-12: 맞는 자릿수가 매번 '두 배'")

fig, ax = plt.subplots(figsize=(8, 4.8))
xs = np.linspace(0.8, 2.3, 300)
ax.plot(xs, f(xs), "k-", lw=2, label=r"$f(x)=x^2-2$")
ax.axhline(0, color="gray", lw=1)
x = 2.0
for k in range(3):
    fx, slope = f(x), df(x)
    x_next = x - fx / slope
    tx = np.linspace(x_next - 0.15, x + 0.1, 20)
    ax.plot(tx, fx + slope * (tx - x), "-", color="tab:orange", lw=1.5)
    ax.plot([x, x], [0, fx], ":", color="tab:red")
    ax.plot([x], [fx], "o", color="tab:red")
    offsets = [(0, -22), (28, -34), (-34, -34)]  # 라벨끼리 겹치지 않게 위치를 따로 준다
    ax.annotate(f"$x_{k}$={x:.4f}", (x, 0), textcoords="offset points", xytext=offsets[k], ha="center",
                fontsize=9, arrowprops=dict(arrowstyle="-", color="gray", lw=0.8))
    x = x_next
ax.plot([math.sqrt(2)], [0], "r*", ms=15, label=r"참값 $\sqrt{2}$")
ax.set_xlabel("x")
ax.set_ylim(-1.5, 3)
ax.set_title("뉴턴법: 접선이 x축과 만나는 점이 다음 근사값")
ax.legend(loc="upper left")
save(fig, HERE, "02_newton_geometry.png")

# ---------------------------------------------------------------- 실험 4
section("실험 4: 네 방법 비교  f(x) = cos(x) - x,  참값 r = 0.7390851332151607")
fc = lambda x: math.cos(x) - x
dfc = lambda x: -math.sin(x) - 1
_, h_bis = bisection(fc, 0, 1, tol=1e-15)
_, h_fp = fixed_point(math.cos, 1.0, tol=1e-15)
_, h_sec = secant(fc, 0.0, 1.0, tol=1e-15)
_, h_new = newton(fc, dfc, 1.0, tol=1e-15)
for name, h in [("이분법", h_bis), ("고정점", h_fp), ("할선법", h_sec), ("뉴턴법", h_new)]:
    print(f"{name}: 반복 {len(h)}번")


def errs_of(h):
    return [max(abs(x - r), 1e-17) for x in h]


fig, ax = plt.subplots(figsize=(8.5, 5))
for name, h, style in [("이분법", h_bis, "o-"), ("고정점 반복", h_fp, "s-"),
                       ("할선법", h_sec, "^-"), ("뉴턴법", h_new, "d-")]:
    ax.semilogy(range(len(h)), errs_of(h), style, ms=4, label=name)
ax.axhline(2.2e-16, color="gray", ls="--")
ax.text(40, 3.5e-16, "기계 엡실론 약 2.2e-16", color="gray", fontsize=9)
ax.set_xlim(0, 50)
ax.set_xlabel("반복 횟수 n")
ax.set_ylabel("오차 |x_n - r|  (로그 눈금)")
ax.set_title("같은 문제를 푸는 네 가지 방법의 수렴 속도")
ax.legend()
save(fig, HERE, "02_convergence_compare.png")

# ---------------------------------------------------------------- 실험 5
section("실험 5: 수렴 차수 추정  (f(x) = x^2 - 2)")
#   float64 로는 오차가 1e-16 에서 멈춰서 차수를 못 본다 → 60자리 Decimal 로 계산한다.
from decimal import Decimal, getcontext  # noqa: E402

getcontext().prec = 60
fD = lambda x: x * x - 2
dfD = lambda x: 2 * x
exactD = Decimal(2).sqrt()
_, hnD = newton(fD, dfD, Decimal(1), tol=Decimal(0), max_iter=6)
_, hsD = secant(fD, Decimal(1), Decimal(2), tol=Decimal(0), max_iter=10)
en = [float(abs(x - exactD)) for x in hnD]
es = [float(abs(x - exactD)) for x in hsD]
print("뉴턴 오차 :", [f"{e:.1e}" for e in en])
print("뉴턴 차수 추정:", [f"{p:.2f}" for p in estimate_order([abs(x - exactD) for x in hnD])], "(이론: 2)")
print("할선 오차 :", [f"{e:.1e}" for e in es])
print("할선 차수 추정:", [f"{p:.2f}" for p in estimate_order([abs(x - exactD) for x in hsD])], "(이론: 약 1.618)")
hn = [float(x) for x in hnD]  # 실험 6 그래프에서 재사용

# ---------------------------------------------------------------- 실험 6
section("실험 6: 뉴턴법이 실패할 때")
g = lambda x: x**3 - 2 * x + 2
dg = lambda x: 3 * x**2 - 2
_, hc = newton(g, dg, 0.0, max_iter=8)
print("f=x^3-2x+2, x0=0 :", [round(x, 3) for x in hc], "← 0 과 1 을 영원히 왕복")

# 겹근: (x-1)^2 = 0 에서는 뉴턴이 선형 수렴으로 떨어진다
m = lambda x: (x - 1) ** 2
dm = lambda x: 2 * (x - 1)
_, hm = newton(m, dm, 2.0, tol=0, max_iter=30)
em = [abs(x - 1) for x in hm]
print("겹근 (x-1)^2 에서 오차 :", [f"{e:.1e}" for e in em[:6]], "← 매번 정확히 절반")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
xs = np.linspace(-1.5, 1.8, 300)
axes[0].plot(xs, g(xs), "k-", lw=2, label=r"$f(x)=x^3-2x+2$")
axes[0].axhline(0, color="gray", lw=1)
x = 0.0
for _ in range(4):
    x_next = x - g(x) / dg(x)
    tx = np.linspace(min(x, x_next) - 0.2, max(x, x_next) + 0.2, 10)
    axes[0].plot(tx, g(x) + dg(x) * (tx - x), "-", color="tab:orange")
    axes[0].plot([x, x], [0, g(x)], ":", color="tab:red")
    x = x_next
axes[0].set_ylim(-2, 5)
axes[0].set_title("뉴턴법의 함정 1: x0=0 에서 0↔1 무한 왕복")
axes[0].legend(loc="upper left")
axes[1].semilogy(range(len(em)), em, "o-", label="겹근 (x-1)^2 : 오차가 절반씩")
axes[1].semilogy(range(len(hn)), [max(e, 1e-17) for e in en], "d-", label="단순근 x^2-2 : 제곱씩")
axes[1].set_xlim(0, 12)
axes[1].set_ylim(1e-17, 2)
axes[1].set_xlabel("반복 횟수 n")
axes[1].set_title("뉴턴법의 함정 2: 겹근에서는 느려진다")
axes[1].legend()
save(fig, HERE, "02_newton_failures.png")

# ---------------------------------------------------------------- 실험 7
section("실험 7: 뉴턴 프랙탈  z^3 - 1 = 0 (복소수 평면)")
N = 700
xs = np.linspace(-1.6, 1.6, N)
Z = xs[None, :] + 1j * xs[:, None]
roots = np.array([1, np.exp(2j * np.pi / 3), np.exp(-2j * np.pi / 3)])
iters = np.zeros(Z.shape, dtype=int)
for k in range(40):
    with np.errstate(all="ignore"):
        Z = Z - (Z**3 - 1) / (3 * Z**2)
    done = (np.abs(Z[..., None] - roots).min(axis=-1) < 1e-6) & (iters == 0)
    iters[done] = k + 1
iters[iters == 0] = 40
basin = np.abs(Z[..., None] - roots).argmin(axis=-1)
img = np.zeros(Z.shape + (3,))
base = np.array([[0.85, 0.25, 0.25], [0.25, 0.65, 0.3], [0.25, 0.4, 0.85]])
shade = 1.0 - (iters / 40.0) ** 0.6 * 0.85
for i in range(3):
    img[basin == i] = base[i]
img *= shade[..., None]
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.imshow(img, extent=(-1.6, 1.6, -1.6, 1.6), origin="lower")
ax.plot(roots.real, roots.imag, "w*", ms=14, mec="k")
ax.set_title("뉴턴법의 '수렴 영역' 지도: 시작점 색 = 도착하는 근")
ax.set_xlabel("실수부")
ax.set_ylabel("허수부")
ax.grid(False)
save(fig, HERE, "02_newton_fractal.png")
print("그래프를 확인해 보세요 → figures/ 폴더")
