"""14_filter_search_genai.py 문제 5 — 메타데이터 필터링"""  # 이 파일은 특정 문서 안에서만 검색하는 방법을 보여 줍니다.

from pathlib import Path  # 인덱스 파일 존재 여부를 확인하기 위해 Path를 사용합니다.

from langchain_community.vectorstores import FAISS  # FAISS 인덱스 생성, 로드, 증분 추가에 사용합니다.


from common import EXERCISE_FAISS_DIR, get_embeddings, load_and_chunk, print_documents  # 공통 경로와 유틸리티 함수를 불러옵니다.

FILES = ["멤버십정책.pdf", "환불교환정책.pdf"]  # FAISS 필터 실습에 사용할 여러 문서 목록입니다.


def load_faiss_index() -> FAISS:  # 디스크에 저장된 FAISS 인덱스를 메모리로 로드하는 함수입니다.
    index_file = Path(EXERCISE_FAISS_DIR) / "index.faiss"  # FAISS 핵심 인덱스 파일 경로를 만듭니다.
    if not index_file.exists():  # 인덱스 파일이 없으면 먼저 build_index를 실행해야 합니다.
        raise FileNotFoundError("FAISS 인덱스가 없습니다. 먼저 src/10_build_index_genai.py를 실행하세요.")  # 실행 순서를 안내하는 오류를 발생시킵니다.
    emb = get_embeddings()  # 검색 질문 임베딩에 사용할 같은 임베딩 객체를 생성합니다.
    return FAISS.load_local(str(EXERCISE_FAISS_DIR), emb, allow_dangerous_deserialization=True)  # 저장된 벡터를 재임베딩 없이 로드합니다.


def search_in_doc(vs: FAISS, query: str, source: str | None = None, k: int = 3):  # 특정 문서 필터를 적용할 수 있는 검색 함수입니다.
    metadata_filter = {"source": source} if source else None  # source가 있으면 해당 파일명만 검색하도록 필터를 만듭니다.
    return vs.similarity_search(query, k=k, filter=metadata_filter)  # 필터 조건에 맞는 청크 안에서 유사도 검색을 수행합니다.


def main() -> None:  # PyCharm 실행 진입점입니다.
    vs = load_faiss_index()  # FAISS 인덱스를 생성하고 저장합니다.
    query = "VIP 등급 혜택은?"  # 멤버십 문서에서 답해야 하는 질문을 준비합니다.
    all_results = search_in_doc(vs, query, source=None, k=3)  # 필터 없이 전체 문서에서 검색합니다.
    filtered_results = search_in_doc(vs, query, source="멤버십정책.pdf", k=3)  # 멤버십정책 문서 안에서만 검색합니다.
    print_documents("필터 없음 - 전체 문서 검색", all_results)  # 전체 검색 결과를 출력합니다.
    print_documents("필터 적용 - 멤버십정책.pdf 안에서만 검색", filtered_results)  # 필터 검색 결과를 출력합니다.
    print("필터를 사용하면 관련 없는 문서가 섞이는 노이즈를 줄일 수 있습니다.")  # 필터링의 효과를 설명합니다.


if __name__ == "__main__":  # 직접 실행 여부를 확인합니다.
    main()  # FAISS 필터 검색 실습을 실행합니다.
