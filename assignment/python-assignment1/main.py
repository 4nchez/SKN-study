import loop.while_mission as lw
import fileio.fileio_mission as fm

def menu():
    prompt = '''
	*** 파이썬 과제 1 ***
	1. while 실습문제
	2. fileio 실습문제
	9. 과제 실행 테스트 끝내기
    '''
    print(prompt)
 
    while (no := input('원하는 메뉴 번호 입력 :')):
        if no == '1':
            lw.sungjuk_process()
        elif no == '2':
            fm.emp_process()
        elif no == '9':
            break
        else:
            break
        print(prompt)
	

if __name__=='__main__':
    menu()