import pygame
import math
import GetFaceData


# 所有部位的父类，器官
class Organ():
    color = (0, 0, 0)  # 颜色
    size = 0  # 大小
    rect = ()  # 图形尺寸
    LEFT = 0
    TOP = 0

    def __init__(self, screen, color, length, width, left, top, size):
        self.screen = screen  # 屏幕
        self.color = color  # 颜色
        self.size = size  # 大小
        self.length = length  # 长
        self.width = width  # 宽
        self.left = left  # 左间距
        self.top = top  # 上间距
        self.LEFT = left  # 左间距
        self.TOP = top  # 上间距
        self.set_rect()

    # 设置rect
    def set_rect(self):
        self.rect = (self.left, self.top, self.length, self.width)

    # 移动
    def move(self, x, y):
        self.left = int(x * 6.4) + self.LEFT
        self.top = int(y * 3.5) + self.TOP
        self.set_rect()


# 嘴巴 椭圆形
class Mouth(Organ):
    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, length, width, left, top, size)
        self.set_rect()

    def draw(self):  # 画个嘴巴
        self.set_rect()
        pygame.draw.ellipse(self.screen, self.color, self.rect, self.size)

    def close(self):
        self.width //= 2
        self.top += self.width // 2
        self.set_rect()

    def open(self):
        self.top -= self.width // 2
        self.width *= 2
        self.set_rect()

    def angry(self):
        pygame.draw.line(self.screen, self.color, (self.left, self.top + self.width),
                         (self.left + self.length // 2, self.top), 10)
        pygame.draw.line(self.screen, self.color, (self.left + self.length // 2, self.top),
                         (self.left + self.length, self.top + self.width), 10)


# 脸部，准确说是脸框 矩形
class Face(Organ):
    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, length, width, left, top, size)
        self.set_rect()

    def draw(self):  # 画个脸
        self.set_rect()
        pygame.draw.rect(self.screen, self.color, self.rect, self.size)


# 眼睛 圆形
class Eye(Organ):
    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, length, width, left, top, size)
        self.set_rect()

    def draw(self):  # 画眼睛
        self.set_rect()
        pygame.draw.ellipse(self.screen, self.color, self.rect, self.size)

    def close(self):  # 眨眼时闭眼
        self.width = self.length // 2
        self.top += self.width // 2
        self.set_rect()

    def open(self):  # 眨眼时睁眼
        self.top -= self.width // 2
        self.width = self.length
        self.set_rect()

    def left_angry(self):
        pygame.draw.line(self.screen, self.color, (self.left, self.top),
                         (self.left + self.length, self.top + self.width), 10)

    def right_angry(self):
        pygame.draw.line(self.screen, self.color, (self.left + self.length, self.top),
                         (self.left, self.top + self.width), 10)
