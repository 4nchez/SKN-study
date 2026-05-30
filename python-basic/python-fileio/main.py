# main.py
# 프로젝트 (에플리케이션)를 실행하는 스크립트
# CLI (Command Line Interface) : 실행시 터미널(command prompt)에 글자로 메시지가 출력되고, 키보드 입력으로 실행
# GUI (Graphic User Interface) : 실행시 윈도우 창이 열리면서, 메뉴바/툴바 등을 마우스로 클릭으로 실행

import fileio_sample.fileio_module as fs
import loop.while_sample as lw
import fileio_sample.fileio_module2 as fs2

# CLI 방식의 메뉴 출력용 함수
def menu():
    print('파일입출력 및 예외처리 테스트용 프로그램 시작 ---------------------------')
    
    # 파이썬에서는 여러 줄의 문자열 값을 표현할 때 3쌍의 따옴표를 이용함
    prompt = '''
    1. 파일에 저장하기 테스트 1
    2. 파일에 저장하기 테스트 2 : 경로 지정 저장
    3. 파일에 저장하기 테스트 3 : 추가쓰기 모드 확인
    4. 파일로 부터 읽어오기 테스트
    5. while 반복문 사용 테스트 1
    6. while 반복문 사용 테스트 2
    7. os 모듈의 함수 확인 1
    9. 메뉴 끝내기
    10. 파일 내용 줄단위로 리스트에 저장하기
    11. 컬렉션 아이템들을 파일에 저장하기
    12. 이진 데이터로 파일에 저장하기
    13. 파일로 부터 이진 데이터 읽어오기
    '''
        
    while True:
        # print('1. 파일에 저장하기 테스트 1')
        # print('2. 파일로 부터 읽어오기 테스트 1')
        # print('9. 메뉴 끝내기')
        
        print(prompt)
        no = int(input('원하는 메뉴 번호 입력 :'))
        
        if no == 1:
            fs.test_fwrite()
        elif no == 2:
            fs.test_fwrite2()
        elif no == 3:
            fs.test_fwrite3()
        elif no == 4:
            fs.test_fread()
        elif no == 5:
            lw.test_while()
        elif no == 6:
            lw.print_unicode()
        elif no == 7:
            fs.test_osmodule()
        elif no == 9:
            break
        elif no == 10:
            fs.test_fread2()
        elif no == 11:
            fs.test_writelines()
        elif no == 12:
            fs2.test_binary_fileio()
        elif no == 13:
            fs2.test_binary_fileio2()
        else:
            break
    # while end -----------------
    
    print('테스트 종료! --------------------------------------')
    return
# def menu() end -----------------

if __name__=='__main__':
    # fs.test_fwrite()
    # lw.test_while()
    menu()
    print('프로그램 종료!')

