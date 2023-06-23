import imageio
import numpy as np
from math import sqrt
import sys
import argparse
import os
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



def get_fish_xn_yn(source_x, source_y, radius, distortion):
    """
    Get normalized x, y pixel coordinates from the original image and return normalized 
    x, y pixel coordinates in the destination fished image.
    :param distortion: Amount in which to move pixels from/to center.
    As distortion grows, pixels will be moved further from the center, and vice versa.
    """

    if 1 - distortion*(radius**2) == 0:
        return source_x, source_y

    return source_x / (1 - (distortion*(radius**2))), source_y / (1 - (distortion*(radius**2)))


def fish(img, distortion_coefficient):
    """
    :type img: numpy.ndarray
    :param distortion_coefficient: The amount of distortion to apply.
    :return: numpy.ndarray - the image with applied effect.
    """

    # If input image is only BW or RGB convert it to RGBA
    # So that output 'frame' can be transparent.
    w, h = img.shape[0], img.shape[1]
    if len(img.shape) == 2:
        # Duplicate the one BW channel twice to create Black and White
        # RGB image (For each pixel, the 3 channels have the same value)
        bw_channel = np.copy(img)
        img = np.dstack((img, bw_channel))
        img = np.dstack((img, bw_channel))
    if len(img.shape) == 3 and img.shape[2] == 3:
        print("RGB to RGBA")
        img = np.dstack((img, np.full((w, h), 255)))

    # prepare array for dst image
    dstimg = np.zeros_like(img)

    # floats for calcultions
    w, h = float(w), float(h)

    # easier calcultion if we traverse x, y in dst image
    for x in range(len(dstimg)):
        for y in range(len(dstimg[x])):

            # normalize x and y to be in interval of [-1, 1]
            xnd, ynd = float((2*x - w)/w), float((2*y - h)/h)

            # get xn and yn distance from normalized center
            rd = sqrt(xnd**2 + ynd**2)

            # new normalized pixel coordinates
            xdu, ydu = get_fish_xn_yn(xnd, ynd, rd, distortion_coefficient)

            # convert the normalized distorted xdn and ydn back to image pixels
            xu, yu = int(((xdu + 1)*w)/2), int(((ydu + 1)*h)/2)

            # if new pixel is in bounds copy from source pixel to destination pixel
            if 0 <= xu and xu < img.shape[0] and 0 <= yu and yu < img.shape[1]:
                dstimg[x][y] = img[xu][yu]

    return dstimg.astype(np.uint8)


def parse_args(args=sys.argv[1:]):
    """Parse arguments."""

    parser = argparse.ArgumentParser(
        description="Apply fish-eye effect to images.",
        prog='python3 fish.py')

    parser.add_argument("-i", "--image", help="path to image file."
                        " If no input is given, the supplied example 'grid.jpg' will be used.",
                        type=str, default="grid.jpg")

    parser.add_argument("-o", "--outpath", help="file path to write output to."
                        " format: <path>.<format(jpg,png,etc..)>",
                        type=str, default="fish.png")

    parser.add_argument("-d", "--distortion",
                        help="The distoration coefficient. How much the move pixels from/to the center."
                        " Recommended values are between -1 and 1."
                        " The bigger the distortion, the further pixels will be moved outwars from the center (fisheye)."
                        " The Smaller the distortion, the closer pixels will be move inwards toward the center (rectilinear)."
                        " For example, to reverse the fisheye effect with --distoration 0.5,"
                        " You can run with --distortion -0.3."
                        " Note that due to double processing the result will be somewhat distorted.",
                        type=float, default=0.5)

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()
    try:
        imgobj = imageio.imread(args.image)
    except Exception as e:
        print(e)
        sys.exit(1)
    if os.path.exists(args.outpath):
        ans = input(
            args.outpath + " exists. File will be overridden. Continue? y/n: ")
        if ans.lower() != 'y':
            print("exiting")
            sys.exit(0)
    
    output_img = fish(imgobj, args.distortion)
    imageio.imwrite(args.outpath, output_img, format='png')










# import cv2
# import numpy as np
# import fish

# def transform_image_region(image, x, y, width, height, distortion_coefficient):
#     # 余分な領域を含む範囲内の部分画像を切り出します
#     extra_width = int(width * 0.5)
#     extra_height = int(height * 0.5)
#     region_of_interest = image[max(0, y-extra_height):y+height+extra_height, max(0, x-extra_width):x+width+extra_width]

#     # 部分画像を歪ませます（ここでは例として distortion_coefficient を使用）
#     distorted_region = fish.fish(region_of_interest, distortion_coefficient)

#     # 歪ませた領域を元の画像上の位置に戻します
#     image_with_alpha = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)*3
#     image_with_alpha[max(0, y-extra_height):y+height+extra_height, max(0, x-extra_width):x+width+extra_width] = distorted_region

#     # RGBA形式からRGB形式に戻します
#     image_rgb = cv2.cvtColor(image_with_alpha, cv2.COLOR_RGBA2RGB)

#     return image_rgb

# # 画像の読み込み
# image = cv2.imread("face01.png")

# # 変形する範囲の座標とサイズ（例として、左上の座標が (100, 100) で、幅と高さが 200 ピクセル）
# x = 100
# y = 100
# width = 50
# height = 50

# # 歪ませる係数（例として、0.5）
# distortion_coefficient = 0.5

# # 画像の指定範囲のみを変形
# transformed_image = transform_image_region(image, x, y, width, height, distortion_coefficient)

# transformed_image = transform_image_region(transformed_image, 100,200,50,50, distortion_coefficient)

# # 変形後の画像を表示
# cv2.imshow("Transformed Image", transformed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()