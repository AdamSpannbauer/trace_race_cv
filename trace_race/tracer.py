from collections import deque
import math
import cv2


class Tracer:
    def __init__(self, max_size=5, max_length=10, color=(0, 0, 255)):
        self.points = deque(maxlen=max_length)
        self.sizes = [math.ceil(max_size / (i * 0.3 + 1)) for i in range(max_length)]
        self.color = color

    def draw(self, img):
        for i, p in enumerate(reversed(self.points)):
            cv2.circle(img, p, self.sizes[i], self.color, -1)
