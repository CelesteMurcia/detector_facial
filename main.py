import cv2
import mediapipe as mp
from camara          import Camara
from detector        import DetectorRostros
from gestos          import detectar_gesto, detectar_gesto_doble, detectar_mano_arriba, confirmar_gesto
from emociones       import detectar_emocion
from mostrar         import mostrar_imagen
from pantalla_inicio import mostrar_pantalla_inicio
import estilos

# Pantalla de inicio
if not mostrar_pantalla_inicio():
    exit()

# Inicialización
camara   = Camara()
detector = DetectorRostros()

mp_manos  = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
manos     = mp_manos.Hands(
    max_num_hands=2,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.7
)

mp_cara = mp.solutions.face_mesh
cara    = mp_cara.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

emocion_actual = None
clave_anterior = None
contador       = 0
frames_mostrar = 0

while True:
    ret, frame = camara.leer_frame()
    if not ret or frame is None:
        continue

    clave_activa = None
    rgb          = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False

    # Detección de rostros
    rostros = detector.detectar(frame)
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x+w, y+h),
                      estilos.COLOR_RECTANGULO, estilos.GROSOR_RECTANGULO)

    # Detección de emoción cada 5 frames
    contador += 1
    if contador % 5 == 0:
        resultados_cara = cara.process(rgb)
        emocion_actual  = detectar_emocion(resultados_cara)

    if emocion_actual:
        clave_activa = emocion_actual

    # Detección de gestos
    resultado = manos.process(rgb)
    rgb.flags.writeable = True

    if resultado.multi_hand_landmarks:
        for mano in resultado.multi_hand_landmarks:
            mp_dibujo.draw_landmarks(
                frame, mano, mp_manos.HAND_CONNECTIONS,
                mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
                mp_dibujo.DrawingSpec(color=(0, 0, 255), thickness=1)
            )

        gesto_doble = detectar_gesto_doble(resultado.multi_hand_landmarks)
        if gesto_doble:
            gesto_confirmado = confirmar_gesto(gesto_doble)
            if gesto_confirmado:
                clave_activa   = gesto_confirmado
                frames_mostrar = 15
        else:
            for mano in resultado.multi_hand_landmarks:
                mano_alta = detectar_mano_arriba(mano, frame.shape[0])
                if mano_alta:
                    gesto_confirmado = confirmar_gesto(mano_alta)
                    if gesto_confirmado:
                        clave_activa   = gesto_confirmado
                        frames_mostrar = 15
                    break

                gesto = detectar_gesto(mano)
                gesto_confirmado = confirmar_gesto(gesto)
                if gesto_confirmado:
                    clave_activa   = gesto_confirmado
                    frames_mostrar = 15
                    break
    else:
        confirmar_gesto(None)

    # Mantiene imagen visible unos frames más
    if not clave_activa and frames_mostrar > 0:
        clave_activa    = clave_anterior
        frames_mostrar -= 1

    if clave_activa:
        clave_anterior = clave_activa

    # Muestra el frame final con todo el diseño
    frame_final = mostrar_imagen(frame, clave_activa)
    cv2.imshow("Simulador Facial", frame_final)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q'):
        break

camara.liberar()