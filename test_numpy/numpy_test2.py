# path : numpy_test2.py
# numpy 는 Ndarray 클래스를 사용함 : C언어로 만든 내부 로직을 제공함
# type 을 확인하면, 배열의 자료형은 numpy.Ndarray
# Ndarray : N-Dimensional Array 줄임말 (N차원 배열)
# 1차원배열부터 다차원 배열을 다룰 수 있음

import numpy as np

# 2차원 배열 만들기
# 1차원 배열 여러 개 (값의 갯수가 같아야 함)를 하나로 묶으면 => 2차원 배열
# 1차원 배열 == 벡터 (Vector)
# 2차원 배열 == 매트릭스 (Matrix) : 행과 열로 구성된 행렬(표) 형태
# [[list], [list], [list], .....] : list of list 형태일 것 (단, 리스트 안의 값 갯수가 같아야 함)

tar = np.array([[0, 1, 2], [3, 4, 5]]) # 2행 3열 2차원 배열
print(tar)
print(len(tar)) # 2 : 행 갯수
print(len(tar[0])) # 3 : 0행 안의 값(열) 갯수
print(tar.size, np.size(tar)) # 6 : 총 값 갯수

# 2차원 배열의 각 값(요소)에 접근 (인덱싱) : 배열변수[행순번][열순번]
# 행(row, 제 2축) : 세로방향 순번
# 열(column, 제 1축) : 가로방향 순번
# 2중 for 문 사용
for r_index in range(len(tar)): # range(2) => 0, 1 : 행반복
    for c_index in range(len(tar[r_index])): # range(3) : 0, 1, 2 : 각 행별 열반복
        print('tar[{}][{}]: {}'.format(r_index, c_index, tar[r_index][c_index]))

# 3차원 배열
# 값의 종류가 같고, 행과 열갯수가 같은 2차원 배열들의 묶음
# 면(깊이, depth), 행(줄, row, 높이, height), 열(칸, column)로 구성됨 = Tensor (텐서)라고 함
thar = np.array([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], # 0면
                 [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]]) # 1면
# 2면 3행 4열 Tensor

print(thar)
print(len(thar)) # 면 갯수 : 2
print(len(thar[0])) # 0면의 행 갯수 : 3
print(len(thar[1])) # 1면의 행 갯수 : 3
print(len(thar[0][0])) # 0면의 0행의 열 갯수 : 4

# 3차원 배열 안의 각 값(요소)을 다루려면 (인덱싱) : 배열변수[면순번][행순번][열순번]
# 3중 for 문 사용
for didx in range(len(thar)): # 면반복 : range(2) => 0, 1
    for ridx in range(len(thar[didx])): # 행반복 : range(3) => 0, 1, 2
        for cidx in range(len(thar[didx][ridx])): # 열반복 : range(4) => 0, 1, 2, 3
            print("thar[{}][{}][{}] : {}".format(didx, ridx, cidx, thar[didx][ridx][cidx]))
        print('-----------------------------------------------')

# 배열의 차원(ndim)과 크기(shape) 알아내기
# 배열변수.ndim, 배열변수.shape
print(tar.ndim) # 2
print(tar.shape) # 튜플로 리턴 : (2, 3) 2행 3열을 의미함
print(thar.ndim) # 3
print(thar.shape) # (2, 3, 4) : 2면 3행 4열을 의미함

# 1차원 배열의 ndim, shape 확인
ar = np.array([1, 2, 3])
print(ar.ndim) # 1
print(ar.shape) # (3, )

# 2차원 배열의 인덱싱 : 배열변수[행순번][열순번] == 배열변수[행순번, 열순번]
# 콤마(,)를 이용할 수도 있음 => 축(axis) 이라고 함
# 행(x축), 열(y축)이 됨
print('0행0열의 값 : ', tar[0][0], tar[0, 0])
print('1행0열의 값 : ', tar[1][0], tar[1, 0])
print('마지막행 마지막열의 값 : ', tar[-1][-1], tar[-1, -1])

arr = np.ones((2, 3))
print(arr.ndim)
print(arr.shape)
print(arr)

arr = np.zeros((2, 3))
print(arr.ndim)
print(arr.shape)
print(arr)

arr = np.full((2, 3), 10)
print(arr.ndim)
print(arr.shape)
print(arr)

arr = np.empty((2, 3)) # 이전에는 쓰레기값이 채워짐. 최신 버전에서 0 채워짐
print(arr.ndim)
print(arr.shape)
print(arr)
