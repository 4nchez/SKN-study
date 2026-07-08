"""13_incremental_update_genai.py 문제 4 — 인덱스 증분 업데이트"""  # 이 파일은 add_documents로 새 문서만 추가하는 방법을 보여 줍니다.

import shutil  # 기존 인덱스 폴더를 깨끗하게 초기화하기 위해 사용합니다.
from pathlib import Path  # 인덱스 파일 존재 여부를 확인하기 위해 Path를 사용합니다.

from langchain_community.vectorstores import FAISS  # FAISS 인덱스 생성, 로드, 증분 추가에 사용합니다.

from common import EXERCISE_FAISS_DIR, get_embeddings, load_and_chunk, print_documents  # 공통 경로와 유틸리티 함수를 불러옵니다.

NEW_FILE = ["환불교환정책.pdf"]  # 나중에 증분으로 추가할 새 문서입니다.


def reset_exercise_faiss_dir() -> None:  # 실습 결과를 매번 동일하게 만들기 위해 FAISS 폴더를 초기화합니다.
    if EXERCISE_FAISS_DIR.exists():  # 기존 FAISS 인덱스 폴더가 존재하는지 확인합니다.
        shutil.rmtree(EXERCISE_FAISS_DIR)  # 기존 인덱스 폴더를 삭제합니다.
    EXERCISE_FAISS_DIR.mkdir(parents=True, exist_ok=True)  # 새 인덱스를 저장할 폴더를 다시 생성합니다.


def load_faiss_index() -> FAISS:  # 디스크에 저장된 FAISS 인덱스를 메모리로 로드하는 함수입니다.
    index_file = Path(EXERCISE_FAISS_DIR) / "index.faiss"  # FAISS 핵심 인덱스 파일 경로를 만듭니다.
    if not index_file.exists():  # 인덱스 파일이 없으면 먼저 build_index를 실행해야 합니다.
        raise FileNotFoundError("FAISS 인덱스가 없습니다. 먼저 src/10_build_index_genai.py를 실행하세요.")  # 실행 순서를 안내하는 오류를 발생시킵니다.
    emb = get_embeddings()  # 검색 질문 임베딩에 사용할 같은 임베딩 객체를 생성합니다.
    return FAISS.load_local(str(EXERCISE_FAISS_DIR), emb, allow_dangerous_deserialization=True)  # 저장된 벡터를 재임베딩 없이 로드합니다.


def main() -> None:  # PyCharm 실행 진입점입니다.
    # reset_exercise_faiss_dir()  # 이전 실행 결과를 삭제하고 새 실습 상태를 만듭니다.
    vs = load_faiss_index()  # 저장된 FAISS 인덱스를 로드합니다.
    emb = get_embeddings()  # 임베딩 객체를 생성합니다.
    query = "환불은 며칠 걸리나요?"  # 증분 전후 비교에 사용할 질문입니다.
    before = vs.similarity_search(query, k=2)  # 멤버십 문서 추가 전 검색을 수행합니다.
    print_documents("증분 전 검색 - 맴버쉽정책만 있는 상태", before)  # 추가 전 검색 결과를 출력합니다.
    vs2 = FAISS.load_local(str(EXERCISE_FAISS_DIR), emb, allow_dangerous_deserialization=True)  # 저장된 기존 인덱스를 로드합니다.
    new_chunks = load_and_chunk(NEW_FILE)  # 새로 추가할 환불정책 문서를 청킹합니다.
    vs2.add_documents(new_chunks)  # 새 청크만 임베딩하여 기존 인덱스에 덧붙입니다.
    vs2.save_local(str(EXERCISE_FAISS_DIR))  # 증분 추가된 인덱스를 다시 저장합니다.
    after = vs2.similarity_search(query, k=2)  # 환불정책 문서 추가 후 같은 질문을 검색합니다.
    keep = vs2.similarity_search("VIP 등급 조건은?", k=2)  # 기존 환불 지식이 유지되는지 확인합니다.
    print_documents("증분 후 검색 - 환불정책 추가 상태", after)  # 추가 후 검색 결과를 출력합니다.
    print_documents("기존 지식 유지 확인 - 환불 질문", keep)  # 기존 지식 검색 결과를 출력합니다.


if __name__ == "__main__":  # 직접 실행된 경우를 확인합니다.
    main()  # 증분 업데이트 실습을 실행합니다.
