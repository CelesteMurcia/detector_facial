import cv2

class DetectorRostros:
    def __init__(self):
        self.clasificador = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def detectar(self, frame):
        alto  = frame.shape[0]
        ancho = frame.shape[1]

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gris = cv2.equalizeHist(gris)

        rostros = self.clasificador.detectMultiScale(
            gris,
            scaleFactor=1.05,
            minNeighbors=8,
            minSize=(80, 80),
            maxSize=(400, 400)
        )

        rostros_validos = []
        for (x, y, w, h) in rostros:
            if w < ancho * 0.1 or h < alto * 0.1:
                continue
            if w > ancho * 0.9 or h > alto * 0.9:
                continue
            proporcion = w / h
            if proporcion < 0.6 or proporcion > 1.4:
                continue
            rostros_validos.append((x, y, w, h))

        return rostros_validos