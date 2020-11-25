import servo
import sensor
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

class Mapping:
    def __int__(self):
        self.mapServo = 5
        self.frequence = 50
        self.height = 550
        self.width = 1000

        GPIO.setup(self, self.mapServo, GPIO.OUT)
        self.servoPwm = GPIO.PWM(self.mapServo, self.frequence)
        self.servoPwm.start(servo.angle_to_percent(0))
        
        self.firstData = {}
        self.secondData = {}        
    
    def getData(self):
        self.servoPwm.start(servo.angle_to_percent(0))
        for i in range(0, 181, 1):    
            ii = i / 180 * 100
            if (0 <= ii and ii <= 100):
                self.servoPwm.ChangeDutyCycle(servo.angle_to_percent(ii))
                self.firstData[i] = int(sensor.MAPgetDistance())
            time.sleep(0.1)

    def draw(self, data):
        img = np.zeros((self.height, self.width, 3), np.uint8)
        startX = self.width/2
        startX = int(startX)
        startY = self.height - 10
        startY = int(startY)
        start = (int(startX), (startY)) # (300,390)

        dataKey = list(data.keys())
        valueKey = list(data.values())

        # print(len(dataKey)) # = 181
        # print(len(valueKey)) # = 181

        angle = []
        length = []

        cv2.circle(img, start, 8, (0, 0, 255), -1)

        for i in range(0, len(dataKey)):
            angle.append(dataKey[i])
            length.append(valueKey[i])
            
            destX = length[i] * np.cos(angle[i]*(np.pi/180))
            destY = length[i] * np.sin(angle[i]*(np.pi/180))
            
            destX = int(destX)
            #print("destX" + str(destX))
            destY = int(destY)        
            #print("destY" + str(destY))        
            if(angle[i] <= 90):
                destX = startX + destX 
                destY = startY - destY 
            elif(angle[i] <= 180):
                destX = startX + destX
                destY = startY - destY
            else:
                continue
            
            # Ranging distance: 2cm – 500 cm, Effectual angle: <15°
            if ( 2 <= length[i] & length[i] < 500 ):
                destination = (destX, destY)
                #cv2.line(img, start, destination, (255, 0, 0))
                cv2.circle(img, destination, 3, (0, 255, 0),-1)
            
            #print(str(angle[i]) + "도, " + str(length[i]) + "cm " + "destination (" + str(destX) + "," + str(destY) + ")")
            
        cv2.imshow('MAP',img)
        cv2.waitKey(0)

if __name__ == '__main__':
    mp = Mapping()
    try:
        mp.getData()
        mp.draw(mp.firstData)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        cv2.destroyAllWindows()