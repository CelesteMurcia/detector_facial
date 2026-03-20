import cv2

class Camara:
    def __init__(self, indice=0):
        self.cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW)

        # Resolución original
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS,          60)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,   1)

    def leer_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Solo modo espejo
            frame = cv2.flip(frame, 1)
        return ret, frame

    def liberar(self):
        self.cap.release()
        cv2.destroyAllWindows()