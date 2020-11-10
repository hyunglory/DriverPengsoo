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
        self.onLineServer()
        self.command = Command()
        self.device = Device()
        self.db = MongoDB()

    # 데이터 검증
    def validateData(self, data):
        ret = False
        if (data.notnull()):
            return False
        data = data.strip()
        print("")
        return ret

    # 분기문
    def controllData(self, data):        
        start_index = data.find('[')
        data = data[start_index:]
        end_index = data.find("]")
        who = data[:end_index]
        cmd = data[end_index+1:]
        print("who:",who)

        if (who == "[Car]"):

            delay = 0.005 # 테스트중..
            sec = 0.1 #테스트중..
            
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
            else:
                MecanumDriver.carStop()

            outputStr = "자동차 이동명령("+cmd+") 실행"
            self.db.insert_command_one(cmd, outputStr, self.device.MOTOR)
           
        elif (who == "[PS]"):
            if (cmd == self.command.P_UP):
                MecanumDriver.carForward_sec(delay, sec)
            elif(cmd == self.command.P_DOWN):
                MecanumDriver.carReverse_sec(delay, sec)
            elif(cmd == self.command.p_LEFT):
                MecanumDriver.carLeft_sec(delay, sec)
            elif(cmd == self.command.P_RIGHT):
                MecanumDriver.carRight_sec(delay, sec)
            elif(cmd == self.command.P_STOP):
                MecanumDriver.carStop()

            outputStr = "펭수 음성명령("+cmd+") 실행"
            self.db.insert_command_one(cmd, outputStr, self.device.MOTOR)

        else:
            outputStr = "[미처리] 알수없는 명령("+cmd+") 실행"
            self.db.insert_command_one(cmd, outputStr, self.device.MOTOR)
            print(outputStr)

    # 서버 통신
    def onLineServer(self):
        try:
            while True:
                # 클라이언트로 메시지가 도착하면 다음 줄로 넘어가고
                # 그렇지 않다면 대기(Blocking)
                data, addr = self.server.recvfrom(self.BUFSIZE)                
                # 받은 메시지와 클라이언트 주소 화면에 출력
                print('[Server] Received Data : %r from %r' % (data, addr))

                # 데이터검증(쓰레기제거)
                self.validateData(data)

                # 분기처리
                self.controllData(data)            

                # 받은 메시지를 클라이언트로 다시 전송
                #server.sendto(data, addr)
        except:
            print("[Server] Exception Error!!!", sys.exc_info())    



if __name__ == "__main__":
    sv = server()


