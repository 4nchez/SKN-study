# path : ./exception/except_sample.py
# module : exception.except_sample
# 파이썬에서의 예외 처리 (Exception Handling) 테스트 스크립트

'''
예외 : 소스 코드로 해결할 수 있는 에러
에러의 종류 :
    - 시스템 에러 : 소스 코드로 해결 못 하는 에러
        메모리 부족, 하드디스크(저장 장치) 용량 부족, 베터리 전원 부족 등
    - 구문(문법) 에러 : 코드를 잘못 작성한 경우의 에러임
        개발툴에서 자동 검사됨, 구문을 수정해서 해결함
    - 런타임 에러 : 실행시 발생하는 에러
        사용자 입력 오류 등 에러 발생하면 코드 수정해서 해결함
        
에러 처리 방법 :
    if 조건문으로 에러 상황을 예측해서 미리 조치하는 것이 일반적임
    => 예외 상황 (예측된 에러 상황)을 처리하는 별도의 구문이 있음 : 예외 처리 구문 사용을 권장함
'''

def test_error():
    '에러 발생 예제 테스트 함수'
    # print('test error) # SyntaxError: unterminated string literal (detected at line 22)

    # a = 10
    # b = 0
    # c = a / b # ZeroDivisionError: division by zero
    
    # 4 + new * 3 # NameError: name 'new' is not defined
    
    lst = [1, 2]
    # print(lst[2]) # IndexError: list index out of range
    
    dct = {'a': 100, 'b': 200}
    # print(dct['c']) # KeyError: 'c'
# ------------------------------------------------

# 런타임 에러 중에 사용자가 입력값을 잘못 입력하는 경우
def test_input_error():
    '입력 오류 관련 에러 테스트용 함수'
    # num = int(input('정수를 입력하세요 : ')) # 문자나 논리값을 입력했다면
    # ValueError: invalid literal for int() with base 10: 'a'
    # if 문으로 처리할 수 없는 에러 발생 상황인 경우 => 예외 처리 구문으로 해결함
    
    # 해결방법 1: 입력 따로 조건 처리로 형변환 따로 작성함
    num = input('정수를 입력하세요 : ')
    if num.isdecimal(): # 정수 10진수인가?
        num = int(num)
        print(num, type(num))
    else:
        print('정수 숫자만 입력해야 합니다. 다시 입력하세요.')
# ---------------------------------------------------------------

# 해결방법 2 : 예외 처리 방법 (예외 처리 구문으로 작성)
'''
try:
    런타임 에러 발생 가능성이 있는 구문들 또는 일반 구문들
except:
    에러가 발생했을 때 실행할 구문(들)
'''
def test_input_error2():
    try:
        num = int(input('정수를 입력하세요 : '))
        print(num, type(num))
    except:
        print('정수만 입력하세요. 다시 입력하세요.')
# ----------------------------------------------

# 예외 처리시 except: 에 pass를 사용하면
# 오류 발생시 프로그램을 멈추지 않고 계속 동작되게 할 수 있음
def except_pass():
    lst = ['3', '예외처리', 4, 2, 67.5, 'python']
    digit_num = []
    print(lst)
    
    # lst 에서 숫자만 골라내서 digit_num 에 기록 저장 처리함
    for idx in range(len(lst)): # len(lst) : 저장 갯수 리턴 => range(갯수) : 0 ~ 갯수 -1 까지의 숫자를 생성함
        try:
            digit_num.append(int(lst[idx]))
        except:
            pass
    # for ---------------------------------
    
    print(digit_num)
# ---------------------------------------------------

# finally : 예외 발생과 상관없이 반드시 실행할 구문을 작성하는 영역임
import math # 수학 계산 관련 함수들을 제공하는 모듈임

def test_finally():
    'finally 구문 사용 테스트 함수'
    try: # 예외 발생 가능성이 있는 구문 작성 영역
        radius = float(input('반지름 : '))
    except: # 에러가 발생했을 때 처리할 구문 작성 영역
        print('숫자만 입력해야 합니다.')
    else: # 에러가 발생하지 않았을 때 처리 구문 작성영역 (반드시 except 다음에 사용함)
        print('반지름 : ', radius)
        print('원 면적 : ', math.pi * math.pow(radius, 2))
    finally: # 반드시 실행해야 되는 구문 작성 영역
        print('예외 처리 구문 종료함')
# 여기 서부터 2026-05-07
    # try 구동 --> 에러 발생 --> except --> finally
    # try 구동 --> 정상 작동 --> else --> finally
  
# 파이썬에서의 예외 처리 구문 조합 형태
# try: ~ except: ~
# try: ~ except: ~ else : ~
# try: ~ finally: ~
# try: ~ except: ~ finally: ~
# try: ~ except: ~ else : ~ finally: ~
# 잘못 사용된 경우 : try: ~ else: ~

# def test_except():
#     'try: ~ else: ~ 로 잘못 사용된 경우 테스트 함수'
#     try:
#         print('try area....')
#     else: # SyntaxError: expected 'except' or 'finally' block
#         print('else area....')

# -----------------------------------------------------------
# try 쪽에서 여러 종류의 에러가 발생할 경우
# except 에서 에러 종류별로 예외 처리를 하고자 한다면 except: 여러 개 사용할 수 있음(갯수 제한 없음)
# except 에러종류이름: 또는 except 에러정류이름 as 변수명:
# 주의 사항 : 에러클래스의 상속 계층 구조에 따라 하위(후손) 클래스를 먼저 작성할 것 (다형성 때문임)

def multi_except():
    '다중 except 사용 테스트 함수'
    try:
        # print(3 / 0)
        lst = []
        # print(lst[0])
        # lst.append(int(input('숫자 입력 :')))
        # print(lst)
        print('2' + 4)
        
    except ZeroDivisionError:
        print('0으로 나눌 수 없습니다.')
    except IndexError:
        print('리스트 인덱스 잘못 사용됨')
    except TypeError:
        print('계산식 오류')
    except Exception as e:
        print('에러가 발생함 : ', e)

# 예외를 강제로 발생시키기 -------------------------------------
# raise 예외클래스명 또는 raise 예외클래스명('에러 메시지')
# 주로 함수나 클래스 메소드 작성시에 이용함
# 코드상 지정하는 조건일 때 에러 발생시키고, 해당 함수를 사용하는 위치에서 예외 처리함
def ndiv(a, b):
    if b == 0:
        raise Exception('0 나누기 못 함')
    return a / b

# ndiv() 함수를 사용하는 위치에서 예외 처리함
def test_ndiv():
    '예외 발생 구문이 있는 함수 사용 테스트'
    try:
        # 예외 발생 구문이 들어 있는 함수를 실행
        result = ndiv(2, 3)
        print(result)
        result = ndiv(12, 0)
        print(result)
    except Exception as e:
        print(e)
# 여기 까지 2026-05-07

# 실행 테스트
if __name__=='__main__':
    # test_error()
    # test_input_error()
    # test_input_error2()
    # except_pass()
    # test_finally()
    # test_except()
    # multi_except()
    test_ndiv()