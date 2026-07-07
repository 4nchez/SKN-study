# app/security.py
# 비밀번호 해싱, 비밀번호 검증, JWT 토큰 생성/해석 기능을 모아둔 보안 유틸 파일입니다.

import os  # .env에서 보안 설정값을 읽기 위해 사용합니다.
from datetime import datetime, timedelta, timezone  # JWT 만료 시간을 계산하기 위해 사용합니다.
from typing import Optional  # 선택적 로그인(비로그인 허용) 타입 힌트에 사용합니다.
from dotenv import load_dotenv  # .env 파일을 환경변수로 불러옵니다.
from fastapi import Depends, HTTPException, status  # 인증 실패 응답과 의존성 주입에 사용합니다.
from fastapi.security import OAuth2PasswordBearer  # Swagger Authorize 버튼과 Bearer 토큰 인증에 사용합니다.
from jose import JWTError, jwt  # JWT 토큰 인코딩과 디코딩에 사용합니다.
from passlib.context import CryptContext  # 안전한 비밀번호 해싱을 위해 사용합니다.
from sqlalchemy.orm import Session  # DB 세션 타입 힌트에 사용합니다.
from app.database import get_db  # DB 세션 의존성 함수입니다.
from app.models.models import User  # 현재 로그인 사용자를 조회하기 위해 User 모델을 가져옵니다.

load_dotenv()  # .env 파일 값을 환경변수로 등록합니다.

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")  # JWT 서명에 사용할 비밀키입니다.
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # JWT 서명 알고리즘입니다.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))  # 토큰 만료 시간입니다.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # bcrypt 방식으로 비밀번호를 해싱합니다.

# 로그인이 필수인 API에서 사용하는 스킴입니다. 토큰이 없으면 자동으로 401을 발생시킵니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Swagger에서 로그인 API를 토큰 발급 URL로 인식하게 합니다.

# 로그인이 선택인 API(비회원도 이용 가능한 챗봇/장바구니 등)에서 사용하는 스킴입니다.
# auto_error=False로 설정하면 토큰이 없어도 예외를 던지지 않고 None을 반환합니다.
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    # 사용자가 입력한 원문 비밀번호를 DB 저장용 해시 문자열로 변환합니다.
    return pwd_context.hash(password)  # bcrypt 해시 결과를 반환합니다.


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 로그인 시 입력한 원문 비밀번호와 DB에 저장된 해시 비밀번호가 일치하는지 검증합니다.
    return pwd_context.verify(plain_password, hashed_password)  # 일치하면 True, 아니면 False를 반환합니다.


def create_access_token(data: dict) -> str:
    # JWT 액세스 토큰을 생성합니다.
    to_encode = data.copy()  # 원본 데이터가 변경되지 않도록 복사합니다.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # 만료 시각을 계산합니다.
    to_encode.update({"exp": expire})  # JWT payload에 만료 시각을 추가합니다.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # payload를 서명하여 JWT 문자열로 변환합니다.
    return encoded_jwt  # 완성된 JWT 토큰을 반환합니다.


def _decode_username(token: str) -> Optional[str]:
    # JWT 토큰을 디코딩하여 username(sub)을 꺼내는 내부 공용 함수입니다.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # 토큰을 검증하고 payload를 추출합니다.
        return payload.get("sub")  # payload에서 사용자 아이디를 꺼내 반환합니다.
    except JWTError:  # 토큰 위조, 만료, 형식 오류가 발생한 경우입니다.
        return None  # 유효하지 않은 토큰이면 None을 반환합니다.


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # 로그인이 반드시 필요한 API에서 사용하는 의존성 함수입니다. 실패 시 401 오류를 발생시킵니다.
    credentials_exception = HTTPException(  # 토큰 검증 실패 시 반환할 401 오류 객체입니다.
        status_code=status.HTTP_401_UNAUTHORIZED,  # 인증 실패 HTTP 상태 코드입니다.
        detail="인증 정보가 올바르지 않습니다.",  # 클라이언트에 전달할 오류 메시지입니다.
        headers={"WWW-Authenticate": "Bearer"},  # Bearer 인증 실패임을 나타냅니다.
    )
    username = _decode_username(token)  # 토큰에서 username을 추출합니다.
    if username is None:  # 토큰이 유효하지 않으면 인증 실패입니다.
        raise credentials_exception  # 401 오류를 발생시킵니다.

    user = db.query(User).filter(User.username == username).first()  # 토큰의 username으로 DB에서 회원을 조회합니다.
    if user is None:  # DB에 해당 사용자가 없으면 인증 실패입니다.
        raise credentials_exception  # 401 오류를 발생시킵니다.
    return user  # 인증된 현재 사용자 객체를 반환합니다.


def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)
) -> Optional[User]:
    # 로그인이 선택인 API(챗봇, 장바구니 등)에서 사용하는 의존성 함수입니다.
    # 로그인 토큰이 있으면 해당 회원 객체를, 없거나 유효하지 않으면 None을 반환합니다(비회원 이용 허용).
    if not token:  # Authorization 헤더 자체가 없는 경우입니다.
        return None  # 비회원으로 간주합니다.
    username = _decode_username(token)  # 토큰에서 username을 추출합니다.
    if username is None:  # 토큰이 유효하지 않은 경우입니다.
        return None  # 비회원으로 간주합니다.
    return db.query(User).filter(User.username == username).first()  # 회원 조회 결과를 반환합니다(없으면 None).
