# path : ./class_oop3.py
# 파이썬에서의 OOP 의 상속, 다형성 테스트 스크립트

# 상속 (Inheritance)
# 부모 클래스의 기능을 물려받아, 새로운 클래스를 만드는 것
# 코드 중복 줄이고, 재사용성을 높이는 것이 목적임

# 다형성 (Polymorphism)
# 파이썬에서는 다형성은 같은 메서드 이름인데 객체 타입에 따라 다른 동작을 하는 것을 말함
# 자바로 비교하면 부모 메서드 오버라이딩해서 동적 바인딩되는 개념임
# 일반적인 객체 지향의 다형성(부모 타입으로 후손 객체 여러 개를 다루는 기술)과는 다름

# 부모 클래스 (Base Class) 준비
class Animal: # 클래스명은 첫글자 대문자로 (관례)
    def speak(self):
        print('동물이 우는 소리를 냅니다.')
# class Animal ------------------------------

# 자식(후손) 클래스 (Sub Class)
class Dog(Animal): # 파이썬에서 상속 표현 : class 후손클래스명(부모클래스명):
    def speak(self): # 부모 메서드를 오버라이딩(overriding)함 : 후손이 부모 메서드를 다시 작성하는 것 (파이썬에서는 별도 표식은 없음)
        # return super().speak() # 오버라이딩된 메서드 안에서 같은 이름의 부모 메서드를 실행함 (부모의 speak() 실행하라는 뜻임)
        print('강아지가 멍멍 짖습니다.')
# class Dog ---------------------------------

class Cat(Animal):
    def speak(self):
        # return super().speak()
        print('고양이가 야옹 웁니다.')
# class Cat ---------------------------------

# 다형성 테스트
animals = [
    Dog(),
    Cat(),
    Animal()
]

for a in animals:
    a.speak() # 같은 메서드인데, 참조 객체에 따라 다른 결과 출력 => 파이썬에서의 다형성임