import pygame


# 所有部位的父类，器官
class Organ():
    color = (0, 0, 0)  # 颜色
    size = 0  # 大小

    def __init__(self, screen, color, size):
        self.screen = screen
        self.color = color
        self.size = size


# 嘴巴 椭圆形
class Mouth(Organ):
    length = 0  # 嘴巴的长
    width = 0  # 宽
    left = 0  # 离屏幕左端间距
    top = 0  # 离屏幕上端间距
    rect = ()  # 构成的矩形元组

    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, size)
        self.length = length
        self.width = width
        self.left = left
        self.top = top
        self.set_rect()

    def set_rect(self):
        self.rect = (self.left, self.top, self.length, self.width)

    def draw(self):  # 画个嘴巴
        pygame.draw.ellipse(self.screen, self.color, self.rect, self.size)

    def close(self):
        self.width //= 2
        self.top += self.width // 2
        self.set_rect()

    def open(self):
        self.top -= self.width // 2
        self.width *= 2
        self.set_rect()


# 脸部，准确说是脸框 矩形
class Face(Organ):
    length = 0  # 脸的长
    width = 0  # 宽
    left = 0  # 离屏幕左端间距
    top = 0  # 离屏幕上端间距
    rect = ()  # 构成的矩形元组

    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, size)
        self.length = length
        self.width = width
        self.left = left
        self.top = top
        self.set_rect()

    def set_rect(self):
        self.rect = (self.left, self.top, self.length, self.width)

    def draw(self):  # 画个脸
        pygame.draw.rect(self.screen, self.color, self.rect, self.size)


# 眼睛 圆形
class Eye(Organ):
    left = 0  # 离屏幕左端间距
    top = 0  # 离屏幕上端间距
    radius = 0  # 眼睛的半径
    pos = ()  # 眼睛的位置

    def __init__(self, screen, color, length, width, left, top, size):
        Organ.__init__(self, screen, color, size)
        self.length = length
        self.width = width
        self.left = left
        self.top = top
        self.set_rect()

    def set_rect(self):
        self.rect = (self.left, self.top, self.length, self.width)

    def draw(self):  # 画眼睛
        pygame.draw.ellipse(self.screen, self.color, self.rect, self.size)

    def close(self):  # 眨眼时闭眼
        self.width = self.length // 2
        self.top += self.width // 2
        self.set_rect()

    def open(self):  # 眨眼时睁眼
        self.top -= self.width // 2
        self.width = self.length
        self.set_rect()
