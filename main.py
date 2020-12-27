import pygame
import Robot

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
    # 创建
    robot = Robot.Robot()
    robot.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == '__main__':
    main()
