import sensor
import servo
import MecanumDriver
import RPi.GPIO as GPIO
import time

FL0, FR0, LL0, LR0
FL45, FR45, LL45, LR45
FL90, FR90, LL90, LR90

FowardBehindLimit = 10
sideLimit = 5
diagonalLimit = 15

carFunc = []

def returnCarFunc(delay, sec):
    for i in carFunc:
        if (carFunc[i] == "carLeft"):
            carFunc[i] == "carRight"
        elif (carFunc[i] == "carRight"):
            carFunc[i] == "carLeft"
        else :
            carFunc[i] == "wrong value"
    
    for i in carFunc:
        if (carFunc[i] == "carLeft"):
            carLeft_sec(delay, sec)
        elif (carFunc[i] == "carRight"):
            carRight_sec(delay, sec)
        else :
            carStop()
    
    

def checkFront():
    pwmGo(0)    # 앞뒤 방향
    FL0 = FLgetDistance()
    FR0 = FRgetDistance()
    LL0 = LLgetDistance()
    LR0 = LRgetDistance()

def checkAll(): # 전체 센서 값 저장
    
    pwmGo(0)    # 앞뒤 방향
    FL0 = FLgetDistance()
    FR0 = FRgetDistance()
    LL0 = LLgetDistance()
    LR0 = LRgetDistance()

    pwmGo(45)   # 대각선 방향
    FL45 = FLgetDistance()
    FR45 = FRgetDistance()
    LL45 = LLgetDistance()
    LR45 = LRgetDistance()

    pwmGo(90)   # 측면 방향
    FL90 = FLgetDistance()   
    FR90 = FRgetDistance()
    LL90 = LLgetDistance()
    LR90 = LRgetDistance()

def avoidMode(delay, sec):
    
    while True : # 현재 그 좌표아니면
        #go(좌표+)
        checkAll()

        if (FL0 < FowardBehindLimit or FR0 < FowardBehindLimit):
            carStop()
            checkAll()

            if (FL90 < sideLimit or LL90 < sideLimit):
                carRight_sec(delay, sec)
                carFunc.append("carRight")    
            elif (FR90 < sideLimit or LR90 < sideLimit):
                carLeft_sec(delay, sec)
                carFunc.append("carLeft")
            elif (FL45 > FR45):
                carLeft_sec(delay, sec)
                carFunc.append("carLeft")
            else :
                carRight_sec(delay, sec)
                carFunc.append("carRight") 
        else:
            carForward_sec(delay,sec)
            checkAll()

            if(FL90 > sideLimit and FR90 > sideLimit and LL90 > sideLimit and LR90 > sideLimit):
                returnCarFunc()
                if (carFunc[0] == "carLeft"):
                    carLeft_sec(delay,sec)
                    del carFunc[0]
                elif (carFunc[0] == "carRight"):
                    carRight_sec(delay, sec)
                    del carFunc[0]
                else:
                    carStop()

            else:
                minVal = min(FL90, FR90, LL90, LR90)
                if (minVal < sideLimit):
                    if (minVal == FL90 or minVal == LL90): 
                        carRight_sec(delay, sec)
                        carFunc.append("carRight")
                    elif (minVal == FR90 or minVal == LR90):
                        carLeft_sec(delay,sec)
                        carFunc.append("carLeft")
                    else:
                        carStop()
                    
                        
if __name__ == '__main__':
    try:
        delay = 0.0005
        sec = 0.5

        carForward_sec(delay, sec)
        avoidMode(delay, sec)