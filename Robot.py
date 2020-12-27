import Organ

FACE_COLOR = (0, 0, 0)
FACE_LENGTH = 320
FACE_WIDTH = int(FACE_LENGTH * 0.618)
FACE_SIZE = 10
FACE_LEFT = 800
FACE_TOP = 400

MOUTH_COLOR = (0, 0, 0)
MOUTH_LENGTH = FACE_LENGTH // 3
MOUTH_WIDTH = int(MOUTH_LENGTH * 0.5)
MOUTH_SIZE = 0
MOUTH_LEFT = FACE_LEFT + FACE_LENGTH // 3
MOUTH_TOP = FACE_TOP + FACE_WIDTH // 8 * 5

EYE_COLOR = (0, 0, 0)
EYE_SIZE = 0
LEFT_EYE_LEFT = FACE_LEFT + FACE_LENGTH // 4
RIGHT_EYE_LEFT = FACE_LEFT + FACE_LENGTH // 4 * 3
EYE_TOP = FACE_TOP + FACE_WIDTH // 8 * 3
EYE_RADIUS = FACE_WIDTH // 6


class Robot:
    def __init__(self):
        self.face = Organ.Face(FACE_COLOR, FACE_LENGTH, FACE_WIDTH, FACE_LEFT, FACE_TOP, FACE_SIZE)
        self.mouth = Organ.Mouth(MOUTH_COLOR, MOUTH_LENGTH, MOUTH_WIDTH, MOUTH_LEFT, MOUTH_TOP, MOUTH_SIZE)
        self.left_eye = Organ.Eye(EYE_COLOR, LEFT_EYE_LEFT, EYE_TOP, EYE_RADIUS, EYE_SIZE)
        self.right_eye = Organ.Eye(EYE_COLOR, RIGHT_EYE_LEFT, EYE_TOP, EYE_RADIUS, EYE_SIZE)

    def draw(self, surface):
        self.face.draw(surface)
        self.mouth.draw(surface)
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)
