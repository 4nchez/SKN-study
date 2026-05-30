sungjuk_list = []
def sungjuk_process():
    prompt = '''
            *** 원하는 메뉴 번호를 선택하세요. ***
            1. 추가
            2. 삭제
            3. 출력
            4. 끝내기
        '''
    print(prompt)
     
    while (no := input('원하는 메뉴 번호 입력 :')):
        if no == '1':
            sno = int(input('번호 : '))
            sname = input('이름 : ')
            score = int(input('점수 : '))
            sungjuk_list.append([sno, sname, score])
            print('새로운 학생정보가 추가되었습니다.')
        
        elif no == '2':
            try:
                print(f'현재 저장된 아이템의 갯수는 {len(sungjuk_list)}개 입니다.')
                index = int(input('제거할 아이템의 순번 : '))
                sungjuk_list.pop(index-1)
                print(f'현재 저장된 아이템의 갯수는 {len(sungjuk_list)}개 입니다.')
            except:
                print('순번이 잘못 입력되었습니다. 확인하고 다시 입력하세요.')
        
        elif no == '3':
            for idx, data in enumerate(sungjuk_list):
                print(f'{idx} : {data}')
        
        elif no == '4':
            print('성적관리 프로그램이 종료되었습니다.')
            break
        else:
            print('성적관리 프로그램이 종료되었습니다.')
            break 
        
        print(prompt)
        