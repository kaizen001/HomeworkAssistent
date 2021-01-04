import queue
import threading
from enum import Enum
from queue import Queue

import cv2
import os
from math import sin, cos, radians
import ctypes
import time
import numpy as np


class STATE(Enum):
    WRITING = 0
    SLEEPING = 1
    LOOKING_AROUND = 2
    DEFAULT = 3


class CvData:
    faceBiasX = 0  # -100-100,float，左右方向偏移
    faceBiasY = 0  # -100-100,float，上下方向偏移
    state = STATE.DEFAULT  # 状态


class OriginData:
    isFaceHere = False
    eyesNumber = 0
    faceXRate = 0
    faceYRate = 0


cvData = CvData  # 读这个

cap = cv2.VideoCapture(0)
assets = os.path.join('assets')
scl, scb = 1920, 1080
rface = cv2.CascadeClassifier(os.path.join("face_detector", "haarcascade_frontalface_default.xml"))
reyeg = cv2.CascadeClassifier(os.path.join("face_detector", "haarcascade_eye_tree_eyeglasses.xml"))
reye = cv2.CascadeClassifier(os.path.join("face_detector", "haarcascade_eye.xml"))
faceSettings = {
    'scaleFactor': 1.3,
    'minNeighbors': 5,
    'minSize': (1, 1),
}
eyeSettings = {
    'scaleFactor': 1.3,
    'minNeighbors': 3,
    'minSize': (1, 1),
}


def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1] * 0.4
    y = pos[1] - img.shape[0] * 0.4
    newx = x * cos(radians(angle)) + y * sin(radians(angle)) + img.shape[1] * 0.4
    newy = -x * sin(radians(angle)) + y * cos(radians(angle)) + img.shape[0] * 0.4
    return int(newx), int(newy), pos[2], pos[3]


class FaceRecogn(threading.Thread):
    q = np.array([[0, 0, 0, 0], [0, 0, 0, 0]])

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("fps: ", fps)

    def run(self):
        print("开始线程：" + self.name)

        while True:
            # 读图像
            if cap.isOpened():  # try to get the first frame
                ret, imgn = cap.read()
                imgn = cv2.resize(imgn, (640, 360), )  # 图片形状
                img = np.array(cv2.flip(imgn, +1))
                if ret != True:
                    print('FFFF')
            else:
                rval = False
                print('FALLLLLLL')
                break

            imgout = img.copy()

            dataBuff = OriginData
            dataBuff.isFaceHere = False
            for angle in [0, -25, 25]:
                rimg = rotate_image(img, angle)

                # 人脸
                fdetected = rface.detectMultiScale(rimg, **faceSettings)
                if len(fdetected):
                    fx, fy, fw, fh = rotate_point(fdetected[-1], img, -angle)
                    cv2.rectangle(imgout, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
                    if fx < 0: fx = 0
                    if fy < 0: fy = 0
                    # print("fx:",fx,"  fy:",fy,"  fw:",fw,"  fh:",fh)
                    # 眼睛
                    imge = img[fy:fy + fh, fx:fx + fw]
                    # cv2.imshow('face', imge)  # 魔性大脸
                    imge = rotate_image(imge, angle)
                    edetected = reye.detectMultiScale(imge, **eyeSettings)
                    # print(len(edetected))
                    if len(edetected):
                        for elm in edetected:
                            d = [rotate_point(elm, imge, -angle)]
                            for x, y, w, h in d:
                                cv2.rectangle(imgout, (fx + x, fy + y), (fx + x + w, fy + y + h), (0, 255, 0), 2)

                    dataBuff.isFaceHere = True
                    dataBuff.faceXRate = ((fx + (fw / 2.0)) - 320) * 100 / 320
                    dataBuff.faceYRate = ((fy + (fh / 2.0)) - 180) * 100 / 180
                    dataBuff.eyesNumber = len(edetected)
                    break

            if self.q[..., 1].size == 20:
                self.q = np.insert(self.q, 0,
                                   [int(dataBuff.isFaceHere), int(dataBuff.eyesNumber), int(dataBuff.faceXRate),
                                    int(dataBuff.faceYRate)], axis=0)
                self.q = np.delete(self.q, 19, axis=0)
                faceInNumber = sum(self.q[..., 0])
                eyeNumber = sum(self.q[..., 1])
                avgXRate = sum(self.q[..., 2]) / self.q[..., 1].size
                avgYRate = sum(self.q[..., 3]) / self.q[..., 1].size

                if faceInNumber >= 5 and eyeNumber >= 5:
                    cvData.state = STATE.WRITING
                    cvData.faceBiasX = avgXRate
                    cvData.faceBiasY = avgYRate
                elif faceInNumber >= 5:
                    cvData.state = STATE.SLEEPING
                    cvData.faceBiasX = avgXRate
                    cvData.faceBiasY = avgYRate
                else:
                    cvData.state = STATE.LOOKING_AROUND
                # print(faceInNumber, '     ', eyeNumber)
            else:
                self.q = np.insert(self.q, 0,
                                   [int(dataBuff.isFaceHere), int(dataBuff.eyesNumber), int(dataBuff.faceXRate),
                                    int(dataBuff.faceYRate)], axis=0)

            # print(cvData.state, '   ', cvData.faceBiasX, '   ', cvData.faceBiasY)
            # print(self.q[..., 1].size)

            # cv2.imshow('img', imgout)  # 用来显示图片，运行时可以删除
            if cv2.waitKey(5) != -1:
                break

        cv2.destroyAllWindows()
        quit()

        print("退出线程：" + self.name)


if __name__ == '__main__':
    faceR = FaceRecogn(1, "CvThread", 1)
    faceR.run()

    thread1 = FaceRecogn(1, "CvThread", 1)
    thread1.start()
    thread1.join()
