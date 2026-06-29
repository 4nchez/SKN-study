from app.config import Config
from app.predict import load_artifacts, predict_text
from app.train import train_model


if __name__ == "__main__":
    config = Config()

    train_model(config)

    model, metadata = load_artifacts(config)

    sample_news = "“그레이시는 통통하고 행복해 보였다”…목장 탈출한 기린, 2주 만에 무사 발견" # 세계

    predicted_label = predict_text(sample_news, model, metadata, config)

    # 최종 예측 결과를 화면에 출력한다.
    print("\n새 기사:", sample_news)
    print("예측 카테고리:", predicted_label)
