from pydantic_settings import BaseSettings

# BaseSettings는 운영체제 환경 변수와 .env 파일의 값을
# 자동으로 읽어와 파이썬 객체에 매핑하고, 타입 검증까지 수행하는 기본 클래스이다.


class Settings(BaseSettings):
    """
    애플리케이션에서 사용하는 환경 설정을 한곳에서 관리하기 위한 클래스.

    BaseSettings를 상속하면 클래스의 필드와 운영체제 환경 변수,
    그리고 .env 파일의 값을 자동으로 매핑하여 객체를 생성한다.
    또한 각 필드의 자료형에 맞게 값을 변환하고 검증한다.

    필드 선언 예시:
        필드명: 자료형
        필드명: 자료형 = 기본값
    """

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    # 업로드 가능한 최대 파일 크기(바이트 단위)
    # 필요에 따라 값을 변경할 수 있다.
    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024  # 20MB

    # 업로드 시 이 값을 초과하는 파일은
    # 라우터에서 검사하여 HTTP 413(Payload Too Large) 오류를 반환한다.


    class Config:
        """
        BaseSettings의 동작 방식을 설정하는 내부 클래스.
        """

        # 프로젝트 루트의 .env 파일을 함께 읽도록 설정
        env_file = ".env"

        # .env 파일의 문자 인코딩 지정
        env_file_encoding = "utf-8"


# Settings 객체 생성
settings = Settings()

# Settings 객체를 전역으로 생성하면 애플리케이션 전체에서
# 하나의 인스턴스를 공유하여 사용할 수 있다.
# (일반적으로 설정 객체는 싱글톤처럼 사용한다.)

"""
애플리케이션이 시작되면 다음 순서로 동작한다.

1. 운영체제 환경 변수와 .env 파일을 읽는다.
2. OPENAI_API_KEY와 같은 필수 설정이 존재하는지 확인한다.
3. 각 값을 선언된 자료형(str, int 등)에 맞게 변환하고 검증한다.
4. 검증이 완료되면 Settings 객체를 생성하여 애플리케이션 전체에서 사용한다.
"""