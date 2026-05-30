# path : ./function/func_sample3.py

# 파이썬 함수 만들기에서 매개변수들 설정 테스트 스크립트

def tmax(a, b):
    '두 개의 값을 전달받아서, 둘 중 큰 값을 리턴하는 함수, call by value 방식 사용'
    print(f'a : {a}, b : {b}, type : {type(a)}, {type(b)}')
    result = 0
    if a > b:
        result = a
    else:
        result = b
    return result

def func_callby_value():
    'tmax() 함수 테스트용, 매개변수와 전달인자 갯수 일치 확인용 함수'
    result = tmax(10, 20) # call by value
    print('큰 값 : ', result)
    result = tmax(33.4, 12.5)
    print('큰 값 : ', result)
    
    print('큰 값 : ', tmax('M', 'm'))

    # 전달값과 매개변수 갯수가 다를 경우
    # result2 = tmax(120) # TypeError: tmax() missing 1 required positional argument: 'b'
    # result2 = tmax(10, 20, 30) # TypeError: tmax() takes 2 positional arguments but 3 were given
# --------------------------------------------------

# 파이썬에서는 군집자료형을 전달받는 매개변수는 주소를 받는다.
def list_in_max(plist):
    '리스트 객체를 전달받아서, 저장된 값들 중 가장 큰 값을 찾아내서 리턴하는 함수'
    print(f'plist : {plist}, 주소 : {id(plist)}')
    max_v = plist[0]
    for item in plist:
        if item > max_v:
            max_v = item
    
    return max_v
# --------------------------------

# 함수 호출시 함수 쪽으로 주소를 전달 : call by address (call by reference)
def func_callby_reference():
    '함수 쪽으로 주소 전달 테스트용 함수'
    nlist = [45, 1, 33, 12, 90, 123, 7]
    print(f'nlist : {nlist}, 주소 : {id(nlist)}')
    result = list_in_max(nlist)
    print(f'가장 큰 값 : {result}')
# -----------------------------------------------------


# 기본 매개변수 : 기본값을(default) 가진 매개변수
# def 함수명(매개변수 = 기본값, 매개변수 = 기본값):
# 주의 : 뒤쪽(오른쪽 끝) 매개변수부터 기본값 지정해야 함
#      즉, def 함수명(매개변수, 매개변수, 매개변수=기본값): # ok : 함수(값, 값)
#         def 함수명(매개변수=기본값, 매개변수, 매개변수): # error : 함수(, 값, 값)
#         def 함수명(매개변수, 매개변수=기본값, 매개변수): # error : 함수(값, , 값)

# 해당 함수 실행 시 기본 매개변수에 전달값은 생략할 수 있음
# 전달값이 없으면, 준비된 기본값을 사용함
# def tmin(a, b, c=0): => 실행시 : tmin(10, 20), tmin(10, 20, 30)
# def tmin(a, b = 0, c = 0): => 실행시 : tmin(10), tmin(10, 20), tmin(10, 20, 30)
def tmin(a = 0, b = 0, c = 0): # 실행시 : tmin(), tmin(10), tmin(10, 20), tmin(10, 20, 30)
    '3개의 값을 전달받아서, 가장 작은 값을 찾아내서 리턴하는 함수'
    print(f'a : {a}, b : {b}, c : {c}')
    min_v = 0
    if a < b and a < c: 
        min_v = a
    elif b < c:
        min_v = b
    else:
        min_v = c
    return min_v
# ---------------------------------

def func_default_param():
    '기본값 매개변수가 있는 함수 사용 테스트용'
    print(f'가장 작은 값 : {tmin(12, 3, 45)}')
    print(f'가장 작은 값 : {tmin(12, 3)}')
    print(f'가장 작은 값 : {tmin(12)}')
    print(f'가장 작은 값 : {tmin()}')
# ----------------------------------

# 재귀 호출 함수 (Recursive Call Function)
# 함수 안에서 자신을 실행하는 함수 (반복문과 유사함)
# 주의 : 무한 루프가 되지 않도록 종료 조건을 반드시 기술해야 함
# 파이썬은 무한 루프에 빠지면 자동으로 일정 구간 반복 후에 에러 발생시킴
def fectorial(n):
    if n == 0:
        return 1
    else:
        print(n, '*', end=' ')
        return n * fectorial(n-1)

if __name__=='__main__':
    # func_callby_value()
    # func_callby_reference()
    # func_default_param()
    print('\n10! : ', fectorial(10))