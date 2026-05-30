# path : ./module/used_module.py
# module : module.used_module
# 파이썬에서 모듈 만들어 사용하기 테스트 스크립트

# 모듈 (module) : 파이썬 소스 파일이다. (파일명.py)
# 파일명이 모듈명임
# 모듈용 소스 파일에는 함수와 전역변수가 저장되면 됨
# 모듈이 제공하는 함수와 전역변수를 사용하려면, import 문을 선언해야 함
# import 모듈명 또는 import 패키지명.모듈명 [as 줄임말]
# 모듈명.함수명(), 모듈명.전역변수명 또는 모듈줄임말.함수명(), 모듈줄임말.전역변수명

# 파이썬이 제공하는 표준 모듈 사용
import keyword
# keyword.py 파일을 의미함

print(keyword.kwlist) # 예약어 목록 확인
# 모듈명.전역변수

# 모듈은 다른 파이썬 파일에서 사용할 수 있도록 함수(기능)와 전역변수(값)들을 따로 저장해서 제공하는 소스 파일이다.

# 모듈 임포트시에 모듈명에 대한 줄임말을 같이 선언할 수도 있음
# import 패키지명.모듈명 as 줄임말
import keyword as k

print(k.kwlist)
print(k.__file__) # 해당 모듈(소스파일)의 위치가 출력됨

# 현재 설치되어 있는 모듈 확인
# help('modules')

# 모듈 설명 참조
# help('random')

# 파이썬이 제공하는 표준 모듈들 ------------------------
import os # 파일이나 디렉토리 관련 기능을 제공

print(os.getcwd())

import time # 날짜와 시간 관련 기능을 제공

print(time.localtime()) # 현재 날짜와 시간 정보 제공
time.sleep(1) # 1초 멈춤
print(time.localtime())

import random # 임의의 숫자를 발생시키는 기능을 제공

print(random.random()) # 0.0 <= random float < 1.0
print(random.randint(1, 5)) # 1 <= random int <= 5
print(random.randrange(1, 10, 2)) # 1 <= 2 간격의 정수 < 10

import math # 수학 계산관련 기능 제공

print('원주율 : ', math.pi)
print('5! : ', math.factorial(5))

import calendar # 달력을 출력해서 날짜 지정 기능 제공

calendar.prmonth(2026, 5)

# __name__ : 현재 실행되고 있는 모듈 이름 확인
print(__name__) # __main__ : main 모듈 이름 출력
# 프로그램을 실행하면 기본으로 파일은 main 모듈(파일)이 됨
# 즉, main 만 실행할 수 있다는 의미임

# -----------------------------------------------------
# 사용자 정의 모듈 사용하기
# 모듈 파일과 사용 파일이 같은 폴더 안에 있으면, 파일명만 사용함 (폴더명 사용 안 함)
import mymodule as my

print('더하기 : ', my.sum(10, 20)) # 매개변수가 2개이면, 전달값도 2개여야 함 (반드시 갯수 일치해야 함)
print('빼기 : ', my.sub(15, 7))
print('곱하기 : ', my.mul(15, 3))
print('나누기한 몫 : ', my.div(13, 3))

try:
    print('나누기한 나머지', my.mod(12, 5))
except ZeroDivisionError as msg:
    print(msg)
    pass # 프로그램 중지하지 않고 계속 진행됨

print('가장 큰 값 : ', my.max())
print('가장 큰 값 : ', my.max(10))
print('가장 큰 값 : ', my.max(1, 2, 3, 4, 5, 6, 7, 8, 9))

print('가장 작은 값 : ', my.min())
print('가장 작은 값 : ', my.min(10))
print('가장 작은 값 : ', my.min(1, 2, 3, 4, 5, 6, 7, 8, 9))

print('글자 갯수 : ', my.strlen()) # 전달값이 없으면, 매개변수의 기본값이 사용됨
print('글자 갯수 : ', my.strlen('module test')) # 기본 매개변수에 값 전달하면, 전달값이 먼저 사용됨

print('my 원주율 : ', my.pi)
print('카운트 : ', my.count)

# 외부 모듈을 사용하려면
# 1. vscode 에서는 프로젝트 안에 가상환경을 생성함
# 터미널에서 현재 프로젝트 폴더>python -m venv 가상환경폴더명
# 2. 가상환경 활성화 (activate) : 자동으로 활성화됨
# 자동 활성화 안 될 경우 직접 활성화시킴
# ps 터미널 > ./가상환경폴더명/Scripts/Activate.ps1 입력하고 엔터
# cmd 터미널 > ./가상환경폴더명/Scripts/Activate.bat 입력하고 엔터
# linux > source ./가상환경폴더명/bin/activate
# (가상환경이름) 현재 프로젝트 경로 > 표시되면 가상환경 활성화된 것임
# 3. 터미널에서 외부 모듈 설치 : pip install 모둘명
# python --version
# pip list
# 설치 예 > pip install requests

import requests
import numpy as np
import pandas as pd

