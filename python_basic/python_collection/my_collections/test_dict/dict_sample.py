# file path : test_dict/dict_sample.py
# module : test_dict.dict_sample

# 사전(dict) 자료형
# 자바의 Map 과 같은 구조로 key 와 value 를 한 쌍(pair)으로 저장하는 집합 자료형임
# dict 에서 key 는 변경되지 않는 값이어야 함 (키는 지정하면 변경할 수 없음) <= 키에 튜플 사용할 수 있음
# dict 에 저장하는 value 는 데이터 제한 없음
# json, xml 로 변환할 때 많이 사용됨

# dict 정의 방법 1: dict() 함수 사용
def dict_test1():
    dct1 = dict()
    print(dct1, type(dct1))
    
    # dict 정의 방법 2 : 중괄호 {} 사용
    dct2 = {}
    print(dct2, type(dct2))
# -----------------------------------

# list 나 tuple 처럼 인덱스를 사용할 수 없음 (인덱스 없음)
# 키(key) 를 이용해서 값 변경, 조회, 추가할 수 있음 => 사전변수[키]
# dict 저장 방식 : {키 : 값, 키: 값, .....} 쌍으로 저장함
def test_dict2():
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    print(dict1, type(dict1))
    
    dict2 = {1: 'python', 'a': [1,2,3,], (1,2): 345}
    print(dict2, type(dict2))
    
    # 값 변경 : 사전변수[존재하는 키] = 바꿀값
    # 변경시에는 저장되어 있는 키만 사용해야 함
    dict2['a'] = 77
    print(dict2, type(dict2))
    
    # 아이템 추가 : 사전변수[없는키] = 값
    # 저장되어 있지 않는 키를 사용함
    dict2[3] = [11, 22, 33]
    print(dict2, type(dict2))

    # 값 조회 : 사전변수[키]
    # 주의 : 없는 키로 조회하면 KeyError 발생함
    # print(dict['c']) # KeyError : 'c'
    print(dict2['a'])
# -----------------------------------

def dict_test_function():
    'dict 내정함수 활용'
    dict1 = {
        'a': 10,
        'b': 25,
        'c': 77
    }
    print(dict1, type(dict1))

    # 키에 대한 리스트 만들기 : keys() 함수
    print('dict1 의 키 목록 : ', dict1.keys())
    
    # 값에 대한 리스트 만들기 : values() 함수
    print('dict1 의 값 목록 : ', dict1.values())
    
    # (키, 값) 을 item 이라고 함, 아이템들을 리스트 만들기 : items() 함수
    print('dict1 의 아이템 목록 : ', dict1.items())
    
    # 사전과 사전을 합치기 : update() 함수
    # 사전1.update(사전) => 사전1을 변경함
    # 사전1과 사전2에 동일한 키가 있을 경우에는, 사전1의 해당 키의 값이 사전2의 값으로 변경됨
    dict2 = {'name': '갤럭시', 'price': 1500000, 'tax': 0.15}
    dict3 = {'content': '최신 모델입니다.', 'price': 8800000}
    print('dict2 : ', dict2)
    print('dict3 : ', dict3)

    dict2.update(dict3)
    print('dict2 : ', dict2)

    # pop(key) 함수 : 해당 키에 대한 아이템을 꺼내면서 제거함
    tax = dict2.pop('tax')
    print('dict2 : ', dict2)
    print('tax : ', tax)
    
    # clear() 함수 : 딕셔너리 안을 비움 (저장 아이템 전체 삭제)
    dict1.clear()
    print('dict1 : ', dict1)

    # copy() 함수 : 사전 객체를 새로 만들고, 아이템들을 복사함 (deep copy : 깊은 복사)
    dict4 = dict3.copy()
    print('dict4 : ', dict4, id(dict4))
    print('dict3 : ', dict3, id(dict3))
    
    dict5 = dict3 # 주소 복사임 : 얕은 복사 (shallow copy)
    print('dict5 : ', dict5, id(dict5))

    # in 연산자 : dict 안에 키 또는 값이 존재하는지 확인
    # 키 존재 여부 => 키 in 사전변수
    print('name 키가 존재하느냐 ? ', 'name' in dict2) # True
    print('tax 키가 존재하느냐 ? ', 'tax' in dict3) # False
    
    # 값 존재여부 => 값 in 사전변수.values()
    print('갤럭시 값이 존재하느냐? ', '갤럭시' in dict2.values()) # True
    print('0.15 값이 존재하느냐? ', 0.15 in dict2.values()) # False
    
    # 키로 값 조회 : 사전변수[키] 또는 사전변수.get(key)
    print('name : ', dict2['name'], dict2.get('name'))
    # 사전변수[키]는 없는 키로 조회하면 에러 발생함
    # get(키) 은 없는 키 사용하면 None 리턴
    print('tax : ', dict3.get('tax')) # None

    # del 사전변수[키] : 아이템 제거
    del dict2['name']
    print('dict2 : ', dict2)
    
# ---------------------------------------------------


# 실행 확인
if __name__=='__main__':
    # dict_test1()
    # test_dict2()
    dict_test_function()