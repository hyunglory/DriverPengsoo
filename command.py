'''
** 명령어를 담당하는 클래스 **
** 작성요령 **
대문자와 _를 사용함

'''
class Command:
    
    def __init__(self):
        # 자동차 명령어
        self.FOWARD         = 'Forward'
        self.REVERSE        = 'Reverse'
        self.LEFT           = 'Left'
        self.RIGHT          = 'Right'
        self.DIR1           = 'Dir1'
        self.DIR5           = 'Dir5'
        self.DIR7           = 'Dir7'
        self.DIR11          = 'Dir11'
        self.RIGHT_ROT      = 'RightRotate'
        self.LEFT_ROT       = 'LeftRotate'
        self.STOP           = 'stop'
        self.TEST           = 'TEST'

        # 펭수 명령어
        self.SPEAK          = '음성명령'
        self.START_MUSIC    = '노래'
        self.GREETING       = '인사'
        self.AGAIN          = '다시'
        self.CAPTURE        = '사진'
        self.START          = '시작'
        self.STOP           = '그만'
        self.END            = '종료'
        self.NEXT           = '다음'

        self.P_UP           = '앞으로'
        self.P_DOWN         = '뒤로'
        self.P_RIGHT        = '오른쪽으로'
        self.p_LEFT         = '왼쪽으로'
        self.P_STOP         = '멈춰'

class Device:

    def __init__(self):
        self.SPEAKER    = 'SPEAKER'
        self.CAMERA     = 'CAMERA'
        self.MOTOR      = 'MOTOR'
        self.GYRO       = 'GYRO'
