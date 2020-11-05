import RPi.GPIO as GPIO
import time
from sensor import getDistance1
from sensor import getDistance2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class MotorFunction:
    def __init__(self,ena,direction,pul,duration,delay):
        self.ena=ena
        self.direction=direction
        self.pul=pul
        self.duration=duration
        self.delay=delay
        GPIO.setup(ena,GPIO.OUT)
        GPIO.setup(direction,GPIO.OUT)
        GPIO.setup(pul,GPIO.OUT)

    def forward(self):
            GPIO.output(self.ena,GPIO.HIGH)
            GPIO.output(self.direction,GPIO.HIGH)
            
            GPIO.output(self.pul,GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.pul,GPIO.LOW)
            time.sleep(self.delay)
            
        
    def reverse(self):
            GPIO.output(self.ena, GPIO.HIGH)
            GPIO.output(self.direction, GPIO.LOW)
            GPIO.output(self.pul, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.pul, GPIO.LOW)
            time.sleep(self.delay)
        

    def stop(self):
        GPIO.output(self.ena, GPIO.LOW)
        return

    def speed(self,speed):
        self.delay = 0.00001 % speed
        return self.delay

    def DirRev(self):
        GPIO.output(self.direction, GPIO.LOW)

    def DirFor(self):
        GPIO.output(self.direction, GPIO.HIGH)
        
    def Testforward(self):
        GPIO.output(self.ena,GPIO.HIGH)
        #GPIO.output(self.direction,GPIO.HIGH)
                            
        GPIO.output(self.pul,GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.pul,GPIO.LOW)
        time.sleep(self.delay)

def setDelay(delay):
    motorFL.speed(delay)
    motorFR.speed(delay)    
    motorRL.speed(delay)
    motorRR.speed(delay)

def carForward():
    motorFL.forward()
    motorFR.forward()    
    motorRL.forward()
    motorRR.forward()

def carReverse():
    motorFL.reverse()
    motorFR.reverse()    
    motorRL.reverse()
    motorRR.reverse()

def carLeft():
    motorFL.reverse()
    motorFR.forward()
    motorRL.forward()
    motorRR.reverse()

def carRight():
    motorFL.forward()
    motorFR.reverse()
    motorRL.reverse()
    motorRR.forward()

def carDir11():  # 11시 
    motorFR.forward()
    motorRL.forward()

def carDir1():   # 1시
    motorFL.forward()
    motorRR.forward()

def carDir7():  # 7시 
    motorFL.reverse()
    motorRR.reverse()

def carDir5():  # 5시
    motorFR.reverse()
    motorRL.reverse()

def rightRotate():
    motorFL.forward()
    motorFR.reverse()
    motorRL.forward()
    motorRR.reverse()

def leftRotate():
    motorFL.reverse()
    motorFR.forward()
    motorRL.reverse()
    motorRR.forward()

def carStop():
    motorFL.stop()
    motorFR.stop()
    motorRL.stop()
    motorRR.stop()

def carDirFor():
    motorFL.DirFor()
    motorFR.DirFor()
    motorRL.DirFor()
    motorRR.DirFor()
    
def carDirRev():
    motorFL.DirRev()
    motorFR.DirRev()
    motorRL.DirRev()
    motorRR.DirRev()

def carTestForward():
    motorFL.Testforward()
    motorFR.Testforward()    
    motorRL.Testforward()
    motorRR.Testforward()

def startFor(method,delay):  # delay초 동안만 실행
    delay = delay
    close_time = time.time() + delay
    while True:
        method()
        if time.time() > close_time:
            break


motorFL=MotorFunction(22, 27, 17, 1600, 0.0001)
motorFR=MotorFunction(25, 24, 23, 1600, 0.0001)
motorRL=MotorFunction(26, 19, 13, 1600, 0.0001)
motorRR=MotorFunction(21, 20, 16, 1600, 0.0001)



while True:
    Fsensor = getDistance1()
    Bsensor = getDistance2()

    
    startFor(carTestForward,1)
    if Fsensor < 100:
        carStop()
        carDirRev()
    elif Bsensor < 100:
        carStop()
        carDirFor()
          

    
    

    