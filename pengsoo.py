import numpy as np
import cv2
import speech_recognition as sr
import media
import servor
from command import Command
from command import Device
from mongodb import MongoDB
import sys

order = ['명령:','입력완료']
command = Command()
device = Device()
db = MongoDB()
faceCascade = cv2.CascadeClassifier('ha/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0) # 웹캠 설정
cap.set(3, 960) # 영상 가로길이 설정
cap.set(4, 480) # 영상 세로길이 설정
checkid=0
r = sr.Recognizer()

while True:
    if checkid==0 :
        ret, frame = cap.read() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,1.2,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            if w*h>=60000:
                checkid=1
        cv2.imshow('divx', frame)
        if checkid==1:
            cv2.destroyAllWindows()
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    elif checkid==1:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print(order[0])
            audio_text = r.listen(source)
            try:
                print(order[1])
                r2=r.recognize_google(audio_text,language='ko-KR')
                print(r2)
                if r2 == command.START_MUSIC:
                    music = media.music()
                    db.insert_command_one(command.START_MUSIC,'',device.SPEAKER)
                elif r2 == command.GREETING:
                    hi=servor.hi()
                    hi.start(0)
                    db.insert_command_one(command.GREETING,'',device.SPEAKER)
                elif r2 == command.CAPTURE:
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    cv2.imshow('divx', frame)
                    cv2.imwrite("c.jpg",frame)
                    cap.release()
                    db.insert_command_one(command.CAPTURE,'',device.CAMERA)
                elif r2 == command.END:
                    db.insert_command_one(command.END,'',device.SPEAKER)
                    break
            
            except:
                print(sys.exc_info())



