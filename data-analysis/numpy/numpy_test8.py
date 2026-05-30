# path : numpy_test8.py

import numpy as np

# 배열 생성과 초기화 동시에 처리하는 함수 확인
# 초기값 : 변수 공간에 첫번째로 기록되는 값
# 변수 공간 만들면서 바로 초기값 기록하는 것을 초기화라고 함
# np.array([........]) => 리스트 값들로 초기화함

# zeros() : 배열 생성시 0으로 초기화함
# 사용 : 배열변수 = np.zeros(배열할당갯수) => 1차원배열 생성하고, 0으로 초기화함
# 사용 : 배열변수 = np.zeros((행갯수, 열갯수))  => 2차원배열 생성하고, 0으로 초기화함
# 사용 : 배열변수 = np.zeros((면갯수, 행갯수, 열갯수)) => 3차원배열 생성하고, 0으로 초기화함

ar = np.zeros(5)
print(ar)   # [0. 0. 0. 0. 0.]
print(ar.dtype)  # float64
print(ar.ndim)  
print(ar.shape)

br = np.zeros((2, 3))
print(br)
print(br.dtype)
print(br.ndim)
print(br.shape)

# array() 와 마찬가지로 dtype 매개변수 사용할 수 있음
cr = np.zeros((5, 2), dtype='i4')
print(cr)
print(cr.dtype)  # int32
print(cr.ndim)
print(cr.shape)

# zeros() 함수로 문자배열로 초기화할 수도 있음
# 문자열은 빈 문자열('')로 초기화됨
dr = np.zeros(5, dtype='U4')
print(dr)   # ['' '' '' '' '']
print(dr.dtype)  # <U4

# 각 인덱스 위치의 문자값 기록
dr[0] = 'abc'
dr[1] = '가나다라마'
dr[2] = 'abcdefghijklmn'
dr[3] = 'a b c d e' # 공백도 포함
print(dr) # ['abc' '가나다라' 'abcd' 'a b ' '']

# ones() 함수
# 배열 생성하면서, 1로 초기화함
er = np.ones((2, 3, 4), dtype='i8')  # 2면3행4열의  3차원배열 생성하고, 정수 1로 초기화함
print(er)
print(er.dtype) # int64

# zeros_like(), ones_like() 함수
# 다른 배열과 같은 크기(shape)의 배열을 생성하면서 초기화함
# 예 : 2행3열인 2차원배열인 br 과 같은 크기(shape)의 배열을 생성하려면
fr = np.ones_like(br, dtype='f')
print(fr)
print(fr.shape, br.shape, fr.shape == br.shape)

# empty() 함수
# 값이 없는 빈 배열 생성시 사용함 => 배열 생성이 빠름
gr = np.empty((4, 3))
print(gr)  # 이전에 메모리에 기록되어 있던 쓰레기값이 출력됨
# 각 인덱스에 값을 기록하면, 덮어쓰기되면서 지워짐

# arange() 함수
# 파이썬의 range() 함수와 같음
# 배열 생성시에 지정한 범위의 값들을 초기값으로 기록해 넣을 때 사용함
# 시작값, 종료값, 증가치 설정하면, 규칙에 따라 수열을 만듦
hr = np.arange(10) # 10개 : 0 ~ 9 까지의 정수를 수열로 초기화함
print(hr)

hr2 = np.arange(3, 21, 2) # 종료값 -1 까지 숫자 발생함
print(hr2)

# linespace(), logspace() 함수
# linespace(시작값, 끝값, 구간갯수) : 나누어진 구간을 초기값으로 해서 배열을 생성
# logspace(시작값, 끝값, 구간갯수) : 구간 갯수만큼의 로그구간값을 초기값으로 해서 배열 생성
ir = np.linspace(0, 100, 5) # 0부터 100까지를 5구간으로 나눈 값을 초기값으로 함
print(ir) # [  0.  25.  50.  75. 100.]

ir2 = np.logspace(0.1, 1, 10) # 10의 0.1제곱(약1.26)부터 10의 1제곱(10)까지를 10개로 나눈 값으로 초기화함
print(ir2)
# 로그 : 어떤 수를 만들기 위해 몇 번 곱했는지?
# 예 : 2를 몇번 곱해야 8이 되는가? => 답 : 3번
# 상용로그 : 밑이 10인 로그
# log10(100) => 답 : 2 (10을 2번 곱해야 100이 됨)
# 자연로그 : 밑이 e인 로그
# ln(x)
