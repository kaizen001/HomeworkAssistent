import threading
import pygame
import time
import GetFaceData as cv

SCREEN_COLOR = (255, 255, 255)


# 用来控制眨眼的线程类
class WinkThread(threading.Thread):
    def __init__(self, robot, screen, background):
        threading.Thread.__init__(self)
        self.robot = robot
        self.screen = screen
        self.background = background

    # 开始眨眼
    def run(self) -> None:
        while True:
            time.sleep(0.5)
            self.background.fill(SCREEN_COLOR)
            self.robot.wink1()  # 闭眼阶段
            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            time.sleep(0.1)
            self.background.fill(SCREEN_COLOR)
            self.robot.wink2()  # 睁眼阶段
            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            print(cv.cvData.state)
