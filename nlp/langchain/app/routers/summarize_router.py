from fastapi import APIRouter, File, UploadFile, HTTPException

# APIRouter : 엔드포인트(라우트)를 별도의 모듈로 분리하여 관리하기 위한 클래스
# File : multipart/form-data 형식으로 전송된 파일을 입력값으로 받기 위한 클래스
# UploadFile : 업로드된 파일을 효율적으로 다루기 위한 클래스
#              (파일 스트리밍, 파일명, Content-Type 등의 메타데이터 제공)

from fastapi.responses import HTMLResponse

# HTML 형식의 응답을 반환할 때 사용하는 Response 클래스

from app.core.config import settings
from app.services.pdf_service import save_upload_to_temp, load_pdf_documents
from app.services.summarize_service import summarize_documents


router = APIRouter(
    # 이 라우터의 모든 URL 앞에 "/api"를 자동으로 붙인다.
    # 예) @router.get("/") → /api/
    #     @router.post("/summarize") → /api/summarize
    prefix="/api",

    # Swagger(OpenAPI) 문서에서 "summarize" 그룹으로 표시
    tags=["summarize"],
)


@router.get("/", response_class=HTMLResponse)
def home():
    """
    테스트용 파일 업로드 페이지를 반환하는 엔드포인트.

    response_class=HTMLResponse를 지정하면
    반환값을 HTML 응답으로 클라이언트에게 전송한다.
    """
    return """
    <!DOCTYPE html>
        <body>
            <h2>PDF Summarizer</h2>
            <form method="POST" action="/api/summarize" enctype="multipart/form-data">
                <input type="file" name="file" accept="application/pdf" />
                <button type="submit">Upload & Summarize</button>
            </form>
        </body>
    </html>
    """


@router.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    """
    POST /api/summarize 요청을 처리하는 엔드포인트.

    브라우저에서 PDF 파일을 업로드하면 다음 순서로 처리한다.

    1. 파일 형식 및 용량 검사
    2. 임시 파일로 저장
    3. PDF에서 텍스트 추출
    4. AI를 이용해 내용 요약
    5. 결과를 클라이언트에 반환
    """

    if file.content_type not in ("application/pdf", "application/x-pdf"):
        raise HTTPException(status_code=400, detail="pdf 파일만 업로드할 수 있습니다.")

    data = await file.read()
    if len(data) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="파일은 최대 20MB까지 전송할 수 있습니다.")

    temp_path = save_upload_to_temp(data)
    try:
        docs, page_count = load_pdf_documents(temp_path)
        if page_count == 0:
            raise HTTPException(status_code=400, detail="pdf에서 텍스트를 추출하지 못했습니다.")

        summary = summarize_documents(docs)
        return {
            "file_name": file.filename,
            "pages": page_count,
            "summary": summary,
        }
    except HTTPException:
        # 발생한 HTTPException을 그대로 다시 발생시켜
        # FastAPI가 클라이언트에게 해당 오류를 응답하도록 한다.
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 처리중 오류 발생: {str(e)}")