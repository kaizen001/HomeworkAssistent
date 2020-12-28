class STATE(Enum):
    WRITING = 0
    SLEEPING = 1
    LOOKING_AROUND = 2
    
class CvData:
    faceBiasX = 0#-100-100,float，左右方向偏移
    faceBiasY = 0#-100-100,float，上下方向偏移
    state = STATE.WRITING#状态

cvData = CvData
