"""3단원: 연립일차방정식 A x = b 를 푸는 알고리즘 모음 (직접 구현)

[직접법]  가우스 소거, LU 분해          → 유한 번의 연산으로 (반올림 오차를 빼면) 정확한 답
[반복법]  Jacobi, Gauss-Seidel, SOR     → 추측값을 계속 개선해서 답에 접근
"""
import numpy as np


# ----------------------------------------------------------------- 대입 (삼각행렬 풀기)
def forward_substitution(L, b):
    """L y = b 를 푼다. L 은 하삼각행렬. 위에서 아래로 한 줄씩."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y


def back_substitution(U, y):
    """U x = y 를 푼다. U 는 상삼각행렬. 아래에서 위로 한 줄씩."""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


# ----------------------------------------------------------------- 가우스 소거
def gauss_solve(A, b, pivot=True, verbose=False):
    """가우스 소거법 (전진 소거 + 후진 대입).

    pivot=True  : 부분 피벗팅(각 열에서 절댓값이 가장 큰 행을 위로 올림)
    pivot=False : 피벗팅 없음 (일부러 위험한 버전을 실험해 보려고 둔 옵션)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    for k in range(n - 1):
        if pivot:
            p = k + int(np.argmax(np.abs(A[k:, k])))
            if p != k:
                A[[k, p]] = A[[p, k]]
                b[[k, p]] = b[[p, k]]
                if verbose:
                    print(f"  [행 교환] {k + 1}행 <-> {p + 1}행")
        if A[k, k] == 0:
            raise ZeroDivisionError("피벗이 0 입니다. (특이행렬이거나 피벗팅이 필요해요)")
        m = A[k + 1:, k] / A[k, k]              # 승수(multiplier) 들
        A[k + 1:, k:] -= np.outer(m, A[k, k:])  # 아래 행들에서 (승수 × k행) 을 뺀다
        b[k + 1:] -= m * b[k]
        if verbose:
            print(f"  [단계 {k + 1}] 승수 = {np.round(m, 4)}")
            print(np.round(np.column_stack([A, b]), 4))
    return back_substitution(A, b)


# ----------------------------------------------------------------- LU 분해
def lu_decompose(A, pivot=True):
    """부분 피벗팅이 있는 LU 분해:  A[perm] = L @ U.

    L : 대각이 1 인 하삼각행렬 (소거에 쓴 승수들이 들어 있다)
    U : 상삼각행렬 (소거가 끝난 결과)
    perm : 행을 어떻게 섞었는지 (P A = L U 의 P 에 해당)
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    perm = np.arange(n)
    for k in range(n - 1):
        if pivot:
            p = k + int(np.argmax(np.abs(A[k:, k])))
            if p != k:
                A[[k, p]] = A[[p, k]]
                perm[[k, p]] = perm[[p, k]]
        if A[k, k] == 0:
            raise ZeroDivisionError("피벗이 0 입니다.")
        A[k + 1:, k] /= A[k, k]                                   # 승수를 아래 빈칸에 저장
        A[k + 1:, k + 1:] -= np.outer(A[k + 1:, k], A[k, k + 1:])
    L = np.tril(A, -1) + np.eye(n)
    U = np.triu(A)
    return perm, L, U


def lu_solve(perm, L, U, b):
    """LU 분해를 이용해 A x = b 풀기: L y = P b,  U x = y."""
    y = forward_substitution(L, np.asarray(b, dtype=float)[perm])
    return back_substitution(U, y)


# ----------------------------------------------------------------- 반복법
def _rel_residual(A, x, b):
    return np.linalg.norm(b - A @ x) / np.linalg.norm(b)


def jacobi(A, b, x0=None, tol=1e-10, max_iter=10000):
    """Jacobi 반복: 새 값을 구할 때 '이전 단계의 값'만 쓴다. (한꺼번에 갱신)

    반환: (근사해, 상대잔차 기록)
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    x = np.zeros_like(b) if x0 is None else np.array(x0, dtype=float)
    d = np.diag(A)
    hist = [_rel_residual(A, x, b)]
    for _ in range(max_iter):
        x = (b - A @ x + d * x) / d      # = (b - (A-D) x) / D
        hist.append(_rel_residual(A, x, b))
        if hist[-1] < tol or not np.isfinite(hist[-1]):
            break
    return x, hist


def sor(A, b, omega=1.0, x0=None, tol=1e-10, max_iter=10000):
    """SOR 반복. omega = 1 이면 Gauss-Seidel.

    Gauss-Seidel: 새 값을 구하자마자 그 자리에서 바로 갱신해서, 같은 단계의 다음 계산에 쓴다.
    SOR         : Gauss-Seidel 이 제안한 이동량에 omega 를 곱해 '더 크게(1<omega<2)' 움직인다.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    hist = [_rel_residual(A, x, b)]
    for _ in range(max_iter):
        for i in range(n):
            sigma = A[i, :i] @ x[:i] + A[i, i + 1:] @ x[i + 1:]   # x[:i] 는 이미 새 값!
            x_gs = (b[i] - sigma) / A[i, i]
            x[i] = (1 - omega) * x[i] + omega * x_gs
        hist.append(_rel_residual(A, x, b))
        if hist[-1] < tol or not np.isfinite(hist[-1]):
            break
    return x, hist


def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=10000):
    return sor(A, b, omega=1.0, x0=x0, tol=tol, max_iter=max_iter)


# ----------------------------------------------------------------- 수렴 분석 도구
def jacobi_matrix(A):
    """Jacobi 반복의 '반복 행렬' T_J = -D^{-1} (L + U).  x_new = T_J x + c"""
    A = np.asarray(A, dtype=float)
    D = np.diag(np.diag(A))
    return -np.linalg.solve(D, A - D)


def gauss_seidel_matrix(A):
    """Gauss-Seidel 의 반복 행렬 T_GS = -(D + L)^{-1} U"""
    A = np.asarray(A, dtype=float)
    return -np.linalg.solve(np.tril(A), np.triu(A, 1))


def spectral_radius(T):
    """스펙트럴 반지름 = 고유값 절댓값의 최댓값. 이게 1보다 작아야 반복이 수렴한다."""
    return float(np.max(np.abs(np.linalg.eigvals(T))))


def is_diagonally_dominant(A):
    """각 행에서 대각 성분의 크기가 나머지 성분 크기의 합보다 큰가? (엄격한 행 대각 우세)"""
    A = np.abs(np.asarray(A, dtype=float))
    off = A.sum(axis=1) - np.diag(A)
    return bool(np.all(np.diag(A) > off))
