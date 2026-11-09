# 수치해석 취미 로드맵

주 1시간 기준, 천천히. 한 단원이 2~3주여도 괜찮아요.
**원칙: 라이브러리를 쓰기 전에 직접 구현 → 그래프로 오차 확인 → 라이브러리와 비교.**

## 진행 상황

- [x] 1. 오차와 부동소수점 → [01_floating_point](01_floating_point/lesson.md)
- [ ] 2. 방정식의 근 찾기: 이분법, 고정점, 뉴턴, 할선 → [02_root_finding](02_root_finding/lesson.md) (자료 작성 완료, 읽고 연습문제 풀기)
- [ ] 3. 연립일차방정식: 가우스 소거, LU, Jacobi, Gauss-Seidel → [03_linear_systems](03_linear_systems/lesson.md) (자료 작성 완료, 읽고 연습문제 풀기)
- [ ] 4. 보간과 근사: 라그랑주, 스플라인, 최소제곱
- [ ] 5. 수치 미분과 적분
- [ ] 6. 상미분방정식: 오일러, 룽게-쿠타
- [ ] 7. 고유값 문제
- [ ] 8. 심화(선택): 편미분방정식, FFT, 최적화

1~3단원은 복습이라 개념은 빠르게 훑고, "왜 그렇게 되는지"와 "얼마나 빨리 수렴하는지"를 실험으로 확인하는 데 시간을 씁니다.

### 현재 상태 메모 (새 세션에서 이어갈 때 이걸 먼저 보여 주세요)

- 1단원: 이해 질문 몇 개 주고받음 (cos(1e-8) 에서 1-cos x 가 0이 되는 이유, 상쇄, 지수 표기법 `1e-8`).
  `exercises.py` 문제 1(이차방정식 안정화), 2(테일러 급수 e^x)는 아직 안 풂.
- 2, 3단원: lesson.md 와 코드, 그래프, 연습문제까지 만들어 둠. 아직 읽거나 풀지 않음.
- 다음 할 일: 2단원 lesson.md 읽기 → experiments 실행 → exercises 1~3번 → 3단원 같은 순서.

## 한 주 루틴 (약 1시간)

1. 15분: `lesson.md` 읽기 (모르는 건 바로 질문)
2. 30분: `experiments.py` 돌려 보고 값 바꿔 보기, `figures/` 의 그림 보기
3. 15분: `exercises.py` 의 TODO 채우기 → 코드 리뷰

## 폴더 구조

```
numeric/
  ROADMAP.md
  requirements.txt       필요한 파이썬 패키지 (numpy, matplotlib)
  common_plot.py         그래프 공통 설정 (한글 폰트 등)
  01_floating_point/     lesson.md, experiments.py, exercises.py
  02_root_finding/       lesson.md, rootfinding.py, experiments.py, exercises.py, figures/
  03_linear_systems/     lesson.md, linsys.py, experiments.py, exercises.py, figures/
  04_...                 (다음에 만들어요)
```

## 실행 방법

```
pip install -r requirements.txt
python 01_floating_point/experiments.py
python 02_root_finding/experiments.py      # figures/ 에 그래프 저장
python 03_linear_systems/experiments.py    # 약 30초 걸림
```

그래프의 한글은 Windows(맑은 고딕), macOS(AppleGothic), Linux(NanumGothic) 중 설치된 폰트를 자동으로 써요.
없으면 한글이 네모로 보일 수 있지만 계산에는 영향이 없어요.
