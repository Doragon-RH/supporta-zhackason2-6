import dlib
import cv2
import sys
from imutils import face_utils


def process_image(path, name):
    face_detector = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')
    face_predictor = dlib.shape_predictor(
        'shape_predictor_68_face_landmarks.dat')
    img = cv2.imread(path)
    img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        img_gry, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        print("Error: No face detected.")
        sys.exit()

    x, y, w, h = faces[0]
    x1, y1, x2, y2 = x, y, x + w, y + h
    face = dlib.rectangle(left=x, top=y, right=x2, bottom=y2)

    landmark = face_predictor(img_gry, face)
    landmark = face_utils.shape_to_np(landmark)

    if len(landmark) < 68:
        print("Error: Failed to detect face landmarks.")
        sys.exit()

    trim = img[y1:y2, x1:x2]
    output = f"./tmp/trim_{name}.png"
    cv2.imwrite(output, trim)

    return output
