import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                              QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore    import Qt

class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.iniciado = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simulador Facial")
        self.setFixedSize(700, 400)
        self.setStyleSheet("background-color: #111111;")

        # Centrar en pantalla
        pantalla = QApplication.desktop().screenGeometry()
        x = (pantalla.width()  - self.width())  // 2
        y = (pantalla.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()
        layout.setContentsMargins(60, 50, 60, 40)
        layout.setSpacing(10)

        # Título
        titulo = QLabel("Detector Facial")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: #ffffff;
            font-size: 30px;
            font-weight: bold;
            font-family: Arial;
        """)
        layout.addWidget(titulo)

        # Línea
        linea = QLabel()
        linea.setFixedHeight(1)
        linea.setStyleSheet("background-color: #2a2a2a;")
        layout.addWidget(linea)

        # Bienvenida
        bienvenida = QLabel("Bienvenido a nuestro detector facial")
        bienvenida.setAlignment(Qt.AlignCenter)
        bienvenida.setStyleSheet("""
            color: #aaaaaa;
            font-size: 16px;
            font-family: Arial;
            padding-top: 10px;
        """)
        layout.addWidget(bienvenida)

        # Instrucción
        instruccion = QLabel(
            "Antes de comenzar, asegúrate de estar cerca de la cámara\n"
            "y de que solo tú te encuentres frente a ella."
        )
        instruccion.setAlignment(Qt.AlignCenter)
        instruccion.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            font-family: Arial;
            padding-top: 5px;
            padding-bottom: 20px;
        """)
        layout.addWidget(instruccion)

        # Tip
        tip = QLabel("Mantén una expresión neutral al inicio para mejores resultados.")
        tip.setAlignment(Qt.AlignCenter)
        tip.setStyleSheet("""
            color: #888888;
            font-size: 13px;
            font-family: Arial;
        """)
        layout.addWidget(tip)

        layout.addStretch()

        # Botón
        btn = QPushButton("Comenzar")
        btn.setFixedSize(160, 40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a5c;
                color: #ffffff;
                font-size: 14px;
                font-family: Arial;
                border: 1px solid #2a5a8c;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: ##2a5a8c;
                border: 1px solid #4a8abc6;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)
        btn.clicked.connect(self.comenzar)

        layout_btn = QHBoxLayout()
        layout_btn.addStretch()
        layout_btn.addWidget(btn)
        layout_btn.addStretch()
        layout.addLayout(layout_btn)

        # Instrucción teclado
        tecla = QLabel("Presiona Enter o haz clic en Comenzar para iniciar")
        tecla.setAlignment(Qt.AlignCenter)
        tecla.setStyleSheet("""
            color: #666666;
            font-size: 11px;
            font-family: Arial;
            padding-top: 8px;
        """)
        layout.addWidget(tecla)

        self.setLayout(layout)

    def comenzar(self):
        self.iniciado = True
        self.close()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.comenzar()
        elif event.key() == Qt.Key_Escape:
            self.close()


def mostrar_pantalla_inicio():
    app     = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    app.exec_()
    return ventana.iniciado