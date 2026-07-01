"""
PyTorch 기반 문자 단위 Seq2Seq 번역 모델을 정의하는 파일입니다.
"""

import torch.nn as nn


class Encoder(nn.Module):
    """
    입력 문장을 읽어 문장 전체의 의미를 은닉 상태로 압축하는 인코더입니다.
    """

    def __init__(self, vocab_size, embed_size, hidden_size):
        # 부모 클래스(nn.Module)를 초기화합니다.
        super().__init__()

        # 문자 인덱스를 밀집 벡터(임베딩)로 변환하는 계층입니다.
        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=0)

        # 순차 데이터를 처리하는 GRU 계층입니다.
        # batch_first=True는 입력 텐서의 형태를 (배치, 시간, 특성)으로 사용함을 의미합니다.
        self.gru = nn.GRU(
            input_size=embed_size,
            hidden_size=hidden_size,
            batch_first=True,
        )

    def forward(self, source_idx):
        # 입력 문장의 문자 인덱스를 임베딩 벡터 시퀀스로 변환합니다.
        embedded = self.embedding(source_idx)

        # 입력 문장을 순서대로 처리하여 마지막 은닉 상태를 생성합니다.
        output, hidden = self.gru(embedded)

        # 디코더는 마지막 은닉 상태를 초기 상태로 사용하므로 hidden을 반환합니다.
        return hidden


class Decoder(nn.Module):
    """
    인코더의 은닉 상태를 바탕으로 번역 문장을 한 글자씩 생성하는 디코더입니다.
    """

    def __init__(self, vocab_size, embed_size, hidden_size):
        # 부모 클래스(nn.Module)를 초기화합니다.
        super().__init__()

        # 출력 문자 인덱스를 임베딩 벡터로 변환하는 계층입니다.
        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=0)

        # 이전 입력 문자와 이전 은닉 상태를 이용하여 새로운 은닉 상태를 계산하는 GRU 계층입니다.
        self.gru = nn.GRU(
            input_size=embed_size,
            hidden_size=hidden_size,
            batch_first=True,
        )

        # GRU의 출력 벡터를 문자 사전 크기의 점수(logits)로 변환하는 선형 계층입니다.
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, decoder_input_idx, hidden):
        # 디코더 입력 문자 인덱스를 임베딩 벡터로 변환합니다.
        embedded = self.embedding(decoder_input_idx)

        # 인코더에서 전달받은 은닉 상태를 초기 상태로 사용하여 출력을 계산합니다.
        output, hidden = self.gru(embedded, hidden)

        # 각 시점의 출력 벡터를 문자별 예측 점수(logits)로 변환합니다.
        logits = self.fc(output)

        # 문자별 예측 점수와 마지막 은닉 상태를 반환합니다.
        return logits, hidden


class Seq2SeqTranslator(nn.Module):
    """
    인코더와 디코더를 하나로 묶은 Seq2Seq 번역 모델입니다.
    """

    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()

        # 입력 문장을 의미 벡터로 압축하는 인코더를 생성합니다.
        self.encoder = Encoder(vocab_size, embed_size, hidden_size)

        # 의미 벡터를 이용하여 번역 문장을 생성하는 디코더를 생성합니다.
        self.decoder = Decoder(vocab_size, embed_size, hidden_size)

    def forward(self, source_idx, decoder_input_idx):
        # 입력 문장을 인코더에 전달하여 마지막 은닉 상태를 얻습니다.
        hidden = self.encoder(source_idx)

        # 디코더가 이전 정답 문자들을 입력으로 받아 다음 문자의 점수를 예측합니다.
        logits, _ = self.decoder(decoder_input_idx, hidden)

        # 각 문자에 대한 예측 점수(logits)를 반환합니다.
        return logits