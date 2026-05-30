# str_practice.py
# 문자자료형(str) 실습문제
'''
 키보드로 입력받아 요구대로 처리하고 출력하시오.
 입력 내용 :
  회원이름 : 이순신 (member_name : str)
  회원아이디 : leess88@hi.org (member_id : str)
  패스워드 : pass1234 (member_passwd : str)
  나이 : 45 (age : int)
  키 : 187.5 (height : float)
출력 내용 : format() 메소드 사용함
 이순신 회원의 아이디는 leess88@hi.org 이고, 암호는 pass** 입니다.
 나이는 45세이고, 키는 187.5 cm 입니다.
 
출력시 처리조건 :
  암호는 첫글자부터 4글자만 슬라이싱한 다음 나머지 글자수에 맞춰서     * 로 출력되게 함
  키는 소숫점아래 첫자리까지만 출력되게 포멧팅함
'''
# member_name = input("회원이름 : ")
# member_id = input("회원아이디 : ")
# member_passwd = input("패스워드 : ")
# age = int(input("나이 : "))
# height = float(input("키 : "))

# print('{} 회원의 아이디는 {} 이고, 암호는 {}** 입니다.'.format(member_name, member_id, (member_passwd[:4] + (len(member_passwd)-4) * '*')))
# print('나이는 {}세이고, 키는 {:.1f} cm 입니다.'.format(age, height))

member_name = input('회원 이름 : ')
member_id = input('회원아이디 : ')
member_passwd = input('패스워드 : ')
age = int(input('나이 : '))
height = float(input('키 : '))

# 암호 앞 4글자 제외한 * 문자 갯수 계산
repeat_count = len(member_passwd) - 4
print_pwd = member_passwd[0:4] + ('*' * repeat_count)

# f-format string 사용
print(f'{member_name} 회원의 아이디는 {member_id} 이고, 암호는 {print_pwd} 입니다.')
# format() 함수 사용
print('나이는 {0}세이고, 키는 {1:.1f} cm 입니다.'.format(age, height))

# 또는 포멧 서식 사용
print_str = '나이는 %d세이고, 키는 %.1fcm 입니다.'%(age, height)
print(print_str)


# --------------------------------------
# 문자열에 포멧(format)을 적용해서 코드를 작성할 수도 있음
# 문자열 값 사이에 다른 종류의 값이나 변수를 적용하려고 할 때 이용함
# 정수 십진수(decimal) : %d
# 정수 8진수(octal) : %o
# 정수 16진수(hex) : %x
