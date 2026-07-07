# app/models/models.py
# MySQL 테이블과 매핑되는 SQLAlchemy ORM 모델을 정의합니다.
# User(회원) / Menu(메뉴) / Order(주문=장바구니 겸용) / OrderItem(주문 상세) / Payment(결제) 5개 테이블입니다.

from datetime import datetime  # 생성일/수정일 기본값을 만들기 위해 사용합니다.
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, JSON  # 컬럼 타입 정의에 사용합니다.
from sqlalchemy.orm import relationship  # 테이블 간 관계(ORM 조인)를 표현하기 위해 사용합니다.
from app.database import Base  # 모든 ORM 모델이 상속받는 Base 클래스를 가져옵니다.


class User(Base):
    # users 테이블: 회원 정보를 저장합니다.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # 회원 고유 번호이며 기본키입니다.
    username = Column(String(50), unique=True, index=True, nullable=False)  # 로그인 아이디이며 중복을 허용하지 않습니다.
    password_hash = Column(String(255), nullable=False)  # 원문 비밀번호가 아니라 해시된 비밀번호를 저장합니다.
    name = Column(String(50), nullable=False)  # 회원 이름을 저장합니다.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 회원 가입 시각을 UTC 기준으로 저장합니다.

    # 한 명의 회원은 여러 개의 주문(Order)을 가질 수 있습니다.
    orders = relationship("Order", back_populates="user")


class Menu(Base):
    # menus 테이블: 커피 메뉴 정보를 저장합니다. (기존 menu_data.py의 하드코딩 데이터를 대체합니다)
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)  # 메뉴 고유 번호입니다.
    name = Column(String(100), nullable=False)  # 메뉴 이름입니다.
    category = Column(String(50), nullable=False)  # 메뉴 카테고리(coffee, dessert, non_coffee 등)입니다.
    temperature = Column(JSON, nullable=False, default=list)  # 선택 가능한 온도 옵션 리스트입니다. 예: ["hot", "ice"]
    taste_tags = Column(JSON, nullable=False, default=list)  # 추천에 사용할 맛 태그 리스트입니다.
    description = Column(Text, nullable=True)  # 메뉴 설명입니다.
    price = Column(Integer, nullable=False)  # 메뉴 가격입니다.

    # 하나의 메뉴는 여러 주문 상세(OrderItem)에서 참조될 수 있습니다.
    order_items = relationship("OrderItem", back_populates="menu")


class Order(Base):
    # orders 테이블: 장바구니와 주문(결제 전/후)을 함께 표현합니다.
    # status가 "cart"이면 담고 있는 중인 장바구니, "paid"이면 결제 완료된 주문입니다.
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # 주문 고유 번호입니다.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # 주문한 회원입니다. 비회원 주문을 허용하기 위해 nullable로 둡니다.
    status = Column(String(20), nullable=False, default="cart")  # 주문 상태: cart(장바구니) / paid(결제완료) / canceled(취소)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 주문(장바구니) 생성 시각입니다.
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 마지막 변경 시각입니다.

    user = relationship("User", back_populates="orders")  # 주문한 회원 객체입니다.
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # 주문에 담긴 상세 항목들입니다.
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")  # 결제 완료 시 생성되는 결제 정보입니다.


class OrderItem(Base):
    # order_items 테이블: 하나의 주문(Order)에 담긴 개별 메뉴 항목입니다.
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)  # 주문 상세 고유 번호입니다.
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)  # 소속된 주문(장바구니) ID입니다.
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)  # 담은 메뉴 ID입니다.
    name = Column(String(100), nullable=False)  # 담을 당시의 메뉴 이름(스냅샷)입니다. 이후 메뉴명이 바뀌어도 주문내역은 유지됩니다.
    temperature = Column(String(10), nullable=False, default="ice")  # 선택한 온도(hot/ice)입니다.
    quantity = Column(Integer, nullable=False, default=1)  # 수량입니다.
    price = Column(Integer, nullable=False)  # 담을 당시의 단가(스냅샷)입니다.
    subtotal = Column(Integer, nullable=False)  # 단가 * 수량 소계입니다.
    option_note = Column(String(255), nullable=True, default="")  # 샷 추가, 시럽 추가 등 요청사항입니다.

    order = relationship("Order", back_populates="items")  # 소속 주문 객체입니다.
    menu = relationship("Menu", back_populates="order_items")  # 참조하는 메뉴 객체입니다.


class Payment(Base):
    # payments 테이블: 주문 1건당 결제 1건(1:1)을 저장합니다.
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)  # 결제 고유 번호입니다.
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)  # 결제 대상 주문 ID입니다. (1:1 관계이므로 unique)
    amount = Column(Integer, nullable=False)  # 결제 금액입니다.
    method = Column(String(30), nullable=False, default="demo")  # 결제 수단입니다. (데모 프로젝트이므로 기본값 demo)
    status = Column(String(20), nullable=False, default="completed")  # 결제 상태입니다. (completed/failed/canceled)
    paid_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 결제 완료 시각입니다.

    order = relationship("Order", back_populates="payment")  # 결제 대상 주문 객체입니다.
