import sensor
import servo
import time
import sys
import socket
FL0 = 0
FR0 = 0
LL0 = 0
LR0 = 0
FL45 = FR45 = LL45 = LR45 = 0
FL90 = FR90 = LL90 = LR90 = 0

FrontLimit = 20
diagonalLimit = 20
sideLimit = 20
sleep=1.5


carFunc = []

def returnCarFunc(delay, sec):
    if(not carFunc):
        return True

    for i in range(len(carFunc)):
        if (carFunc[i] == "carLeft"):
            carFunc[i] == "carRight"
        elif (carFunc[i] == "carRight"):
            carFunc[i] == "carLeft"
        else :
            carFunc[i] == "wrong value"
    
    # for i in range(len(carFunc)):
    #     if (carFunc[i] == "carLeft"):
    #         client("[Car]Left")
    #     elif (carFunc[i] == "carRight"):
    #         client("[Car]Right")
    #     else :
    #         client("[Car]Stop")
    if (carFunc[0] == "carLeft"):
        client("[Car]Left")
        del carFunc[0]
    elif (carFunc[i] == "carRight"):
        client("[Car]Right")
        del carFunc[0]


def checkAll(): # 전체 센서 값 저장
    global FL0, FR0, LL0, LR0 
    global FL45, FR45, LL45, LR45
    global FL90, FR90, LL90, LR90  

        
    FL0 = sensor.FLgetDistance()
    FR0 = sensor.FRgetDistance()
    #LL0 = sensor.LLgetDistance()
    #LR0 = sensor.LRgetDistance()
    print("0도 " + "FL: " + str(FL0) + " FR " + str(FR0))
    

    servo.pwmGo(55)   # 대각선 방향
    time.sleep(0.8)
    FL45 = sensor.FLgetDistance()
    FR45 = sensor.FRgetDistance()
    #LL45 = sensor.LLgetDistance()
    #LR45 = sensor.LRgetDistance()
    print("45도 " + "FL: " + str(FL45) + " FR " + str(FR45))
    

    servo.pwmGo(110)   # 측면 방향
    time.sleep(0.8)
    FL90 = sensor.FLgetDistance()   
    FR90 = sensor.FRgetDistance()
    LL90 = sensor.LLgetDistance()
    LR90 = sensor.LRgetDistance()
    print("90도 " + "FL: " + str(FL90) + " FR " + str(FR90)+ " LL " + str(LL90)+ " LR "+ str(LR90))
    servo.pwmGo(0)  # 앞뒤 방향
    

def avoidMode(sleep):
    checkAll()
    if (FL90 < sideLimit):
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)

    elif (FL45 < diagonalLimit):
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Forward")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Forward")
        time.sleep(sleep)

    elif (FL0 < FrontLimit):
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Dir5")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Dir5")
        time.sleep(sleep)

    elif (FR0 < FrontLimit):
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Dir7")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Dir7")
        time.sleep(sleep)

    elif (FR45 < diagonalLimit):
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Forward")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Forward")
        time.sleep(sleep)

    elif (FR90 < sideLimit):
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)

    elif (LL90 < sideLimit):
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)
        client("[Car]Right")
        time.sleep(sleep)

    elif (LR90 < sideLimit):
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)
        client("[Car]Left")
        time.sleep(sleep)

    elif(max(FL90, FL45,FL0, FR0, FR45, FR90, LL90, LR90) >= FrontLimit) :
        print("-------------------------------------------------------")
        print("리미트 범위 초과")
        print("-------------------------------------------------------")
        client("[Car]Forward")
        time.sleep(sleep)
        maxVal = max(FL90, FL45,FL0, FR0, FR45, FR90, LL90, LR90)
        if (maxVal == FL90):
            client("[Car]Left")
            time.sleep(sleep)
            client("[Car]Left")
            time.sleep(sleep)

        elif (maxVal == FL45):
            client("[Car]Dir11")
            time.sleep(sleep)
            client("[Car]Dir11")
            time.sleep(sleep)

        elif (maxVal == FL0):
            client("[Car]Forward")
            time.sleep(sleep)
            client("[Car]Forward")
            time.sleep(sleep)

        elif (maxVal == FR0):
            client("[Car]Forward")
            time.sleep(sleep)
            client("[Car]Forward")
            time.sleep(sleep)

        elif (maxVal == FR45):
            client("[Car]Dir1")
            time.sleep(sleep)
            client("[Car]Dir1")
            time.sleep(sleep)

        elif (maxVal == FR90):
            client("[Car]Right")
            time.sleep(sleep)
            client("[Car]Right")
            time.sleep(sleep)

        elif (maxVal == LL90):
            client("[Car]Left")
            time.sleep(sleep)
            client("[Car]Left")
            time.sleep(sleep)
        
        elif (maxVal == LR90):
            client("[Car]Right")
            time.sleep(sleep)
            client("[Car]Right")
            time.sleep(sleep)
        else:
            print("예외값 오류2")

    else:
        print("예외값 오류1")
                
                
        

            

        
                    
                        
def client(data):

    host = "192.168.0.55" # 라파4: 55 / 라파3 139
    port = 9999
    data = data.encode()

    # IP 주소 변수에 서버 주소와 포트 설정 
    addr = host, port

    # 소켓 생성
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
    # 클라이언트 포트 설정 : 자동
    s.bind(('', 0))

    # 준비 완료 화면에 출력
    # print ('udp echo client ready')
    s.sendto(data, addr)
    print ("{} 전송완료".format(data))

if __name__ == '__main__':
    while True:
        servo.pwmGo(0)
        FL0 = sensor.FLgetDistance()
        FR0 = sensor.FRgetDistance()
        print("0도 " + "FL: " + str(FL0) + " FR " + str(FR0))
        if(FL0 < FrontLimit or FR0 < FrontLimit):
            avoidMode(sleep)
        else :
            client("[Car]Forward")
            time.sleep(sleep)


            
        

# go(목적지)
# avoidMode()를 반복해야 할듯
