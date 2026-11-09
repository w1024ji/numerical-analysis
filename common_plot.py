"""그래프 공통 설정 (한글 폰트, 저장 경로)."""
import os

import matplotlib

matplotlib.use("Agg")  # 창을 띄우지 않고 파일로만 저장
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import LogFormatter

# 한글 폰트: 설치된 것 중 첫 번째를 사용 (Windows: 맑은 고딕, Mac: AppleGothic, Linux: Nanum)
for name in ("Malgun Gothic", "AppleGothic", "NanumGothic", "Noto Sans CJK KR"):
    if any(f.name == name for f in font_manager.fontManager.ttflist):
        # 한글 폰트에 없는 기호(−, 약간의 수학 기호)는 DejaVu Sans 가 대신 그려 준다
        plt.rcParams["font.family"] = [name, "DejaVu Sans"]
        break
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["mathtext.fontset"] = "dejavusans"  # 수식($...$)은 DejaVu 로 (한글 폰트에 없는 기호 방지)
plt.rcParams["figure.dpi"] = 110
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3


def save(fig, here, name):
    """here: 호출한 스크립트의 __file__. 같은 폴더의 figures/ 에 저장한다."""
    # 로그 눈금 라벨은 기본이 mathtext(10^{−5})라 한글 폰트에서 마이너스 글리프가 깨진다 → 평문으로
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            if axis.get_scale() == "log":
                axis.set_major_formatter(LogFormatter(labelOnlyBase=True))
    folder = os.path.join(os.path.dirname(os.path.abspath(here)), "figures")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print("저장:", path)
