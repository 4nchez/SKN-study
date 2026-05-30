# path : numpy_test7.py

import numpy as np

# 배열 생성시에 array() 함수 사용
# array() 함수 사용시에 dtype 매개변수를 이용해서, 배열에 저장되는 값의 종류를 명시할 수 있음
# dtype을 사용하지 않으면, 자동으로 기록되는 값의 자료형이 지정됨
x1 = np.array([1, 2, 3])
print(x1.dtype)   # int64 : 정수(integer) 64비트 => 64비트 정수
print(type(x1))   # <class 'numpy.ndarray'>

x2 = np.array([1.0, 2.0, 3.0])
print(x2.dtype)   # float64 : 실수(float) 64비트 => 64비트 실수
print(type(x2))   # <class 'numpy.ndarray'>

# 배열 생성시 dtype 인수에 자료형을 지정할 경우
# 제공되는 접두사 뒤에 바이트(또는 비트)수를 지정함. ex) int64, float64
# 문자타입(char type) 접두사 뒤에는 글자수를 지정할 수 있음
# b : boolean
# i : integer
# f : float
# u : unsigned int (부호없는 정수 : 0과 양수는 그대로 사용, 음수를 양수로 변환한 정수)
# ex) -128 ~ 0 ~ 127 => unsigned 하면 0 ~ 255가 됨 (-128이 양수 127 뒤로 옮겨져서 128이 됨)
# c : 복소수 (complex)
# O : Object
# S : String (바이트문자열), 1byte : 1글자
# U : Unicode string (유니코드 문자열), 2byte : 1글자
# 사용 예 : i8 (정수8바이트 == 64비트, int64), f8 (실수8바이트 == float64), U24 (유니코드문자열 24글자)

x3 = np.array([1, 2, 3], dtype='f')
print(x3.dtype)   # float32
print(x3)   # [1. 2. 3.]
print(x3[0] + x3[1])  # 1.0 + 2.0 => 3.0 : float + float => float

x4 = np.array([1, 2, 3], dtype='U')
print(x4.dtype)   # <U1 : 유니코드문자1글자
print(x4)  # ['1' '2' '3']
print(x4[0] + x4[1])  # '1' + '2' => 문자합치기 : '12'

# inf 와 nan
# numpy 에서 무한대를 표현하기 위해 np.inf (infinity 줄임말)
# 정의할 수 없는 숫자를 표현하기 위해 np.nan (not a number 줄임말)
# 예 : 1을 0으로 나누기하는 경우, 0에 대한 로그값 계산시 무한대인 np.inf 가 결과로 표시됨
# 예 : 0을 0으로 나누기하는 경우 np.nan 이 표시됨

print(np.array([0, 1, -1, 0]) / np.array([1, 0, 0, 0]))  # [  0.  inf -inf  nan]
# RuntimeWarning: divide by zero encountered in divide
# RuntimeWarning: invalid value encountered in divide

print(np.log(0))  # -inf
# RuntimeWarning: divide by zero encountered in log

print(np.exp(-np.inf))  # e 를 무한대로 작은수만큼 제곱하라는 뜻임 => 0에 가까워짐 : 0.0으로 표현됨
# np.inf : 무한대를 의미함
# -np.inf : 마이너스 무한대 (아주아주 작은 값을 뜻함)
# np.exp(x)  => 지수 e 의 x 제곱을 계산하는 함수임
