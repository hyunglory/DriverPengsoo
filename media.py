import pygame
import speech_recognition as sr
import random
from Command import command

class music:

    
    def __init__(self):
        command = Command()
        
        self.music_cmd = ["Playing... - func => playingmusic", "명령 : 1. 그만 | 2. 다음", "명령을 확인중...", "다시 말해 주세요.", "재생을 정지합니다."]

        self.filename = ['music/Do It.mp3', 'music/noma - Color.mp3', 'music/Sakura.mp3', 'music/Dawn.mp3', 'music/Tomorrow.mp3']

        self.music_num = random.randrange(0,5)
        
        self.initMixer()
        self.r = sr.Recognizer()
        self.playmusic(self.filename[self.music_num])
        self.count = self.music_num
        
    def playmusic(self,soundfile):
        pygame.init()
        pygame.mixer.init()
        self.clock= pygame.time.Clock()
        pygame.mixer.music.load(soundfile)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            #print("Playing... - func => playingmusic")
            print(self.music_cmd[0])
            
            self.clock.tick(1000) # 초당 1000프레임이상이 안되게 제한
            
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                print("%s번째 곡 : %s"%((self.count%5)+1, self.filename[self.count%5]))

                #print("명령 : 1. 그만 | 2. 다음")
                print(self.music_cmd[1])
                
                self.audio_text = self.r.listen(source)
                try :
                    #print("명령을 확인중...")
                    print(self.music_cmd[2])
                    
                    r2=self.r.recognize_google(self.audio_text,language='ko-KR')
                    print(r2)
                    
                    if command.STOP in r2:
                        self.stopmusic()
                        db.insert_command_one(command.STOP,'',SPEAKER)
                        
                    elif command.NEXT in r2:
                        self.count+=1
                        self.playmusic(self.filename[self.count%5])
                        db.insert_command_one(command.NEXT,'',SPEAKER)
                    
                except KeyboardInterrupt:
                    self.stopmusic()
                    print("\nPlay stopped by user")

                except:
                    #print("다시 말해 주세요.")
                    print(self.music_cmd[3])
                    print("")
         
 
    def stopmusic(self):
        """stop currently playing music"""
        #print("재생을 정지합니다.")
        print(self.music_cmd[4])
        pygame.mixer.music.stop()
    
    def getmixerargs(self):
        pygame.mixer.init()
        freq, size, chan= pygame.mixer.get_init()
        return freq, size, chan
    
    
    def initMixer(self):
        BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
        FREQ, SIZE, CHAN= self.getmixerargs()
        pygame.mixer.init(FREQ, SIZE, CHAN,BUFFER)
    
 
'''You definitely need test mp3 file (a.mp3 in example) in a directory, say under 'C:\\Temp'
   * To play wav format file instead of mp3,
      1) replace a.mp3 file with it, say 'a.wav'
      2) In try except clause below replace "playmusic()" with "playsound()"
     
'''
if __name__ == "__main__":
               
    music=music()
    pass
    

