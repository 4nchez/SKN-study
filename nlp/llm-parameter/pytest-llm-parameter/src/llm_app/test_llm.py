# LLM이 대답 할 수 있는 질문과 대답 할 수 없는 실시간 사내 정보 관련 질문 결과 확인용

# 가장 단순한 LLM 호출 한 번
from google import genai

# Gemini 모델명과 API Key 정보 불러오기
from .config import GEMINI_MODEL, require_env

# GOOGLE_API_KEY가 정상 설정되어 있는지 확인하고 값을 가져옴
api_key = require_env("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) # Gemini 클라이언트 생성

def ask(question: str) -> str:
    # generate_content = "한 번 묻고 → 한 번 답받기"의 가장 기본 호출
    resp = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=question,
    )
    return resp.text # 모델이 생성한 답변(문자열)

# 질문 1: 일반 지식 → LLM 이 잘 답함
print(ask("블루투스 이어버드를 고를 때 무엇을 봐야 하나요? 3 가지만 짧게."))

# 질문 2: 실시간 사내 정보 → LLM 혼자서는 불가
print(ask("승승장구몰 주문번호 O000123 은 지금 배송 어디까지 왔나요?"))


# pytest가 인식할 수 있도록 함수화
def test_llm_responses():
    # 질문 1: 일반 지식
    res1 = ask("블루투스 이어버드를 고를 때 무엇을 봐야 하나요? 3 가지만 짧게.")
    print("\n[질문 1 답변]:", res1)

    # 질문 2: 실시간 사내 정보
    res2 = ask("승승장구몰 주문번호 O000123 은 지금 배송 어디까지 왔나요?")
    print("\n[질문 2 답변]:", res2)

    # 테스트 통과를 위한 임의의 단언(assert)
    assert res1 is not None
    assert res2 is not None