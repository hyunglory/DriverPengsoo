#초음파센서 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  
TRIG1 = 10 #front
ECHO1 = 9
TRIG2 = 18 #behind
ECHO2 = 12

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.setwarnings(False)

def getDistance1():
    GPIO.output(TRIG1, False)
    time.sleep(0.000001)
    GPIO.output(TRIG1, True)
    time.sleep(0.000001)
    GPIO.output(TRIG1, False)

    while GPIO.input(ECHO1) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO1) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end-pulse_start
    distance1 = round(pulse_duration * 17150, 2)
        
    return distance1

def getDistance2():
    GPIO.output(TRIG2, False)
    time.sleep(0.000001)
    GPIO.output(TRIG2, True)
    time.sleep(0.000001)
    GPIO.output(TRIG2, False)

    while GPIO.input(ECHO2) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO2) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end-pulse_start
    distance2 = round(pulse_duration * 17150, 2)
        
    return distance2

if __name__ == '__main__':
    try:
        while True:
            print("front :" + str(getDistance1()))
            print("behind :" + str(getDistance2()))

    except KeyboardInterrupt:
        GPIO.cleanup()