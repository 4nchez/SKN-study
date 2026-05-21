# path : pandas_test2.py

import numpy as np
import pandas as pd

# Series 클래스
s = pd.Series([12356784, 5437689, 3440451, 2805246], index=['서울', '부산', '인천', '대구'])
print(s)

# Series.index 속성 : 인덱스 라벨 확인
print(s.index)  # Index(['서울', '부산', '인천', '대구'], dtype='str')

# Series.values 속성 : data 확인
print(s.values)  # [12356784  5437689  3440451  2805246]

# Series.name 속성 : 시리즈에 이름을 붙일 수 있음
# index.name 속성 : 시리즈의 인덱스에도 이름을 붙일 수 있음
s.name = '인구'
s.index.name = '도시'
print(s)

# 시리즈 연산
# numpy의 배열 벡터화연산을 Series 에도 사용할 수 있음
# 단, 시리즈의 값(values, data)에만 연산이 허용됨 (인덱스 라벨은 연산할 수 없음)

# 예 : 인구 숫자를 백만단위로 만들기 위해, 시리즈 객체에 1000000 나누기함
print(s / 1000000)

# 시리즈 인덱싱
# numpy의 배열처럼 인덱싱 가능함 : 시리즈변수[인덱스순번] 대신에 시리즈변수.iloc[순번]
# 인덱싱시에 인덱스 라벨을 사용함 : 시리즈변수['라벨'] 대신에 시리즈변수.loc['라벨'] 
# print(s[1])  # error
print(s.iloc[1])
print(s['부산'])
print(s.부산)
print(s.iloc[1], s.loc['부산'], s['부산'], s.부산)  # 4가지 방법

# 인덱서(배열 인덱싱)를 이용하면, 배열 순서를 바꾸거나 특정 데이터들을 선택할 수 있음
# 시리즈변수.iloc[[순서나열리스트]], 시리즈변수.loc[[라벨나열리스트]]
print(s.iloc[[0, 3, 1]])   # 시리즈로 반환됨
'''
도시
서울    12356784
대구     2805246
부산     5437689
Name: 인구, dtype: int64
'''
print(s.loc[['서울', '대구', '부산']])  # 시리즈로 리턴됨

# 조건부 인덱싱도 가능함
# data 에 조건값이 만족되는 인덱스만 추출함
print(s[(300e4 < s) & (s < 500e4)])  # 인구수가 300만 초과 ~ 500만 미만 사이의 값을 골라냄
'''
도시
인천    3440451
Name: 인구, dtype: int64
'''

# 슬라이싱
print(s[1:3])  # index 1 ~ index 3 - 1 까지
'''
도시
부산    5437689
인천    3440451
Name: 인구, dtype: int64
'''
print(s['부산':'대구'])   # 대구 포함됨
'''
도시
부산    5437689
인천    3440451
대구    2805246
Name: 인구, dtype: int64
'''

# 시리즈와 딕셔너리(사전) 자료형
# 시리즈의 인덱스 라벨이 딕셔너리의 카(key)에 해당됨
# 딕셔너리에서 in 과 items() 함수를 시리즈에도 사용할 수 있음 => 인덱스라벨(key), 값(value)
print('서울' in s)  # True : 인덱스라벨에 '서울'이 있느냐
print('대전' in s)  # False

print(s.items())  # <zip object at 0x000001C6674CD140>
# [(key, value), (key, value), ......]
# (key, value) == item

for k, v in s.items():
    print('%s = %d' % (k, v))
