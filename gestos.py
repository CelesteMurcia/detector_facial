from collections import Counter
import math

historial_gestos    = []
FRAMES_CONFIRMACION = 10

def angulo_dedo(puntos, base, medio, punta):
    # Calcula el ángulo entre tres puntos del dedo
    # Un ángulo grande = dedo extendido, pequeño = doblado
    ax = puntos[base].x  - puntos[medio].x
    ay = puntos[base].y  - puntos[medio].y
    bx = puntos[punta].x - puntos[medio].x
    by = puntos[punta].y - puntos[medio].y

    dot     = ax * bx + ay * by
    mag_a   = math.sqrt(ax**2 + ay**2)
    mag_b   = math.sqrt(bx**2 + by**2)

    if mag_a * mag_b == 0:
        return 0

    cos_ang = dot / (mag_a * mag_b)
    cos_ang = max(-1, min(1, cos_ang)) 
    return math.degrees(math.acos(cos_ang))


def dedo_extendido(puntos, base, medio, punta, umbral=150):
    # Dedo extendido si el ángulo es mayor al umbral
    return angulo_dedo(puntos, base, medio, punta) > umbral


def detectar_gesto(mano):
    p = mano.landmark

    # Detecta si es mano derecha o izquierda
    es_derecha = p[17].x < p[5].x


    indice  = dedo_extendido(p, 5,  6,  8,  umbral=140)
    medio   = dedo_extendido(p, 9,  10, 12, umbral=150)
    anular  = dedo_extendido(p, 13, 14, 16, umbral=150)
    menique = dedo_extendido(p, 17, 18, 20, umbral=150)

    # Pulgar con ángulo diferente por su orientación
    pulgar  = dedo_extendido(p, 2,  3,  4,  umbral=140)

    dedos = [indice, medio, anular, menique]

    if all(dedos) and pulgar:
        return "pregunta"

    if not any(dedos) and not pulgar:
        return "puño"
    
    if indice and not medio and not anular and not menique:
        return "idea"

    if pulgar and not any(dedos):
        return "me gusta"

    if pulgar and menique and not indice and not medio and not anular:
        return "tranquilo"

    
    if indice and medio and not anular and not menique:
        return "pensando"

    return None


def confirmar_gesto(gesto_nuevo):
    global historial_gestos

    historial_gestos.append(gesto_nuevo)

    if len(historial_gestos) > FRAMES_CONFIRMACION:
        historial_gestos.pop(0)

    if len(historial_gestos) < FRAMES_CONFIRMACION:
        return None

    conteo = Counter(historial_gestos)
    gesto_mas_comun, veces = conteo.most_common(1)[0]

    if veces >= FRAMES_CONFIRMACION * 0.75 and gesto_mas_comun is not None:
        return gesto_mas_comun

    return None


def detectar_gesto_doble(lista_manos):
    if len(lista_manos) < 2:
        return None

    gestos  = [detectar_gesto(mano) for mano in lista_manos]
    munecas = [mano.landmark[0].y for mano in lista_manos]

    if gestos.count("puño") == 2:
        return "puños"
    if gestos.count("pregunta") == 2:
        return "asombro"

    return None


def detectar_mano_arriba(mano, alto_frame):
    muneca_y = mano.landmark[0].y
    if muneca_y < 0.35:
        return "mano_arriba"
    return None