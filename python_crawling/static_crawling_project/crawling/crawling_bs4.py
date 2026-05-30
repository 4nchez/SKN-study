# path : crawling\\crawling_bs4.py
# bs4 (beautifulSoup4) 를 이용한 정적 웹 크롤링 테스트 스크립트 1

# 패키지 설치: pip install beautifulsoup4
# import bs4  # 웹 페이지의 웹 문서를 html 로 분석하는 모듈임
# import urllib.request  # 웹 상의 데이터를 가져오는 모둘임
import urllib.request, bs4

# 1. url 로 웹페이지에 접속함
web_page = urllib.request.urlopen('https://www.naver.com/')
print(web_page)  # <http.client.HTTPResponse object at 0x000002CEE4CBB250>

# 2. 접속한 페이지 소스를 읽어옴
# html_code = web_page.read()
# print(html_code)  # 출력확인 (인코딩된 상태임)

# 3. 읽어온 인코딩된 소스를 html 태그 구문으로 바꿈
decoding_code = bs4.BeautifulSoup(web_page, 'html.parser')
print(decoding_code)
