import math

import cv2
import numpy as np


def processing_sin(path, name):
    img = cv2.imread(path)
    height, width, _ = img.shape

    amps = [1, 3, 6, 10, 15]
    freq = 0.1
    for i, amp in enumerate(amps):
        sins = []
        for w in range(width):
            x = w
            y = int(amp * math.sin(freq * x))
            sins.append((x, y))

        img_sin = np.zeros_like(img)

        for y in range(height):
            for x in range(width):
                conv_x = sins[x][0]
                conv_y = sins[x][1] + y
                if conv_y < 0 or conv_y >= height:
                    continue
                img_sin[y, x] = img[conv_y, conv_x]

        cv2.imwrite(f"./tmp/B_{name}_{i+1}.png", img_sin)
