import cv2


def mosaic(path, ratio):
    small = cv2.resize(path, None, fx=ratio, fy=ratio,
                       interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small,
                      path.shape[:2][::-1],
                      interpolation=cv2.INTER_NEAREST)


def processing_mosaic(path, name):
    img = cv2.imread(path)

    ratios = [0.08, 0.2, 0.4, 0.7, 1]

    for i, ratio in enumerate(ratios):
        img_mosaic = mosaic(img, ratio)

        cv2.imwrite(f"./tmp/C_{name}_{5-i}.png", img_mosaic)
