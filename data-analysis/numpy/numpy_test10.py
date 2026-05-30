# path : numpy_test10.py

import numpy as np

# 배열 연결
# 두 개이상의 배열들을 연결(concatenate) 해서 하나의 큰 배열을 만듦
# 사용함수 : hstack, vstack, dstack, r_, c_, tile

# hstack (horizental stack)
# 행의 갯수가 같은 2차원 배열들을 옆으로(가로, 수평) 합칠 때 사용
# 열의 갯수가 늘어남
ar1 = np.ones((2, 3))
print(ar1)
ar2 = np.zeros((2, 2))
print(ar2)

print(np.hstack([ar1, ar2]))

# vstack (vertical stack)
# 열의 갯수가 같은 2차원 배열들을 위아래로 (세로, 수직) 합칠 때 사용
# 행의 갯수가 늘어남
br1 = np.ones((2, 3))
print(br1)
br2 = np.zeros((3, 3))
print(br2)

print(np.vstack([br1, br2]))

# dstack (depth stack)
# 행과 열이 같은 2차원 배열 여러 개를 깊이(depth, z축, channel, 면) 방향으로 합침
# a행b열의 2차원 배열을 n개 합치면, 결과는 a면b행n열이 됨
cr1 = np.ones((3, 4))
print(cr1)
cr2 = np.zeros((3, 4))
print(cr2)

cr3 = np.dstack([cr1, cr2])
print(cr3)
print(cr3.shape) # (3, 4, 2)

# stack() 함수 : 기본적으로 (dstack) 과 유사함
# 다른 점은 n개를 합치면 n면이 됨
cr3 = np.stack([cr1, cr2])
print(cr3)
print(cr3.shape) # (2, 3, 4)

# r_ : hstack 과 유사하게 좌우로 배열을 합침
# 함수임에도 소괄호(parenthesis, ())를 사용하지 않고, 인덱싱처럼 대괄호(braket, [])를 사용함
# 특수 메서드라고 함 : 인덱서라고 함
# np.r_[배열생성구문 | 배열변수, 배열생성구문 | 배열변수, .......]
cr4 = np.r_[np.array([1, 2, 3]), np.array([4, 5, 6])]
print(cr4)   # [1 2 3 4 5 6]

# c_ : indexer 임
# 배열의 차원을 증가시킨 후, 좌우로 연결하는 인덱서임
# 1차원 배열을 연결하면 2차원 배열이 된다는 의미 : 배열의 값 갯수가 행, 합쳐지는 배열 갯수가 열이 됨
cr4 = np.c_[np.array([1, 2, 3]), np.array([4, 5, 6])]
print(cr4) 
print(cr4.shape)  # (3, 2)

# tile() 함수 : 배열을 지정한 횟수만큼 복사해서 연결함
# tile(배열변수, 열반복횟수), tile(배열변수, (행반복, 열반복))
dr = np.array([[1, 2, 3], [4, 5, 6]])  # 2행3열
dr1 = np.tile(dr, 2)   # 열 2번 반복
print(dr1)
print(dr1.shape)  # 2행6열

dr2 = np.tile(dr, (3, 2))   # 행은 3번, 열은 2번 반복
print(dr2)
print(dr2.shape)   # 6행6열

# 2차원 그리드 포인트 생성
# 변수가 2개인 2차원 함수의 그래프를 그리거나 표를 작성하려면,
# 2차원 영역에 대한 (x, y) 좌표값 쌍, 즉 그리드 포인트(grid point)가 필요함
# meshgrid() 함수로 x, y 좌표를 구성할 배열을 생성할 수 있음

# 예 : x 값이 0, 1, 2 이고, y값이 0, 1, 2, 3, 4 라면
# meshgrid() 로 사각형 영역을 구성할 가로축의 점들과 세로축의 점들을 조합해서
# 결과로 그리드 포인트 x 행렬과 y 행렬을 만들어 줌
x = np.arange(3)
print(x)
y = np.arange(5)
print(y)

metrix_X, metrix_Y = np.meshgrid(x, y)
print(metrix_X)
print(metrix_Y)

# (x, y) 조합
grid_xy = [ list(zip(x, y))   for x, y in zip(metrix_X, metrix_Y)]
print(grid_xy)