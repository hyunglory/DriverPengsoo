from smbus2 import SMBus
from bitstring import Bits
import math
import time
import RPi.GPIO as GPIO
 
bus = SMBus(1)
DEV_ADDR = 0x68
 
register_gyro_xout_h = 0x43
register_gyro_yout_h = 0x45
register_gyro_zout_h = 0x47
sensitive_gyro = 131.0
 
register_accel_xout_h = 0x3B
register_accel_yout_h = 0x3D
register_accel_zout_h = 0x3F
sensitive_accel = 16384.0
 
def read_data(register):
    high = bus.read_byte_data(DEV_ADDR,register)
    low = bus.read_byte_data(DEV_ADDR,register+1)
    val = (high << 8) + low
    return val
 
def twocomplements(val):
    s = Bits(uint=val,length=16)
    return s.int
 
def gyro_dps(val):
    return twocomplements(val)/sensitive_gyro
 
def accel_g(val):
    return twocomplements(val)/sensitive_accel
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_x_rotation(x,y,z):
    radians = math.atan(x/dist(y,z))
    return radians
 
def get_y_rotation(x,y,z):
    radians = math.atan(y/dist(x,z))
    return radians
 
bus.write_byte_data(DEV_ADDR,0x6B,0b00000000)

GPIO.setmode(GPIO.BCM)
 
# LED1 = 18
# LED2 = 23
 
# GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)
print("test----------------------")
 
try:
    while True:
        x = read_data(register_accel_xout_h)
        print(x)
        y = read_data(register_accel_yout_h)
        print(y)
        z = read_data(register_accel_zout_h)
        print(z)
        # aX = get_x_rotation(accel_g(x),accel_g(y),accel_g(z))
        # print(aX)
        # aY = get_y_rotation(accel_g(x),accel_g(y),accel_g(z))
        # print(aY)
        # data = str(aX) + ' , ' + str(aY) + '$'
 
        # if aX > 0.7 or aX < -0.5:
        #     print("on LED1")
        #     # GPIO.output(LED1, GPIO.HIGH)
        # else:
        #     GPIO.output(LED1, GPIO.LOW)
 
        # if aY < -0.5 or aY > 0.5:
        #     print("on LED2")
        #     # GPIO.output(LED2, GPIO.HIGH)
        # else:
        #     pass
        #     # GPIO.output(LED2, GPIO.LOW)
 
        # print(data)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("\nInterrupted!")
except:
    print("\nClosing socket")
finally:
    bus.close()
GPIO.cleanup()