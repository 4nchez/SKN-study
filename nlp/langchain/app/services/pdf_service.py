import os
# 파이썬 표준 라이브러리.
# 운영체제 관련 기능을 제공하며, 여기서는 파일 디스크립터(fd)를 닫기 위해 사용한다.

import tempfile
# 파이썬 표준 라이브러리.
# 임시 파일이나 임시 디렉터리를 생성하기 위한 모듈이다.
# Windows와 Linux 등 다양한 운영체제에서 사용할 수 있다.

from typing import List, Tuple
# 함수의 매개변수와 반환 타입을 명시하기 위한 타입 힌트 모듈
# List : 리스트 타입
# Tuple : 튜플 타입

from langchain_community.document_loaders import PyPDFLoader
# PDF 파일에서 텍스트를 추출하여
# LangChain의 Document 객체 목록으로 변환하는 클래스

from langchain_core.documents import Document
# LangChain에서 사용하는 문서 표준 객체
# page_content : 문서 본문
# metadata : 페이지 번호, 파일 경로 등의 부가 정보


def save_upload_to_temp(pdf_bytes: bytes, suffix: str = ".pdf") -> str:
    """
    업로드된 PDF 바이너리 데이터를 임시 파일로 저장하고,
    생성된 파일의 경로를 반환한다.

    tempfile을 사용하므로 Windows와 Linux에서 모두 안전하게 동작한다.
    """

    fd, path = tempfile.mkstemp(suffix=suffix)

    # tempfile.mkstemp()
    #   - (fd, path)를 반환한다.
    #   - fd   : 운영체제가 생성한 파일 디스크립터(정수)
    #   - path : 생성된 임시 파일의 경로
    #
    # suffix=".pdf"
    #   - 생성되는 임시 파일의 확장자를 .pdf로 지정한다.

    os.close(fd)

    # mkstemp()가 열어 둔 파일 디스크립터를 닫는다.
    # Windows에서는 열린 파일을 다시 열려고 하면 "사용 중인 파일" 오류가 발생할 수 있으므로 먼저 닫아 준다.

    with open(path, "wb") as f:
        # with 문을 사용하면 블록이 종료될 때 파일이 자동으로 닫혀 리소스 누수를 방지한다.
        f.write(pdf_bytes)

    # 저장된 임시 파일의 경로 반환
    return path


def load_pdf_documents(pdf_path: str) -> Tuple[List[Document], int]:
    """
    PDF 파일을 읽어 LangChain Document 목록으로 변환한다.

    반환값:
        - Document 리스트
        - 전체 페이지 수(Document 개수)
    """

    loader = PyPDFLoader(pdf_path)

    # PyPDFLoader(pdf_path)
    #   - 지정한 PDF 파일을 읽기 위한 로더 객체를 생성한다.
    #   - 일반적으로 페이지 단위의 Document 객체를 생성한다.
    #   - LangChain 버전에 따라 지원되는 옵션이 달라질 수 있다.

    docs = loader.load()

    # loader.load()
    #   - PDF를 읽어 텍스트를 추출한다.
    #   - 각 페이지를 하나의 Document 객체로 만들어 리스트로 반환한다.

    return docs, len(docs)