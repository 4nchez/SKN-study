# path : numpy_test1.py
# numpy 모듈 : 배열(행렬)을 다루기 위한 모듈임

'''
배열의 특징 (리스트와 다른 점)
1. 처음부터 저장할 갯수 지정함 (리스트는 저장 갯수에 제한없음)
2. 한 가지 종류의 값만 저장함 (리스트는 여러 종류를 저장함)
3. 리스트와 동일하게 저장 순번(index)을 사용함
'''
import numpy as np

# 1차원 배열 다루기 : numpy.array([한가지 종류로만 저장된 리스트]) => 리스트를 배열로 바꿈
# 배열변수 = np.array([list])
# 배열변수는 배열객체의 주소를 가짐 : 배열 레퍼런스임 (주소저장변수임)
# 주로 정수 | 실수 | 논리값으로 구성됨

ar = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(ar)
print(ar.dtype, type(ar))   # int64 <class 'numpy.ndarray'>
print(len(ar), ar.size, np.size(ar))

# 배열은 벡터화(각 인덱스별로) 연산이 가능하다.
# 리스트일 때의 벡터화 연산 처리 예 :
datalist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(type(datalist))   # <class 'list'>

# 리스트 안의 각 값을 모두 2배 증가처리 연산을 수행한다면
double_datalist = [x*2 for x in datalist]
print(double_datalist)

# 위의 처리를 배열로 바꿔서 벡터화 연산을 수행한다면
print(ar * 2)

# 배열의 벡터화 연산은 비교연산, 논리연산, 산술연산 모두 가능함
# Ndarray 클래스에 각 연산자에 대한 연산자오버로딩 메소드가 정의 제공되고 있기 때문임
ar1 = np.array([1, 2, 3])
br1 = np.array([10, 20, 30])

print(2 * ar1 + br1)  # 2 * ar1[0] + br1[0], 2 * ar1[1] + br1[1], 2 * ar1[2] + br1[2]
# [12 24 36]

print(ar1 == 2)   # ar1[0] == 2, ar1[1] == 2, ar1[2] == 2
# [False, True, False]

print((ar1 == 2) & (br1 > 10))  # [False, True, False] & [False, True, True]
# [0] & [0] => False
# [1] & [1] => True
# [2] & [2] => False
# [False, True, False]

# 1차원 배열의 각 인덱스 위치의 값(요소, element)에 접근 : 인덱싱(indexing)
for index in range(0, ar.size):   # range(0, 10) => 0 ~ 9 까지 정수 생성
    print(index, ' : ', ar[index])
    