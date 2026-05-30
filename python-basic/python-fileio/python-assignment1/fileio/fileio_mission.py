import pickle

emp_list = {}

def print_dict(dct : dict):
    for key in dct.keys():
        print(f'{key} : {emp_list[key]}')

def emp_process():
    prompt = '''
        *** 직원 정보 관리 서비스 ***
        1. 새 직원정보 추가
        2. 직원정보 삭제
        3. 전체 출력
        4. 파일에 저장
        5. 파일로 부터 직원정보 읽어오기
        9. 서비스 끝내기
        '''
    print(prompt)
    
    while (no := input('원하는 메뉴 번호 입력 :')):
        if no == '1':
            empid = input('사번 : ')
            empname = input('이름 : ')
            empno = input('주민번호 : ')
            email = input('이메일 : ')
            phone = input('전화번호 : ')
            salary = int(input('급여 : '))
            job = input('직급 : ')
            dept = input('부서 : ')
            emp_list[empid] = [empid, empname, empno, email, phone, salary, job, dept]
        
        elif no == '2':
            try:
                empid = input('삭제할 사번 : ')
                emp_dict = emp_list.pop(empid)
                print(f'{empid} 번 사번의 직원 정보가 삭제되었습니다.')
            except:
                print('사번이 잘못 입력되었습니다. 확인하고 다시 입력하세요.')
        
        elif no == '3':
            print_dict(emp_list)
                
        elif no == '4':
            f = open('employees.dat', 'wb')
            pickle.dump(emp_list, f)
            f.close()
                
        elif no == '5':
            f = open('employees.dat', 'rb')
            emp_dict = pickle.load(f)
            print_dict(emp_dict)
            f.close()
        
        elif no == '9':
            print('직원 관리 프로그램을 종료합니다.')
            break
        else:
            print('직원 관리 프로그램을 종료합니다.')
            break 
        
        print(prompt)