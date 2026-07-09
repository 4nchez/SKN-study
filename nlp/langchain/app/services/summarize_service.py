from typing import List

from langchain.chains.summarize import load_summarize_chain
# LLM과 요약 전략(map_reduce, refine 등)을 조합한 문서 요약 체인을 생성하는 함수

from langchain_openai import ChatOpenAI
# LangChain에서 OpenAI Chat 모델을 사용하기 위한 래퍼 클래스
# 내부적으로 OpenAI API를 호출하며 LangChain의 체인, 에이전트, 도구와 연동된다.

from langchain_text_splitters import RecursiveCharacterTextSplitter
# 긴 문서를 여러 개의 작은 청크(chunk)로 분할하는 클래스
# 문단 → 문장 → 문자 순으로 분할하여 가능한 한 문맥을 유지한다.

from langchain_core.documents import Document

from langchain.prompts import PromptTemplate
# 한국어 요약 프롬프트를 작성하기 위해 사용

from app.core.config import settings


def summarize_documents(docs: List[Document]) -> str:
    """
    긴 문서를 안전하게 요약한다.

    처리 순서
    1. 문서를 여러 개의 청크(chunk)로 분할한다.
    2. map_reduce 방식으로 각 청크를 요약한다.
    3. 부분 요약을 다시 종합하여 최종 요약을 생성한다.
    """

    # 1. 문서를 청크 단위로 분할
    # LLM은 한 번에 처리할 수 있는 토큰 수에 제한이 있다.
    # 따라서 문서 전체를 한 번에 입력하면 오류가 발생하거나
    # 요약 품질이 떨어질 수 있으므로 적절한 크기로 분할한다.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,     # 청크 하나의 최대 문자 수
        chunk_overlap=150,   # 인접한 청크가 공유하는 문자 수
    )

    split_docs = splitter.split_documents(docs)

    # 2. OpenAI Chat 모델 생성
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,          # 사용할 모델 이름
        api_key=settings.OPENAI_API_KEY,      # .env에서 읽어온 OpenAI API Key
        temperature=0.2,                      # 낮을수록 일관되고 사실 중심의 결과를 생성
    )

    # ---------------- 한국어 요약 프롬프트 ----------------

    MAP_PROMPT = PromptTemplate(
        template="""
다음 문서는 PDF의 일부 내용이다.
이 내용을 한국어로 간결하게 요약하시오.

문서 내용:
{text}

한국어 요약:
""",
        input_variables=["text"],
    )

    REDUCE_PROMPT = PromptTemplate(
        template="""
다음은 문서의 부분 요약들이다.
이 요약들을 종합하여 전체 문서를 한국어로 정리하시오.

부분 요약들:
{text}

최종 한국어 요약:
""",
        input_variables=["text"],
    )

    # ----------------------------------------------------

    # 3. map_reduce 방식의 요약 체인 생성
    chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",

        # 한국어로 요약을 생성하기 위한 프롬프트
        map_prompt=MAP_PROMPT,
        combine_prompt=REDUCE_PROMPT,
    )

    # map_reduce 처리 과정
    #
    # 1. Map 단계
    #    각 Document(청크)를 개별적으로 요약한다.
    #
    # 2. Reduce 단계
    #    부분 요약들을 다시 하나로 합쳐
    #    최종 문서 요약을 생성한다.

    # 요약 체인 실행
    # 입력은 딕셔너리 형태로 전달한다.
    result = chain.invoke({"input_documents": split_docs})

    # 생성된 최종 요약을 반환한다.
    # strip()은 앞뒤 공백과 줄바꿈을 제거한다.
    return result.get("output_text", "").strip()