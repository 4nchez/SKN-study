from __future__ import annotations

from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://news.naver.com/",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

SECTION_URLS: Dict[str, str] = {
    "경제": "https://news.naver.com/section/101",
    "사회": "https://news.naver.com/section/102",
    "생활/문화": "https://news.naver.com/section/103",
    "세계": "https://news.naver.com/section/104",
    "IT/과학": "https://news.naver.com/section/105",
}


def crawl_section(url: str) -> List[str]:
    """한 섹션의 기사 제목을 수집한다."""

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # JS:
    # document.querySelectorAll('.sa_list:first-child .sa_text')
    items = soup.select(".sa_list:first-child .sa_text")
    titles = []

    for item in items:
        a = item.find("a")
        if a:
            titles.append(a.get_text(strip=True))

    return titles


def load_news_data() -> Tuple[List[str], List[str]]:

    texts: List[str] = []
    labels: List[str] = []

    for category, url in SECTION_URLS.items():
        try:
            titles = crawl_section(url)

            texts.extend(titles)
            labels.extend([category] * len(titles))

            print(f"{category}: {len(titles)}건")
        except Exception as e:
            print(f"{category} 오류: {e}")

    return texts, labels


if __name__ == "__main__":
    texts, labels = load_news_data()

    for text, label in zip(texts[:10], labels[:10]):
        print(f"[{label}] {text}")