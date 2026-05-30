# path : crawling\\crawling2_bs4.py
# url 을 키보드로 입력받아서 크롤링 작동 테스트용 스크립트 2

import urllib.request, bs4

url = input('접속할 url 입력 : ')
# url: 웹 상에서의 자원까지의 경로를 의미함
# 표현: 프로토콜://도메인명/폴더명/파일명?이름=값&이름=값#표식이름
# 도메인명: 웹서버의 ip주소:포트번호 가 매핑된 이름임
# 쿼리스트링: 서버측의 대상에게로 전달되는 값들을 표현한 것 - ?이름=전송값&이름=전송값
# 쿼리스트링은 pathvariable 로 대체될 수 있음
# https://www.ktv.go.kr/news/latest/view?content_id=744735
# https://search.naver.com/search.naver?sm=tab_sug.top&where=nx&ssc=tab.nx.all&query=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&oquery=%EC%98%81%ED%99%94&tqi=jSc15dqo6DvZHH4umjC-241500&acq=%EC%98%81%ED%99%94&acr=2&qdt=0&ackey=yxdi0d5o

web_page = urllib.request.urlopen(url)
result_code = bs4.BeautifulSoup(web_page, 'html.parser')
print(result_code)

