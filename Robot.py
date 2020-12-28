import Organ

# 脸的各项数值
FACE_COLOR = (0, 0, 0)  # 脸的颜色
FACE_LENGTH = 320  # 脸的长度
FACE_WIDTH = int(FACE_LENGTH * 0.618)  # 脸的宽度
FACE_SIZE = 10  # 脸的粗细
FACE_LEFT = 800  # 脸的左间距
FACE_TOP = 400  # 脸的上间距

# 嘴的各项数值
MOUTH_COLOR = (0, 0, 0)  # 嘴的颜色
MOUTH_LENGTH = FACE_LENGTH // 4  # 嘴的长度  说话时状态
MOUTH_WIDTH = int(MOUTH_LENGTH * 0.6)  # 嘴的宽度  说话时状态
MOUTH_SIZE = 0  # 嘴的大小 全部填充
MOUTH_LEFT = FACE_LEFT + FACE_LENGTH // 8 * 3  # 嘴的左间距
MOUTH_TOP = FACE_TOP + FACE_WIDTH // 8 * 5  # 嘴的上间距

# 眼睛的各项数值
EYE_COLOR = (0, 0, 0)  # 眼睛的颜色
EYE_LENGTH = FACE_WIDTH // 4
EYE_WIDTH = EYE_LENGTH
LEFT_EYE_LEFT = FACE_LEFT + FACE_LENGTH // 4 - EYE_LENGTH // 2  # 左眼距离
RIGHT_EYE_LEFT = FACE_LEFT + FACE_LENGTH // 4 * 3 - EYE_LENGTH // 2  # 右眼距离
EYE_TOP = FACE_TOP + FACE_WIDTH // 8 * 3 - EYE_LENGTH // 2  # 眼睛上间距
EYE_SIZE = 0  # 眼睛大小 全部填充


# 机器人
class Robot:
    def __init__(self, screen):
        self.screen = screen
        self.face = Organ.Face(self.screen, FACE_COLOR, FACE_LENGTH, FACE_WIDTH, FACE_LEFT, FACE_TOP, FACE_SIZE)
        self.mouth = Organ.Mouth(self.screen, MOUTH_COLOR, MOUTH_LENGTH, MOUTH_WIDTH, MOUTH_LEFT, MOUTH_TOP, MOUTH_SIZE)
        self.left_eye = Organ.Eye(self.screen, EYE_COLOR, EYE_LENGTH, EYE_WIDTH, LEFT_EYE_LEFT, EYE_TOP, EYE_SIZE)
        self.right_eye = Organ.Eye(self.screen, EYE_COLOR, EYE_LENGTH, EYE_WIDTH, RIGHT_EYE_LEFT, EYE_TOP, EYE_SIZE)
        self.draw()

    # 画出机器人
    def draw(self):
        self.face.draw()
        self.mouth.draw()
        self.left_eye.draw()
        self.right_eye.draw()

    # 机器人开始眨眼
    def wink1(self):
        self.right_eye.width = self.right_eye.length // 2
        self.left_eye.width = self.left_eye.length // 2
        self.right_eye.top += self.right_eye.width // 2
        self.left_eye.top += self.left_eye.width // 2
        self.left_eye.set_rect()
        self.right_eye.set_rect()
        self.draw()

    # 眨眼完回去
    def wink2(self):
        self.right_eye.top -= self.right_eye.width // 2
        self.left_eye.top -= self.left_eye.width // 2
        self.right_eye.width = self.right_eye.length
        self.left_eye.width = self.left_eye.length
        self.left_eye.set_rect()
        self.right_eye.set_rect()
        self.draw()
