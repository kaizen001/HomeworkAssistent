class STATE(Enum):
    WRITING = 0
    SLEEPING = 1
    LOOKING_AROUND = 2
    
class CvData:
    faceBiasX = 0#-100-100,float，左右方向偏移
    faceBiasY = 0#-100-100,float，上下方向偏移
    state = STATE.WRITING#状态

cvData = CvData

import cv2
import os
from math import sin, cos, radians
import ctypes
import time
import numpy as np


def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

if __name__=='__main__':

    # pygame.init()
    black = (255,255,255)
    ix = 960
    iy = 960

    assets = os.path.join('assets')

    # user32 = ctypes.windll.user32
    # scl,scb = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    scl,scb = 1920, 1080
    # print("Width: ",scl,"Height: ",scb) #screen metrics

    camera =  cv2.VideoCapture(0)

    #face = cv2.CascadeClassifier(os.path.join("face_detector","haarcascade_frontalface_alt2.xml"))
    rface = cv2.CascadeClassifier(os.path.join("face_detector","haarcascade_frontalface_default.xml"))
    reyeg = cv2.CascadeClassifier(os.path.join("face_detector", "haarcascade_eye_tree_eyeglasses.xml"))
    reye = cv2.CascadeClassifier(os.path.join("face_detector", "haarcascade_eye.xml"))
    fps = camera.get(cv2.CAP_PROP_FPS)
    print("fps: ",fps)
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

    running = True
    while running:
        #读图像
        if camera.isOpened():  # try to get the first frame
            ret, imgn = camera.read()
            imgn = cv2.resize(imgn, (640, 360), )#图片形状
            img = np.array(cv2.flip(imgn, +1))
            if ret != True:
                print('FFFF')
        else:
            rval = False
            print('FALLLLLLL')
            break

        imgout = img.copy()
        for angle in [0, -25, 25]:
            rimg = rotate_image(img, angle)

            #人脸
            fdetected = rface.detectMultiScale(rimg, **faceSettings)
            if len(fdetected):
                fx,fy,fw,fh = rotate_point(fdetected[-1], img, -angle)
                cv2.rectangle(imgout, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
                if fx < 0: fx = 0
                if fy < 0: fy = 0

                #眼睛
                imge = img[fy:fy+fh,fx:fx+fw]
                cv2.imshow('face', imge)  # 魔性大脸
                imge = rotate_image(imge, angle)

                edetected = reye.detectMultiScale(imge, **eyeSettings)
                print(len(edetected))
                if len(edetected):
                    for elm in edetected:
                        d = [rotate_point(elm, imge, -angle)]
                        for x, y, w, h in d:
                            cv2.rectangle(imgout, (fx+x, fy+y), (fx+x + w, fy+y + h), (0, 255, 0), 2)

                break

        # for angle in [0, -25, 25]:
        #     rimg = rotate_image(img, angle)
        #     detected = face.detectMultiScale(rimg, **settings)
        #     if len(detected):
        #         detected = [rotate_point(detected[-1], img, -angle)]
        #         break



        cv2.imshow('img',imgout)
        if cv2.waitKey(5) != -1:
            break

    cv2.destroyAllWindows()
    pygame.quit()
    quit()

    
