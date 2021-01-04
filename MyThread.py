import threading
from GetFaceData import STATE
import GetFaceData as gfd
import time
import pygame

SCREEN_COLOR = (255, 255, 255)


# 用来控制眨眼的线程类
class WinkThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    # 开始眨眼
    def run(self) -> None:
        while True:
            if self.robot.status == STATE.WRITING:
                self.robot.wink()


# 用来控制说话的线程类
class SpeakThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    # 开始说话
    def run(self) -> None:
        while True:
            if self.robot.status == STATE.WRITING:
                continue
            self.robot.speak()


class Working(threading.Thread):
    def __init__(self, robot, cvData):
        threading.Thread.__init__(self)
        self.robot = robot
        self.cvData = cvData

    def run(self) -> None:
        while True:
            self.robot.move(self.cvData)
            print(gfd.cvData.state, '   ', gfd.cvData.faceBiasX, '   ', gfd.cvData.faceBiasY)
            # time.sleep(0.1)


class Music(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self) -> None:
        while True:
            if self.robot.status == STATE.LOOKING_AROUND:
                pygame.mixer.init()
                pygame.mixer.music.load('xuexi.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                time.sleep(2)
            if self.robot.status == STATE.SLEEPING:
                pygame.mixer.init()
                pygame.mixer.music.load('xingxing.mp3')
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                time.sleep(2)
