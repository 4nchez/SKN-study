"""
학습된 모델을 불러와 영어 <-> 한국어 번역을 수행하는 파일입니다.
"""

import re
import torch
from src.config import (
    MODEL_PATH, META_PATH, DATA_PATH,
    EMBED_SIZE, HIDDEN_SIZE, MAX_OUTPUT_LEN,
    SOS_TOKEN, EOS_TOKEN, UNK_TOKEN, PAD_TOKEN
)
from src.data_utils import normalize_text, encode_text
from src.model import Seq2SeqTranslator


def detect_language(text: str) -> str:
    """
    입력 문장에 한글이 포함되어 있으면 ko, 그렇지 않으면 en으로 판단합니다.
    """
    # 정규표현식으로 한글 음절이 포함되어 있는지 검사합니다.
    if re.search(r"[가-힣]", text):
        # 한글이 하나라도 있으면 한국어로 판단합니다.
        return "ko"
    else:
        # 한글이 없으면 영어로 판단합니다.
        return "en"


def build_directional_source(text: str, source_lang: str) -> str:
    """
    입력 언어에 따라 번역 방향 토큰을 문장 앞에 추가합니다.
    """
    if source_lang == "en":
        # 영어 입력이면 한국어 번역 방향 토큰을 문장 앞에 추가합니다.
        return "<EN2KO>" + normalize_text(text)
    else:
        # 한국어 입력이면 영어 번역 방향 토큰을 문장 앞에 추가합니다.
        return "<KO2EN>" + normalize_text(text)


def load_model():
    """
    저장된 모델 가중치와 문자 사전을 불러옵니다.
    """
    # 모델 메타 파일이나 가중치 파일이 없으면 먼저 학습을 수행하도록 안내합니다.
    if not MODEL_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("학습된 모델 파일이 없습니다. 먼저 python -m src.train 명령을 실행하세요.")

    # CPU 환경에서도 안전하게 불러오기 위해 map_location을 CPU로 지정합니다.
    meta = torch.load(META_PATH, map_location=torch.device("cpu"))

    # 저장된 문자 → 인덱스 사전을 가져옵니다.
    char2idx = meta["char2idx"]

    # 저장된 인덱스 → 문자 사전을 가져옵니다.
    idx2char = meta["idx2char"]

    # 저장된 문자 사전 크기에 맞게 모델을 생성합니다.
    model = Seq2SeqTranslator(
        vocab_size=len(char2idx),
        embed_size=meta.get("embed_size", EMBED_SIZE),
        hidden_size=meta.get("hidden_size", HIDDEN_SIZE),
    )

    # 학습된 가중치를 모델에 불러옵니다.
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))

    # 추론 시에는 dropout이나 batch normalization이 학습 모드로 동작하지 않도록 모델을 평가 모드로 전환합니다.
    model.eval()

    # 모델과 문자 사전을 반환합니다.
    return model, char2idx, idx2char


def load_exact_dictionary():
    """
    학습 데이터에 있는 문장은 정확한 번역을 우선하기 위해 딕셔너리로 읽습니다.
    """
    # pandas 의존성을 줄이기 위해 csv 모듈을 사용합니다.
    import csv

    # 정확한 번역을 저장할 딕셔너리를 생성합니다.
    mapping = {}

    # CSV 파일을 UTF-8 인코딩으로 엽니다.
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        # DictReader는 첫 번째 행의 en, ko 컬럼명을 기준으로 각 행을 읽습니다.
        reader = csv.DictReader(f)

        # 각 번역 쌍을 순회합니다.
        for row in reader:
            # 영어 문장을 정규화합니다.
            en = normalize_text(row["en"])
            # 한국어 문장을 정규화합니다.
            ko = normalize_text(row["ko"])
            # 영어 -> 한국어 번역을 등록합니다.
            mapping[("en", en)] = ko
            # 한국어 -> 영어 번역을 등록합니다.
            mapping[("ko", ko)] = en

    # 완성된 번역 사전을 반환합니다.
    return mapping


def translate(text: str, model=None, char2idx=None, idx2char=None) -> str:
    """
    입력 문장을 자동으로 방향 판별하여 번역합니다.
    """
    # 빈 문자열이면 안내 문구를 반환합니다.
    if not text or not text.strip():
        return "번역할 문장을 입력하세요."

    # 입력 언어를 자동으로 판별합니다.
    source_lang = detect_language(text)

    # 학습 데이터에 있는 문장을 우선 번역하기 위해 정확 매칭 사전을 불러옵니다.
    exact_dict = load_exact_dictionary()

    # 정규화된 입력 문장으로 정확 매칭을 시도합니다.
    exact_key = (source_lang, normalize_text(text))

    # 정확히 일치하는 문장이 있으면 즉시 반환합니다.
    if exact_key in exact_dict:
        return exact_dict[exact_key]

    # 모델이 전달되지 않았다면 저장된 모델과 문자 사전을 불러옵니다.
    if model is None or char2idx is None or idx2char is None:
        model, char2idx, idx2char = load_model()

    # 번역 방향 토큰을 포함한 입력 문자열을 생성합니다.
    source_text = build_directional_source(text, source_lang)

    # 입력 문장을 문자 인덱스 리스트로 변환합니다.
    source_idx = encode_text(source_text, char2idx, add_eos=True)

    # 모델 입력 형태 [배치, 시퀀스 길이]에 맞게 배치 차원을 추가합니다.
    source_tensor = torch.tensor(source_idx, dtype=torch.long).unsqueeze(0)

    # 추론 시에는 기울기를 계산하지 않습니다.
    with torch.no_grad():
        # 입력 문장을 인코더의 은닉 상태로 변환합니다.
        hidden = model.encoder(source_tensor)
        # 디코더의 첫 입력은 SOS 토큰입니다.
        decoder_input = torch.tensor([[char2idx[SOS_TOKEN]]], dtype=torch.long)
        # 생성된 문자를 저장할 리스트입니다.
        result_chars = []

        # 최대 출력 길이까지 한 글자씩 생성합니다.
        for _ in range(MAX_OUTPUT_LEN):
            # 현재 은닉 상태와 이전 문자를 이용하여 다음 문자의 점수를 계산합니다.
            logits, hidden = model.decoder(decoder_input, hidden)

            # 가장 높은 점수를 가진 문자 인덱스를 선택합니다.
            next_id = int(torch.argmax(logits[:, -1, :], dim=-1).item())
            # 선택한 인덱스를 문자로 변환합니다.
            next_char = idx2char.get(next_id, UNK_TOKEN)

            # EOS 토큰이 생성되면 문장 생성을 종료합니다.
            if next_char == EOS_TOKEN:
                break

            # 특수 토큰은 결과 문자열에 포함하지 않습니다.
            if next_char not in {PAD_TOKEN, SOS_TOKEN, UNK_TOKEN}:
                result_chars.append(next_char)

            # 다음 시점의 입력으로 방금 예측한 문자를 사용합니다.
            decoder_input = torch.tensor([[next_id]], dtype=torch.long)

    # 생성된 문자들을 하나의 문자열로 합칩니다.
    result = "".join(result_chars).strip()

    if not result:
        # 아무 문자도 생성하지 못한 경우 안내 문구를 반환합니다.
        return "변역 결과를 생성하지 못했습니다. 학습 데이터를 늘리거나 모델의 하이퍼파라미터를 변경해 주세요."
    else:
        # 최종 번역 결과를 반환합니다.
        return result