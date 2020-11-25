#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  

FLTRIG = 27 #FL
FLECHO = 22
FRTRIG = 23   #FR
FRECHO = 24
LLTRIG = 19
LLECHO = 26
LRTRIG = 20
LRECHO = 21
MAPTRIG = 15
MAPECHO = 18

GPIO.setup(FLTRIG, GPIO.OUT)
GPIO.setup(FLECHO, GPIO.IN)
GPIO.setup(FRTRIG, GPIO.OUT)
GPIO.setup(FRECHO, GPIO.IN)
GPIO.setup(LLTRIG, GPIO.OUT)
GPIO.setup(LLECHO, GPIO.IN)
GPIO.setup(LRTRIG, GPIO.OUT)
GPIO.setup(LRECHO, GPIO.IN)
GPIO.setup(MAPTRIG, GPIO.OUT)
GPIO.setup(MAPECHO, GPIO.IN)


GPIO.setwarnings(False)

def MAPgetDistance():
    
    GPIO.output(MAPTRIG, False)
    time.sleep(0.0001)
    GPIO.output(MAPTRIG, True)
    time.sleep(0.0001)
    GPIO.output(MAPTRIG, False)
    
    while GPIO.input(MAPECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(MAPECHO) == 1:
        pulse_end = time.time()
        
        

    pulse_duration = pulse_end-pulse_start
    distance = round(pulse_duration * 17150, 2)

    if (distance > 500):
        distance = 500

    return distance

def FLgetDistance():
    
    GPIO.output(FLTRIG, False)
    time.sleep(0.0001)
    GPIO.output(FLTRIG, True)
    time.sleep(0.0001)
    GPIO.output(FLTRIG, False)
    
    while GPIO.input(FLECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(FLECHO) == 1:
        pulse_end = time.time()
        
        

    pulse_duration = pulse_end-pulse_start
    distance = round(pulse_duration * 17150, 2)

    if (distance > 500):
        distance = 500

    return distance

def FRgetDistance():
    GPIO.output(FRTRIG, False)
    time.sleep(0.0001)
    GPIO.output(FRTRIG, True)
    time.sleep(0.0001)
    GPIO.output(FRTRIG, False)

    while GPIO.input(FRECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(FRECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end-pulse_start
    distance = round(pulse_duration * 17150, 2)

    if (distance > 500):
        distance = 500
        
    return distance

def LLgetDistance():
    GPIO.output(LLTRIG, False)
    time.sleep(0.0001)
    GPIO.output(LLTRIG, True)
    time.sleep(0.0001)
    GPIO.output(LLTRIG, False)

    while GPIO.input(LLECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(LLECHO) == 1:
        
        pulse_end = time.time()

    pulse_duration = pulse_end-pulse_start
    distance = round(pulse_duration * 17150, 2)

    if (distance > 500):
        distance = 500
        
    return distance

def LRgetDistance():
    GPIO.output(LRTRIG, False)
    time.sleep(0.0001)
    GPIO.output(LRTRIG, True)
    time.sleep(0.0001)
    GPIO.output(LRTRIG, False)

    while GPIO.input(LRECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(LRECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end-pulse_start
    distance = round(pulse_duration * 17150, 2)

    if (distance > 500):
        distance = 500
        
    return distance


if __name__ == '__main__':
    try:
        while True:
            
            print("FL " + str(FLgetDistance()))
            print("FR " + str(FRgetDistance()))
            print("LL " + str(LLgetDistance()))
            print("LR " + str(LRgetDistance()))
            time.sleep(0.5)
            print("------------------------------------------")
            

    except KeyboardInterrupt:
        GPIO.cleanup()
