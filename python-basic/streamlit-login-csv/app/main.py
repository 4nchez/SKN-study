# path : ./app/main.py
'''
기능 :
1. data/users.csv 파일에서 로그인 계정 정보를 읽어온다.
2. 사용자가 입력한 이메일과 비밀번호가 csv 의 값과 일치하면 로그인 성공 처리한다.
3. 로그인 실패 시 팝업창에 오류 메세지 표시한다.
4. 로그인이 성공 후 csv 데이터 파일을 업로드하면 테이블과 통계 그래프를 출력한다.
'''

from pathlib import Path # 운영체제에 안전한 파일 경로 처리를 위한 표준 라이브러리임

import matplotlib.pyplot as plt # 그래프 생성을 위한 라이브러리
import pandas as pd # csv 읽기, 데이터프레임 처리, 통계 계산 라이브러비
import streamlit as st # Streamlit 웹 화면 구성 라이브러리

# 현재 파일 위치 : 프로젝트/app/main.py
# parents[1] 은 프로젝트 루트 폴더를 의미함
BASE_DIR = Path(__file__).resolve().parents[1]
# print(__file__)
# print(Path(__file__))
# print(Path(__file__).resolve())
# print(BASE_DIR)

# 사용자 계정 정보가 저장된 CSV 파일 경로
USER_CSV_PATH = BASE_DIR/'data'/'users.csv'

# 1. 기본 페이지 설정
st.set_page_config(
    page_title='CSV 로그인 데이터 분석 앱', # 브라우저 탭 제목
    page_icon='📊', # 브라우저 탭 아이콘
    layout='wide', # 화면을 넓게 사용
)

# 2. 세션 상태 (로그인 상태 관리) 초기화 함수
def init_session_state() -> None:
    '''
    Streamlit 은 버튼 클릭 이나 입력시 스크립트를 다시 실행함.
    로그인 상태를 유지하려면 st.session_state 에 값을 저장해 두면 됨
    '''
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False # 로그인 여부 저장 (현재 로그아웃 상태)
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = '' # 로그인한 사용자 이메일 저장용
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = '' # 로그인한 사용자 이름 저장용
    
    if 'show_login_error' not in st.session_state:
        st.session_state.show_login_error = False # 로그인 실패 팝업 표시 여부 저장
    return
# ------------------------------------------

# 3. 사용자 csv 읽기 함수
# csv 파일은 매번 새로 읽을 필요가 없으므로 캐시 처리함
@st.cache_data
def load_users() -> pd.DataFrame:
    'data/users.csv 파일에서 로그인 계정 정보를 읽어오는 함수'
    if not USER_CSV_PATH.exists():
        # 파일이 없으면 앱 실행을 중단하고 오류 출력
        st.error(f'사용자 csv 파일이 없습니다. : {USER_CSV_PATH}')
        st.stop()
    # if --------------------------------
    
    user_df = pd.read_csv(USER_CSV_PATH)
    
    # 필수 컬럼 존재 여부 확인 (이메일, 비밀번호, 이름 컬럼)
    require_columns = {'email', 'password', 'name'}
    if not require_columns.issubset(user_df.columns):
        st.error('users.csv 파일에는 email, password, name 컬럼이 존재해야 합니다.')
        st.stop()
    # if --------------------------------
    
    # 비교를 위해 문자열 타입으로 변환
    user_df['email'] = user_df['email'].astype(str)
    user_df['password'] = user_df['password'].astype(str)
    user_df['name'] = user_df['name'].astype(str)

    return user_df
# ---------------------------------------

# 4. 로그인 검증 함수
def check_login(email: str, password: str) -> tuple[bool, str]:
    '''
    입력한 이메일/비밀번호가 users.csv 에 있는지 확인한다.
    반환값 :
     - (True, 사용자이름) : 로그인 성공
     - (False, '') : 로그인 실패
    '''
    users_df = load_users()
    
    # 입력값 앞뒤 공백 제거
    # email = email.strip()
    # password = password.strip()
    
    # email 과 password 가 모두 일치하는지 검사
    matched = users_df[(users_df['email'] == email) & (users_df['password'] == password)]

    if not matched.empty: # 로그인 성공
        # 일치하는 값이 있다면, 사용자 이름 반환
        return True, matched.iloc[0]['name']
    # if ------------------------------------
    
    return False, '' # 로그인 실패
# -------------------------------------------

# 5.로그인 실패 팝업창
@st.dialog('로그인 실패')
def login_error_dialog() -> None:
    '로그인 실패 메세지를 팝업창으로 출력하는 함수'
    st.error('아이디와 암호가 일치하지 않습니다. 확인하고 다시 입력하세요.')

    # 닫기 버튼 클릭시 팝업 상태를 False 로 바꾸고 화면을 다시 실행함
    if st.button('닫기'):
        st.session_state.show_login_error = False
        st.rerun()
# -------------------------------

# 6. 로그인 화면 구성
def show_login_page() -> None:
    '로그인 화면 출력 함수'
    st.title('로그인 하세요.')
    st.write('이메일과 비밀번호를 입력하세요.')

    # 로그인 폼 영역
    with st.form('login_form'):
        email = st.text_input('이메일 : ', placeholder='user@example.com')
        password = st.text_input('비밀번호 : ', type='password', placeholder='1234')
        submitted = st.form_submit_button('로그인')

        # 로그인 버튼 클릭시 검증
        if submitted:
            success, user_name = check_login(email, password)
            
            if success:
                # 로그인 성공 정보 저장
                st.session_state.logged_in = True
                st.session_state.user_email = email.strip()
                st.session_state.user_name = user_name
                st.session_state.show_login_error = False
                st.rerun()
            else:
                # 로그인 실패 팝업 표시
                st.session_state.show_login_error = True

        # 로그인 실패 상태이면 팝업 함수 호출
        if st.session_state.show_login_error:
            login_error_dialog()
        
        # 숨기기
        # with st.expander('테스트 계정 보기'):
        #     st.code('admin@example.com/1234\nstudent@example.com/pass123\nteacher@example.com/teach123')
# -------------------------------------------

# 7. 업로드 csv 데이터 파일 읽기 함수
def read_upload_csv(uploaded_file) -> pd.DataFrame:
    '사용자가 업로드한 csv 데이터 파일을 읽어서 pandas 의 DataFrame 으로 만들어서 리턴하는 함수'
    try:
        return pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        # 한글 Windows csv 가 cp949로 저장된 경우에 대비함
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding='cp949')
# -------------------------------------------------------------------

# 8. 데이터 분석 화면 구성
def show_dashboard_page() -> None:
    '로그인 성공 후 표시되는 데이터 분석 페이지'
    st.title('로그인 성공 - CSV 데이터 분석')

    # 상단 사용자 정보와 로그아웃 버튼 표시
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f'{st.session_state.user_name} 님 로그인 성공 : {st.session_state.user_email}')
    
    with col2:
        if st.button('로그아웃'):
            st.session_state.logged_in = False
            st.session_state.user_email = ''
            st.session_state.user_name = ''
            st.session_state.show_login_error = False
            st.rerun()

    st.divider()
    
    # 파일 업로드 위젯
    uploaded_file = st.file_uploader(
        '분석할 csv 데이터 파일을 선택하세요 : ',
        type=['csv'],
        help='예 : data/sample_sales.csv 파일을 업로드해서 테스트 할 수 있습니다.',
    )
    
    if uploaded_file is None:
        st.info('CSV 파일을 업로드하면 테이블과 통계 그래프가 표시됩니다.')
        st.write('프로젝트에 포함된 예제 데이터 파일 : data/sample_sales.csv')
        return
    
    # 업로드한 파일 읽기
    df = read_upload_csv(uploaded_file)
    
    st.subheader('1. 읽어온 데이터 테이블')
    st.dataframe(df, use_container_width=True)

    st.subheader('2. 기본 데이터 정보')
    col1, col2, col3 = st.columns(3)
    col1.metric('행 갯수', len(df))
    col2.metric('열 갯수', len(df.columns))
    col3.metric('결측치 갯수', int(df.isna().sum().sum()))

    st.subheader('3. 숫자 컬럼 통계 요약')
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        st.warning('숫자형 컬럼이 없어서 통계 그래프를 표시할 수 없습니다.')
        return
    
    # 숫자형 컬럼의 통계값 표시
    st.dataframe(numeric_df.describe(), use_container_width=True)

    st.subheader('4. 통계 그래프')

    # 그래프로 표시할 숫자 컬럼 선택
    selected_column = st.selectbox(
        '그래프로 표시할 숫자 컬럼을 선택하세요',
        numeric_df.columns,
    )
    
    # 그래프 종류 선택
    chart_type = st.radio(
        '그래프 종류를 선택하세요 : ',
        ['선 그래프', '막대 그래프', '히스토그램'],
        horizontal=True,
    )
    
    if chart_type == '선 그래프':
        # 선택 컬럼의 값을 선 그래프로 출력
        st.line_chart(numeric_df[selected_column])
    
    elif chart_type == '막대 그래프':
        # 선택 컬럼의 값을 막대 그래프로 출력
        st.bar_chart(numeric_df[selected_column])
        
    else:
        # 히스토그램은 matplotlib 로 직접 생성함
        fig, ax = plt.subplots()
        ax.hist(numeric_df[selected_column].dropna(), bins=10)
        ax.set_title(f'{selected_column} Histogram')
        ax.set_xlabel(selected_column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)    
# ----------------------------------------------------

# 9. 메인 실행 흐름
def main() -> None:
    '앱의 시작 함수'
    init_session_state()
    
    # 로그인 여부에 따라 다른 화면 표시
    if st.session_state.logged_in:
        show_dashboard_page()
    else:
        show_login_page()
# ---------------------------------------

# 이 파일을 직접 실행할 때 main() 함수 실행
if __name__=='__main__':
    main()