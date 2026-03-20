import cv2
import numpy as np
from titulo_barra import dibujar_barras

def crear_fondo(frame, panel_derecho, clave=None):
    alto_frame  = frame.shape[0]
    ancho_frame = frame.shape[1]

    ancho_total = ancho_frame * 2 + 3
    alto_total  = alto_frame + 110

    fondo = np.zeros((alto_total, ancho_total, 3), dtype=np.uint8)

    y_ini = 60
    fondo[y_ini:y_ini + alto_frame, 0:ancho_frame] = frame

    cv2.line(fondo, (ancho_frame, y_ini),
             (ancho_frame, y_ini + alto_frame), (50, 50, 50), 1)

    panel_x = ancho_frame + 2
    fondo[y_ini:y_ini + alto_frame,
          panel_x:panel_x + ancho_frame] = panel_derecho

    dibujar_barras(fondo, ancho_total, y_ini + alto_frame, clave)

    return fondo
