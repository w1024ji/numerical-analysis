"""1단원 연습문제. TODO 부분을 채워 보세요."""
import math


# 문제 1. 이차방정식 x^2 + b x + c = 0 의 근을 안정적으로 구하기
# b = 1e8, c = 1 처럼 b가 매우 클 때, 공식 (-b ± sqrt(b^2 - 4c)) / 2 는
# 한쪽 근에서 상쇄가 일어난다.
#   (a) 나이브 버전이 어느 근에서 왜 틀리는지 확인하기
#   (b) 근과 계수의 관계 x1 * x2 = c 를 이용해 안정한 버전 만들기
def roots_naive(b, c):
    d = math.sqrt(b * b - 4 * c)
    return (-b + d) / 2, (-b - d) / 2


def roots_stable(b, c):
    # TODO: 상쇄가 일어나지 않는 쪽 근을 먼저 구하고, 나머지는 c / x1 로 구하세요.
    raise NotImplementedError


# 문제 2. e^x 를 테일러 급수 sum x^n / n! 로 계산하기
# x = -20 일 때 항을 많이 더하면 math.exp(-20) 과 얼마나 다를까?
# 힌트: 양수 항과 음수 항이 크게 커졌다 작아지며 상쇄된다.
# x > 0 에서 계산하고 1/e^|x| 로 바꾸면 어떻게 될까?
def exp_taylor(x, n_terms=100):
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    b, c = 1e8, 1.0
    print("naive :", roots_naive(b, c))
    # print("stable:", roots_stable(b, c))
    # 정답 근사: x1 ~ -1e-8, x2 ~ -1e8

    # for x in (1, -1, -20):
    #     print(x, exp_taylor(x), math.exp(x))
