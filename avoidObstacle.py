#import sensor
#import servo
#import MecanumDriver
#import RPi.GPIO as GPIO
import time
import sys
from socket import *

FL0 = FR0 = LL0 = LR0 = 0
FL45 = FR45 = LL45 = LR45 = 0
FL90 = FR90 = LL90 = LR90 = 0

FowardBehindLimit = 10
sideLimit = 5
diagonalLimit = 15

carFunc = []

def returnCarFunc(delay, sec):
    for i in range(len(carFunc)):
        if (carFunc[i] == "carLeft"):
            carFunc[i] == "carRight"
        elif (carFunc[i] == "carRight"):
            carFunc[i] == "carLeft"
        else :
            carFunc[i] == "wrong value"
    
    for i in range(len(carFunc)):
        if (carFunc[i] == "carLeft"):
            MecanumDriver.carLeft_sec(delay, sec)
        elif (carFunc[i] == "carRight"):
            MecanumDriver.carRight_sec(delay, sec)
        else :
            MecanumDriver.carStop()

    
    

def checkFront():
    servo.pwmGo(0)    # 앞뒤 방향
    FL0 = sensor.FLgetDistance()
    FR0 = sensor.FRgetDistance()
    LL0 = sensor.LLgetDistance()
    LR0 = sensor.LRgetDistance()

def checkAll(): # 전체 센서 값 저장
    print("checkAll")
    servo.pwmGo(0)    # 앞뒤 방향
    FL0 = sensor.FLgetDistance()
    FR0 = sensor.FRgetDistance()
    LL0 = sensor.LLgetDistance()
    LR0 = sensor.LRgetDistance()

    servo.pwmGo(45)   # 대각선 방향
    FL45 = sensor.FLgetDistance()
    FR45 = sensor.FRgetDistance()
    LL45 = sensor.LLgetDistance()
    LR45 = sensor.LRgetDistance()

    servo.pwmGo(90)   # 측면 방향
    FL90 = sensor.FLgetDistance()   
    FR90 = sensor.FRgetDistance()
    LL90 = sensor.LLgetDistance()
    LR90 = sensor.LRgetDistance()

def avoidMode(delay, sec):
    
    while True : # 현재 그 좌표아니면
        
        checkAll()

        if (FL0 < FowardBehindLimit or FR0 < FowardBehindLimit):
            # MecanumDriver.carStop()
            client("[Car]stop")
            checkAll()

            if (FL90 < sideLimit or LL90 < sideLimit):
                # MecanumDriver.carRight_sec(delay, sec)
                client("[Car]Right")
                carFunc.append("carRight")    
            elif (FR90 < sideLimit or LR90 < sideLimit):
                # MecanumDriver.carLeft_sec(delay, sec)
                client("[Car]Left")
                carFunc.append("carLeft")
            elif (FL45 > FR45):
                # MecanumDriver.carLeft_sec(delay, sec)
                client("[Car]Left")
                carFunc.append("carLeft")
            else :
                # MecanumDriver.carRight_sec(delay, sec)
                client("[Car]Right")
                carFunc.append("carRight") 
        else:
            # MecanumDriver.carForward_sec(delay,sec)
            client("[Car]Forward")
            checkAll()

            if(FL90 > sideLimit and FR90 > sideLimit and LL90 > sideLimit and LR90 > sideLimit):
                returnCarFunc(delay, sec)
                if (carFunc[0] == "carLeft"):
                    # MecanumDriver.carLeft_sec(delay,sec)
                    client("[Car]Left")
                    del carFunc[0]
                elif (carFunc[0] == "carRight"):
                    # MecanumDriver.carRight_sec(delay, sec)
                    client("[Car]Right")
                    del carFunc[0]
                elif (carFunc == None):
                    # MecanumDriver.carStop()
                    client("[Car]stop")
                else:
                    # MecanumDriver.carStop()
                    client("[Car]stop")

            else:
                minVal = min(FL90, FR90, LL90, LR90)
                if (minVal < sideLimit):
                    if (minVal == FL90 or minVal == LL90): 
                        # MecanumDriver.carRight_sec(delay, sec)
                        client("[Car]Right")
                        carFunc.append("carRight")
                    elif (minVal == FR90 or minVal == LR90):
                        # MecanumDriver.carLeft_sec(delay,sec)
                        client("[Car]Left")
                        carFunc.append("carLeft")
                    else:
                        # MecanumDriver.carStop()
                        client("[Car]stop")
                    
                        
def client(data):

    host = "192.168.0.55" # 라파4: 55 / 라파3 139
    port = 9999
    data = data.encode()

    # IP 주소 변수에 서버 주소와 포트 설정 
    addr = host, port

    # 소켓 생성
    s = socket(AF_INET, SOCK_DGRAM)
   
    # 클라이언트 포트 설정 : 자동
    s.bind(('', 0))

    # 준비 완료 화면에 출력
    print ('udp echo client ready')
    s.sendto(data, addr)
    print ("{} 전송완료".format(data))

if __name__ == '__main__':
    while True:
        delay = 0.0005
        sec = 0.5

        client("[Car]Forward")
        time.sleep(0.5)
        
        # MecanumDriver.carForward_sec(delay, sec)
        # avoidMode(delay, sec)
        # time.sleep(0.5)
        # returnCarFunc(delay, sec)



# go(목적지)
# avoidMode()를 반복해야 할듯
