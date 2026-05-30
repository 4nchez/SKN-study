# Streamlit 사용 : 로그인 기능과 csv 파일 업로드 및 데이터 분석 프로젝트

## 로그인을 위한 테스트 계정
|email | password |
|--|--|
|admin@example.com| ****** |
|student@example.com| ******|
|teacher@example.com| ******|

## 실행
```
python -m venv .venv
pip install -r requirements.txt
streamlit run app/main.py
```

## 프로젝트 구조
프로젝트명 : streamlit_login_csv_project
```
streamlit_login_csv_project/
├── .venv/                     # 가상환경 폴더
├── requirements.txt           # 외부 모듈 설치 목록 파일
├── README.md                  # 프로젝트 설명 파일
├── data/
│   ├── sample_sales.csv       # 데이터 분석용 데이터 파일
│   └── users.csv              # 로그인할 사용자 정보 저장 파일
└── app/
    └── main.py                # GUI 코드 파일
```

## 기능 설명
- 로그인 계정 정보는 `data/users.csv` 파일에서 읽어옵니다.
- 로그인 실패 시 팝업 창에 아래 메시지를 출력합니다.
  - `아이디와 암호가 일치하지 않습니다. 확인하고 다시 입력하세요.`
- 팝업의 닫기 버튼을 누르면 다시 로그인 페이지가 표시됩니다.
- 로그인 성공 후 CSV 파일을 업로드하면 다음 기능을 제공합니다.
  - 데이터 테이블 출력
  - 기본 통계 정보 출력
  - 선 그래프(Line Chart) 출력
  - 막대 그래프(Bar Chart) 출력
  - 히스토그램(Histogram) 출력

## 배포 방법
GitHub 에 프로젝트를 업로드한 뒤 Streamlit Community Clooud 에서 새 앱 만들고 실행파일을 업로드함