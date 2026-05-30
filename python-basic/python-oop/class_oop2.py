# path : ./class_oop2.py
# oop 에서의 연산자 오버로딩 (operator overloading)

# 오버로딩 : 클래스 안에서 이름이 같은 메서드 중복 작성(정의)
# 파이썬에서는 생성자와 메서드는 오버로딩 안 됨 => 작성은 할 수 있으나, 마지막에 작성된 것으로 덮어쓰기됨
# C++, Python 에서는 값 계산에 사용되는 연산자를 객체 간의 연산으로 재정의할 수 있음
# 연산자 : 값 계산에 사용되는 기호
# 객체 간의 연산은 불가능함
# 클래스 안에 연산자와 관련된 예약어를 사용해서, 객체 간의 연산이 가능하도록 기존 연산자에 대한 메서드를 추가 작성하는 것

'''
객체와 객체간 연산과 객체와 값의 연산이 있음
객체 + 값(객체) : __add__(self, 값 또는 객체):
    return self.필드 + 값 또는 return self.필드 + other.필드
객체 - 값(객체) : __sub__(self, 값 또는 객체):
    return self.필드 - 값 또는 return self.필드 - other.필드
객체 * 값(객체) : __mul__(self, 값 또는 객체):
    return self.필드 * 값 또는 return self.필드 * other.필드
객체 / 값(객체) : __truediv__(self, 값 또는 객체):
    return self.필드 / 값 또는 return self.필드 / other.필드
객체 // 값(객체) : __floordiv__(self, 값 또는 객체):
    return self.필드 // 값 또는 return self.필드 // other.필드
객체 ** 값 : __pow__(self, 값):
    return self.필드 ** 값

객체 > 값(객체) : __gt__(self, 값 또는 객체):
    return self.필드 > 값 또는 return self.필드 > other.필드
객체 >= 값(객체) : __ge__(self, 값 또는 객체):
    return self.필드 >= 값 또는 return self.필드 >= other.필드
객체 < 값(객체) : __lt__(self, 값 또는 객체):
    return self.필드 < 값 또는 return self.필드 < other.필드
객체 <= 값(객체) : __le__(self, 값 또는 객체):
    return self.필드 <= 값 또는 return self.필드 <= other.필드
객체 == 값(객체) : __eq__(self, 값 또는 객체):
    return self.필드 == 값 또는 return self.필드 == other.필드
객체 != 값(객체) : __ne__(self, 값 또는 객체):
    return self.필드 != 값 또는 return self.필드 != other.필드
    
시퀀스나 맵 타입에 대해서도 연산자 오버로딩 가능함

타입 변환 관련 메서드 오버로딩
__int__(self):
    return int(self.필드명)
    
__float__(self):
    return float(self.필드명)

__bool__(self):
    return bool(self.필드명)
'''

class OOP:
    # field : private
    __num = 0
    
    # constructor
    def __init__(self, num):
        self.__num = num

    # 연산자 오버로딩 메서드 추가
    def __add__(self, value):
        '+ 연산자를 메서드로 오버로딩 처리'
        return self.__num + value
    
    def __sub__(self, value):
        '- 연산자를 메서드로 오버로딩 처리'
        return self.__num - value
    
    def __mul__(self, value):
        '* 연산자를 메서드로 오버로딩 처리'
        return self.__num * value
    
    def __truediv__(self, value):
        '/ 연산자를 메서드로 오버로딩 처리'
        return self.__num / value
    
    # getter
    def get_num(self):
        return self.__num
# class OOP --------------------------------

# 클래스 객체 생성
ref = OOP(100)
print('ref 가 참조하는 인스턴스 안의 __num 값 : ', ref.get_num())

# 객체와 값의 연산 (기본적으로 객체와 값의 연산은 불가능임)
# print('ref > 30 : ', ref > 30) # TypeError: '>' not supported between instances of 'OOP' and 'int'
print('ref + 30 : ', ref + 30)
print('ref - 30 : ', ref - 30)
print('ref * 30 : ', ref * 30)
print('ref / 30 : ', ref / 30)


# len() : 길이(저장된 값의 갯수)를 구하는 내장함수
# 리스트, 튜플, 문자열 같은 시퀀스 자료형에 주로 사용
# 연산자 오버로딩으로 추가할 수 있음
class MyNumber:
    def __init__(self, value):
        self.value = value # 필드 동적 추가
        
    def __len__(self):
        return self.value
# class MyNumber -----------------------------

ref = MyNumber(5)
print('len() : ', len(ref))

# in 연산자 오버로딩도 가능함
class MyBox:
    def __init__(self, items):
        self.items = items # 필드 동적 추가
    
    def __len__(self): # len()
        return len(self.items)
    
    def __contains__(self, item): # in 연산자
        return item in self.items
# class MyBox -------------------------------

box = MyBox([1, 2, 3])

print(len(box)) # 3
print(2 in box) # True
print(5 in box) # False

# 인덱싱 : [index] 연산자 오버로딩
class MyList:
    def __init__(self, data):
        self.data = data
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index): # [index] 인덱싱 연산자 오버로딩
        return self.data[index]

    def __str__(self): # 자바의 toString() 같은 메서드임
        return str(self.data)
# class MyList ---------------------------------

myList = MyList([10, 20, 30])

print(len(myList)) # 3
print(myList[0]) # 10
print(myList[1]) # 20
print(myList) # __str__실행
