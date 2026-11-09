"""3단원 실험: 연립일차방정식. 실행하면 figures/ 폴더에 그래프가 저장됩니다.

    python 03_linear_systems/experiments.py        (약 20~40초 걸려요. 실험 5 의 시간 측정 때문)
"""
import os
import sys
import time
from decimal import Decimal, getcontext

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common_plot import save  # noqa: E402
from linsys import (gauss_solve, lu_decompose, lu_solve, jacobi, gauss_seidel, sor,  # noqa: E402
                    jacobi_matrix, gauss_seidel_matrix, spectral_radius, is_diagonally_dominant)

HERE = __file__
np.set_printoptions(precision=4, suppress=True, linewidth=120)


def section(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------- 실험 1
section("실험 1: 2x2 연립방정식의 기하학적 의미 (그림만 저장)")
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
xs = np.linspace(-1, 5, 100)
# (a) 해가 하나: x + y = 3,  x - y = 1   → (2, 1)
axes[0].plot(xs, 3 - xs, label="x + y = 3")
axes[0].plot(xs, xs - 1, label="x - y = 1")
axes[0].plot([2], [1], "k*", ms=14)
axes[0].set_title("해가 하나: 두 직선이 한 점에서 만난다")
# (b) 해가 없음: 평행
axes[1].plot(xs, 3 - xs, label="x + y = 3")
axes[1].plot(xs, 4 - xs, label="x + y = 4")
axes[1].set_title("해가 없음: 평행한 두 직선 (특이행렬)")
# (c) 해가 무수히 많음: 같은 직선
axes[2].plot(xs, 3 - xs, lw=6, alpha=0.5, label="x + y = 3")
axes[2].plot(xs, 3 - xs, "--", label="2x + 2y = 6")
axes[2].set_title("해가 무수히 많음: 같은 직선 (특이행렬)")
for ax in axes:
    ax.set_xlim(-1, 5)
    ax.set_ylim(-2, 5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right")
save(fig, HERE, "03_geometry.png")

# ---------------------------------------------------------------- 실험 2
section("실험 2: 가우스 소거 과정을 한 단계씩 (손으로 푸는 것과 똑같이)")
A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
b = np.array([8, -11, -3], dtype=float)
print("A | b =")
print(np.column_stack([A, b]))
x = gauss_solve(A, b, pivot=False, verbose=True)
print("해 x =", x, " (정답: [2, 3, -1])")

# ---------------------------------------------------------------- 실험 3
section("실험 3: 피벗팅이 왜 필요한가   A = [[eps, 1], [1, 1]],  b = [1, 2]")
getcontext().prec = 60


def exact_x1(eps):
    """x1 = 1/(1-eps) 의 참값 (60자리 정밀도)"""
    return 1 / (1 - Decimal(eps))


print(f"{'eps':>8} {'피벗팅 없음 x1':>18} {'피벗팅 x1':>18} {'참값 x1':>18}")
eps_list = [10.0**-k for k in range(1, 21)]
err_no, err_yes = [], []
for eps in eps_list:
    A = np.array([[eps, 1.0], [1.0, 1.0]])
    b = np.array([1.0, 2.0])
    x_no = gauss_solve(A, b, pivot=False)
    x_yes = gauss_solve(A, b, pivot=True)
    ex = float(exact_x1(eps))
    err_no.append(max(abs(x_no[0] - ex), 1e-17))
    err_yes.append(max(abs(x_yes[0] - ex), 1e-17))
    if round(-np.log10(eps)) in (1, 4, 8, 12, 16, 20):
        print(f"{eps:>8.0e} {x_no[0]:>18.12f} {x_yes[0]:>18.12f} {ex:>18.12f}")

fig, ax = plt.subplots(figsize=(8.5, 4.8))
ax.loglog(eps_list, err_no, "o-", label="피벗팅 없음", color="tab:red")
ax.loglog(eps_list, err_yes, "s-", label="부분 피벗팅", color="tab:blue")
ax.loglog(eps_list, [2.2e-16 / e for e in eps_list], "k--", lw=1, label="기계 엡실론 / eps  (이론적 증가 추세)")
ax.set_xlabel("첫 피벗 eps (오른쪽으로 갈수록 더 작다)")
ax.set_ylabel("x1 의 절대오차")
ax.set_title("피벗이 작을수록 피벗팅 없는 소거의 오차가 폭발한다")
ax.invert_xaxis()
ax.legend()
save(fig, HERE, "03_pivoting.png")

# ---------------------------------------------------------------- 실험 4
section("실험 4: LU 분해  (A 를 L 과 U 로 쪼개기)")
A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
perm, L, U = lu_decompose(A)
print("perm =", perm, " (행을 이 순서로 섞었다는 뜻)")
print("L =\n", L)
print("U =\n", U)
print("A[perm] 와 L @ U 의 차이 =", np.abs(A[perm] - L @ U).max())
swaps = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))   # 순열의 역전 개수
sign = (-1) ** swaps                                                       # 행 교환 부호
print("det(A) = (행 교환 부호) × (U 의 대각선 곱)")
print("   numpy:", round(np.linalg.det(A), 6), "  직접 계산:", round(sign * np.prod(np.diag(U)), 6))
print("해 =", lu_solve(perm, L, U, np.array([8, -11, -3.0])))

# ---------------------------------------------------------------- 실험 5
section("실험 5: 계산 시간이 n 에 따라 어떻게 늘어나는가 (이론: n^3)")
ns = [100, 200, 400, 800, 1600]
t_mine, t_np = [], []
rng = np.random.default_rng(1)
np.linalg.solve(rng.normal(size=(50, 50)), rng.normal(size=50))   # 워밍업 (첫 호출의 초기화 시간 제외)
print(f"{'n':>6} {'내 가우스 소거(초)':>20} {'numpy.linalg.solve(초)':>26}")
for n in ns:
    A = rng.normal(size=(n, n))
    b = rng.normal(size=n)
    t0 = time.perf_counter()
    gauss_solve(A, b)
    t_mine.append(time.perf_counter() - t0)
    t0 = time.perf_counter()
    np.linalg.solve(A, b)
    t_np.append(time.perf_counter() - t0)
    print(f"{n:>6} {t_mine[-1]:>20.4f} {t_np[-1]:>26.4f}")
print("n 이 2배가 될 때 시간 배율(내 소거):", [f"{t_mine[i + 1] / t_mine[i]:.1f}" for i in range(len(ns) - 1)], " (이론값 8)")

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.loglog(ns, t_mine, "o-", label="내 가우스 소거")
ax.loglog(ns, t_np, "s-", label="numpy.linalg.solve (LAPACK)")
ref = np.array(ns, dtype=float) ** 3
ax.loglog(ns, ref / ref[-1] * t_mine[-1], "k--", lw=1, label="기울기 3 (n^3)")
ax.set_xlabel("행렬 크기 n")
ax.set_ylabel("걸린 시간 (초)")
ax.set_title("가우스 소거의 비용은 n^3 에 비례한다 (로그-로그에서 기울기 3)")
ax.legend()
save(fig, HERE, "03_scaling.png")

section("실험 5b: LU 분해는 '한 번 쪼개 두고 여러 번 재사용' 하는 것")
n, k = 400, 30
A = rng.normal(size=(n, n))
bs = rng.normal(size=(k, n))
t0 = time.perf_counter()
for bb in bs:
    gauss_solve(A, bb)
t_every = time.perf_counter() - t0
t0 = time.perf_counter()
perm, L, U = lu_decompose(A)
t_fact = time.perf_counter() - t0
t0 = time.perf_counter()
for bb in bs:
    lu_solve(perm, L, U, bb)
t_solves = time.perf_counter() - t0
print(f"n={n}, 우변 b {k}개")
print(f"  매번 처음부터 소거      : {t_every:.3f} 초")
print(f"  LU 한 번 + 대입 {k}번   : {t_fact:.3f} + {t_solves:.3f} = {t_fact + t_solves:.3f} 초")

# ---------------------------------------------------------------- 실험 6
section("실험 6: 조건수 - 힐베르트 행렬")
print(f"{'n':>3} {'cond(H)':>12} {'해의 상대오차':>16} {'상대 잔차':>14}")
rows = []
for n in range(2, 15):
    H = 1.0 / (np.arange(1, n + 1)[:, None] + np.arange(n)[None, :])   # H[i,j] = 1/(i+j+1)
    x_true = np.ones(n)
    b = H @ x_true
    x = np.linalg.solve(H, b)
    err = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
    res = np.linalg.norm(b - H @ x) / np.linalg.norm(b)
    c = np.linalg.cond(H)
    rows.append((n, c, err, res))
    print(f"{n:>3} {c:>12.3e} {err:>16.3e} {res:>14.3e}")
Hs = np.array(rows)
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.semilogy(Hs[:, 0], Hs[:, 1], "k^-", label="조건수 cond(H)")
ax.semilogy(Hs[:, 0], Hs[:, 1] * 2.2e-16, "k--", lw=1, label="cond × 기계엡실론 (오차의 이론적 상한 추세)")
ax.semilogy(Hs[:, 0], np.maximum(Hs[:, 2], 1e-17), "o-", color="tab:red", label="해의 상대오차")
ax.semilogy(Hs[:, 0], np.maximum(Hs[:, 3], 1e-17), "s-", color="tab:blue", label="상대 잔차 (b - Hx)")
ax.set_xlabel("행렬 크기 n")
ax.set_title("힐베르트 행렬: 잔차는 항상 작은데 해는 점점 엉터리가 된다")
ax.legend(fontsize=9)
save(fig, HERE, "03_condition.png")

# ---------------------------------------------------------------- 실험 7
section("실험 7: Jacobi vs Gauss-Seidel 을 손으로 따라가기 (4x4 예제)")
A = np.array([[10, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8]], dtype=float)
b = np.array([6, 25, -11, 15], dtype=float)
x_true = np.array([1, 2, -1, 1], dtype=float)
print("대각 우세 행렬인가?", is_diagonally_dominant(A), "  정답 x =", x_true)
xj = np.zeros(4)
xg = np.zeros(4)
print(f"{'k':>2} | {'Jacobi x_k':<36} {'오차':>9} | {'Gauss-Seidel x_k':<36} {'오차':>9}")
for k in range(0, 7):
    print(f"{k:>2} | {str(np.round(xj, 4)):<36} {np.linalg.norm(xj - x_true):>9.2e} | "
          f"{str(np.round(xg, 4)):<36} {np.linalg.norm(xg - x_true):>9.2e}")
    xj, _ = jacobi(A, b, x0=xj, max_iter=1)
    xg, _ = gauss_seidel(A, b, x0=xg, max_iter=1)

# ---------------------------------------------------------------- 실험 8
section("실험 8: 수렴 속도 비교 (스펙트럴 반지름)")


def tridiag(n, diag):
    return diag * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)


results = {}
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
cases = [("(a) 대각 우세 (대각 4, 나머지 -1), n=50", tridiag(50, 4.0), 1.1),
         ("(b) 1차원 푸아송 (대각 2, 나머지 -1), n=30", tridiag(30, 2.0), None)]
for ax, (title, A, om) in zip(axes, cases):
    n = A.shape[0]
    b = np.ones(n)
    rJ = spectral_radius(jacobi_matrix(A))
    rG = spectral_radius(gauss_seidel_matrix(A))
    # SOR 최적 omega: 이 형태의 행렬에서는 2 / (1 + sqrt(1 - rJ^2)) 로 알려져 있다
    omega = 2 / (1 + np.sqrt(1 - rJ**2))
    rS = spectral_radius(np.linalg.solve(np.diag(np.diag(A)) / omega + np.tril(A, -1),
                                         (1 / omega - 1) * np.diag(np.diag(A)) - np.triu(A, 1)))
    _, hj = jacobi(A, b, tol=1e-8, max_iter=20000)
    _, hg = gauss_seidel(A, b, tol=1e-8, max_iter=20000)
    _, hs = sor(A, b, omega=omega, tol=1e-8, max_iter=20000)
    print(title)
    print(f"   스펙트럴 반지름   Jacobi={rJ:.5f}  Gauss-Seidel={rG:.5f} (= Jacobi^2 = {rJ**2:.5f})  SOR(w={omega:.3f})={rS:.5f}")
    print(f"   상대잔차 1e-8 까지 반복 횟수   Jacobi={len(hj) - 1}  Gauss-Seidel={len(hg) - 1}  SOR={len(hs) - 1}")
    print(f"   이론 예측 반복 횟수 ln(1e-8)/ln(rho)   Jacobi~{np.log(1e-8) / np.log(rJ):.0f}  GS~{np.log(1e-8) / np.log(rG):.0f}  SOR~{np.log(1e-8) / np.log(rS):.0f}")
    results[title] = (len(hj) - 1, len(hg) - 1, len(hs) - 1)
    ax.semilogy(hj, label=f"Jacobi  (rho={rJ:.4f})")
    ax.semilogy(hg, label=f"Gauss-Seidel  (rho={rG:.4f})")
    ax.semilogy(hs, label=f"SOR w={omega:.2f}  (rho={rS:.4f})")
    kk = np.arange(len(hj))
    ax.semilogy(kk, rJ**kk * hj[0], "k:", lw=1, label="rho_J^k (이론 기울기)")
    ax.set_ylim(1e-9, 3)
    ax.set_xlim(0, min(len(hj), 600) if om else len(hj) * 0.9)
    ax.set_xlabel("반복 횟수 k")
    ax.set_ylabel("상대잔차  norm(b - A x_k) / norm(b)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=9)
save(fig, HERE, "03_jacobi_vs_gs.png")

# ---------------------------------------------------------------- 실험 9
section("실험 9: 같은 연립방정식, 방정식 순서만 바꿨는데 수렴/발산이 갈린다")
A1 = np.array([[1, 2], [3, 1]], dtype=float)
b1 = np.array([3, 4], dtype=float)         # 해 (1, 1)
A2 = A1[[1, 0]]                             # 행 순서를 바꿈
b2 = b1[[1, 0]]
for name, A, b in [("원래 순서  [[1,2],[3,1]]", A1, b1), ("행 교환     [[3,1],[1,2]]", A2, b2)]:
    rJ = spectral_radius(jacobi_matrix(A))
    print(f"{name}  대각우세={is_diagonally_dominant(A)}  Jacobi 스펙트럴 반지름={rJ:.4f}  → {'수렴' if rJ < 1 else '발산'}")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
for ax, (A, b, ttl) in zip(axes, [(A1, b1, "원래 순서: x+2y=3, 3x+y=4"), (A2, b2, "순서 교환: 3x+y=4, x+2y=3")]):
    _, hj = jacobi(A, b, tol=1e-12, max_iter=25)
    _, hg = gauss_seidel(A, b, tol=1e-12, max_iter=25)
    ax.semilogy(hj, "o-", label="Jacobi")
    ax.semilogy(hg, "s-", label="Gauss-Seidel")
    ax.set_xlabel("반복 횟수 k")
    ax.set_ylabel("상대잔차")
    ax.set_title(ttl)
    ax.legend()
save(fig, HERE, "03_row_order.png")
print("그래프를 확인해 보세요 → figures/ 폴더")
