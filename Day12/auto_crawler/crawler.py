# 운영체제 환경변수 값을 읽기 위해 os 모듈을 가져온다.
import os

# 현재 날짜와 시간을 저장하기 위해 datetime을 가져온다.
from datetime import datetime

# 상대 URL을 절대 URL로 변환하기 위해 urljoin을 가져온다.
from urllib.parse import urljoin

# HTML 문서를 분석하기 위해 BeautifulSoup을 가져온다.
from bs4 import BeautifulSoup

# .env 파일에 저장된 환경변수를 읽기 위해 load_dotenv를 가져온다.
from dotenv import load_dotenv

# Playwright를 동기 방식으로 사용하기 위해 sync_playwright를 가져온다.
# Playwright는 실제 브라우저를 실행해서 동적 웹페이지도 크롤링할 수 있게 해준다.
from playwright.sync_api import sync_playwright

# models.py에 정의된 CrawlItem 데이터 클래스를 가져온다.
from models import CrawlItem


# .env 파일을 읽어서 os.getenv()로 사용할 수 있게 한다.
load_dotenv()


# 네이버 뉴스 데이터를 크롤링하는 클래스이다.
class NaverNewsCrawler:
    # 객체가 생성될 때 자동으로 실행되는 생성자이다.
    def __init__(self):
        # .env 파일의 CRAWL_URL 값을 읽어온다.
        # 만약 CRAWL_URL 값이 없으면 기본값으로 https://news.naver.com/ 사용
        self.url = os.getenv("CRAWL_URL", "https://news.naver.com/")

    # 외부에서 호출하는 대표 크롤링 메서드이다.
    # limit은 최대 몇 개의 데이터를 수집할지 지정한다.
    def crawl(self, limit: int = 30) -> list[CrawlItem]:
        # 웹페이지 HTML을 가져온다.
        html = self._get_html()

        # 가져온 HTML에서 필요한 데이터를 추출한다.
        return self._parse(html, limit)

    # 실제 브라우저를 실행해서 HTML을 가져오는 내부 메서드이다.
    # 메서드 이름 앞의 _는 내부에서 사용하는 함수라는 의미로 자주 사용된다.
    def _get_html(self) -> str:
        # Playwright 실행 컨텍스트를 연다.
        # with 구문을 사용하면 작업이 끝난 뒤 자원이 자동 정리된다.
        with sync_playwright() as p:
            # Chromium 브라우저를 실행한다.
            # headless=True는 브라우저 창을 화면에 보이지 않게 실행한다는 뜻이다.
            browser = p.chromium.launch(headless=True)

            # 새 브라우저 페이지를 만든다.
            # user_agent는 실제 사용자의 브라우저처럼 보이게 하기 위한 설정이다.
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
                )
            )

            # 지정된 URL로 이동한다.
            # wait_until="networkidle"은 네트워크 요청이 어느 정도 끝날 때까지 기다린다.
            # timeout=60000은 최대 60초까지 기다린다는 뜻이다.
            page.goto(self.url, wait_until="networkidle", timeout=60000)

            # 페이지가 완전히 렌더링될 시간을 조금 더 준다.
            # 1500ms = 1.5초
            page.wait_for_timeout(1500)

            # 현재 브라우저 페이지의 전체 HTML을 문자열로 가져온다.
            html = page.content()

            # 브라우저를 닫는다.
            browser.close()

            # 수집한 HTML 문자열을 반환한다.
            return html

    # HTML에서 뉴스 제목과 링크를 추출하는 내부 메서드이다.
    def _parse(self, html: str, limit: int) -> list[CrawlItem]:
        # BeautifulSoup 객체를 생성한다.
        # "lxml"은 빠른 HTML 파서이다.
        soup = BeautifulSoup(html, "lxml")

        # 최종 수집 결과를 저장할 리스트이다.
        result = []

        # 중복 제목을 제거하기 위해 set 자료구조를 사용한다.
        # set은 같은 값을 중복 저장하지 않는다.
        seen = set()

        # HTML 문서 안의 모든 a 태그를 찾는다.
        # a 태그는 보통 링크를 의미한다.
        for a in soup.select("a"):
            # a 태그 안의 텍스트를 가져온다.
            # strip=True는 앞뒤 공백을 제거한다.
            title = a.get_text(strip=True)

            # a 태그의 href 속성 값을 가져온다.
            # href에는 이동할 링크 주소가 들어 있다.
            href = a.get("href")

            # 제목이나 링크가 없으면 사용할 수 없는 데이터이므로 건너뛴다.
            if not title or not href:
                continue

            # 제목 길이가 너무 짧으면 뉴스 제목이 아닐 가능성이 높으므로 제외한다.
            if len(title) < 8:
                continue

            # 이미 수집한 제목이면 중복이므로 제외한다.
            if title in seen:
                continue

            # 현재 제목을 중복 확인용 set에 추가한다.
            seen.add(title)

            # CrawlItem 객체를 생성하여 결과 리스트에 추가한다.
            result.append(
                CrawlItem(
                    # 뉴스 제목
                    title=title,

                    # urljoin은 상대경로 링크를 절대경로 링크로 변환한다.
                    # 예: /main/read.naver → https://news.naver.com/main/read.naver
                    link=urljoin(self.url, href),

                    # 크롤링 대상 원본 URL
                    source_url=self.url,

                    # 현재 크롤링한 시간
                    crawled_at=datetime.now()
                )
            )

            # 수집 개수가 limit 이상이면 반복문을 중단한다.
            if len(result) >= limit:
                break

        # 최종 수집 결과 리스트를 반환한다.
        return result