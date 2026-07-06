# 기본 Python 프로젝트 : LLM Parameter 실습 프로젝트

# 패키지 설치
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

# 프로젝트 구조
```text
pytest-llm-parameter/
    |--- .env     # 환경변수 파일
    |--- src/
        |--- llm_app/
            |--- __init__.py        # 패키지 초기화 파일
            |--- config.py          # .env load, API Key 확인, 모델명 관리
            |--- llm_service.py     # Gemini / OpenAI 호출 함수
            |--- utils.py           # 콘솔 입력 / 출력 보조 함수
            |--- test_llm.py         # 두 가지 질문 응답 비교 테스트
```