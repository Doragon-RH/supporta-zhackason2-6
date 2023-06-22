import cv2
import matplotlib.pyplot as plt

img = cv2.imread("test.png")    #画像読み込み("ファイル名を入力")

#色の変更も可能
# imreadの第二引数を0にすることでグレースケール
# img = cv2.imread(image_path, 0)

# 1にするとカラー画像：デフォルト
# img = cv2.imread(image_path, 1)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #matplotlibとcvの色を調整

# cv2.resizeでリサイズ(画像のサイズをあわせる)
resize_img = cv2.resize(img, (50, 50))  #サイズを小さくすることで見え方(モザイクのようにする)を変更することも可能

#描画領域の設定も可能
# fig=plt.figure(figsize=(8,8))

# matplotlibを用いて表示
plt.imshow(resize_img)  
plt.show()


# image_path = 'test.png'
# img = cv2.imread(image_path,0)

# # カスケード分類器を表すパスを定義
# cascade_path = 'haarcascade_frontalface_alt2.xml'

# # カスケード分類器を読み込む
# cascade = cv2.CascadeClassifier(cascade_path)

# # 画像にカスケード分類器を適用させる
# # scaleFactor: 顔検出する検索窓の拡大率
# # minNeighbors: 近くにこの値以上の検出された矩形がないとNG。大きくすると精度は上がるが、検出されない可能性も高まる
# # minSize: 検出する矩形の最小サイズ
# face_list = cascade.detectMultiScale(img, scaleFactor=1.1,
#                                              minNeighbors=2, minSize=(64, 64))

eye_cascade_path = 'data/haarcascade_eye.xml'

eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

src = cv2.imread('assets/icon.png')
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

eyes = eye_cascade.detectMultiScale(src_gray)


for x, y, w, h in eyes:
    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imwrite('./sample_after.png', src)


# # print(face_list)
# img=cv2.imread("test.png")
# cv2.imshow("変顔",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("test.png",img) #名前を指定して保存
