from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import pytesseract


def tesser_predict(PATH)-> str:
  image = cv2.imread(PATH)
  image = imutils.resize(image, height=500)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)
  edged = cv2.Canny(blurred, 50 , 200 , 255)
  # Находим контуры на карте, затем сортируем их в порядке убывания 
  cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
  displayCnt = None
  for c in cnts:
    # аппроксимируем контур
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # если в контуре имеется 4 вершины, то находим экран
    if len(approx) == 4:
      displayCnt = approx
      break
  warped = four_point_transform(gray, displayCnt.reshape(4, 2))
  custom_config = r'--oem 3 --psm 6 outputbase digits'
  point = pytesseract.image_to_string(warped, config=custom_config)
  dg = ''.join([i for i in point if i.isdigit()])
  return dg


