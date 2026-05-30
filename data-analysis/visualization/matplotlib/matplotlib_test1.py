# path: ./matplotlib/matplotlib_test1.py
# matplotlib 모듈 사용한 시각화 테스트 스크립트

# 패키지 추가 설치 : pip install matplotlib

import matplotlib as mpl
import matplotlib.pyplot as plt

def test_plot1():
    '간단한 plot 그리기 : 기본은 선그래프임 (line plot)'
    # 그래프를 표현할 데이터는 리스트 또는 배열이여야 함
    sample_data = [1, 4, 9, 16]

    plt.title('Line Plot')   # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(sample_data)   # 선 그래프 만드는 함수 (y축값만 지정함) => x축은 자동 0, 1, 2, 3, ... 으로 표시됨
    # 리스트가 하나이면, y축 값으로 사용됨
    plt.show()   # 만든 그래프 출력 함수 (랜더링)

def test_plot2():
    # title('표시할 그래프제목')
    # x축 값도 함께 지정 : plot([x축 값들], [y축 값들])
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title('x ticks')   
    plt.plot(x_data, y_data)     
    plt.show() 

# 그래프에 한글을 사용하려면, 한글 폰트 파일을 다운받아서 사용함 ----------------------------------------------
import matplotlib.font_manager as fm

def test_fonts():
    # 라이브러리 자원 (설치한 패키지) 저장 폴더 경로 확인하기
    print(mpl.matplotlib_fname())
    # .venv\lib\site-packages\matplotlib\mpl-data\matplotlibrc

    # matplotlib 에서 다운받은 글꼴을 그래프(plot)의 기본 글꼴로 사용하게 하려면
    # .venv\lib\site-packages\matplotlib\mpl-data\fonts\ttf
    # ttf 폴더 안에 다운받은 한글 글꼴 파일을 복사해 넣음

    # 글꼴 파일들 복사해 넣고 나서, matplotlib 캐시에 변경 내용을 반영함
    # 1. 캐시 파일 저장 위치 확인함
    print(mpl.get_cachedir()) # \Users\{user_name}\.matplotlib
    # 2. 해당 위치의 캐시 파일을 직접 파일 탐색기에서 찾아내서 .matplotlib 폴더 삭제함
    #    => 이전 폰트 리스트 정보를 가진 캐시임
    # 3. 프로그램 다시 실행(Run) => 파일탐색기에서 캐시 파일 다시 생긴 것 확인
    # => 만약, 캐시파일 안 생기면 컴퓨터 리부팅함

def test_fonts2():
    # 폰트 설정:
    # 첫번째 방법 : rc parameters 를 설정해서, 설정 이후에 그래프 작업 전체에 사용하게 함

    # 현재 사용되고 있는 폰트 종류와 글자 크기 확인
    print(mpl.rcParams['font.family'])
    print(mpl.rcParams['font.size'])

    # 한글 폰트로 설정 변경해 봄
    mpl.rc('font', family='NanumGothic')
    mpl.rc('axes', unicode_minus=False)
    # axes 에 적용되는 유니코드(0~65535) 숫자에 음수 부호 사용 해제를 지정함 (사용 못하게 함)

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title('한글 그래프 제목')
    plt.plot(x_data, y_data)
    plt.xlabel('x축 제목')
    plt.ylabel('y축 제목')
    plt.show()

def test_fonts3():
    # 그래프의 특정 부분만 원하는 글꼴로 설정 변경할 수도 있음
    # 이용할 글꼴 파일의 위치는 어디든 상관없음
    font_path = './fonts/NanumGothicBold.ttf'
    font_prop = fm.FontProperties(fname=font_path)

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title('예제 그래프', fontproperties=font_prop)
    plt.plot(x_data, y_data)
    plt.xlabel('x축 제목', fontproperties=font_prop)
    plt.ylabel('y축 제목', fontproperties=font_prop)
    plt.show()

def test_fonts4():
    # 각 객체마다 별도의 폰트 적용 : fontdict 인수에 넣어서 사용함
    font1 = {'family': 'NanumGothic', 'size': 24, 'color': 'blue', 'weight': 'bold'}
    font2 = {'family': 'NanumGothic', 'size': 16, 'color': 'red', 'weight': 'bold'}
    font3 = {'family': 'NanumGothic', 'size': 12, 'color': 'green', 'weight': 'light'}

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title('예제 그래프', fontdict=font1)
    plt.plot(x_data, y_data)
    plt.xlabel('x축 제목', fontdict=font2)
    plt.ylabel('y축 제목', fontdict=font3)
    plt.show()


if __name__ == '__main__':
    # test_plot1()
    # test_plot2()
    # test_fonts()
    # test_fonts2()
    # test_fonts3()
    test_fonts4()