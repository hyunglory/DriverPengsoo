import sys
import smbus
import math
import time
from time import sleep  # time module
import RPi.GPIO as GPIO
from UDPserver import server
import socket


class mpu6050:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        servoPin=14 #서보모터 핀위치를 '빨갈주'로 변경하여 5V위치에 설치 
        GPIO.setup(servoPin, GPIO.OUT)
        self.pwm = GPIO.PWM(servoPin,50)
        self.pwm.start(7.3) #서보 초기 시작위치 지정 

        # slave address
        self.DEV_ADDR = 0x68         # device address
        # register address
        self.ACCEL_XOUT = 0x3b
        self.ACCEL_YOUT = 0x3d
        self.ACCEL_ZOUT = 0x3f
        self.TEMP_OUT = 0x41
        self.GYRO_XOUT = 0x43
        self.GYRO_YOUT = 0x45
        self.GYRO_ZOUT = 0x47
        self.PWR_MGMT_1 = 0x6b       # PWR_MGMT_1
        self.PWR_MGMT_2 = 0x6c       # PWR_MGMT_2

        self.bus = smbus.SMBus(1)                  
        self.bus.write_byte_data(self.DEV_ADDR, self.PWR_MGMT_1, 0)

        self.temperature = 24.0


    # Sub function
    # 1byte read
    def read_byte(self, adr):
        return self.bus.read_byte_data(self.DEV_ADDR, adr)
    # 2byte read
    def read_word(self, adr):
        high = self.bus.read_byte_data(self.DEV_ADDR, adr)
        low = self.bus.read_byte_data(self.DEV_ADDR, adr+1)
        val = (high << 8) + low
        return val
    # Sensor data read
    def read_word_sensor(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):         # minus
            return -((65535 - val) + 1)
        else:                       # plus
            return val
    #
    #
    def get_temp(self):
        temp = self.read_word_sensor(self.TEMP_OUT)
        x = temp / 340 + 36.53      # data sheet(register map)
        return x

    # (full scale range ±250 deg/s
    #        LSB sensitivity 131 LSB/deg/s
    #        -> ±250 x 131 = ±32750 LSB[16bit])
    #   Gyroscope Configuration GYRO_CONFIG (reg=0x1B)
    #   FS_SEL(Bit4-Bit3)でfull scale range/LSB sensitivit.
    #
    # get gyro data
    def get_gyro_data_lsb(self, ):
        x = self.read_word_sensor(self.GYRO_XOUT)
        y = self.read_word_sensor(self.GYRO_YOUT)
        z = self.read_word_sensor(self.GYRO_ZOUT)
        return [x, y, z]
    def get_gyro_data_deg(self, ):
        x,y,z = self.get_gyro_data_lsb()
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
    def get_accel_data_lsb(self):
        x = self.read_word_sensor(self.ACCEL_XOUT)
        y = self.read_word_sensor(self.ACCEL_YOUT)
        z = self.read_word_sensor(self.ACCEL_ZOUT)
        return [x, y, z]
    # get accel data
    def get_accel_data_g(self):
        x,y,z = self.get_accel_data_lsb()
        x = x / 16384.0
        y = y / 16384.0
        z = z / 16384.0
        return [x, y, z]

    #-----------------------------------
    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def get_z_rotation(self, x,y,z):
        radians = math.atan2(z, self.dist(x,y))
        return math.degrees(radians)



    #___________________________________________
    #20190413 모터콘트롤 함수부분 
    def aa_bb(self, ):
    
        x_angle=self.get_x_rotation(accel_x, accel_y, accel_z)
        for i in range(3,13): #3에서 12까지 숫자 생성

            # desiredPosition=x_angle
            # DC=1./18*(desiredPosition)+7.3 #<<<7.3서보의 중간위치값 
            # pwm.ChangeDutyCycle(DC)
    #___________________________________________        
            if x_angle > 3:
                bb = "<<____"
            elif x_angle < -3:
                bb = "____>>"
            else:
                bb = "__==__"

            return bb
    #___________________________________________

    


if __name__ == "__main__":

    mpu = mpu6050()

    try:        
        while (1):
            temp = mpu.get_temp()
            add = (temp-4)
            
            accel_x,accel_y,accel_z = mpu.get_accel_data_g()
            x_angle = mpu.get_x_rotation(accel_x, accel_y, accel_z) #y각도값
            
            bb = mpu.aa_bb() #모터콘트롤 함수호출 실행 
        
            print("Temp:%04.1f""`C"% add,
                "| Angle",
                "x:%3.2f " % mpu.get_x_rotation(accel_x, accel_y, accel_z),
                "Direction: %s"  % bb)
        
    #              "x:%06.3f " % get_x_rotation(accel_x, accel_y, accel_z),
    #              "y:%06.3f " % get_y_rotation(accel_x, accel_y, accel_z),
    #              "z:%06.3f " % get_z_rotation(accel_x, accel_y, accel_z),
    #              "Dir.: %s"  % bb)
            
            
            msg = '%04.1f'% add
            mpu.temperature = msg
            # print(msg)
            # server.sendMessage(msg)
            # sleep(1)


            with socket.socket() as s:
                s.connect(('192.168.0.25', 9999))
                line = input('42')
                s.sendall(line.encode())
                res = s.recv(1024)
                print('send.....end....')



    except KeyboardInterrupt:
        print("     == stop ==")
    
    mpu.pwm.stop()
    GPIO.cleanup()
