# path : numpy_test5.py
# numpy 데이터 샘플링

import matplotlib.pyplot as plt
import numpy as np

# linespace(start, end, 추출데이터갯수)
x = np.linspace(-5, 5, 50)
sin = np.sin(x)
plt.plot(x, sin, label='sine')
plt.legend()
# plt.show()

# 데이터 샘플링 (표본 추출) : choice() 함수 사용
# np.random.choice(a, size=None, replace=True, p=None)
# a : 배열변수 (배열값을 사용해도 됨), 정수숫자 (range(정수) 범위의 랜덤값을 만듦)
# size : 정수숫자, 추출할 데이터 갯수 지정
# replace : True | False, 같은 값 여러번 선택 가능(True) | 불가능(False)
# p : 배열변수나 배열 표기, 각 값의 선택 확률을 지정함 (단, 확률의 합계는 1이어야 함)

ch1 = np.random.choice(5, 5, replace=False)  # shuffle 과 같음
# 5 : range(5) 로 적용됨 => 0 ~ 4 사이의 랜덤 정수 5개 발생, 중복 안됨
print(ch1) # [4 1 3 0 2]
print(type(ch1)) # <class 'numpy.ndarray'>

ch2 = np.random.choice(5, 3, replace=False)  # shuffle 과 같음
# 5 : range(5) 로 적용됨 => 0 ~ 4 사이의 랜덤 정수 3개 발생, 중복 안됨
print(ch2)
print(type(ch2)) 

ch3 = np.random.choice(5, 10)
print(ch3)

ch3 = np.random.choice(5, 10, p=[0.1, 0, 0.3, 0.6, 0])
# 0~ 4 사이의 정수를 10개 추출 (중복 선택 가능)
# p=[0.1(숫자0의 선택확률), 0(숫자1의 선택확률), 0.3(숫자2의 선택확률), 0.6(숫자3의 선택확률), 0(숫자4의 선택확률)]
# 유사하게 선택됨
print(ch3)

# numpy 에서 난수 생성함수 3가지 제공됨 : rand, randn, randint
# rand(갯수) : 0.0 <= 난수 < 1.0 사이의 균일한 확률분포로 난수를 갯수만큼 발생함
r1 = np.random.rand(10)
print(r1)
print(type(r1))

r2 = np.random.rand(3, 5)  # 3행 5열의 2차원배열 생성하고, 15개의 난수를 발생함
print(r2)
print(type(r2))
print(r2.shape)
print(r2.ndim)

# randn(갯수)
# 기댓값이 0이고 표준편차가 1인 표준정규분포를 따르는 난수를 생성함
# 표준정규분포 : 숫자들이 가운데로 많이 모이고 양쪽으로 갈수록 점점 적어지는 모양을 말함 (종모양)
# 기대값 == 평균
# 숫자들이 0을 중심으로 모여있다는 의미임
# 표준편차는 값이 퍼져있는 정도를 의미함
# 표준편차(평균의 차이)가 1이면, 숫자들이 -1 <= 0 <= 1 범위의 값이 많이 모여있다는 의미임
r3 = np.random.randn(10)   # 1차원배열로 값 10개 생성
print(r3)
print(type(r3))
print(r3.shape)

r4 = np.random.randn(3, 5)   # 3행5열의 2차원배열로 값 15개 생성
print(r4)
print(type(r4))
print(r4.shape)

# randint(low, high=None, size=None)
# low <= 난수 < high 사이의 정수를 size 갯수만큼 발생시키면서 배열 생성함
# high 가 생략되면, 0 ~ low 까지의 범위에서 값 발생함
r5 = np.random.randint(10, size=10) # 0 <= 정수난수 < 10 사이의 정수 10개 발생
print(r5)

r6 = np.random.randint(10, 20, size=10) # 10 <= 정수난수 < 20 사이의 정수 10개 발생
print(r6)

r7 = np.random.randint(10, 20, size=(3, 5)) # 10 <= 정수난수 < 20 사이의 정수 15개 2차원배열 발생
print(r7)