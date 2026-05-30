# path : ./class_sample.py
# 파이썬에서 클래스 만들어 사용하기

# 파이썬은 객체 지향 스크립트 언어이다. : 클래스 만들어서 작동시키는 프로그래밍
# 절차 지향 프로그래밍도 가능함 : 작성된 순서대로 작동시키는 프로그래밍
# 파이썬은 하이브리드 프로그래밍 언어이다.

# 파이썬에서 클래스 만들기
'''
class 클래스명:
    멤버변수 = 초기값
    
    def 멤버함수명(self, 매개변수, 매개변수=기본값, *가변매개변수):
        필드에 대한 값 처리에 대한 코드 작성
        self.멤버변수 = 변경할 값 | 계산식
        return self.필드명 또는 return 결과값
        
- 매개변수 self : 자바, C++, C# 의 this 와 같음
'''

# 클래스 이름은 첫글자로 영어대문자 권장함 (Nameing Rule, 자바스크립트와 같음)
class SClass:
    pass # 멤버가 없는 빈 클래스 작성할 수 있음
# 비어있는 클래스는 실행시 namespace 가 할당됨 => 이름만 있어도 메모리 공간이 할당됨

# 클래스 사용 : 객체 (인스턴스) 생성 (메모리에 클래스에 대한 객체 공간(instance) 할당)
ref1 = SClass()
ref2 = SClass()

print('ref1 이 가진 주소 : ', id(ref1))
print('ref2 이 가진 주소 : ', id(ref2))

# 파이썬은 실행할 때(동적으로) 멤버변수(필드)를 추가할 수 있음
ref1.score = 100 # ref1 이 참조하는 인스턴스 안에 score 를 추가하고, 100을 기록 저장함
print('ref1이 참조하는 객체 안의 score 필드값 : ', ref1.score)
# print('ref2이 참조하는 객체 안의 score 필드값 : ', ref2.score) # AttributeError: 'SClass' object has no attribute 'score'