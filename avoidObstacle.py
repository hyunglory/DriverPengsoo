import sensor
import servo
import MecanumDriver
import RPi.GPIO as GPIO
import time

FL0 = FR0 = LL0 = LR0 = 0
FL45 = FR45 = LL45 = LR45 = 0
FL90 = FR90 = LL90 = LR90 = 0

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
            MecanumDriver.carStop()
            checkAll()

            if (FL90 < sideLimit or LL90 < sideLimit):
                MecanumDriver.carRight_sec(delay, sec)
                carFunc.append("carRight")    
            elif (FR90 < sideLimit or LR90 < sideLimit):
                MecanumDriver.carLeft_sec(delay, sec)
                carFunc.append("carLeft")
            elif (FL45 > FR45):
                MecanumDriver.carLeft_sec(delay, sec)
                carFunc.append("carLeft")
            else :
                MecanumDriver.carRight_sec(delay, sec)
                carFunc.append("carRight") 
        else:
            MecanumDriver.carForward_sec(delay,sec)
            checkAll()

            if(FL90 > sideLimit and FR90 > sideLimit and LL90 > sideLimit and LR90 > sideLimit):
                returnCarFunc(delay, sec)
                if (carFunc[0] == "carLeft"):
                    MecanumDriver.carLeft_sec(delay,sec)
                    del carFunc[0]
                elif (carFunc[0] == "carRight"):
                    MecanumDriver.carRight_sec(delay, sec)
                    del carFunc[0]
                elif (carFunc == None):
                    MecanumDriver.carStop()
                else:
                    MecanumDriver.carStop()

            else:
                minVal = min(FL90, FR90, LL90, LR90)
                if (minVal < sideLimit):
                    if (minVal == FL90 or minVal == LL90): 
                        MecanumDriver.carRight_sec(delay, sec)
                        carFunc.append("carRight")
                    elif (minVal == FR90 or minVal == LR90):
                        MecanumDriver.carLeft_sec(delay,sec)
                        carFunc.append("carLeft")
                    else:
                        MecanumDriver.carStop()
                    
                        
if __name__ == '__main__':
    while True:
        delay = 0.0005
        sec = 0.5

        MecanumDriver.carForward_sec(delay, sec)
        avoidMode(delay, sec)

# go(목적지)
# avoidMode()를 반복해야 할듯
