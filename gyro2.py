# -eHan`- coding: utf-8 -*-
#!/usr/bin/python
import sys
import smbus
import math
import time
from time import sleep  # time module
import RPi.GPIO as GPIO
#__________________________________
GPIO.setmode(GPIO.BCM)
servoPin=14 #서보모터 핀위치를 '빨갈주'로 변경하여 5V위치에 설치 
GPIO.setup(servoPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin,50)
pwm.start(7.3) #서보 초기 시작위치 지정 
#__________________________________
# define
# slave address
DEV_ADDR = 0x68         # device address
# register address
ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
PWR_MGMT_1 = 0x6b       # PWR_MGMT_1
PWR_MGMT_2 = 0x6c       # PWR_MGMT_2

bus = smbus.SMBus(1)                  
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)


# Sub function
# 1byte read
def read_byte(adr):
    return bus.read_byte_data(DEV_ADDR, adr)
# 2byte read
def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8) + low
    return val
# Sensor data read
def read_word_sensor(adr):
    val = read_word(adr)
    if (val >= 0x8000):         # minus
        return -((65535 - val) + 1)
    else:                       # plus
        return val
#
#
def get_temp():
    temp = read_word_sensor(TEMP_OUT)
    x = temp / 340 + 36.53      # data sheet(register map)
    return x

# (full scale range ±250 deg/s
#        LSB sensitivity 131 LSB/deg/s
#        -> ±250 x 131 = ±32750 LSB[16bit])
#   Gyroscope Configuration GYRO_CONFIG (reg=0x1B)
#   FS_SEL(Bit4-Bit3)でfull scale range/LSB sensitivit.
#
# get gyro data
def get_gyro_data_lsb():
    x = read_word_sensor(GYRO_XOUT)
    y = read_word_sensor(GYRO_YOUT)
    z = read_word_sensor(GYRO_ZOUT)
    return [x, y, z]
def get_gyro_data_deg():
    x,y,z = get_gyro_data_lsb()
    x = x / 131.0
    y = y / 131.0
    z = z / 131.0
    return [x, y, z]
#
# (full scale range ±2g
#        LSB sensitivity 16384 LSB/g)
#        -> ±2 x 16384 = ±32768 LSB[16bit])
#   Accelerometer Configuration ACCEL_CONFIG (reg=0x1C)
#   AFS_SEL(Bit4-Bit3)でfull scale range/LSB sensitivity.
#
# get accel data
def get_accel_data_lsb():
    x = read_word_sensor(ACCEL_XOUT)
    y = read_word_sensor(ACCEL_YOUT)
    z = read_word_sensor(ACCEL_ZOUT)
    return [x, y, z]
# get accel data
def get_accel_data_g():
    x,y,z = get_accel_data_lsb()
    x = x / 16384.0
    y = y / 16384.0
    z = z / 16384.0
    return [x, y, z]

#-----------------------------------
def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)



#___________________________________________
#20190413 모터콘트롤 함수부분 
def aa_bb():
 
    x_angle=get_x_rotation(accel_x, accel_y, accel_z)
    for i in range(3,13): #3에서 12까지 숫자 생성

        desiredPosition=x_angle
        DC=1./18*(desiredPosition)+7.3 #<<<7.3서보의 중간위치값 
        pwm.ChangeDutyCycle(DC)
#___________________________________________        
        if x_angle > 3:
            bb = "<<____"
        elif x_angle < -3:
            bb = "____>>"
        else:
            bb = "__==__"

        return bb
#___________________________________________

try:
       
    while (1):
        temp = get_temp()
        add = (temp-4)
        
        accel_x,accel_y,accel_z = get_accel_data_g()
        x_angle = get_x_rotation(accel_x, accel_y, accel_z) #y각도값
        
        bb = aa_bb() #모터콘트롤 함수호출 실행 
       
        print("Temp:%04.1f""`C"% add,
              "| Angle",
              "x:%3.2f " % get_x_rotation(accel_x, accel_y, accel_z),
              "Direction: %s"  % bb)
      
#              "x:%06.3f " % get_x_rotation(accel_x, accel_y, accel_z),
#              "y:%06.3f " % get_y_rotation(accel_x, accel_y, accel_z),
#              "z:%06.3f " % get_z_rotation(accel_x, accel_y, accel_z),
#              "Dir.: %s"  % bb)
         
        print 
#        sleep(0.1)

except KeyboardInterrupt:
    print("     == stop ==")

pwm.stop()
GPIO.cleanup()
