import Organ
from GetFaceData import STATE
from GetFaceData import CvData
import random
import pygame
import time
import math

SCREEN_COLOR = (255, 255, 255)
RED = (255, 0, 0)

# 脸的各项数值
FACE_COLOR = (0, 0, 0)  # 脸的颜色
FACE_LENGTH = 320  # 脸的长度
FACE_WIDTH = int(FACE_LENGTH * 0.618)  # 脸的宽度
FACE_SIZE = 10  # 脸的粗细
FACE_LEFT = 800  # 脸的左间距
FACE_TOP = 450  # 脸的上间距

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
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.face = Organ.Face(self.background, FACE_COLOR, FACE_LENGTH, FACE_WIDTH, FACE_LEFT, FACE_TOP, FACE_SIZE)
        self.mouth = Organ.Mouth(self.background, MOUTH_COLOR, MOUTH_LENGTH, MOUTH_WIDTH, MOUTH_LEFT, MOUTH_TOP,
                                 MOUTH_SIZE)
        self.left_eye = Organ.Eye(self.background, EYE_COLOR, EYE_LENGTH, EYE_WIDTH, LEFT_EYE_LEFT, EYE_TOP, EYE_SIZE)
        self.right_eye = Organ.Eye(self.background, EYE_COLOR, EYE_LENGTH, EYE_WIDTH, RIGHT_EYE_LEFT, EYE_TOP, EYE_SIZE)
        self.status = STATE.WRITING
        self.draw()

    # 画出机器人
    def draw(self):
        self.face.draw()
        self.mouth.draw()
        self.left_eye.draw()
        self.right_eye.draw()

    # 机器人眨眼
    def wink(self):
        # 每次眨眼间间隔
        n = random.random()
        time.sleep(n + 2)
        # 闭眼阶段
        self.background.fill(SCREEN_COLOR)
        self.right_eye.close()
        self.left_eye.close()
        self.draw()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
        # 睁眼阶段
        time.sleep(0.1)
        self.background.fill(SCREEN_COLOR)
        self.left_eye.open()
        self.right_eye.open()
        self.draw()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    # 说话
    def speak(self):
        self.background.fill(SCREEN_COLOR)
        self.mouth.close()
        self.draw()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
        time.sleep(0.1)
        self.background.fill(SCREEN_COLOR)
        self.mouth.open()
        self.draw()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    # 获得CvData然后进行移动
    def move(self, cvData):  # x,y取值为-100-100
        self.background.fill(SCREEN_COLOR)
        self.status = cvData.state
        self.face.move(cvData.faceBiasX, cvData.faceBiasY)
        self.mouth.move(cvData.faceBiasX, cvData.faceBiasY)
        self.left_eye.move(cvData.faceBiasX, cvData.faceBiasY)
        self.right_eye.move(cvData.faceBiasX, cvData.faceBiasY)
        if self.status == STATE.WRITING:
            self.draw()
        else:
            self.angry()
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

        self.face.move(-cvData.faceBiasX, -cvData.faceBiasY)
        self.mouth.move(-cvData.faceBiasX, -cvData.faceBiasY)
        self.left_eye.move(-cvData.faceBiasX, -cvData.faceBiasY)
        self.right_eye.move(-cvData.faceBiasX, -cvData.faceBiasY)


    def angry(self):
        self.face.draw()
        self.mouth.angry()
        self.left_eye.left_angry()
        self.right_eye.right_angry()
        size = self.face.width // 4
        pygame.draw.arc(self.background, RED,
                        (self.face.left - 2 * size, self.face.top - size, size * 2, size * 2),
                        math.pi * 5 / 3, math.pi / 6, 10)

        pygame.draw.arc(self.background, RED,
                        (self.face.left - size, self.face.top + size, size * 2, size * 2),
                        math.pi * 1 / 6, math.pi * 2 / 3, 10)

        pygame.draw.arc(self.background, RED,
                        (self.face.left + size, self.face.top, size * 2, size * 2),
                        math.pi * 2 / 3, math.pi * 7 / 6, 10)

        pygame.draw.arc(self.background, RED,
                        (self.face.left, self.face.top - 2 * size, size * 2, size * 2),
                        math.pi * 7 / 6, math.pi * 5 / 3, 10)
