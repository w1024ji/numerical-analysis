"""2단원: 근 찾기 알고리즘 모음 (직접 구현)

모든 함수는 "반복 과정에서의 근사값 목록(history)"도 함께 돌려줍니다.
그래서 나중에 오차가 어떻게 줄어드는지 그래프로 그릴 수 있어요.
"""
import math


def bisection(f, a, b, tol=1e-12, max_iter=200):
    """이분법. f(a)와 f(b)의 부호가 달라야 한다.

    반환: (근사근, 각 반복에서의 중점 목록)
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a)와 f(b)의 부호가 같습니다. 구간에 근이 있다는 보장이 없어요.")
    history = []
    for _ in range(max_iter):
        c = (a + b) / 2
        history.append(c)
        fc = f(c)
        if fc == 0 or (b - a) / 2 < tol:
            return c, history
        if fa * fc < 0:      # 근이 왼쪽 절반에 있다
            b, fb = c, fc
        else:                # 근이 오른쪽 절반에 있다
            a, fa = c, fc
    return c, history


def fixed_point(g, x0, tol=1e-12, max_iter=200):
    """고정점 반복 x_{n+1} = g(x_n). 수렴하면 x = g(x) 의 해를 얻는다."""
    x = x0
    history = [x]
    for _ in range(max_iter):
        x_new = g(x)
        history.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, history
        x = x_new
    return x, history


def newton(f, df, x0, tol=1e-12, max_iter=100):
    """뉴턴법 x_{n+1} = x_n - f(x_n)/f'(x_n)."""
    x = x0
    history = [x]
    for _ in range(max_iter):
        d = df(x)
        if d == 0:
            raise ZeroDivisionError(f"x={x} 에서 도함수가 0입니다. 접선이 수평이라 다음 점을 못 구해요.")
        x_new = x - f(x) / d
        history.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, history
        x = x_new
    return x, history


def secant(f, x0, x1, tol=1e-12, max_iter=100):
    """할선법. 도함수 대신 두 점을 잇는 직선(할선)의 기울기를 쓴다."""
    history = [x0, x1]
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if f1 == f0:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        history.append(x2)
        if abs(x2 - x1) < tol:
            return x2, history
        x0, x1 = x1, x2
    return x1, history


def estimate_order(errors):
    """연속한 오차 e_{n-1}, e_n, e_{n+1} 로 수렴 차수 p 를 추정한다.

    e_{n+1} ~ C e_n^p  이면  p ~ log(e_{n+1}/e_n) / log(e_n/e_{n-1})
    """
    orders = []
    for i in range(1, len(errors) - 1):
        e0, e1, e2 = errors[i - 1], errors[i], errors[i + 1]
        if min(e0, e1, e2) <= 0 or e0 == e1:
            continue
        orders.append(math.log(e2 / e1) / math.log(e1 / e0))
    return orders
