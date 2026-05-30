# path : ./test_matplotlib/matplotlib_test3.py
# matplotlib.pyplot 의 그래프별 속성 / 인수 사용 테스트

import os
import math
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 공통 유틸 함수 : 한글 폰트 설정 (시스템에 설치 / 로컬 폰트파일  설정 모두 가능)
# 기본값 지정된 매개변수 있는 함수로 작성함
# 함수 사용시 : 
# 값이 전달오면 매개변수가 받아서 사용함
# 값 전달이 없으면 지정된 기본값 사용함
def setup_korean_font(prefer_family: str = 'NanumGothic',
                      local_font_path: str = './fonts/NanumGothic.ttf',
                      local_bold_path: str = './fonts/NanumGothicBold.ttf'):
    '''
    목적 :
    - 그래프 제목/ 축 라벨 등에 한글이 깨지지 않게 폰트 설정
    - 시스템에 'NanumGothic'이 설치되어 있지 않으면, ./fonts 폴더의 ttf 파일을 직접 지정해서 해결하도록 함
    - mpl.rc('font', family=.....) : matplotlib 기본 폰트 지정
    - mpl.rc('axes', unicode_minus=False) : 음수 기호(-)가 깨지는 문제 방지 처리함
    '''
    mpl.rc('axes', unicode_minus=False)

    # 1) 시스템 폰트로 설정 시도
    mpl.rc('font', family=prefer_family)

    # 2) 실제로 해당 글꼴(font family) 이 있는지 검사 (없으면 로컬 폰트로 강제 적용함)
    available = set(f.name for f in fm.fontManager.ttflist)
    if prefer_family not in available:  # mpl 폰트 목록에 전달받은 글꼴이 없다면        
        if os.path.exists(local_font_path):   # 로컬 폰트 파일이 존재하면, 그 글꼴로 지정 처리함
            font_prop = fm.FontProperties(fname=local_font_path)
            mpl.rcParams['font.family'] = font_prop.get_name()
        elif os.path.exists(local_bold_path):
            font_prop = fm.FontProperties(fname=local_bold_path)
            mpl.rcParams['font.family'] = font_prop.get_name()
        else:
            print('[WARN] 한글 폰트가 시스템 또는 로컬 위치에 모두 존재하지 않습니다.')
            # 전송온 폰트 또는 로컬 폰트가 없다면, 기본 폰트로 진행됨
# def ---------------------------------------------------------------------------------------------------------        

# 선 그래프 변형 : marker / linestyle / linewidth / alpha / grid
def test_line_detail():
    '''
    plt.plot() 을 다양한 인수로 변형하는 실습
    [핵심 인수]
    - x, y : x축, y축 데이터 (리스트 / 배열 / Series 가능)
    - marker : 각 데이터 포인트에 찍히는 점의 모양 지정 ('o', 's', '^', 'D', 'x', '*', ........)
    - linestyle : 선 스타일(종류) ('-', '--', ':', '-.')
    - linewidth : 선 두께(굵기) - 숫자
    - alpha : 투명도 (0.0 (투명) ~ 1.0(불투명))
    - label : 범례(legend)에 표시할 이름
    '''
    setup_korean_font()

    x = [1, 2, 3, 4, 5]
    y1 = [2, 3, 5, 7, 11]
    y2 = [1, 4, 6, 8, 9]

    plt.figure(figsize=(8, 4))  # figure (창) 크기 (가로, 세로 inch)

    plt.plot(x, y1, 
             marker='o',    # 점 모양 : 원
             linestyle='-', # 실선
             linewidth=2,   # 선굵기
             alpha=0.9,     # 투명도
             label='소수 수열') # 범례 라벨

    plt.plot(x, y2, 
             marker='s',    # 점 모양 : 사각형
             linestyle='--', # dash 선
             linewidth=2,   # 선굵기
             alpha=0.7,     # 투명도
             label='비교 수열') # 범례 라벨

    plt.title('선 그래프 : 마커/선스타일/투명도 적용 실습')
    plt.xlabel('x 값')
    plt.ylabel('y 값')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='best')  # 범례 위치 자동

    plt.show()

# 2) 선그래프 : 특정 점만 값 표시 (annotate / text)
def test_line_annotate_specific_points():
    '''
    특정 값만 선 위에 값 표시하는 실습 (예: 최대값, 임계치 초과 지점)
    [핵심 함수 / 인수]
    - plt.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords='offset points', arrowprops=....)
        * text: 표시할 문자열
        * xy: 실제 데이터 좌표
        * xytext : 텍스트 위치 (오프셋 : 간격)
        * textcoords: xy에서 몇 포인트 떨어진 곳에 글자 배치
        * arrowprops : 화살표 스타일 (dict)
    - plt.text(x, y, s) : 좌표에 텍스트만 찍기 (간단)
    '''
    setup_korean_font()

    x = list(range(1, 11))
    y = [v * v - 3 * v + 5 for v in x] # 임의 수식

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='D', linestyle='-', linewidth=2)

    plt.title('선 그래프 : 특정 값만 라벨링(annotate)')
    plt.xlabel('x')
    plt.ylabel('y')

    # 예 : 최대값 위치 찾기
    max_idx = max(range(len(y)), key=lambda i: y[i])    # 제일 큰 값의 인덱스 추출
    # range(len(y)) : 0 ~ 9 까지의 수열
    max_x, max_y = x[max_idx], y[max_idx]

    plt.annotate(
        text=f'최대값 : {max_y}',
        xy=(max_x, max_y),  # 화살표가 가리킬 데이터 좌표
        xytext=(10, 20),    # 텍스트를 데이터 점에서 (10, 20) 포인트로 이동 처리함
        textcoords='offset points', # xytext 단위를 포인트로 해석
        arrowprops=dict(arrowstyle='->', linewidth=1.5) # 화살표 모양, 굵기
    )

    # 예 : 임계치 (y >= 50) 인 지점만 텍스트로 표시
    for xi, yi in zip(x, y):
        if yi >= 50:
            plt.text(xi, yi, str(yi))   # (x, y) 에 문자열 표시
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

# 3) 막대 그래프 : 막대별 색 다르게 지정, edgecolor + hatch
def test_bar_colors_each_hatch():
    '''
    bar 그래프에서 막대별 색상 다르게 지정 실습
    [핵심 함수/인수]
    - plt.bar(x, height, color=...., edgecolor=...., linewidth=...., hatch=....)
        * x : 막대 위치 (카테고리 라벨 리스트도 가능)
        * height : 막대 높이 (숫자 리스트 | 배열 : 카테고리별 값에 해당)
        * color : 색상 (단일 문자열 | 리스트로 막대별 색 지정)
        * edgecolor : 막대 테두리색
        * linewidth : 테두리 두께
        * hatch : 무늬 패턴 ('/', '\\', 'x', '-', '+', 'o', 'O', '.', '*')
    '''
    setup_korean_font()

    categories = ['A', 'B', 'C', 'D', 'E']
    values = [5, 2, 7, 4, 6]

    colors = ['red', 'orange', 'green', 'blue', 'purple'] # 막대별 색상 리스트
    hatches = ['/', '\\', 'x', '-', 'o']

    plt.figure(figsize=(8, 4))
    bars = plt.bar(categories, values,
                   color=colors,   # 막대별 색상
                   edgecolor='black', # 바 테두리색
                   linewidth=1.2)    # 바 테두리 선 두께
    
    # 막대별 hatch 적용 : plt.bar() 에 hatch 인수에 리스트를 못 넣는 버전도 있음 (루프가 안전)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    
    plt.title('막대 그래프 : 막대별 색상/무늬/테두리 적용')
    plt.xlabel('카테고리')
    plt.ylabel('값')
    plt.grid(axis='y', linestyle=':', alpha=0.6)    # y축 방향 격자만
    plt.show()

# 4) 막대그래프 : 값 라벨(막대 위 숫자 표시), 정렬 / 축범위
def test_bar_value_labels_ylim():
    '''
    막대 위에 값을 표시 (레포트/대시 보드에서 아주 많이 사용)
    - plt.text(x, y, s, ha='center', va='bottom')
        * ha (horizental alignment) : 수평 정렬('left', 'center', 'right')
        * va (vertical alignment) : 수직 정렬('bottom', 'center', 'top')
    - plt.ylim(min, max) : y축 값 표시 범위 지정 (라벨이 잘리지 않게 하기 위함)
    '''
    setup_korean_font()

    x = ['1분기', '2분기', '3분기', '4분기']
    y = [120, 80, 150, 130]

    plt.figure(figsize=(8, 4))
    bars = plt.bar(x, y, color='skyblue', edgecolor='black')

    # 값 라벨 표시
    for bar in bars:
        h = bar.get_height()    # 막대 높이 조회
        cx = bar.get_x() + bar.get_width() / 2  # 막대 중앙(너비 가운데) x 좌표
        plt.text(cx, h, f'{h}', ha='center', va='bottom')
    
    plt.title('막대 그래프 : 값 라벨 + y축 범위 조정')
    plt.xlabel('분기')
    plt.ylabel('매출')

    # 라벨이 잘리지 않도록 여유를 줌
    plt.ylim(0, max(y) * 1.2)
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.show()


# 5) 파이 차트 : explode (한 조각 떼기) + autopct + startangle + shadow
def test_pie_explode_autopct():
    '''
    pie 그래프 변형 실습 (한 조각 떨어뜨리고 퍼센트 표시)
    [핵심 함수 / 인수]
    - plt.pie(x, labels=...., explode=...., autopct=...., startangle=..., shadow=...)
        * x : 각 조각의 값 (리스트)
        * labels : 조각의 라벨 리스트
        * explode : 조각을 중심에서 얼마나 떨어뜨릴지 지정 (조각별 거리 리스트)
            예) [0, 0.1, 0, 0] --> 두번째 조각만 튀어 나옴
        * autopct : 퍼센트 표시 포멧 문자열 ('%1.1f%%' 등)
        * startangle : 시작각도 (90 이면 12시 방향부터 시작)
        * shadow : 그림자 여부 (True | False)
    '''
    setup_korean_font()

    labels = ['국어', '영어', '수학', '과학']
    sizes = [30, 25, 35, 10]

    explode = [0, 0.12, 0, 0] # 영어만 한 조각 튀어나오게 설정

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('파이 차트 : explode + autopct + shadow')
    plt.show()

# 6) 파이 차트 : 도넛 스타일로 변형
def test_pie_donut_style():
    '''
    pie 를 도넛 형태로 변형하는 실습
    [핵심 인수]
    - wedgeprops=dict(width:.....) : width 를 주면 가운데가 뚫린 도넛 형태가 됨
            도넛 두께는 0 ~ 1 임
    '''
    setup_korean_font()

    labels = ['A', 'B', 'C', 'D']
    sizes = [40, 20, 25, 15]

    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops=dict(width=0.4))
    plt.title('파이 차트 : 도넛 스타일')
    plt.show()


# 7) 산점도 : 점 크기 / 투명도 / 모양 + 기준선
def test_scatter_size_alpha_mark():
    '''
    scatter 그래프 변형 실습 (점 크기 / 투명도 / 모양)
    [함수 / 인수]
    - plt.scatter(x, y, s=...., alpha=..., marker=....)
        * s : 점 크기 (숫자 | 리스트)
        * alpha : 투명도 (0.0 ~ 1.0)
        * marker : 점 모양
    '''
    setup_korean_font()

    x = [1, 2, 3, 4, 5, 6]
    y = [2, 1, 3, 5, 4, 6]
    sizes = [30, 60, 90, 120, 150, 180]  # 점 크기 변화

    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, s=sizes, alpha=0.7, marker='^') # 삼각형 마커

    # 기준선 (예: y=x)
    plt.plot([1, 6], [1,6], linestyle='--', linewidth=1.5)

    plt.title('산점도 : 점 크기(s) + 투명도(alpha) + 기준선')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()



if __name__ == '__main__':
    # 1) 선그래프
    # test_line_detail()
    # test_line_annotate_specific_points()

    # 2) 막대그래프
    # test_bar_colors_each_hatch()
    # test_bar_value_labels_ylim()

    # 3) 파이그래프
    # test_pie_explode_autopct()
    # test_pie_donut_style()

    # 4) 산점도
    test_scatter_size_alpha_mark()