import sys
from socket import *
from MecanumDriver import *


ECHO_PORT = 9999
BUFSIZE = 256

def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])

    else:
        port = ECHO_PORT

    s = socket(AF_INET, SOCK_DGRAM)
    
    # 포트 설정
    s.bind(('', port))
    
    # 준비 완료 화면에 표시
    print ('udp echo server ready')
    data = ''
    # 무한 루프 돌림
    while 1:
        # 클라이언트로 메시지가 도착하면 다음 줄로 넘어가고
        # 그렇지 않다면 대기(Blocking)
        data, addr = s.recvfrom(BUFSIZE)

        data = data.decode() # byte형을 string형태로
        print('server received %s from %r' % (data, addr))
        
        exeCarFunc(data)
    
        # 받은 메시지를 클라이언트로 다시 전송
        #s.sendto(data, addr)

#[Car]Foward
#[Pso]
def exeCarFunc(data, delay=0.001):
    firstData = data[:5]        # [Car]
    secondData = data[5:]       # Foward

    if (firstData == "[Car]"):
        if (secondData == "Forward"):
            carForward(delay, 1)
        elif(secondData == "Reverse"):
            carReverse(delay, 1)
        elif(secondData == "Left"):
            carLeft(delay, 1)
        elif(secondData == "Right"):
            carRight(delay, 1)
        elif(secondData == "Dir11"):   
            carDir11(delay, 1) 
        elif(secondData == "Dir1"):
            carDir1(delay, 1)
        elif(secondData == "Dir7"):
            carDir7(delay, 1)
        elif(secondData == "Dir5"):   
            carDir5(delay, 1)
        elif(secondData == "RightRotate"):
            rightRotate(delay, 1)
        elif(secondData == "LeftRotate"):
            leftRotate(delay, 1)
        elif(secondData == "Stop"):
            carStop()
        else:
            carStop()    

    # elif (firstData == "[Pso]"):
    #     if

    #else: 
    #    carStop()
    
    

server()
