# cv2 동영상 파일 읽기

import cv2
import sys

# 동영상 파일 읽기용 cv2.VideoCapture 객체 생성
cap = cv2.VideoCapture("../multi/vtest.avi")

if not cap.isOpened(): # 동영상 열기에 실패했다면
    print("Video file open failed!") # 동영상 파일이 없을 때
    sys.exit()

# 동영상 프레임 해상도 출력
print("Frame width : ", round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("Frame height : ", round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# 전체 프레임 개수
print("Frame count : ", round(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
# 초당 프레임 수: FPS 출력
fps = round(cap.get(cv2.CAP_PROP_FPS))
print("FPS : ", round(fps))

delay = round(1000 / fps)

# 매 프레임 처리 및 화면 출력 (영상 출력)
while True:
    ret, frame = cap.read()
    # frame: 동영상으로부터 읽은 프레임(화면) 정보 저장
    # ret: 읽기 성공 여부 저장 (True | False)

    if not ret: # ret가 False이면 (읽기 실패를 의미함)
        break # while 강제 종료

    # 읽은 영상을 화면에 출력 처리
    cv2.imshow("Frame", frame)

    # 읽은 영상에서 테두리(경계, Edge) 선으로 변환해서 출력
    edge = cv2.Canny(frame, 50, 150)
    cv2.imshow("Canny", edge) # 윈도우 창이 열리면서 경계선 처리 영상 출력됨

    # 원래 의도대로 부드럽게 재생하려면 cv2.waitKey(delay)를 사용하는 것이 좋습니다.
    if cv2.waitKey(1) == 27: # ESC 키를 누르면 (항상 윈도우 창에서)
        break

cap.release() # 동영상 자원 해제
cv2.destroyAllWindows() # 윈도우 창 모두 닫기