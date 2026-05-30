# file path : fileio_sample/fileio_module.py
# module : fileio_sample.fileio_module

# 파이썬에서의 파일입출력 처리 테스트용 스크립트 (함수들만 저장된 모듈 파일)
# 파이썬에서의 파일입출력
# open() -> write() or read() -> close()
'''
파일변수 = open('디렉터리명/파일명.확장자', '열기모드')
파일입출력의 기본은 텍스트(문자) 파일 입출력임
열기모드 : 
w(wt), x(xt) : 새로 쓰기
    - w : 대상 파일이 없으면, 파일을 자동으로 새로 만들어서 열기함
          대상 파일이 있으면, 파일 안의 내용을 모두 지우고 새로 쓰기 상태로 열기함
    - x : 대상 파일이 없으면, 파일을 자동으로 새로 만들어서 열기함
          대상 파일이 있으면, 에러 발생함
a(at) : 추가 쓰기 (append)
        대상 파일이 없으면, 파일을 자동으로 새로 만들어서 열기함
        대상 파일이 있으면, 파일 안의 내용을 그대로 두고 추가 쓰기 상태로 열기함
r(rt) : 읽기 전용
        대상 파일이 없으면, 에러 발생함
'''

# 1. 파일을 새로 만들고 값 기록 저장하기 테스트
import os

def test_fwrite():
    # f = open('testa.txt', 'w') # 기본 경로는 현재 폴더 아래에 저장됨
    f = open('testa.txt', 'w', encoding='UTF-8')
    f.write('test file writing check.....\n')
    f.write('2026-05-04')
    f.write('파일에 저장 확인용') # 텍스트 파일의 기본 인코딩은 OS 를 따름 : Windows OS 는 'MS949' (ISO 8859-1)
    f.write('★★★★★★★★★★★★★★★★★★★★★') # 문자인코딩이 달라서 한글과 기호문자가 깨짐
    f.close()
    
    # os 모듈을 활용하면 현재 작업 중인 디렉터리 경로를 확인하고 이용할 수 있음
    print(os.getcwd()) # current wroking directory
    return
# -------------------------------------------------------------------

# 2. 원하는 디렉터리(폴더)에 파일을 만들려면
# open() 함수 첫번째 전달인자(전달값(argument) : 함수의 매개변수(parameter)에게 전달되는 값)에
# 전체경로명과 파일명을 함께 입력하면 됨 => 주의 : 백슬러시(\) 이스케이프 문자를 반드시 2개 표기해야 함
def test_fwrite2():
    # x 모드 : 대상 파일이 존재하면 FileExistsError 발생함 (덮어쓰기 방지용으로 주로 사용함)
    f = open('./fileio_sample/testb.txt', 'x', encoding='UTF-8')
    f.write('test file path using saved.....\n')
    f.write('전체 경로를 포함해서 파일 저장 확인\n')
    f.write('2026년 5월 4일 월요일에 작성한 파일임')
    f.close()
# ----------------------------------------------

# a 모드 : append (추가쓰기 모드)
# 기존 내용 마지막(끝) 위치 뒤에 추가 기록됨
def test_fwrite3():
    f = open('testc.txt', 'a', encoding='UTF-8')
    f.write('test file append mode.....\n')
    f.write('파일의 기존 내용 뒤에 추가쓰기 확인.....\n')
    f.close()
# ----------------------------------------------

# 3. 파이썬에서 파일이나 디렉터리 다루기
# os 모듈이 제공하는 함수 사용함
def test_osmodule():
    # 사용 중인 컴퓨터의 사용자계정(컴퓨터이름) 조회
    print(os.getlogin())
    # 현재 작업 디렉터리 조회
    print(os.getcwd())

    system_user = os.getlogin()
    work_dir = './' + str(system_user) + '/chdir'
    # 디렉터리 만들기 : os.mkdir('만들 디렉터리경로와 디렉터리명')
    os.mkdir(work_dir) # 주의 : 같은 이름의 디렉터리가 있으면 에러남
    
    # 작업 디렉터리 변경하기 : os.chdir('변경할 디렉터리명')
    os.chdir(work_dir)
    print(os.getcwd()) # 확인
    
    # 변경한 디렉터리에 파일 저장
    f = open('sample.txt', 'w', encoding='UTF-8')
    f.write('파이썬으로 디렉터리 만들고, 만든 디렉터리에 파일 생성해서 저장함\n')
    st = '''변경된 디렉터리에 파일 생성하고
    유니코드로 인코딩된 문자열을 기록 저장
    확인함'''
    f.write(st)
    f.close()
    
    # 시스템 환경변수, 디렉터리, 파일 다루기
    # listdir() : 현재 작업 디렉터리 안의 파일들과 하위 디렉터리 목록 조회
    print(os.listdir(os.getcwd()))
    print(os.listdir('.')) # '.' : 현재 디렉터리를 의미함
    print(os.listdir('../')) # '../' : 상위 디렉터리를 의미함
    
    # rename(): 디렉터리나 파일의 이름 바꾸기함
    os.rename('testa.txt', 'samplea.txt')
    
    # path.exists() : 파일이나 디렉터리의 존재 여부 확인
    print(os.path.exists('example.txt')) # 파일이 없으면 False
    print(os.path.exists('sample.txt')) # 파일이 있으면 True
    
    # path.abspath() : 파일이나 디렉터리의 절대경로 조회
    print(os.path.abspath('sample.txt'))
    
    # path.basename(), dirname(), split() : 파일명, 경로명, 두 개 분리
    current_path = os.path.abspath('sample.txt')
    print('current_path : ', current_path)
    print('basename : ', os.path.basename(current_path)) # 파일명.확장자 추출
    print('dirname : ', os.path.dirname(current_path)) # 경로명만 추출
    print('split : ', os.path.split(current_path)) # ('경로명', '파일명.확장자')

    # path.splitdrive(), splittext() : 경로에서 드라이브명만, 확장자만 추출
    print(os.path.splitdrive(current_path)) # ('드라이브명', '나머지경로') 분리
    print(os.path.splitext(current_path)) # ('경로명과파일명', '.확장자') 분리
# ------------------------------------------

# 4. r(rt : read text) : 읽기 전용
# 주의 : 대상 파일이 없으면 에러남
# read() 함수 : 파일안의 전체 내용을 한 번에 읽음
# readline() 함수 : 파일 안의 내용을 한 줄씩 읽음, 마지막 라인을 읽고 나서, 더 이상 읽을 라인이 없으면 None 리턴함
# readlines() 함수 : 파일 안의 내용을 줄단위(아이템)로 모두 읽어서, 리스트로 리턴함
def test_fread():
    print(os.getcwd())
    f = open('sample.txt', 'r', encoding='UTF-8')
    # print(f.read())

    # 파일의 내용을 한 줄씩 읽도록 처리한다면
    line_number = 1
    while True:
        line = f.readline()
        if not line: # line 변수의 값이 없다면 (None 이면)
            break
        print(line_number, ' : ', line, end='') # print() 함수의 end 매개변수의 기본값 '\n' 제거함
        line_number += 1
        
    f.close()
# -------------------------------------

# 한 줄씩 읽은 정보가 리스트에 저장되게 하려면
def test_fread2():
    f = open('sample.txt', 'r', encoding='utf-8')
    lst = f.readlines()
    print(lst)
    f.close()
# ------------------------

# 5. 리스트, 튜플, 셋. 사전 등에 저장한 데이터들을 파일에 저장
# writelines() 함수 사용
def test_writelines():
    tp = ('a', 'b', 'c')
    ls = ['r', 'e', 'd']
    f = open('list.txt', 'w')
    f.writelines(tp)
    f.write('\n')
    f.writelines(ls)
    f.write('\n')
    
    f.close()
# ----------------------------
