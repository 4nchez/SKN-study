# FastAPI의 핵심 클래스 임포트
# FastAPI는 Python 기반의 고성능 웹 API 프레임워크이다.
from fastapi import FastAPI

from app.routers.summarize_router import router as summarize_router
# PDF 요약 기능을 담당하는 라우터
# 이 라우터에는 /api/, /api/summarize 등의 엔드포인트가 정의되어 있다.


# FastAPI 애플리케이션 객체 생성
app = FastAPI(title="PDF Summarizer (LangChain + FastAPI)")

# title
#   - Swagger UI와 ReDoc 같은 자동 생성 API 문서에 표시되는 서비스 이름
#
# app 객체
#   - 애플리케이션의 중심 객체
#   - 라우터 등록, 미들웨어 관리, 요청(Request) 처리,
#     응답(Response) 생성 등의 전체 흐름을 관리한다.


# 라우터 등록
app.include_router(summarize_router)

# 외부 모듈에 정의된 APIRouter를
# 현재 FastAPI 애플리케이션에 등록한다.
# 등록된 라우터의 모든 엔드포인트를
# 애플리케이션에서 사용할 수 있게 된다.