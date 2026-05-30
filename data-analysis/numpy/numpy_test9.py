# path : numpy_test9.py

import numpy as np

# 배열 간의 연산 : 벡터화 연산
# 벡터화 연산을 사용하면, 반복문을 쓰지 않고 배열 각 요소에 대한 연산이 가능함
# 또 다른 장점은 선형대수 공식과 동일한 연산을 간단하게 작성할 수 있음

x = np.arange(1, 10001)  #  1만개(1 ~ 10000) 수열로 초기화
y = np.arange(10001, 20001)  # 1만개 (10001 ~ 20000) 수열로 초기화
z = np.zeros_like(x)  # 1만개, 0으로 초기화

# 벡터화 연산을 사용하지 않으면, 반복문으로 각 요소에 대한 연산을 처리해야 할것임
# z[0] = x[0] + y[0], z[1] = x[1] + y[1], ........ # 1만번 반복
for idx in range(10000):   # 0 ~ 9999 까지의 값을 1만개 수열로 생성함
    z[idx] = x[idx] + y[idx]

# 결과 출력 : 슬라이싱으로 0 ~ 9번 인덱스까지 10개만 확인
print(z[:10]) # [10002 10004 10006 10008 10010 10012 10014 10016 10018 10020]

# 벡터화 연산 사용
z = x + y
print(z[:10])

# 산술연산, 비교연산, 논리연산 모두 벡터화 연산 가능함
ar = np.array([1,2,3,4])
br = np.array([4,2,2,4])

print(ar == br)  # ar[0] == br[0], ar[1] == br[1], .... =>  [False, True, False, True]
print(ar >= br)  # ar[0] >= br[0], ar[1] >= br[1], .... =>  [False, True, True, True]

# 만약, 배열 각 인덱스 값끼리 하나씩 비교한 결과가 아니라,
# 배열의 모든 요소가 다 같은지 (전부 다 True 인지) 알고 싶다면 all() 을 사용하면 됨
cr = np.array([1, 2, 3, 4])
print(np.all(ar == br))  # 모두 다 True 냐? => False
print(np.all(ar == cr))  # True

# 지수함수 (exp), 로그함수 (log) 등 수학 함수들도 벡터화 연산을 지원함
dr = np.arange(5)
print(dr)
print(np.exp(dr))  # exp 함수 : 지수 e의 x 제곱을 구하는 함수

print(10 ** dr)
print(np.log(dr + 1))

# 스칼라(값 1개, 상수)와 벡터(1차원배열) / 행렬(2차원배열)의 곱셈
x = np.arange(10)
print(x)
print(x * 100)

y = np.arange(12).reshape((3, 4))
print(y)
print(y * 100)

# 브로드캐스팅 (broadcasting)
# 행렬(매트릭스, 2차원배열)에 벡터끼리 (행별 | 열별) 덧셈 또는 뺄셈을 하려면 행과 열의 갯수가 같아야 함 (원칙)
# numpy 에서 행과 열의 갯수가 다른 매트릭스끼리 벡터화 연산이 가능하도록 지원함
# 매트릭스 크기가 작은 벡터가 자동으로 크기가 큰 벡터의 행과 열갯수와 맞춰짐 (확장) => 이 기능을 브로드캐스팅이라고 함
# 벡터(1차원 배열), 매트릭스(2차원 배열) 모두 적용됨

# 확인 1
x = np.arange(5)
print(x)
y = np.ones_like(x)
print(y)

print(x + y)
print(x + 1)

# 다차원 배열 확인
dx = np.vstack([range(7)[i:i + 3] for i in range(5)]) # 리스트 내포 (리스트 초기값을 내부 for문 이용해서 생성)
# range(7) => [0, 1, 2, 3, 4, 5, 6]
# [i:i+3] : 슬라이싱, 연속된 숫자 3개씩 잘라내기 하라는 의미임 (0:3, 1:4, 2:5, 3:6, 4:7)
# [0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6] => 5개
# for i in range(5) : i 변수에 0, 1, 2, 3, 4 대입하면서 5번 반복 실행

print(dx) # 5행3열
print(dx.shape)

dy = np.arange(5)[:, np.newaxis] # 5행 1열로 만듦, 차원 1증가처리
print(dy)
print(dy.shape)

# 행갯수는 같으나, 열갯수가 다른 경우, 벡터화 연산 가능함
print(dx + dy) # 브로드캐스팅 적용됨
'''
[[ 0  1  2]
 [ 2  3  4]
 [ 4  5  6]
 [ 6  7  8]
 [ 8  9 10]]
'''

# 차원 축소 연산
# 배열의 가로(행, 줄) 또는 세로(열, 칸) 전체를 하나의 값으로 보고 연산해서
# 하나의 결과를 만드는 것을 축소 연산(demension reduction) 이라고 함
# 1차원 배열은 축소연산 결과값은 1개
# 2차원 배열은 축소연산 결과가 1차원 배열임
# 통계함수가 해당됨 : 
# max(최대값), min(최소값), argmax(최대값의 index), agrmin(최소값의 index), sum(합계), mean(평균),
# median(중간값, 중앙값), std(표준편차), var(분산)
# all(모든 결과가 True 인지 확인), any(결과값 중에 한 개라도 True가 있는지 확인)

x = np.array([1,2,3,4])
print(x)
print(np.sum(x))  # 10
print(x.sum())  # 10

print(x.min())   # 1
print(x.argmin())  # 인덱스 0
print(x.max())   # 4
print(x.argmax())  # 인덱스 3

print(x.mean())
print(np.median(x))  # 중간값 (최댓값과 최솟값의 중간값)

# 정렬 sort()
# 1차원 배열은 값들의 오름차순 | 내림차순 정렬이 됨
# 2차원 배열은 행별(가로값 들)로 정렬 | 열별(세로값 들)로 정렬을 함 (axis 매개변수 사용함)
# axis=0 : 열별로 정렬
# axis=1 | -1 : 기본값, 행별로 정렬

dr = np.array([[4, 3, 5, 7], [1, 12, 11, 9], [2, 15, 1, 14]])
print(dr)
print(dr.shape)  # (3, 4)

print(np.sort(dr)) # 기본은 행별 정렬
print(np.sort(dr, axis=0))

# 값들에 정렬하면 해당 배열의 구조(값의 인덱스)를 바꿈 => 사용시 주의 필요함
dr.sort(axis=1)
print(dr)

# 해결방법 : 값의 위치는 변경하지 않고 정렬하는 방법
# argsort() 함수
# 데이터를 정렬한 다음, 정렬된 인덱스를 반환함
er = np.array([42, 38, 12, 25])
print(er)
fr = np.argsort(er) # 정렬된 index 를 인덱서로 이용함
print(er[fr])
print(er)