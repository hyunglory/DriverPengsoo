import cv2
import numpy as np

###### 노란색 영역지정(추적 예상 색 지정)
yellow_low = np.array([20,50,50])
yellow_upper = np.array([35,255,255])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while cap.isOpened():    
    ret, img = cap.read()
    img_draw = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    
        

    ##### 노란색 마스크 생성
    mask_yellow = cv2.inRange(hsv, yellow_low, yellow_upper)
        
    ##### 노란색 마스크로 노란색 이미지만 추출
    res_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)    
    
    
    ##### 노란색 필셀 값 계산
    pixel_yellow = np.uint8([res_yellow])
    #sum_yellow = np.sum(res_yellow, dtype = np.uint8)
    sum_yellow = np.sum(pixel_yellow)


    ##### 노란색 contour 찾기
    res_yellow_BGR=cv2.cvtColor(res_yellow, cv2.COLOR_HSV2BGR) # 노란색 
    res_gray=cv2.cvtColor(res_yellow_BGR, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4,4),np.uint8)
    res_thres = cv2.morphologyEx(res_gray, cv2.MORPH_OPEN, kernel)
    res, res_thres= cv2.threshold(res_thres,80,255,cv2.THRESH_BINARY_INV)
    contours,_ = cv2.findContours(res_thres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    #### 검출된 노란색에 사각형 그리기
    count=0
    rect_x=[]
    for i in contours:
        (x,y,w,h) = cv2.boundingRect(i)

        if (w>=25 and h>=25 and w!=640 and h!=480):
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
            print(x,y,w,h,"count:",count)
            rect_x.append(x)
            if(count >= 1):
                mean_x = np.mean(rect_x)
                print(mean_x)
            
            count+=1
            
    print("--------------------------------------------------------------")

        
    #cv2.imshow('BGR',res_yellow_BGR)
    cv2.imshow('GRAY',res_gray)
    cv2.imshow('threshold',res_thres)
    #cv2.imshow('threshold',res_thres)
    #cv2.imshow('gray',res_gray)
    cv2.imshow('img',img)
    key = cv2.waitKey(1) & 0xff

cap.release()
cv2.destroyAllWindows()
