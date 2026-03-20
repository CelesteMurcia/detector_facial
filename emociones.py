def detectar_emocion(resultados_cara):
    if not resultados_cara or not resultados_cara.multi_face_landmarks:
        return None

    puntos = resultados_cara.multi_face_landmarks[0].landmark

    # Puntos de la boca 
    labio_sup      = puntos[13].y
    labio_inf      = puntos[14].y
    comisura_izq   = puntos[61].y
    comisura_der   = puntos[291].y
    boca_izq       = puntos[78].y
    boca_der       = puntos[308].y

    # Puntos de cejas 
    ceja_izq       = puntos[107].y
    ceja_der       = puntos[336].y

    # Referencia 
    nariz          = puntos[1].y
    menton         = puntos[152].y

    # Cálculos 
    apertura_boca  = abs(labio_sup - labio_inf)
    centro_boca    = (boca_izq + boca_der) / 2
    dist_cejas     = abs(ceja_izq - nariz) + abs(ceja_der - nariz)
    alto_cara      = abs(nariz - menton)

    # Comisuras hacia arriba = sonrisa o risa
    sonriendo = comisura_izq < centro_boca and comisura_der < centro_boca

    # Sonrisa: comisuras arriba pero boca menos abierta que risa
    sonrisa = sonriendo and 0.02 < apertura_boca <= 0.07


    if sonrisa:
        return "sonrisa"
    elif dist_cejas < 0.22:
        return "enojado"
    elif dist_cejas < 0.30:
        return "neutral"

    return None