# path : ./test_matplotlib/matplotlib_test2.py
# 여러 종류의 그래프 확인 스크립트

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

def test_multiline_plot():
    '여러 개의 선을 그리는 선 그래프 테스트'
    x = [1, 2, 3, 4]
    y1 = [1, 4, 9, 16]
    y2 = [2, 5, 10, 17]

    plt.title('Multi Line Plot')
    plt.plot(x, y1, label='samsung')
    plt.plot(x, y2, label='sk')
    plt.legend()    # 그래프 범례 표시 (plot 의 label 이 표시됨)
    plt.show()

def test_scatter_plot():
    '산점도 (Scatter Plot) : 점 그래프 그리기'
    x = np.random.rand(50)
    y = np.random.rand(50)

    plt.title('Scatter Plot')
    plt.scatter(x, y)
    plt.show()

def test_bar_plot():
    '막대 그래프 그리기'
    names = ['A', 'B', 'C', 'D']
    values = [10, 25, 15, 30]

    plt.title('Bar Chart')
    plt.bar(names, values)
    plt.show()

def test_barh_plot():
    '가로 막대 (Horizental Bar) 그래프 그리기'
    names = ['Python', 'Java', 'C', 'JavaScript']
    scores = [90, 85, 70, 88]

    plt.title('Horizental Bar Chart')
    plt.barh(names, scores)
    plt.show()

def test_histogram():
    '히스토그램 그리기 : 분포 확인 그래프'
    data = np.random.randn(1000)

    plt.title('Histogram')
    plt.hist(data, bins=20)
    plt.show()

def test_pie_chart():
    '원 그래프 (pie chart) : 비율 시각화 용도'
    labels = ['Apple', 'Banana', 'Orange', 'Grape']
    sizes = [30, 25, 20, 25]

    plt.title('Pie Chart')
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.show()

def test_subplot_basic():
    '1행2열 형태의 subplot 이용해서 그래프 그리기'
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]

    plt.subplot(1, 2, 1)    # (줄수, 칸수, 순번)
    plt.title('Line')
    plt.plot(x, y)

    plt.subplot(1, 2, 2)
    plt.title('Bar')
    plt.bar(x, y)

    plt.show()

def test_subplots_object():
    'subplots 객체를 이용하는 방법'
    x = [1, 2, 3, 4]
    y1 = [1, 4, 9, 16]
    y2 = [2, 5, 10, 17]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    # fig : 그래프 그려지는 윈도우 (창) --> 1개
    # axes : 창 안에 그래프 그려지는 영역 --> 2개 (리스트)

    axes[0].plot(x, y1)
    axes[0].set_title('Line Plot')

    axes[1].bar(x, y2)
    axes[1].set_title('Bar Plot')

    plt.tight_layout()
    plt.show()


def test_subplot_2by2():
    '2 x 2 복합 시각화 (보고서용)'
    data = np.random.randn(100)

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    # axes : 2행2열이 리턴됨 --> 그래프 구역에 대한 인덱싱 : axes[0][0] == axes[0, 0] (왼쪽 위)

    axes[0, 0].plot([1, 2, 3], [1, 4, 9])
    axes[0, 0].set_title('Line')

    axes[0, 1].bar(['A', 'B', 'C'], [1, 4, 9])
    axes[0, 1].set_title('Bar')

    axes[1, 0].hist(data, bins=15)
    axes[1, 0].set_title('Histogram')

    axes[1, 1].scatter(np.random.rand(30), np.random.rand(30))
    axes[1, 1].set_title('Scatter')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # test_multiline_plot()
    # test_scatter_plot()
    # test_bar_plot()
    # test_barh_plot()
    # test_histogram()
    # test_pie_chart()
    # test_subplot_basic()
    # test_subplots_object()
    test_subplot_2by2()