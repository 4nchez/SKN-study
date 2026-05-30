# path ./test/test_requests.py
# requests 모듈 사용 테스트

import requests

url = 'https://www.naver.com'

response = requests.get(url)
print(response.status_code)
print(response.text)