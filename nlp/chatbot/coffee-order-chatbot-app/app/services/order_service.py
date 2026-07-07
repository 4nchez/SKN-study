# app/services/order_service.py
# 장바구니(Order status=cart) / 주문 상세(OrderItem) / 결제(Payment) 관련 로직을 모아둔 서비스 파일입니다.
# 로그인한 회원은 회원별로 장바구니가 분리되어 저장되고, 비회원은 공용 게스트 장바구니를 사용합니다.

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.models import Order, OrderItem, Payment, User
from app.services.menu_service import get_menu


# ---------------------- 사용자 메시지 분석 (기존 로직 유지) ----------------------

def extract_temperature(message: str) -> str:
    # 메시지에 차가운 음료 관련 표현이 있으면 ice를 반환합니다.
    if any(word in message.lower() for word in ["아이스", "ice", "차가운", "시원한"]):
        return "ice"
    # 메시지에 따뜻한 음료 관련 표현이 있으면 hot을 반환합니다.
    if any(word in message.lower() for word in ["핫", "hot", "따뜻한", "뜨거운"]):
        return "hot"
    # 별도 표현이 없으면 기본값으로 ice를 반환합니다.
    return "ice"


def extract_quantity(message: str) -> int:
    # 한국어 수량 표현을 숫자로 바꾸기 위한 딕셔너리입니다.
    korean_numbers = {"한": 1, "두": 2, "세": 3, "네": 4, "다섯": 5}
    for word, number in korean_numbers.items():
        if f"{word} 잔" in message or f"{word}잔" in message or f"{word} 개" in message or f"{word}개" in message:
            return number
    for number in range(1, 10):
        if f"{number}잔" in message or f"{number} 잔" in message or f"{number}개" in message or f"{number} 개" in message:
            return number
    return 1


# ---------------------- 장바구니(Order status=cart) 조회/생성 ----------------------

def get_or_create_cart(db: Session, user: Optional[User]) -> Order:
    # 로그인 사용자는 user_id로, 비회원은 user_id가 NULL인 공용 장바구니 1개를 찾거나 새로 만듭니다.
    query = db.query(Order).filter(Order.status == "cart")
    if user:
        query = query.filter(Order.user_id == user.id)
    else:
        query = query.filter(Order.user_id.is_(None))
    order = query.first()
    if order is None:
        order = Order(user_id=user.id if user else None, status="cart")
        db.add(order)
        db.commit()
        db.refresh(order)
    return order


def order_item_to_dict(item: OrderItem) -> Dict:
    # OrderItem ORM 객체를 API 응답용 딕셔너리로 변환합니다.
    return {
        "menu_id": item.menu_id,
        "name": item.name,
        "temperature": item.temperature,
        "quantity": item.quantity,
        "price": item.price,
        "subtotal": item.subtotal,
        "option_note": item.option_note or "",
    }


def cart_items(order: Order) -> List[Dict]:
    # 주문(장바구니)에 담긴 항목 목록을 딕셔너리 리스트로 변환합니다.
    return [order_item_to_dict(item) for item in order.items]


def cart_total(order: Order) -> int:
    # 주문(장바구니) 총액을 계산합니다.
    return sum(item.subtotal for item in order.items)


# ---------------------- 장바구니 담기/조회/비우기 ----------------------

def add_to_cart(
    db: Session,
    user: Optional[User],
    menu_id: int,
    temperature: str,
    quantity: int,
    option_note: str = "",
) -> Dict:
    # 장바구니에 메뉴를 추가합니다.
    menu = get_menu(db, menu_id)
    if menu is None:
        return {"ok": False, "message": "해당 메뉴를 찾을 수 없습니다."}

    # 선택한 온도가 메뉴 옵션에 없으면 가능한 첫 번째 온도로 변경합니다.
    if temperature not in menu.temperature:
        temperature = menu.temperature[0]

    order = get_or_create_cart(db, user)
    item = OrderItem(
        order_id=order.id,
        menu_id=menu.id,
        name=menu.name,
        temperature=temperature,
        quantity=quantity,
        price=menu.price,
        subtotal=menu.price * quantity,
        option_note=option_note,
    )
    db.add(item)
    db.commit()
    db.refresh(order)

    return {
        "ok": True,
        "item": order_item_to_dict(item),
        "cart": cart_items(order),
        "total": cart_total(order),
    }


def get_cart(db: Session, user: Optional[User]) -> Dict:
    # 현재 장바구니 목록과 총액을 반환합니다.
    order = get_or_create_cart(db, user)
    return {"cart": cart_items(order), "total": cart_total(order)}


def clear_cart(db: Session, user: Optional[User]) -> Dict:
    # 장바구니에 담긴 항목을 모두 삭제합니다.
    order = get_or_create_cart(db, user)
    for item in list(order.items):
        db.delete(item)
    db.commit()
    db.refresh(order)
    return {"ok": True, "cart": cart_items(order), "total": cart_total(order)}


# ---------------------- 결제(Payment) 처리 ----------------------

def checkout(db: Session, user: Optional[User], method: str = "demo") -> Dict:
    # 장바구니를 결제 완료 상태로 전환하고 Payment 레코드를 생성합니다.
    order = get_or_create_cart(db, user)
    if not order.items:
        return {"ok": False, "message": "장바구니가 비어 있습니다."}

    total = cart_total(order)
    order.status = "paid"  # 주문 상태를 결제 완료로 변경합니다.

    payment = Payment(order_id=order.id, amount=total, method=method, status="completed")
    db.add(payment)
    db.commit()
    db.refresh(order)

    return {
        "ok": True,
        "message": "데모 결제 페이지로 이동할 수 있습니다.",
        "cart": cart_items(order),
        "total": total,
        "order_id": order.id,
    }


def get_order_history(db: Session, user: User) -> List[Order]:
    # 로그인한 회원의 결제 완료된 주문 내역을 최신순으로 조회합니다. (마이페이지 등에서 활용 가능)
    return (
        db.query(Order)
        .filter(Order.user_id == user.id, Order.status == "paid")
        .order_by(Order.created_at.desc())
        .all()
    )
