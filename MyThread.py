import threading
from GetFaceData import STATE

SCREEN_COLOR = (255, 255, 255)


# 用来控制眨眼的线程类
class WinkThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    # 开始眨眼
    def run(self) -> None:
        while True:
            if self.robot.status != STATE.WRITING:
                continue
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