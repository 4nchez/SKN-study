# FastAPI 웹 서버를 만들기 위해 FastAPI 클래스를 불러옵니다.
from typing import Optional
from fastapi import Depends, FastAPI, Request
# 정적 파일 경로를 연결하기 위해 StaticFiles를 불러옵니다.
from fastapi.staticfiles import StaticFiles
# HTML 템플릿을 렌더링하기 위해 Jinja2Templates를 불러옵니다.
from fastapi.templating import Jinja2Templates
# JSON 응답을 명확하게 반환하기 위해 JSONResponse를 불러옵니다.
from fastapi.responses import JSONResponse
# 경로 처리를 위해 Path를 불러옵니다.
from pathlib import Path
from sqlalchemy.orm import Session

# DB 세션/엔진/Base를 불러옵니다.
from app.database import Base, engine, get_db
# 요청 데이터 구조를 불러옵니다.
from app.schemas import ChatRequest, CartAddRequest, CheckoutRequest
# 회원 인증 라우터를 불러옵니다.
from app.routers.auth import router as auth_router
# 로그인 여부와 무관하게 현재 사용자를 조회하는 의존성입니다(비회원이면 None).
from app.security import get_current_user, get_current_user_optional
from app.models.models import User
# 메뉴/주문 서비스 로직을 불러옵니다.
from app.services import menu_service, order_service
# PyTorch 의도 분류 함수를 불러옵니다.
from app.torch_model import predict_intent
# OpenAI 응답 생성 함수를 불러옵니다.
from app.openai_service import generate_chat_answer, is_openai_ready

# 현재 파일 기준으로 app 디렉터리 경로를 계산합니다.
BASE_DIR = Path(__file__).resolve().parent

# FastAPI 애플리케이션 객체를 생성합니다.
app = FastAPI(title="Coffee Order AI Chatbot", description="FastAPI + OpenAI + PyTorch + MySQL 커피 주문 챗봇", version="2.0.0")

# CSS, JS 같은 정적 파일 경로를 /static URL에 연결합니다.
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# HTML 템플릿 폴더를 설정합니다.
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 회원가입/로그인 라우터를 앱에 등록합니다. (/auth/signup, /auth/login, /auth/me)
app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    # 앱이 시작될 때 테이블이 없으면 생성하고, 메뉴 테이블이 비어 있으면 기본 메뉴를 채워 넣습니다.
    Base.metadata.create_all(bind=engine)  # users/menus/orders/order_items/payments 테이블을 생성합니다.
    db = next(get_db())  # 시드 작업을 위해 임시로 DB 세션을 하나 가져옵니다.
    try:
        menu_service.seed_menus(db)  # menus 테이블이 비어 있으면 기본 메뉴 데이터를 채웁니다.
    finally:
        db.close()  # 사용한 세션을 닫습니다.


# 루트 페이지를 렌더링하는 엔드포인트입니다.
@app.get("/")
def home(request: Request):
    # index.html 템플릿에 요청 객체와 제목을 전달하여 화면을 반환합니다.
    return templates.TemplateResponse("index.html", {"request": request, "app_title": "Coffee Order AI"})


# 서버 상태와 OpenAI 키 설정 상태를 확인하는 엔드포인트입니다.
@app.get("/api/health")
def health():
    # 서버 상태와 OpenAI 준비 여부를 JSON으로 반환합니다.
    return {"status": "ok", "openai_ready": is_openai_ready()}


# 전체 메뉴 목록을 반환하는 엔드포인트입니다. (DB에서 조회)
@app.get("/api/menu")
def menu(db: Session = Depends(get_db)):
    # DB에 저장된 커피 메뉴를 조회하여 반환합니다.
    menus = menu_service.get_all_menus(db)
    return {"menus": [menu_service.menu_to_dict(m) for m in menus]}


# 챗봇 대화 처리 엔드포인트입니다.
# 로그인 여부와 무관하게 이용할 수 있으며, 로그인한 경우 장바구니가 회원 계정에 귀속됩니다.
@app.post("/api/chat")
def chat(
    request_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    # 사용자 메시지를 변수에 저장합니다.
    message = request_data.message
    # PyTorch 모델로 사용자 의도를 예측합니다.
    intent, confidence = predict_intent(message)
    # 사용자 메시지에 맞는 메뉴를 DB에서 검색합니다.
    recommendations = menu_service.find_menus(db, message, top_k=request_data.top_k)
    # 사용자의 메시지에서 온도 옵션을 추출합니다.
    temperature = order_service.extract_temperature(message)
    # 사용자의 메시지에서 수량을 추출합니다.
    quantity = order_service.extract_quantity(message)
    # 현재 장바구니 총액을 조회합니다.
    cart_state = order_service.get_cart(db, current_user)
    # OpenAI에 전달할 시스템 분석 내용을 만듭니다.
    system_context = (
        f"예측 의도: {intent}\n"
        f"신뢰도: {confidence:.2f}\n"
        f"추천 메뉴: {', '.join(m.name for m in recommendations)}\n"
        f"온도 옵션: {temperature}\n"
        f"수량: {quantity}\n"
        f"장바구니 합계: {cart_state['total']}원"
    )
    # OpenAI 또는 로컬 fallback으로 자연어 답변을 생성합니다.
    ai_message = generate_chat_answer(message, system_context)
    # 주문 의도이고 추천 메뉴가 있으면 첫 번째 메뉴를 장바구니에 담을 수 있도록 안내합니다.
    recommendation_dicts = [menu_service.menu_to_dict(m) for m in recommendations]
    if intent == "order" and recommendation_dicts:
        ai_message += f"\n\n'{recommendation_dicts[0]['name']}' 메뉴를 장바구니에 담으려면 추천 카드의 담기 버튼을 눌러주세요."
    # 프론트엔드에서 사용할 JSON 응답을 반환합니다.
    return {
        "message": ai_message,
        "intent": intent,
        "confidence": round(confidence, 3),
        "recommendations": recommendation_dicts,
        "temperature": temperature,
        "quantity": quantity,
        "cart": cart_state["cart"],
        "total": cart_state["total"],
    }


# 추천 카드에서 장바구니에 메뉴를 담는 엔드포인트입니다.
@app.post("/api/cart/add")
def cart_add(
    request_data: CartAddRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    # 전달받은 메뉴 정보를 DB의 장바구니(주문)에 추가합니다.
    result = order_service.add_to_cart(
        db,
        current_user,
        request_data.menu_id,
        request_data.temperature,
        request_data.quantity,
        request_data.option_note,
    )
    # 처리 결과를 JSON으로 반환합니다.
    return JSONResponse(result)


# 현재 장바구니를 조회하는 엔드포인트입니다.
@app.get("/api/cart")
def cart_get(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_optional)):
    # 장바구니 목록과 총액을 반환합니다.
    return order_service.get_cart(db, current_user)


# 장바구니를 초기화하는 엔드포인트입니다.
@app.post("/api/cart/clear")
def cart_clear(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_optional)):
    # 장바구니 항목을 모두 삭제합니다.
    return order_service.clear_cart(db, current_user)


# 데모 결제 처리 엔드포인트입니다. 결제 완료 시 Order 상태가 paid로 바뀌고 Payment 레코드가 생성됩니다.
@app.post("/api/checkout")
def checkout(
    request_data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    # 장바구니를 결제 완료 상태로 전환합니다.
    result = order_service.checkout(db, current_user, request_data.method)
    return result


# 로그인한 회원의 결제 완료 주문 내역을 조회하는 엔드포인트입니다. (로그인 필수)
@app.get("/api/orders/history")
def order_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 회원의 결제 완료 주문 목록을 조회합니다.
    orders = order_service.get_order_history(db, current_user)
    return {
        "orders": [
            {
                "id": o.id,
                "status": o.status,
                "items": order_service.cart_items(o),
                "total": order_service.cart_total(o),
                "created_at": o.created_at,
            }
            for o in orders
        ]
    }
