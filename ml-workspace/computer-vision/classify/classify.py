'''
이 코드는 OpenCV DNN 모듈과 사전 학습된 GoogleNet 모델을 활용하여
제공된 이미지가 어떤 객체로 분류되는지 확인하는 프로그램.
'''

# 프로그램 종료 (sys.exit) 사용
import sys

# 배열 처리, 최댓값 위치 탐색 (argmax)으로 분류 항목 클래스 위치 탐색
import numpy as np

# 이미지 처리 및 딥러닝 모델 활용에 사용
import cv2

# 기본 분류 대상 이미지 지정
# filename = 'space_shuttle.jpg'
# filename = 'beagle.jpg'
# filename = 'cup.jpg'
# filename = 'pineapple.jpg'
# filename = 'scooter.jpg'
filename = 'Tiger-Cat.jpg'

# 실행 시 명령행 인수로 이미지 파일명을 전달하면 해당 파일을 분류할 이미지로 사용하게 함
'''
명령행 프롬프트
....경로 > python classify.py scooter.jpg (엔터)
sys.argv[0] : 'classify.py'
sys.argv[1] : 'scooter.jpg'가 전달됨
'''
if len(sys.argv) > 1:
    filename = sys.argv[1]
    # print("sys.argv[1] : ", filename)
    # sys.exit(0)

# 이미지 파일 읽기
img = cv2.imread(filename) # 이미지를 NumPy 배열 형태로 반환함

if img is None: # 이미지 읽기 실패 여부 확인
    print('Image load failed!') # 파일이 없거나 경로가 잘못된 경우 None 반환
    sys.exit() # 프로그램 강제 종료

# load network : 제공되는 dnn 학습 모델과 구성을 다운로드하여 사용
# https://github.com/AleDel/deepdreamer-touchdesigner/blob/master/models/bvlc_googlenet.caffemodel
net = cv2.dnn.readNet('bvlc_googlenet.caffemodel', 'deploy.prototxt')
# bvlc_googlenet.caffemodel : 학습된 가중치(weight) 파일
# deploy.prototxt : 네트워크 구성 정의 파일 (모델 구조 정의)

if net.empty(): # 모델이 정상 로드되었는지 확인
    print('Network Model Load Failed!')
    exit()

# load class names
# 클래스 이름 (분류 항목) 파일 읽기 : ImageNet 1000개 목록
classNames = None
with open('classification_classes_ILSVRC2012.txt', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# print(type(classNames))
# print(classNames)
# print(len(classNames))
# exit()

# Inference : 준비된 이미지를 모델에 적용해서 클래스 항목으로 분류되는지 테스트
# 이미지 전처리
# 딥러닝 모델은 원본 이미지 그대로 사용할 수 없음
# 모델 입력 형식으로 변환 필요
inputBlob = cv2.dnn.blobFromImage(img, 1, (224, 224), (104, 117, 123))
# img : 입력 이미지
# 1 : 스케일 계수
# (224, 224) : 모델 입력 크기
# (104, 117, 123) : BGR 순서, 평균값 제거

# 전처리된 이미지를 네트워크 입력으로 지정
net.setInput(inputBlob, 'data')  # 생략해도 됨
# data = 입력 레이어 이름

# 순전파 (forward propagation) 수행
# 입력 이미지가 네트워크를 통과하면서 1000개의 클래스 확률 계산
prob = net.forward()

# 모델을 통해서 나온 테스트 결과 확인
# print(prob.shape)
# print(type(prob))
# print(prob)
# exit()

# 결과 분석
# check result & display
out = prob.flatten() # 다차원 배열을 1차원 배열로 변환
classId = np.argmax(out) # 가장 높은 확률의 클래스 인덱스 조회
confidence = out[classId] # 인덱싱 -> 결과 추출

# 출력용 문장 만들기
text = '%s (%4.2f%%)' % (classNames[classId], confidence * 100)
print(text)
# 이미지에 출력 처리
cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()
