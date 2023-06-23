import imageio
import numpy as np
from math import sqrt
import sys
import argparse
import os
import fish
import cv2



def crop_image(image, x, y, width, height):
    """
    特定領域を切り抜く(-> cropped_image)
    """
    cropped_image = image[y:y+height, x:x+width]
    return cropped_image

def processing_fish_pointed(img, name):
    """
    魚眼加工
    """
    height, width, _ = img.shape

    coefficients = [0.01, 0.25, 0.5, 0.75, 1.0]

    for i, coeff in enumerate(coefficients):
        img_fish = fish.fish(img, distortion_coefficient=coeff)
        output = f"./tmp/A_{name}_{i+1}.png"

        n = 1+coeff
        M = cv2.getRotationMatrix2D((width//2, height//2), 0, n)
        img_resize = cv2.warpAffine(img_fish, M, (width, height))

        cv2.imwrite(output, img_resize)


def paste_image(background, foreground, x, y):
    """
    切り取り画像と元画像の貼り付け
    """
    # 背景画像の高さと幅を取得
    bg_height, bg_width = background.shape[:2]

    # 貼り付ける画像の高さと幅を取得
    fg_height, fg_width = foreground.shape[:2]

    # 貼り付ける領域の範囲を計算
    x_end = x + fg_width
    y_end = y + fg_height

    # 貼り付ける領域が背景画像の範囲内であることを確認
    if x < 0 or y < 0 or x_end > bg_width or y_end > bg_height:
        print("Error: The paste region is out of bounds.")
        return background

    # 貼り付ける領域に画像を貼り付け
    alpha = 1.0  # 画像の透明度（1.0で不透明）
    blended = cv2.addWeighted(background[y:y_end, x:x_end], alpha, foreground[:fg_height, :fg_width], 1 - alpha, 0)

    # 背景画像に貼り付けた領域を置き換える
    background[y:y_end, x:x_end] = blended

    return background


# 画像の読み込み
image = cv2.imread("input_image.jpg")

# 切り抜く範囲の座標とサイズ（例として、左上の座標が (100, 100) で、幅と高さが 200 ピクセル）
x = 100
y = 100
width = 200
height = 200

# 画像の特定領域を切り抜く
cropped_image = crop_image(image, x, y, width, height)

# 魚眼加工を加える


# 画像の貼り付け
result_image = paste_image(image, cropped_image, x, y)

# 結果の画像を保存
cv2.imwrite("result_image.jpg", result_image)
