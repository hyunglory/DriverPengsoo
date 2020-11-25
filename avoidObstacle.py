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
cycle=2

carFunc = []

def returnCarFunc():
    
    if(len(carFunc)==0):
        return True
    print("리턴 시작")
    # for i in range(len(carFunc)):
    #     if (carFunc[i] == "[Car]Right"):
    #         carFunc[i] = "[Car]Left"
    #     elif (carFunc[i] == "[Car]Left"):
    #         carFunc[i] = "[Car]Right"
    #     elif (carFunc[i] == "[Car]Dir1"):
    #         carFunc[i] = "[Car]Dir11"
    #     elif (carFunc[i] == "[Car]Dir11"):
    #         carFunc[i] = "[Car]Dir1"

    for i in range(len(carFunc)):
        if (carFunc[i] == "[Car]Right"):
            client("[Car]Right")
            time.sleep(sleep)
        elif (carFunc[i] == "[Car]Left"):
            client("[Car]Left")
            time.sleep(sleep)
        elif (carFunc[i] == "[Car]Dir1"):
            client("[Car]Dir1")
            time.sleep(sleep)
        elif (carFunc[i] == "[Car]Dir11"):
            client("[Car]Dir11")
            time.sleep(sleep)
        elif (carFunc[i] == "[Car]Forward"):
            client("[Car]Forward")
            time.sleep(sleep)

    for i in range(len(carFunc)):
        print("{} 삭제".format(carFunc[0]))
        del carFunc[0]

    print("리턴 종료")   

def checkAll(): # 전체 센서 값 저장
    global FL0, FR0, LL0, LR0 
    global FL45, FR45, LL45, LR45
    global FL90, FR90, LL90, LR90  

    FL0 = sensor.FLgetDistance()
    FR0 = sensor.FRgetDistance()
    #LL0 = sensor.LLgetDistance()
    #LR0 = sensor.LRgetDistance()
    print("[회피]0도 " + "FL: " + str(FL0) + " FR " + str(FR0))
    
    servo.pwmGo(55)   # 대각선 방향
    time.sleep(0.8)
    FL45 = sensor.FLgetDistance()
    FR45 = sensor.FRgetDistance()
    #LL45 = sensor.LLgetDistance()
    #LR45 = sensor.LRgetDistance()
    print("[회피]45도 " + "FL: " + str(FL45) + " FR " + str(FR45))
    
    servo.pwmGo(110)   # 측면 방향
    time.sleep(0.8)
    FL90 = sensor.FLgetDistance()   
    FR90 = sensor.FRgetDistance()
    LL90 = sensor.LLgetDistance()
    LR90 = sensor.LRgetDistance()
    print("[회피]90도 " + "FL: " + str(FL90) + " FR " + str(FR90)+ " LL " + str(LL90)+ " LR "+ str(LR90))
    servo.pwmGo(0)  # 앞뒤 방향
    
def avoidMode(sleep):
    checkAll()
    if (FL90 < sideLimit and sum([FL0,FL45,FL90,LL90]) < sum([FR0,FR45,FR90,LR90])):
        for i in range(cycle):
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)

    elif (FL45 < diagonalLimit and sum([FL0,FL45,FL90,LL90]) < sum([FR0,FR45,FR90,LR90])):
        for i in range(cycle):
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)
            client("[Car]Forward")
            carFunc.append("[Car]Forward")
            time.sleep(sleep)

    elif (FL0 < FrontLimit and sum([FL0,FL45,FL90,LL90]) < sum([FR0,FR45,FR90,LR90])):
        for i in range(cycle):
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)
            client("[Car]Dir1")
            carFunc.append("[Car]Dir11")
            time.sleep(sleep)

    elif (FR0 < FrontLimit and sum([FR0,FR45,FR90,LR90]) < sum([FL0,FL45,FL90,LL90])):
        for i in range(cycle):
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)
            client("[Car]Dir11")
            carFunc.append("[Car]Dir1")
            time.sleep(sleep)

    elif (FR45 < diagonalLimit and sum([FR0,FR45,FR90,LR90]) < sum([FL0,FL45,FL90,LL90])):
        for i in range(cycle):
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)
            client("[Car]Forward")
            carFunc.append("[Car]Forward")
            time.sleep(sleep)

    elif (FR90 < sideLimit and sum([FR0,FR45,FR90,LR90]) < sum([FL0,FL45,FL90,LL90])):
        for i in range(cycle):
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)

    elif (LL90 < sideLimit and sum([FL0,FL45,FL90,LL90]) < sum([FR0,FR45,FR90,LR90])):
        for i in range(cycle):
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)
            client("[Car]Right")
            carFunc.append("[Car]Left")
            time.sleep(sleep)

    elif (LR90 < sideLimit and sum([FR0,FR45,FR90,LR90]) < sum([FL0,FL45,FL90,LL90])):
        for i in range(cycle):
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)
            client("[Car]Left")
            carFunc.append("[Car]Right")
            time.sleep(sleep)

    elif(FL90+FL45+FL0+FR0+FR45+FR90+LL90+LR90 <= FrontLimit*8) :
        print("-------------------------------------------------------")
        print("탈출 모드")
        print("-------------------------------------------------------")
        #maxVal = max(FL90, FL45,FL0, FR0, FR45, FR90, LL90, LR90)
        
    else:
        print("예외값 오류1")
                        
def client(data):

    host = "192.168.0.43" # 라파4: 43 / 라파3 139
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
        LL90 = sensor.FLgetDistance()
        LR90 = sensor.FRgetDistance()
        print("[앞으로]0도 " + "FL: " + str(FL0) + " FR: " + str(FR0))
        print("[앞으로]90도 "+ "LL: " + str(LL90)+ " LR: "+ str(LR90))
        if(FL0 < FrontLimit or FR0 < FrontLimit):
            avoidMode(sleep)
        else :
            client("[Car]Forward")
            time.sleep(sleep)
            #if(len(carFunc)>0 and LR90 > 300 and LL90 > 300):
            for i in range(int(len(carFunc)*2)):
                client("[Car]Forward")
                time.sleep(sleep)

            returnCarFunc()

# go(목적지)
# avoidMode()를 반복해야 할듯
