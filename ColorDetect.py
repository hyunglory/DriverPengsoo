import cv2
import numpy as np
import time
import threading
import MecanumDriver

###### 노란색 영역지정(추적 예상 색 지정)
yellow_low = np.array([20,100,100])
yellow_upper = np.array([35,255,255])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

delay=0.001
sec=0.5
check_size = 70000
center_x=0
size_rect=0

def OpencvDetect():
    global center_x,size_rect
    while cap.isOpened():    
        ret, img = cap.read()
        #img_draw = img.copy()
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
        res_yellow_BGR=cv2.cvtColor(res_yellow, cv2.COLOR_HSV2BGR)
        res_gray=cv2.cvtColor(res_yellow_BGR, cv2.COLOR_BGR2GRAY)
        ##### 커널크기 지정
        kernel = np.ones((4,4),np.uint8)

        ##### 모폴로지 연산 OPEN 밝은영역 감소 CLOSE 밝은영역 증가
        res_thres = cv2.morphologyEx(res_gray, cv2.MORPH_OPEN, kernel)

        #####
        res, res_thres= cv2.threshold(res_thres,80,255,cv2.THRESH_BINARY_INV)
        contours,_ = cv2.findContours(res_thres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        #### 검출된 노란색에 사각형 그리기
        #count=0
        rect_x=[]

        collect_x = []
        collect_y = []
        add_x_w = []
        add_y_h = []

        img=cv2.rectangle(img, (220,0), (420, 480), (0,0,255), 1)
        for i in contours:
            (x,y,w,h) = cv2.boundingRect(i)

            if (w>=10 and h>=10 and w!=640 and h!=480):
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
                #print(x,y,w,h,"count:",count)
                rect_x.append(x)
                collect_x.append(x)
                collect_y.append(y)
                add_x_w.append(x+w)
                add_y_h.append(y+h)

                # if(count >= 1):
                #     mean_x = np.mean(rect_x)
                #     print(mean_x)
                #     if (mean_x > 440):
                #         #MecanumDriver.leftRotate_sec(delay,sec)
                #         print("leftRotate_sec")
                #         time.sleep(0.5)
                #     elif (mean_x < 220):
                #         #MecanumDriver.rightRotate_sec(delay,sec)
                #         print("rightRotate_sec")
                #         time.sleep(0.5)
                # count+=1

        x_min = 0
        y_min = 0
        x_w_max = 0
        y_h_max = 0

        if (len(collect_x) != 0):
            x_min = np.min(collect_x)
            y_min = np.min(collect_y)
            x_w_max = np.max(add_x_w)
            y_h_max = np.max(add_y_h)
        
        cv2.rectangle(img, (x_min,y_min), (x_w_max, y_h_max), (0,255,0), 3)        

        center_x = int((x_min+x_w_max)/2)
        center_y = int((y_min+y_h_max)/2)

        size_rect = (x_w_max-x_min)*(y_h_max-y_min)
        print("size_rect : ", size_rect)

        cv2.circle(img,(center_x,center_y),5,(0,255,255),-1)
        print("center_x : ", center_x)
            
        #cv2.imshow('BGR',res_yellow_BGR)
        #cv2.imshow('GRAY',res_gray)
        #cv2.imshow('threshold',res_thres)
        #cv2.imshow('threshold',res_thres)
        #cv2.imshow('gray',res_gray)
        cv2.imshow('img',img)
        key = cv2.waitKey(1) & 0xff
        time.sleep(0.001)



def followPengsoo(dalay,sec):
    
    if (center_x == 0 or size_rect == 0):
        MecanumDriver.carStop()
        print("carStop")
    else:
        if( center_x < 300):
            if (size_rect < check_size):
                MecanumDriver.leftRotate_sec(delay, sec)
                print("leftRotate")
            else :
                MecanumDriver.carStop()
                print("carStop")
        elif(center_x > 440):
            if (size_rect < check_size):
                MecanumDriver.rightRotate_sec(delay, sec)
                print("RightRotate")
            else :
                MecanumDriver.carStop()
                print("carStop")
        else:
            if (size_rect < check_size):
                MecanumDriver.carForward_sec(delay, sec)
                print("carForward_sec")
            else :
                MecanumDriver.carStop()
                print("carStop")

T1=threading.Thread(target=OpencvDetect)
T1.daemon=True
T1.start()

while True :
    followPengsoo(delay, sec)
    time.sleep(0.5)


cap.release()
cv2.destroyAllWindows()

