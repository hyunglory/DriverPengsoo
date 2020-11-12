#-*- coding: utf-8 -*-
import socket
import sys
import MecanumDriver
from command import Command
from command import Device
from mongodb import MongoDB

class server: 

    def __init__(self):
        self.PORT = 9999
        self.BUFSIZE = 256
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('', self.PORT))
        print ('[Server] Pengsoo Server Ready!')

    # 데이터 검증
    def validateData(self, data):        
        ret = False
        
        if (data != ""):
            return False
        data = data.strip()
        print("")
        return ret

    # 분기문
    def controllData(self, data):  
        command = Command()
        device = Device()
        db = MongoDB()      
        start_index = data.find('[')
        data = data[start_index:]
        end_index = data.find("]")
        who = data[:end_index+1]
        cmd = data[end_index+1:]
        print("who:", who)
        print("cmd:", cmd)

        delay = 0.0005   # 테스트중..
        sec = 0.5       # 테스트중..
        
        # 자동차 
        if (who == "[Car]"):            
            if (cmd == command.FOWARD):
                MecanumDriver.carForward_sec(delay,sec)
            elif(cmd == command.REVERSE):
                MecanumDriver.carReverse_sec(delay,sec)
            elif(cmd == command.LEFT):
                MecanumDriver.carLeft_sec(delay,sec)
            elif(cmd == command.RIGHT):
                MecanumDriver.carRight_sec(delay,sec)
            elif(cmd == command.DIR1):
                MecanumDriver.carDir1_sec(delay,sec)
            elif(cmd == command.DIR5):
                MecanumDriver.carDir5_sec(delay,sec)
            elif(cmd == command.DIR7):
                MecanumDriver.carDir7_sec(delay,sec)
            elif(cmd == command.DIR11):
                MecanumDriver.carDir11_sec(delay,sec)
            elif(cmd == command.RIGHT_ROT):
                MecanumDriver.rightRotate_sec(delay,sec)
            elif(cmd == command.LEFT_ROT):
                MecanumDriver.leftRotate_sec(delay,sec)    
            elif(cmd == command.STOP):
                MecanumDriver.carStop()
            elif(cmd == command.TEST):
                MecanumDriver.carTest()
            else:
                MecanumDriver.carStop()

            outputStr = "자동차 이동명령("+cmd+") 실행"
            # db.insert_command_one(cmd, outputStr, device.MOTOR)
           
        elif (who == "[PS]"):
            if (cmd == command.P_UP):
                MecanumDriver.carForward_sec(delay, sec)
            elif(cmd == command.P_DOWN):
                MecanumDriver.carReverse_sec(delay, sec)
            elif(cmd == command.p_LEFT):
                MecanumDriver.carLeft_sec(delay, sec)
            elif(cmd == command.P_RIGHT):
                MecanumDriver.carRight_sec(delay, sec)
            elif(cmd == command.P_STOP):
                MecanumDriver.carStop()

            outputStr = "펭수 음성명령("+cmd+") 실행"
            # db.insert_command_one(cmd, outputStr, device.MOTOR)

        else:
            outputStr = "[미처리] 알수없는 명령("+cmd+") 실행"
            # db.insert_command_one(cmd, outputStr, device.MOTOR)
            print(outputStr)

    # 서버 통신
    def onLineServer(self):
        try:
            while True:
                # 클라이언트로 메시지가 도착하면 다음 줄로 넘어가고
                # 그렇지 않다면 대기(Blocking)
                data, addr = self.server.recvfrom(self.BUFSIZE)  

                # 받은 데이터 Byte형식 String으로 변환
                data=data.decode()
                # 받은 메시지와 클라이언트 주소 화면에 출력
                print('[Server] Received Data : %r from %r' % (data, addr))

                # 데이터검증
                if(self.validateData(data) != False):
                    continue

                # 분기처리
                self.controllData(data)            



                # 받은 메시지를 클라이언트로 다시 전송
                #server.sendto(data, addr)
        except:
            print("[Server] Exception Error!!!", sys.exc_info())    



if __name__ == "__main__":
    sv = server()


