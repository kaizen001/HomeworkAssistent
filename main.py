import pygame
import Robot
import GetFaceData
import MyThread
import time

SCREEN_COLOR = (255, 255, 255)


def main():
    # 初始化屏幕
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("机器人")
    # 初始化背景
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(SCREEN_COLOR)

    # 创建初始状态的画面
    background.fill(SCREEN_COLOR)
    # 创建
    robot = Robot.Robot(screen, background)
    # robot.angry()

    # 更新一次屏幕
    screen.blit(background, (0, 0))
    pygame.display.update()

    thread1 = GetFaceData.FaceRecogn(1, "CvThread", 1)
    music = MyThread.Music(robot)
    # 让机器人开始眨眼
    wink_thread = MyThread.WinkThread(robot)
    working_thread = MyThread.Working(robot, GetFaceData.cvData)
    wink_thread.start()
    music.start()
    thread1.start()
    working_thread.start()
    thread1.join()
    working_thread.join()
    music.join()
    wink_thread.join()

    # 让机器人开始说话
    # speak_thread = MyThread.SpeakThread(robot)
    # speak_thread.start()
    # speak_thread.join()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    main()
