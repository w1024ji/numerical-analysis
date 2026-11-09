"""2단원 연습문제. TODO 를 채우고 실행해 보세요.

    python 02_root_finding/exercises.py

막히면 rootfinding.py 의 구현을 참고하되, 먼저 종이에 식을 써 보는 걸 추천해요.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rootfinding import bisection, newton, secant  # noqa: E402


# ---------------------------------------------------------------------------
# 문제 1. 이분법이 몇 번 필요할까? (손으로 먼저, 코드로 확인)
#   f(x) = x^3 - x - 2 의 근이 구간 [1, 2] 안에 있다.
#   (a) 오차 1e-6 이하를 보장하려면 이론상 몇 번 반복해야 할까? (lesson.md 의 공식)
#   (b) 실제로 bisection 을 돌려서 반복 횟수를 세어 (a) 와 비교해 보자.
def problem1():
    f = lambda x: x**3 - x - 2
    # TODO (a): 이론상 필요한 횟수를 계산 (math.log2, math.ceil)
    theory = None
    # TODO (b): bisection(f, 1, 2, tol=1e-6) 을 호출해서 len(history) 를 구한다
    actual = None
    print("문제 1 | 이론:", theory, " 실제:", actual)


# ---------------------------------------------------------------------------
# 문제 2. 뉴턴법으로 제곱근 만들기 (바빌로니아 방법)
#   f(x) = x^2 - a 에 뉴턴법을 쓰면 x_{n+1} = (x_n + a / x_n) / 2 가 된다.
#   math.sqrt 를 쓰지 않고 my_sqrt(a) 를 구현하고, 몇 번 만에 수렴하는지 세어 보자.
def my_sqrt(a, tol=1e-15):
    # TODO: 위 점화식을 직접 구현. (반환: 근사값, 반복 횟수)
    raise NotImplementedError


def problem2():
    for a in (2, 10, 12345.678, 1e-6):
        # val, n = my_sqrt(a)
        # print(f"sqrt({a}) = {val}  (반복 {n}번, math.sqrt 와의 차이 {abs(val - math.sqrt(a)):.2e})")
        pass


# ---------------------------------------------------------------------------
# 문제 3. 같은 방정식, 다른 고정점 함수
#   x^2 - 2 = 0 을 x = g(x) 꼴로 바꾸는 방법은 여러 가지다.
#     g1(x) = x^2 + x - 2          (양변에 x 를 더함)
#     g2(x) = 2 / x
#     g3(x) = (x + 2/x) / 2
#   (a) 손으로 g'(sqrt2) 를 계산해서 어느 것이 수렴할지 예측해 보자.
#   (b) 코드로 x0 = 1.5 에서 10번씩 반복해 보고 예측이 맞았는지 확인하자.
#   (c) g3 가 어디서 본 식인지 알아보자. (힌트: 문제 2)
def problem3():
    gs = {
        "g1": lambda x: x**2 + x - 2,
        "g2": lambda x: 2 / x,
        "g3": lambda x: (x + 2 / x) / 2,
    }
    for name, g in gs.items():
        x = 1.5
        # TODO: x = g(x) 를 10번 반복하며 값들을 출력해 보세요.
        # 주의: g1 은 값이 폭발한다. OverflowError 가 나면 그 자체가 답이다.
        pass


# ---------------------------------------------------------------------------
# 문제 4. 수렴 차수를 직접 측정하기
#   f(x) = e^x - 3x^2 의 근 중 하나를 뉴턴법으로 구하고,
#   연속한 오차 e_n 으로부터 p ~ log(e_{n+1}/e_n) / log(e_n/e_{n-1}) 을 계산해 보자.
#   (참값은 같은 방법으로 충분히 많이 돌려서 얻은 마지막 값을 쓰면 된다.)
#   힌트: float64 에서는 오차가 1e-16 에서 멈추니, 몇 개 안 되는 점으로 추정하게 된다.
def problem4():
    f = lambda x: math.exp(x) - 3 * x**2
    df = lambda x: math.exp(x) - 6 * x
    # TODO: x0 = 0.0 근처에서 시작 (근은 약 -0.459).  history 에서 오차를 만들고 p 를 추정해 보세요.


# ---------------------------------------------------------------------------
# 문제 5. (도전) 뉴턴법이 실패하는 경우를 직접 만들어 보기
#   f(x) = cbrt(x) (세제곱근, 근은 0) 에 뉴턴법을 쓰면 x_{n+1} = -2 x_n 이 되어 발산한다.
#   (a) 손으로 x_{n+1} 을 유도해 보자.  (b) 코드로 확인하자.
#   (c) 이분법은 이 문제에서 어떻게 될까? bisection(lambda x: math.copysign(abs(x)**(1/3), x), -1, 2) 를 돌려 보자.
def problem5():
    pass


# ---------------------------------------------------------------------------
# 문제 6. (도전) 나만의 프랙탈
#   experiments.py 의 실험 7 을 복사해서 z^3 - 1 대신 z^4 - 1 (근 4개) 이나 z^5 - 1 로
#   바꿔 그려 보자. 힌트: 뉴턴 갱신식은 Z - (Z**n - 1) / (n * Z**(n-1)),  근은 exp(2j*pi*k/n).


if __name__ == "__main__":
    problem1()
    problem2()
    problem3()
    problem4()
    problem5()
