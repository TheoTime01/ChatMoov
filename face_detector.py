
import cv2
import numpy as np
import logging
import serial

class FaceDetector:
    def __init__(self):
        """
        Initialize the face detector
        :return: None
        """
        self.cap = cv2.VideoCapture(0)
        self.frame_w = 640
        self.frame_h = 480
        self.set_res(self.frame_w, self.frame_h)
        self.ser = serial.Serial('COM17', 250000)

        # Load the haarcascade classifier
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        # Initialize logging
        self.logger = logging.getLogger("FaceDetector")
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def set_res(self, x, y):
        """
        Set the resolution of the camera
        :param x: width
        :param y: height
        :return: None
        """
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

    def detect_faces(self):
        """
        Detect faces in the video stream
        :return: None
        """
        self.logger.info("Face detection started.")
        try:
            while True:

                # Capture frame-by-frame
                ret, frame = self.cap.read()
                self.cap.read()

                frame = cv2.flip(frame, 1)

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=20,
                    minSize=(30, 30)
                )

                # Draw rectangles around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Display the resulting frame
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if len(faces) > 0:
                    face_center_x = faces[0, 0] + faces[0, 2] / 2
                    face_center_y = faces[0, 1] + faces[0, 3] / 2
                    err_x = 30 * (face_center_x - self.frame_w/2) / (self.frame_w/2)
                    err_y = 30 * (face_center_y - self.frame_h/2) / (self.frame_h/2)
                    self.ser.write((str(err_x) + "x!").encode())        
                else:
                    self.ser.write("o!".encode())

        except Exception as e:
            self.logger.error("An error occurred during face detection: %s", str(e))

        finally:
            # When everything is done, release the capture and close the windows
            self.ser.close()
            self.cap.release()
            cv2.destroyAllWindows()
            self.logger.info("Face detection stopped.")

if __name__ == "__main__":
    face_detector = FaceDetector()
    face_detector.detect_faces()