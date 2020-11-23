#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Use Board numerotation mode
GPIO.setwarnings(False) #Disable warnings


#FL, FR, LL, LR Init

frequence = 50
FLpwm_gpio = 5
FRpwm_gpio = 18
LLpwm_gpio = 19
LRpwm_gpio = 26

GPIO.setup(FLpwm_gpio, GPIO.OUT)
GPIO.setup(FRpwm_gpio, GPIO.OUT)
#GPIO.setup(LLpwm_gpio, GPIO.OUT)
#GPIO.setup(LRpwm_gpio, GPIO.OUT)

FLpwm = GPIO.PWM(FLpwm_gpio, frequence)
FRpwm = GPIO.PWM(FRpwm_gpio, frequence)
#LLpwm = GPIO.PWM(LLpwm_gpio, frequence)
#LRpwm = GPIO.PWM(LRpwm_gpio, frequence)

#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4   # 0도 4%, 180도 12.5%
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

def pwmGo(angle):

    FLpwm.start(angle_to_percent(0))
    FRpwm.start(angle_to_percent(0))
    FLpwm.ChangeDutyCycle(angle_to_percent(abs(angle)))
    FRpwm.ChangeDutyCycle(angle_to_percent(abs(angle-110)))
    #LLpwm.start(angle_to_percent(angle))
    #LRpwm.start(angle_to_percent(angle))

def pwmStop():

    FLpwm.stop()
    FRpwm.stop()
    #LLpwm.stop()
    #LRpwm.stop()

    GPIO.cleanup()

def startFor(method,sec):  # sec 초 동안만 실행
   close_time = time.time() + sec
   while True:
       method()
       if time.time() > close_time:
           break

if __name__ == '__main__':
    while True:
        pwmGo(0)
        print("0도")
        time.sleep(0.5)
        pwmGo(55)
        print("45도")
        time.sleep(0.5)
        pwmGo(110)
        print("90도")
        time.sleep(0.5)
