'''
** 명령어를 담당하는 클래스 **
** 작성요령 **
대문자와 _를 사용함

'''
class Command:
    
    def __init__(self):
        # 값을 변경할 수 없도록 상수 사용(대문자+언더바)
        self.START_MUSIC    = '노래'
        self.GREETING       = '인사'
        self.AGAIN          = '다시'
        self.CAPTURE        = '사진'
        self.START          = '시작'
        self.STOP           = '그만'
        self.END            = '종료'
        self.NEXT           = '다음'