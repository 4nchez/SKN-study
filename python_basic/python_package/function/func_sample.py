# path : ./function/func_sample.py
# 파이썬에서 함수 만들어 사용하기 테스트 스크립트

'''
함수 (function) : 반복 사용되는 소스 코드를 분리 작성해서 이름 붙인 것
* 파이썬에서 함수 만들기
def 함수명(매개변수): <-- 매개변수(parameter) : 0 ~ n개
    함수가 실행할 코드 구문들
    ......
    return | return 값 | return 값, 값, 값 ... <-- 여러 개 반환시 받는 변수는 튜플(tuple)임
    
* 함수의 사용(call, 호출) : 함수가 만들어진 형태(signature)에 맞춰서 사용해야 함
 => 함수이름 틀리지 않아야 함 (대소문자 주의, _ 갯수 확인)
 => 매개변수 갯수 일차되게 전달인자(전달값, argument) 사용해야 함
 => 반환값 여부도 확인 : 반환값이 있는 함수는 다른 함수 안에 중첩 사용할 수 있음 => 함수명(반환값이 있는 함수())
'''

# 아무런 기능이 없는 (처리할 코드가 준비중인) 빈 함수를 만들 때는 pass 사용
def func():
    pass

# 함수 이름 아래에 함수 설명(description)을 적어둘 수 있음, 따옴표 사용함
def hello():
    '이 함수는 함수 작성 연습용이다.'
    print('Welcome!!!')
    print('함수명에 예약어, 공백 사용 못 함')
    return # 반환값 없는 리턴은 생략해도 됨

# 매개변수 있고, 반환값 있는 함수
def add(x, y):
    print(f'x : {x}, y : {y}')
    return x + y

# 파이썬에서는 여러 개의 값을 리턴할 수 있음, 자동 tuple 로 처리됨
def func2(a, b):
    print(f'a : {a}, b : {b}')
    return a * 2, b * 2

# 이 스크립트를 실행 파일로 만들려면
if __name__=='__main__':
    # hello() # 함수 실행 (함수 호출, function call)
    # 함수 설명(description)을 확인할 때 help(함수명) 사용
    # help(hello)
    # help(input)
    # help(print)
    
    # 매개변수 있고 반환값 있는 함수 사용 (call)
    # 반환값 받을 변수 = 함수명(매개변수에게 전달할 값, 전달인자) => 매개변수 갯수가 일치해야 함
    result = add(10, 20)
    print('result : ', result)
    print('result : ', add(11, 22))
    
    result2 = func2(100, 200)
    print(result2, type(result2)) # (200, 400) <class 'tuple'>
    
    n1, n2 = func2(3.3, 4.4)
    print(n1, n2, type(n1), type(n2)) # 6.6 8.8 <class 'float'> <class 'float'>