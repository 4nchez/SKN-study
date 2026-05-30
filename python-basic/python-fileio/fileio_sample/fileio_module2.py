# file path : fileio_sample/fileio_module2.py
# module : fileio_sample.fileio_module2

# 파이썬의 기본 파일 입출력은 텍스트 파일 입출력임 (*.txt)
# 텍스트가 아닌 자료형의 파일을 다룰 때는 pickle 모듈 활용
# 바이너리(이진 데이터 : binary) 형식의 파일을 취급할 때 pickle 모듈 사용
# 파일 열기 모드 : wb, rb, ab 로 표기해야 함

import os
import pickle

def test_binary_fileio():
    data = {1:'python', 2:'you need'}
    
    f = open('btest.dat', 'wb')
    # write(str) 사용 못 함 => 파일에 이진 데이터로 기록해야 함
    pickle.dump(data, f) # 파일에 딕셔너리 객체가 가진 데이터를 이진 데이터로 기록함
    f.close()
# ---------------------------------------

def test_binary_fileio2():
    f = open('btest.dat', 'rb')
    read_data = pickle.load(f) # 파일에 기록된 이진 데이터를 읽어들임
    f.close()
    
    print(read_data)
    print(type(read_data)) # wb 는 해당 객체타입 그대로 기록함 : <class 'dict'>
# -----------------------------------------