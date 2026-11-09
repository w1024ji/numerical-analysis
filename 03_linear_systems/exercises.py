"""3단원 연습문제. TODO 를 채우고 실행해 보세요.

    python 03_linear_systems/exercises.py

linsys.py 의 함수들은 마음껏 가져다 써도 되지만, "직접 구현" 이라고 쓰인 문제는
numpy.linalg 을 쓰지 말고 처음부터 짜 보세요. 정답 확인용으로만 numpy 를 쓰는 건 좋아요.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linsys import (gauss_solve, lu_decompose, lu_solve, jacobi, gauss_seidel,  # noqa: E402,F401
                    jacobi_matrix, spectral_radius, is_diagonally_dominant)


# ---------------------------------------------------------------------------
# 문제 1. 손으로 가우스 소거 (종이 + 연필)
#   2x +  y -  z =   8
#  -3x -  y + 2z = -11
#  -2x +  y + 2z =  -3
#   종이로 푼 다음 아래에 답을 적고, gauss_solve 결과와 비교해 보세요. (lesson.md 3절 예제와 같은 문제예요)
#   그리고 승수(multiplier)를 모아서 L 을 직접 만들어 보고, lu_decompose 의 L 과 같은지 확인.
def problem1():
    A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    b = np.array([8, -11, -3], dtype=float)
    my_answer = None   # TODO: 종이로 푼 [x, y, z] 를 적어 보세요
    print("문제 1 | gauss_solve:", gauss_solve(A, b), " 내 답:", my_answer)


# ---------------------------------------------------------------------------
# 문제 2. 후진 대입 직접 구현  (numpy.linalg 금지)
#   상삼각 행렬 U 와 y 가 주어졌을 때 U x = y 를 푸는 함수를 처음부터 구현하세요.
#   (linsys.py 의 back_substitution 을 열어 보지 말고 먼저 시도!)
def my_back_substitution(U, y):
    # TODO: 맨 아래 행부터 위로 올라가며 x[i] 를 구한다.
    raise NotImplementedError


def problem2():
    U = np.array([[2.0, 1.0, -1.0], [0.0, 0.5, 0.5], [0.0, 0.0, -1.0]])
    y = np.array([8.0, 1.0, 1.0])
    # print("문제 2 |", my_back_substitution(U, y), " (정답: [2, 3, -1])")


# ---------------------------------------------------------------------------
# 문제 3. 피벗팅이 정말 필요할까?
#   A = [[1e-17, 1], [1, 1]],  b = [1, 2] 를
#   (a) gauss_solve(..., pivot=False)  (b) gauss_solve(..., pivot=True)  (c) 정답(약 [1, 1])
#   로 비교해 보세요. 어느 쪽이 틀렸고, 왜 틀렸는지 한두 문장으로 설명해 보세요.
#   힌트: 승수 m = 1 / 1e-17 = 1e17 이 만드는 값을 1단원의 "큰 수 + 작은 수" 관점에서 생각해 보세요.
def problem3():
    A = np.array([[1e-17, 1.0], [1.0, 1.0]])
    b = np.array([1.0, 2.0])
    # TODO: 두 가지로 풀어서 출력해 보세요.


# ---------------------------------------------------------------------------
# 문제 4. LU 분해로 행렬식과 여러 개의 우변 풀기
#   (a) lu_decompose 로 A = [[4,3,2],[3,5,1],[2,1,6]] 을 분해하고, det(A) 를 U 의 대각선 곱으로 계산하세요.
#       (행 교환이 있었다면 부호에 주의. perm 이 몇 번의 교환인지 세어야 해요)
#   (b) 같은 A 에 대해 b1=[1,0,0], b2=[0,1,0], b3=[0,0,1] 세 개를 lu_solve 로 풀고,
#       세 해를 열로 모으면 A 의 역행렬이 된다. numpy.linalg.inv(A) 와 같은지 확인.
def problem4():
    A = np.array([[4.0, 3.0, 2.0], [3.0, 5.0, 1.0], [2.0, 1.0, 6.0]])
    # TODO


# ---------------------------------------------------------------------------
# 문제 5. 대각 우세와 반복법
#   A = [[4, 1, 1], [1, 5, 2], [1, 2, 6]],  b = [6, 8, 9]  (정답은 [1, 1, 1])
#   (a) is_diagonally_dominant(A) 를 확인하고, Jacobi 의 스펙트럴 반지름을 구하세요.
#   (b) jacobi 와 gauss_seidel 로 tol=1e-10 까지 몇 번 걸리는지 비교하세요.
#   (c) 반지름이 1 에 가까우면 얼마나 느려질까?
#       A_d = [[d, 1, 1], [1, d+1, 2], [1, 2, d+2]] 로 d = 4, 3, 2.5, 2.2, 2.05 를 바꿔 가며
#       스펙트럴 반지름과 반복 횟수를 표로 만들어 보세요. (d 가 2 이하가 되면 대각 우세가 깨져요. 그때는?)
def problem5():
    A = np.array([[4.0, 1.0, 1.0], [1.0, 5.0, 2.0], [1.0, 2.0, 6.0]])
    b = np.array([6.0, 8.0, 9.0])
    # TODO


# ---------------------------------------------------------------------------
# 문제 6. (도전) Gauss-Seidel 을 직접 구현하고 Jacobi 와 비교  (numpy.linalg 금지)
#   두 방법의 코드 차이는 딱 한 곳이에요. "새로 구한 값을 언제부터 쓰는가" 를 직접 느껴 보세요.
def my_gauss_seidel(A, b, x0, n_iter):
    # TODO: 이중 for 문으로 구현해 보세요. x[i] = (b[i] - sum_{j != i} A[i,j] x[j]) / A[i,i]
    #       단, j < i 인 x[j] 는 이미 이번 반복에서 갱신된 새 값을 써야 합니다.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 문제 7. (도전) 조건수 감각
#   A = [[1, 1], [1, 1.0001]],  b = [2, 2.0001]  → 해는 [1, 1].
#   b 를 b + [0, 0.0001] 로 아주 조금 바꾸면 해가 얼마나 변할까요? (numpy.linalg.solve 사용 OK)
#   np.linalg.cond(A) 를 계산해서, "입력의 변화율 × 조건수 ≈ 출력의 변화율 상한" 이 맞는지 확인하세요.


if __name__ == "__main__":
    problem1()
    problem2()
    problem3()
    problem4()
    problem5()
