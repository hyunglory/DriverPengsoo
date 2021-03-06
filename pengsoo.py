import speech_recognition as sr     # STT 음성인식
import pyttsx3                      # TTS 음성변환
from command import Voice


class Pengsoo:
    def __init__(self):
        self.r = sr.Recognizer()     #음성인식 인스턴스
        self.engine = pyttsx3.init() #음성변환 인스턴스
        self.voice = Voice()        

    def listenVoice(self):
        with sr.Microphone() as source:
            print("[펭수] 음성인식이 동작중입니다.")
            self.engine.say(self.voice.LISTEN)
            self.engine.runAndWait()
            audio = self.r.listen(source, None, 5, None)
            print("[펭수] 입력완료")
        try:
            print("[사용자] " + self.r.recognize_google(audio, language="ko-KR"))
        except sr.UnknownValueError:
            msg = '잘 이해하지 못했어요.'
            print("[펭수] 잘 이해할 수 없습니다.")
            self.engine.say(msg)
        except sr.RequestError as e:
            print("[펭수] 구글 음성 인식으로부터 결과를 요청할 수 없습니다; {0}".format(e))
        return audio

    def speakVoice(self, message):
        self.engine.setProperty('rate', 120)     # setting up new voice rate
        self.engine.say(message)
        self.engine.runAndWait()
        print("[펭수] "+message)


if __name__ == "__main__":
    ps = Pengsoo()
    ps.listenVoice()