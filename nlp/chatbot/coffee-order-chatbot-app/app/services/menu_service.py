# app/services/menu_service.py
# 메뉴(Menu) 관련 CRUD와 추천 검색 로직을 모아둔 서비스 파일입니다.

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.models import Menu
from app.menu_data import COFFEE_MENU


def seed_menus(db: Session) -> None:
    # 앱 최초 실행 시 menus 테이블이 비어 있으면 menu_data.py의 데이터를 한 번만 채워 넣습니다.
    if db.query(Menu).count() > 0:  # 이미 데이터가 있으면 다시 넣지 않습니다.
        return
    for item in COFFEE_MENU:  # 시드 데이터를 순회하며 Menu 레코드를 생성합니다.
        db.add(
            Menu(
                name=item["name"],
                category=item["category"],
                temperature=item["temperature"],
                taste_tags=item["taste_tags"],
                description=item["description"],
                price=item["price"],
            )
        )
    db.commit()  # 시드 데이터를 DB에 반영합니다.


def get_all_menus(db: Session) -> List[Menu]:
    # 전체 메뉴 목록을 조회합니다.
    return db.query(Menu).order_by(Menu.id).all()


def get_menu(db: Session, menu_id: int) -> Optional[Menu]:
    # 메뉴 ID로 단일 메뉴를 조회합니다.
    return db.query(Menu).filter(Menu.id == menu_id).first()


def create_menu(db: Session, data: Dict) -> Menu:
    # 새 메뉴를 추가합니다. (관리자용 CRUD)
    menu = Menu(**data)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def update_menu(db: Session, menu_id: int, data: Dict) -> Optional[Menu]:
    # 기존 메뉴 정보를 수정합니다. (관리자용 CRUD)
    menu = get_menu(db, menu_id)
    if menu is None:
        return None
    for key, value in data.items():
        setattr(menu, key, value)
    db.commit()
    db.refresh(menu)
    return menu


def delete_menu(db: Session, menu_id: int) -> bool:
    # 메뉴를 삭제합니다. (관리자용 CRUD)
    menu = get_menu(db, menu_id)
    if menu is None:
        return False
    db.delete(menu)
    db.commit()
    return True


def find_menus(db: Session, message: str, top_k: int = 3) -> List[Menu]:
    # 메뉴 이름 또는 맛 태그를 기준으로 사용자의 메시지와 어울리는 메뉴를 점수화하여 검색합니다.
    menus = get_all_menus(db)
    normalized = message.lower()
    scored: List[tuple] = []
    for menu in menus:
        score = 0
        # 메뉴 이름이 사용자 메시지에 포함되면 높은 점수를 부여합니다.
        if menu.name.lower().replace(" ", "") in normalized.replace(" ", ""):
            score += 5
        # 맛 태그가 사용자 메시지에 포함되면 점수를 부여합니다.
        for tag in menu.taste_tags:
            if tag in message:
                score += 2
        # 커피라는 단어가 있고 커피 카테고리이면 점수를 약간 부여합니다.
        if "커피" in message and menu.category == "coffee":
            score += 1
        if score > 0:
            scored.append((menu, score))
    # 결과가 없으면 기본 추천 메뉴를 사용합니다.
    if not scored:
        scored = [(menu, 1) for menu in menus[:top_k]]
    # 점수가 높은 순서대로 정렬합니다.
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return [menu for menu, _ in scored[:top_k]]


def menu_to_dict(menu: Menu) -> Dict:
    # Menu ORM 객체를 API 응답용 딕셔너리로 변환합니다.
    return {
        "id": menu.id,
        "name": menu.name,
        "category": menu.category,
        "temperature": menu.temperature,
        "taste_tags": menu.taste_tags,
        "description": menu.description,
        "price": menu.price,
    }
