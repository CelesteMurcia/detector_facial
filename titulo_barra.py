import cv2

def dibujar_barras(fondo, ancho_total, y_inferior, clave=None, titulo="Simulador Facial"):

    # --- Barra superior ---
    cv2.rectangle(fondo, (0, 0), (ancho_total, 60), (17, 17, 17), -1)
    cv2.line(fondo, (0, 60), (ancho_total, 60), (50, 50, 50), 1)

    tam = cv2.getTextSize(titulo, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)[0]
    x   = (ancho_total - tam[0]) // 2
    cv2.putText(fondo, titulo, (x, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    # --- Barra inferior ---
    cv2.rectangle(fondo, (0, y_inferior), (ancho_total, y_inferior + 50),
                  (17, 17, 17), -1)
    cv2.line(fondo, (0, y_inferior), (ancho_total, y_inferior), (50, 50, 50), 1)

    cv2.putText(fondo, "Presiona Q para salir", (20, y_inferior + 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 80, 80), 1)

    if clave:
        texto = clave.upper()
        tam   = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        x     = (ancho_total - tam[0]) // 2
        cv2.putText(fondo, texto, (x, y_inferior + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)