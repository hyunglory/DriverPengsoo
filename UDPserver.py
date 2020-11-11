#-*- coding: utf-8 -*-
import socket
import sys
import MecanumDriver
from command import *
from command import Device
from mongodb import MongoDB
from pengsoo import Pengsoo

class server:
    

    def __init__(self):
        self.command = Command()
        self.device = Device()
        self.db = MongoDB()
        self.ps = Pengsoo()
        self.voice = Voice()

        self.PORT = 9999
        self.BUFSIZE = 256
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('', self.PORT))
        print ('[Server] Pengsoo Server Ready!')        
    # 데이터 검증
    def validateData(self, data):
        if (data == None):
            print("[validateData] 비정상 데이터 - NULL")

            return False
        data = data.strip()
        return False

    def carLogic(self, cmd, delay):
        pass

    def pengsooLogic(self, cmd, delay, sec):
        pass        

    # 분기문
    def controllData(self, data):  
        start_index = data.find('[')
        end_index = data.find("]")

        data = data[start_index:]        
        who = data[:end_index+1]
        cmd = data[end_index+1:]
        print("who:",who)
        print("cmd:", cmd)

        delay = 0.005   # 테스트중..
        sec = 0.1       # 테스트중..
        
        # 자동차 
        if (who == "[Car]"):
            #self.carLogic(cmd, delay)
            if (cmd == self.command.FOWARD):
                MecanumDriver.carForward(delay)
            elif(cmd == self.command.REVERSE):
                MecanumDriver.carReverse(delay)
            elif(cmd == self.command.LEFT):
                MecanumDriver.carLeft(delay)
            elif(cmd == self.command.RIGHT):
                MecanumDriver.carRight(delay)
            elif(cmd == self.command.DIR1):
                MecanumDriver.carDir1(delay)
            elif(cmd == self.command.DIR5):
                MecanumDriver.carDir5(delay)
            elif(cmd == self.command.DIR7):
                MecanumDriver.carDir7(delay)
            elif(cmd == self.command.DIR11):
                MecanumDriver.carDir11(delay)
            elif(cmd == self.command.STOP):
                MecanumDriver.carStop()
            elif(cmd == self.command.TEST):
                MecanumDriver.carTest()
            else:
                MecanumDriver.carStop()

            outputStr = "자동차 이동명령("+cmd+") 실행"
            #self.db.insert_command_one(cmd, outputStr, self.device.MOTOR)
            
        # 펭수
        elif (who == "[PS]"):
            #self.pengsooLogic(cmd, delay, sec)
            outputStr = ""
            if(cmd == self.command.P_LOGIN):
                self.ps.speakVoice(self.voice.WELCOME)
            elif(cmd == self.command.P_SPEAK):                
                retText = self.ps.listenVoice()
                outputStr = "I was given a command to'"+retText+"'"
                self.ps.speakVoice(outputStr)

            elif (cmd == self.command.P_UP):
                MecanumDriver.carForward_sec(delay, sec)
            elif(cmd == self.command.P_DOWN):
                MecanumDriver.carReverse_sec(delay, sec)
            elif(cmd == self.command.p_LEFT):
                MecanumDriver.carLeft_sec(delay, sec)
            elif(cmd == self.command.P_RIGHT):
                MecanumDriver.carRight_sec(delay, sec)
            elif(cmd == self.command.P_STOP):
                MecanumDriver.carStop()

            if(outputStr != ""):
                outputStr = "펭수 음성명령("+cmd+") 실행"
            else:
                pass
            self.db.insert_command_one(cmd, outputStr, self.device.MOTOR)

        else:
            outputStr = "[미처리] 알수없는 명령("+cmd+") 실행"
            db.insert_command_one(cmd, outputStr, device.MOTOR)
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
                if(self.validateData(data) == False):
                    continue

                # 분기처리
                self.controllData(data)            



                # 받은 메시지를 클라이언트로 다시 전송
                #server.sendto(data, addr)
        except:
            print("[Server] Exception Error!!!", sys.exc_info())    



if __name__ == "__main__":
    sv = server()
    sv.onLineServer()


