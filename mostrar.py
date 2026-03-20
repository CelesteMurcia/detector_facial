import cv2
import numpy as np
from fondo import crear_fondo

imagenes_cache = {}

MAPA_IMAGENES = {
    
    # Emociones
    "neutral" : "imagenes_expresiones/perro_serio.png",
    "enojado" : "imagenes_expresiones/gato_enojado.png",

    # Gestos una mano
    "pensando": "imagenes_gestos/chango_pensando.png",
    "tranquilo" : "imagenes_gestos/gato_chill.png",
    "idea" : "imagenes_gestos/gato_idea.png",
    "me gusta" : "imagenes_gestos/gato_lique.png",
    "puño" : "imagenes_gestos/gato_puno.png",
    "pregunta" : "imagenes_gestos/gato_unbrazo.png",

    
    # Gestos dos manos
    "puños"     : "imagenes_dosmanos/gato_punos.png",
    "asombro"    : "imagenes_dosmanos/gato_palmas.png",
}

def cargar_imagen(ruta):
    if ruta not in imagenes_cache:
        img = cv2.imread(ruta)
        imagenes_cache[ruta] = img
    return imagenes_cache[ruta]

def dibujar_etiqueta(frame, texto):
    alto  = frame.shape[0]
    ancho = frame.shape[1]

    # Fondo semitransparente para el texto
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, alto - 50), (ancho, alto), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # Texto centrado abajo
    tam_texto = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    x_texto   = (ancho - tam_texto[0]) // 2
    cv2.putText(frame, texto, (x_texto, alto - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


def mostrar_imagen(frame, clave):
    alto  = frame.shape[0]
    ancho = frame.shape[1]

    if clave in MAPA_IMAGENES:
        img = cargar_imagen(MAPA_IMAGENES[clave])
        if img is not None:
            panel = cv2.resize(img, (ancho, alto))
        else:
            panel = np.zeros((alto, ancho, 3), dtype=np.uint8)
    else:
        panel = np.zeros((alto, ancho, 3), dtype=np.uint8)
        cv2.putText(panel, "Haz un gesto", (ancho//2 - 80, alto//2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 1)
        cv2.putText(panel, "o muestra tu cara", (ancho//2 - 95, alto//2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 1)

    return crear_fondo(frame, panel, clave)
