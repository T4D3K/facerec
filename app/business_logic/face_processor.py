import os

from app.business_logic.models import Image
import cv2
import numpy as np

haar_cascade_path = os.path.join(
    os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml"
)

class InvalidFile(Exception):
    pass

class FaceProcessor:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(haar_cascade_path)

    def face_recognition(self, input_image: Image, output_image: Image):
        img_array = np.frombuffer(input_image.buffer, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            raise InvalidFile("Invalid image data: Unable to decode.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        _, buffer = cv2.imencode(".jpg", img)
        output_image.buffer = buffer.tobytes()
        return len(faces)