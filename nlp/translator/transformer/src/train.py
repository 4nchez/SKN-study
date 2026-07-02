"""
번역 모델을 학습하고 학습된 모델을 파일로 저장하는 실행 파일입니다.
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from src.config import (
    DATA_PATH, MODEL_PATH, META_PATH,
    EMBED_SIZE, HIDDEN_SIZE, BATCH_SIZE, EPOCHS,
    LEARNING_RATE, PAD_TOKEN
)
from src.data_utils import (
    load_translation_pairs, build_vocab,
    TranslationDataset, collate_batch
)
# from src.model import Seq2SeqTranslator
from src.model import TransformerTranslator


def train_model(epochs: int=EPOCHS):
    """
    CSV 번역 데이터를 사용해서 Seq2SeqTranslator 번역 모델을 학습합니다.
    """
    # CUDA를 사용할 수 있으면 GPU를 사용하고, 그렇지 않으면 CPU를 사용합니다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # CSV 파일에서 양방향 번역 학습 데이터를 읽어옵니다.
    pairs = load_translation_pairs(DATA_PATH)
    # 학습 데이터에 등장하는 문자들로 문자 사전을 생성합니다.
    char2idx, idx2char = build_vocab(pairs)
    # 문자 사전의 크기를 계산합니다.
    vocab_size = len(char2idx)
    # PyTorch Dataset 객체를 생성합니다.
    dataset = TranslationDataset(pairs, char2idx)
    # DataLoader는 데이터를 배치 단위로 섞어 모델에 공급합니다.
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch)

    # Seq2Seq 번역 모델을 생성하고 연산 장치로 이동합니다.
    # model = Seq2SeqTranslator(
    #     vocab_size=vocab_size,
    #     embed_size=EMBED_SIZE,
    #     hidden_size=HIDDEN_SIZE,
    # ).to(device)
    model = TransformerTranslator(
        vocab_size=vocab_size,
        embed_dim=EMBED_SIZE,
        ff_dim=HIDDEN_SIZE,
    ).to(device)
    # PAD 토큰은 실제 정답 문자가 아니므로 손실 계산에서 제외합니다.
    criterion = nn.CrossEntropyLoss(ignore_index=char2idx[PAD_TOKEN])
    # Adam 옵티마이저는 학습률을 자동으로 조정하여 안정적인 학습을 돕습니다.
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 지정한 epoch 수만큼 학습을 반복합니다.
    for epoch in range(1, epochs + 1):
        # 모델을 학습 모드로 전환합니다.
        model.train()

        # epoch별 손실 합계를 저장할 변수를 초기화합니다.
        total_loss = 0.0

        # DataLoader에서 미니배치를 하나씩 가져옵니다.
        for source_idx, decoder_idx, decoder_target_idx in loader:
            # 입력 텐서를 연산 장치(GPU 또는 CPU)로 이동합니다.
            source_idx, decoder_idx, decoder_target_idx = source_idx.to(device), decoder_idx.to(device), decoder_target_idx.to(device)

            # 이전 배치에서 계산된 기울기를 초기화합니다.
            optimizer.zero_grad()

            # 순전파를 수행하여 예측 결과를 계산합니다.
            logits = model(source_idx, decoder_idx)
            # CrossEntropyLoss는 입력을 [배치 × 시간, 클래스 수] 형태로 받으므로
            # logits과 정답 텐서의 형태를 변경합니다.
            loss = criterion(logits.reshape(-1, logits.size(-1)), decoder_target_idx.reshape(-1))
            # 손실을 기준으로 역전파를 수행하여 기울기를 계산합니다.
            loss.backward()
            # 기울기 폭주를 방지하기 위해 기울기의 크기를 제한합니다.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            # 계산된 기울기를 사용하여 모델의 가중치를 업데이트합니다.
            optimizer.step()
            # 현재 배치의 손실을 누적합니다.
            total_loss += loss.item()

        # 첫 epoch와 이후 20 epoch마다 평균 손실을 출력하여 학습 진행 상황을 확인합니다.
        if epoch == 1 or epoch % 20 == 0:
            print(f"Epoch {epoch:03d}/{epochs} | Loss: {total_loss / len(loader):.4f}")


    # 모델 저장 폴더가 없으면 생성합니다.
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    # 학습된 모델의 가중치를 저장합니다.
    torch.save(model.state_dict(), MODEL_PATH)
    # 추론에 필요한 문자 사전과 하이퍼파라미터를 함께 저장합니다.
    torch.save({
        "char2idx": char2idx,
        "idx2char": idx2char,
        "embed_size": EMBED_SIZE,
        "hidden_size": HIDDEN_SIZE
    }, META_PATH)

    print(f"모델 저장 완료 : {MODEL_PATH} and {META_PATH}")
    # 학습된 모델과 문자 사전을 반환합니다.
    return model, char2idx, idx2char


# 모델 학습 실행
if __name__ == "__main__":
    # 이 파일을 직접 실행하면 모델 학습을 시작합니다.
    train_model(epochs=EPOCHS)