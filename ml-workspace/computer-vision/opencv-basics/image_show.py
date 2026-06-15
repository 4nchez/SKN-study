import cv2
import sys

# 이미지 파일 불러오기
img = cv2.imread("../images/cat.bmp")

if img is None: # 해당 이미지가 없다면 (이미지 불러오기에 실패했다면)
    print("Image load failed")
    sys.exit()

print(type(img))
print(img.shape)

# 불러온 이미지 출력
cv2.namedWindow("imshow")
cv2.imshow("imshow", img)
cv2.waitKey(0) # 키보드 입력이 있을 때까지 대기

# 창 닫기
cv2.destroyAllWindows()