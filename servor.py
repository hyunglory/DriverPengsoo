import RPi.GPIO as GPIO
import time


class hi:
    def __init__(self):
        self.pin =13 #왼
        self.pin2 = 19 #오
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        self.p2=GPIO.PWM(self.pin2,50)
        self.p= GPIO.PWM(self.pin, 50)  #PMW:펄스 폭 변조
        self.cnt = 0
        print("0: 두손 빠르게, 1: 두손 천천히, 2: 왼손들기, 3: 오른손들기, *: 원상태")
    def start(self,a):
        try:
            self.p.start(0)
            self.p2.start(0)
            self.cnt = 0
            while True:
                if a==0:
                    self.p.ChangeDutyCycle(8)
                    self.p2.ChangeDutyCycle(8)
                    time.sleep(0.2)
                    self.p.ChangeDutyCycle(4)
                    self.p2.ChangeDutyCycle(4)
                    time.sleep(0.2)
                    self.cnt += 1
                    if self.cnt != 3:
                        continue
                    self.p.stop()
                    self.p2.stop()
                    break
                elif a==1:
                    for r1 in range(32,110,1):
                        r1=r1/10
                        print(r1)
                        self.p.ChangeDutyCycle(r1)
                        self.p2.ChangeDutyCycle(r1)
                        time.sleep(0.02)
                    for r2 in range(110,32,-1):
                        r2=r2/10
                        print(r2)
                        self.p.ChangeDutyCycle(r2)
                        self.p2.ChangeDutyCycle(r2)
                        time.sleep(0.02)
                    self.p.stop()
                    self.p2.stop()
                    break
                elif a==2:
                    self.p.ChangeDutyCycle(12)
                    time.sleep(0.02)
                    self.p.stop()
                    break
                elif a==3:
                    self.p2.ChangeDutyCycle(12)
                    time.sleep(0.02)
                    self.p2.stop()
                    break
                else:
                    print("원상복귀")
                    self.p.ChangeDutyCycle(7.5)
                    self.p2.ChangeDutyCycle(7.5)
                    time.sleep(0.02)
                    self.p.stop()
                    self.p2.stop()
                    break

        except KeyboardInterrupt:
            self.p.stop()
            self.p2.stop()
            GPIO.cleanup()

if __name__ == "__main__":
    hi=hi()
    hi.start(0)
    hi.start(1)
    hi.start(2)
    hi.start(3)
    hi.start(4)

