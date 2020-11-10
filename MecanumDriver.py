import RPi.GPIO as GPIO
import time
from sensor import getDistance1
from sensor import getDistance2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class MotorFunction:
    def __init__(self,ena,direction,pul):
        self.ena=ena
        self.direction=direction
        self.pul=pul

        GPIO.setup(ena,GPIO.OUT)
        GPIO.setup(direction,GPIO.OUT)
        GPIO.setup(pul,GPIO.OUT)

    def forwardon(self):
            GPIO.output(self.ena,GPIO.HIGH)
            GPIO.output(self.direction,GPIO.HIGH)
            GPIO.output(self.pul,GPIO.HIGH)
            
    def forwardoff(self):
            GPIO.output(self.pul,GPIO.LOW)
    
    def reverseon(self):
            GPIO.output(self.ena, GPIO.HIGH)
            GPIO.output(self.direction, GPIO.LOW)
            GPIO.output(self.pul, GPIO.HIGH)
            
    def reverseoff(self):        
            GPIO.output(self.pul, GPIO.LOW)
            
    def stop(self):
        GPIO.output(self.ena, GPIO.LOW)

    def DirRev(self):
        GPIO.output(self.direction, GPIO.LOW)

    def DirFor(self):
        GPIO.output(self.direction, GPIO.HIGH)
        
    def Testforward(self):
        GPIO.output(self.ena,GPIO.HIGH)
        GPIO.output(self.pul,GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(self.pul,GPIO.LOW)
        time.sleep(0.0005)

def carForward_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.forwardon()     #    
        motorFR.forwardon()     #    
        motorRL.forwardon()     #
        motorRR.forwardon()     #
        time.sleep(delay)       #
        motorFL.forwardoff()    #
        motorFR.forwardoff()    #
        motorRL.forwardoff()    #
        motorRR.forwardoff()    #
        time.sleep(delay)       #
        if time.time() > close_time:
            break
   

def carReverse_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.reverseon()
        motorFR.reverseon()    
        motorRL.reverseon()
        motorRR.reverseon()
        time.sleep(delay)
        motorFL.reverseoff()
        motorFR.reverseoff()    
        motorRL.reverseoff()
        motorRR.reverseoff()
        time.sleep(delay)
        if time.time() > close_time:
            break
    
def carLeft_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.reverseon()
        motorFR.forwardon()
        motorRL.forwardon()
        motorRR.reverseon()
        time.sleep(delay)
        motorFL.reverseoff()
        motorFR.forwardoff()
        motorRL.forwardoff()
        motorRR.reverseoff()
        time.sleep(delay)
        if time.time() > close_time:
            break
    
def carRight_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.forwardon()
        motorFR.reverseon()
        motorRL.reverseon()
        motorRR.forwardon()
        time.sleep(delay)
        motorFL.forwardoff()
        motorFR.reverseoff()
        motorRL.reverseoff()
        motorRR.forwardoff()
        time.sleep(delay)
        if time.time() > close_time:
            break

def carDir11_sec(delay, sec):  # 11시 
    close_time = time.time() + sec
    while True:
        motorFR.forwardon()
        motorRL.forwardon()
        time.sleep(delay)
        motorFR.forwardoff()
        motorRL.forwardoff()
        time.sleep(delay)
        if time.time() > close_time:
            break
    
def carDir1_sec(delay, sec):   # 1시
    close_time = time.time() + sec
    while True:
        motorFL.forwardon()
        motorRR.forwardon()
        time.sleep(delay)
        motorFL.forwardoff()
        motorRR.forwardoff()
        time.sleep(delay)
        if time.time() > close_time:
            break
    
def carDir7_sec(delay, sec):  # 7시 
    close_time = time.time() + sec
    while True:
        motorFL.reverseon()
        motorRR.reverseon()
        time.sleep(delay)
        motorFL.reverseoff()
        motorRR.reverseoff()
        time.sleep(delay)
        if time.time() > close_time:
            break

def carDir5_sec(delay, sec):  # 5시
    close_time = time.time() + sec
    while True:
        motorFR.reverseon()
        motorRL.reverseon()
        time.sleep(delay)
        motorFR.reverseoff()
        motorRL.reverseoff()
        time.sleep(delay)
        if time.time() > close_time:
            break

def rightRotate_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.forwardon()
        motorFR.reverseon()
        motorRL.forwardon()
        motorRR.reverseon()
        time.sleep(delay)
        motorFL.forwardoff()
        motorFR.reverseoff()
        motorRL.forwardoff()
        motorRR.reverseoff()
        time.sleep(delay)
        if time.time() > close_time:
            break

def leftRotate_sec(delay, sec):
    close_time = time.time() + sec
    while True:
        motorFL.reverseon()
        motorFR.forwardon()
        motorRL.reverseon()
        motorRR.forwardon()
        time.sleep(delay)
        motorFL.reverseoff()
        motorFR.forwardoff()
        motorRL.reverseoff()
        motorRR.forwardoff()
        time.sleep(delay)
        if time.time() > close_time:
            break

def carForward(delay):
    motorFL.forwardon()     #    
    motorFR.forwardon()     #    
    motorRL.forwardon()     #
    motorRR.forwardon()     #
    time.sleep(delay)       #
    motorFL.forwardoff()    #
    motorFR.forwardoff()    #
    motorRL.forwardoff()    #
    motorRR.forwardoff()    #
    time.sleep(delay)       #
        
   

def carReverse(delay):
    motorFL.reverseon()
    motorFR.reverseon()    
    motorRL.reverseon()
    motorRR.reverseon()
    time.sleep(delay)
    motorFL.reverseoff()
    motorFR.reverseoff()    
    motorRL.reverseoff()
    motorRR.reverseoff()
    time.sleep(delay)
        
    
def carLeft(delay):
    motorFL.reverseon()
    motorFR.forwardon()
    motorRL.forwardon()
    motorRR.reverseon()
    time.sleep(delay)
    motorFL.reverseoff()
    motorFR.forwardoff()
    motorRL.forwardoff()
    motorRR.reverseoff()
    time.sleep(delay)
    
def carRight(delay):
    motorFL.forwardon()
    motorFR.reverseon()
    motorRL.reverseon()
    motorRR.forwardon()
    time.sleep(delay)
    motorFL.forwardoff()
    motorFR.reverseoff()
    motorRL.reverseoff()
    motorRR.forwardoff()
    time.sleep(delay)

def carDir11(delay):  # 11시 
    motorFR.forwardon()
    motorRL.forwardon()
    time.sleep(delay)
    motorFR.forwardoff()
    motorRL.forwardoff()
    time.sleep(delay)

    
def carDir1(delay):   # 1시
    motorFL.forwardon()
    motorRR.forwardon()
    time.sleep(delay)
    motorFL.forwardoff()
    motorRR.forwardoff()
    time.sleep(delay)

    
def carDir7(delay):  # 7시 
    motorFL.reverseon()
    motorRR.reverseon()
    time.sleep(delay)
    motorFL.reverseoff()
    motorRR.reverseoff()
    time.sleep(delay)


def carDir5(delay):  # 5시
    motorFR.reverseon()
    motorRL.reverseon()
    time.sleep(delay)
    motorFR.reverseoff()
    motorRL.reverseoff()
    time.sleep(delay)
 

def rightRotate(delay):
    motorFL.forwardon()
    motorFR.reverseon()
    motorRL.forwardon()
    motorRR.reverseon()
    time.sleep(delay)
    motorFL.forwardoff()
    motorFR.reverseoff()
    motorRL.forwardoff()
    motorRR.reverseoff()
    time.sleep(delay)

def leftRotate(delay):
    motorFL.reverseon()
    motorFR.forwardon()
    motorRL.reverseon()
    motorRR.forwardon()
    time.sleep(delay)
    motorFL.reverseoff()
    motorFR.forwardoff()
    motorRL.reverseoff()
    motorRR.forwardoff()
    time.sleep(delay)

    
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

#def startFor(method,sec):  # sec 초 동안만 실행
#    close_time = time.time() + sec
#    while True:
#        method()
#        if time.time() > close_time:
#            break

motorFL=MotorFunction(22, 27, 17)
motorFR=MotorFunction(25, 24, 23)
motorRL=MotorFunction(26, 19, 13)
motorRR=MotorFunction(21, 20, 16)


if __name__ == '__main__':
    try:
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

    except KeyboardInterrupt:
        carStop()      

    
    

    
