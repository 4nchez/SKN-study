# path : numpy_example.py
# numpy 활용 예제

import numpy as np

# 행렬과 벡터의 곱하기
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
x = np.array([10, 20, 30])
print(np.dot(A, x))  # [140 320 500]

# 행렬을 열벡터 또는 행벡터로 바꾸어 계산하기
v1 = A[:, 0]
v2 = A[:, 1]
v3 = A[:, 2]

print(np.dot(x[0], v1) + np.dot(x[1], v2) + np.dot(x[2], v3))   # [140 320 500]

# 크기가 다른 행렬의 곱셈
# m x n 행렬과 n x p 행렬의 곱하기 결과는 m x p 임
# dot() 함수 사용 가능함
# 그냥 곱하기하면 에러임 (같은 크기의 행렬끼리만 연산할 수 있음)
A = np.array([[1, 2, 3], [4, 5, 6]])  # 2행3열
B = np.array([[1, 2], [3, 4], [5, 6]]) # 3행2열
print(np.dot(A, B))  # 2행2열
# print(A * B)  # error

# 스칼라와 벡터의 곱셈
V = np.array([[1], [2], [3]])  # 3행1열 (열벡터)
a = 10
print(a * V)
print(np.dot(a, V))

# 연립방정식의 해(x) 구하기
# Ax = b => x = A역행렬 * b
A = np.array([[4, 3], [3, 2]])
b = np.array([23, 16])
# A 의 역행렬 구함 (= 오른쪽으로 이항시키기 위함)
invA = np.linalg.inv(A)  # inv(행렬) => 역행렬 반환
x = np.dot(invA, b)
print(x)   # [2. 5.]
print(np.allclose(np.dot(A, x), b))  # True (해가 올바름)

# solve() 로 해를 구할 수도 있음 : 선형방정식의 개수와 미지수의 개수가 같을 경우
x = np.linalg.solve(A, b)
print(x)  # [2. 5.]

# lstsq() 로 해를 구할 수도 있음 : 선형방정식의 개수와 미지수의 개수가 다를 경우
A = np.array([[1, 4, 3], [1, 3, 2]])
b = np.array([23, 16])
x = np.linalg.lstsq(A, b, rcond=None)[0]
print(x)  # [-1.  3.  4.]

# 행렬식 |A| 구하기 : det(A) 함수 사용함
A = np.array([[1, 4], [1, 3]])
print(np.linalg.det(A))  # -1.0

# 3 x 3 정방행렬의 행렬식 구하기
A = np.array([[8, 5, 3], [4, 1, 6], [7, 10, 9]])
print(np.linalg.det(A))  # -278.99999999999994

# 예제 1 : 반 학생들의 성적으로 등수 매기기
score = np.array([80, 75, 100, 90, 60])
desc_idx = score.argsort()[::-1]  # 내림차순정렬한 인덱스 배열 생성
rank = np.empty_like(score)
rank[desc_idx] = np.arange(1, len(score) + 1) 
print(score)
print(rank)

# 두 행렬의 곱 : dot(A, B)
# 주의 : 작은 크기에 큰 크기를 곱하면 에러
A = np.array([[8, 5, 3], [4, 1, 6], [7, 10, 9]])  # 3행3열
B = np.array([[0, 3], [1, 4], [2, 5]]) #3행2열
print(np.dot(A, B))  # A.dot(B)  3행2열
print(np.dot(B, A))  # error