import cv2

import fish


def processing_fish(path, name):
    img = cv2.imread(path)
    height, width, _ = img.shape

    coefficients = [0.01, 0.25, 0.5, 0.75, 1.0]

    for i, coeff in enumerate(coefficients):
        img_fish = fish.fish(img, distortion_coefficient=coeff)
        output = f"./tmp/A_{name}_{i+1}.png"

        n = 1+coeff
        M = cv2.getRotationMatrix2D((width//2, height//2), 0, n)
        img_resize = cv2.warpAffine(img_fish, M, (width, height))

        cv2.imwrite(output, img_resize)
