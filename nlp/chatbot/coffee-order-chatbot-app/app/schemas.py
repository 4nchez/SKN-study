# FastAPI 요청과 응답 데이터 구조를 정의하기 위해 Pydantic을 불러옵니다.
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime  # 응답에 날짜와 시간을 포함하기 위해 사용합니다.


# 사용자가 챗봇에 보내는 요청 데이터 구조입니다.
class ChatRequest(BaseModel):
    # 사용자가 입력한 자연어 메시지입니다.
    message: str = Field(..., min_length=1, description="사용자 입력 메시지")
    # 사용자가 선택한 추천 메뉴 개수입니다.
    top_k: int = Field(default=3, ge=1, le=5, description="추천 메뉴 개수")


# 장바구니에 담을 때 사용하는 요청 데이터 구조입니다.
class CartAddRequest(BaseModel):
    # 메뉴 고유 번호입니다.
    menu_id: int = Field(..., description="메뉴 ID")
    # hot 또는 ice 온도 옵션입니다.
    temperature: str = Field(default="ice", description="온도 옵션")
    # 주문 수량입니다.
    quantity: int = Field(default=1, ge=1, le=20, description="수량")
    # 샷 추가, 시럽 추가 등 사용자 요청사항입니다.
    option_note: str = Field(default="", description="추가 옵션")


# 결제 요청 데이터 구조입니다.
class CheckoutRequest(BaseModel):
    # 결제 수단입니다. 데모 프로젝트이므로 기본값은 demo입니다.
    method: str = Field(default="demo", description="결제 수단")


# ---------------------- 회원 관련 스키마 ----------------------

class UserCreate(BaseModel):
    # 회원가입 요청 데이터 구조입니다.
    username: str = Field(..., min_length=3, max_length=50, description="로그인 아이디")  # 아이디 길이를 검증합니다.
    password: str = Field(..., min_length=4, max_length=100, description="로그인 비밀번호")  # 비밀번호 길이를 검증합니다.
    name: str = Field(..., min_length=1, max_length=50, description="회원 이름")  # 이름 길이를 검증합니다.


class UserResponse(BaseModel):
    # 회원가입 성공 후 반환할 회원 정보 구조입니다.
    id: int  # 회원 고유 번호입니다.
    username: str  # 로그인 아이디입니다.
    name: str  # 회원 이름입니다.
    created_at: datetime  # 가입 시각입니다.

    model_config = {"from_attributes": True}  # SQLAlchemy ORM 객체를 Pydantic 응답으로 변환할 수 있게 합니다.


class TokenResponse(BaseModel):
    # 로그인 성공 후 반환할 JWT 토큰 응답 구조입니다.
    access_token: str  # API 인증에 사용할 액세스 토큰입니다.
    token_type: str = "bearer"  # Swagger 인증 방식에서 사용하는 토큰 타입입니다.


# ---------------------- 메뉴 관련 스키마 ----------------------

class MenuOut(BaseModel):
    # DB에 저장된 메뉴 정보를 클라이언트에 반환하는 구조입니다.
    id: int
    name: str
    category: str
    temperature: List[str]
    taste_tags: List[str]
    description: Optional[str] = None
    price: int

    model_config = {"from_attributes": True}


# ---------------------- 장바구니/주문/결제 관련 스키마 ----------------------

class OrderItemOut(BaseModel):
    # 장바구니(또는 주문)에 담긴 개별 항목을 반환하는 구조입니다.
    menu_id: int
    name: str
    temperature: str
    quantity: int
    price: int
    subtotal: int
    option_note: str = ""

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    # 장바구니 또는 주문(결제 완료 포함) 전체 정보를 반환하는 구조입니다.
    id: int
    status: str
    items: List[OrderItemOut]
    total: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentOut(BaseModel):
    # 결제 완료 정보를 반환하는 구조입니다.
    id: int
    order_id: int
    amount: int
    method: str
    status: str
    paid_at: datetime

    model_config = {"from_attributes": True}
