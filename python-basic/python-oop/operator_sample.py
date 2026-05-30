# path : ./operator_sample.py
# 연산자(operator) : 값 계산에 사용되는 기호

'''
[종류(우선순위)로 구분]
최우선 연산자(1) : (), .(직접접근연산자), [](배열기호, 인덱싱)
단항 연산자(2) : +(양수 부호, +1 * 값), -(음수 부호, -1 * 값), ++(1증가), --(1감소), !(논리부정, not), ~(tield, 비트반전)
이항 연산자 (값 연산자 값)
    - 산술 연산자 (3) :  *, /(몫이 실수형), //(몫이 정수형), %(mod, 나누기한 나머지), ** (제곱구하기)
    - 산술 연산자 (4) : +(더하기), -(빼기)
    - 쉬프트 연산자 (5) : <<, >> (비트값 자리 이동 연산자)
    - 관계(비교) 연산자 (6) : >(크냐, 초과), <(작으냐, 미만), >=(크거나 같으냐, 이상), <=(작거나 같으냐, 이하)
    - 관계(비교) 연산자 (7) : ==(같으냐), !=(같지 않느냐)
        값 비교연산자 비교값 => 결과값이 논리값임 (True, False)
    - 논리 연산자 : 논리값(True, False)를 계산함
        (8) : and(True and True => True, 한개라도 False 이면 결과는 False)
        (9) : xor(논리값이 다르면 True, 같으면 False)
        (10) : or(둘 중의 하나만 True이면 결과는 True)
삼항연산자 : 조건표현식 ? 참 : 거짓
대입연산자 : =, +=, -=, *=, /=, //=, %=, **=
나열연산자 : ,
'''

# bool 자료형 확인
def func_bool():
    flag = True
    print('flag : ', flag, type(flag))

    # 파이썬에서는 대소문자 구분함
    # flag = false # NameError: name 'false' is not defined. Did you mean: 'False'?
    
    # bool() 함수 : 값의 논리 상태를 확인할 때 사용함
    print('문자가 있는 문자열 : ', bool('abcd')) # True
    print('빈 문자열 : ', bool('')) # False

    # bool() : 값이 저장되어 있는지, 비어 있는지 확인하는 용도로도 사용함
    print('result : ', bool({'a':10, 'b':20})) # True
    print('result : ', bool({})) # False
    
    # 0을 제외한 모든 값은 True 임
    print('0을 제외한 모든값 : ', bool(12)) # True
    print('0 : ', bool(0)) # False
    
# 비교(관계) 연산자 확인
# 값 연산자 비교값 => 결과는 True | False 임
def op_compare():
    print(' 1 == 1 : ', 1 == 1) # True
    print(' 1 == 2 : ', 1 == 2) # False
    
    print(' 1 > 0 : ', 1 > 0) # True
    print(' 1 < 2 : ', 1 < 2) # True
    
    print(' 1 >= 1 : ', 1 >= 0) # True
    print(' 1 != 0 : ', 1 != 0) # True
    
# 논리 연산자 : 논리값(True, False)을 계산에 사용하는 연산자
# and, or, not
def op_logical():
    a = 1
    b = 2
    
    print(a > 0 and b > 1) # True and True => True
    print(a == 0 or b != 1) # False or True => True
    
    # and 연산자의 특징 :
    # 앞 and 뒤 : 앞이 False 이면 뒤를 실행 안 함
    # 앞이 True 이면 뒤를 실행함
    # 이 성질을 이용하는 짧은 조건문이 있음 (모든 스크립트에서 사용함)
    print('a' and 'b') # 'b' 출력
    print('' and 'b') # '' 출력
    
    # or 연산자의 특징 :
    # 앞 or 뒤 : 앞이 False 이면 뒤를 실행
    # 앞이 True 이면 뒤를 실행 안 함
    print('a' or 'b') # 'a' 출력


# 함수 실행 테스트
if __name__=='__main__':
    # func_bool()
    # op_compare()
    op_logical()
