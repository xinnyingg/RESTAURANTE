# main.py

import sys
# Importamos el módulo sys para acceder a argumentos de la línea de comandos
# y controlar la salida de la aplicación.

from PyQt5.QtWidgets import QApplication
# QApplication es la clase que gestiona la aplicación Qt,
# inicializa el entorno gráfico y el bucle de eventos.

from model import OrderModel
# Importamos nuestra clase OrderModel, que contiene la lógica
# de datos (platos, cantidades, historial).

from view import MainView
# Importamos MainView, nuestra ventana principal generada con QtDesigner
# y adaptada para emitir señales cuando el usuario interactúa.

from presenter import Presenter
# Importamos Presenter, que conecta el modelo y la vista,
# gestiona la lógica de negocio y responde a las señales de la vista.

def main():
    # Punto de entrada de nuestra aplicación

    app = QApplication(sys.argv)
    # Creamos la instancia de QApplication.
    # sys.argv contiene argumentos de línea de comandos (no usados aquí),
    # pero Qt los procesa internamente (p. ej. estilos o paths).

    model = OrderModel()
    # Instanciamos el modelo de datos. Aquí se crean los platos
    # y el historial vacío.

    view = MainView()
    # Creamos la ventana principal, que carga el .ui y define
    # la interfaz gráfica (botones, listas, pestañas...).

    presenter = Presenter(model, view)  # <-- imprescindible
    # Creamos el Presenter, pasando modelo y vista.
    # El Presenter:
    # 1) Conecta señales de la vista (clics de botones) a sus métodos.
    # 2) Llama a refresh_all() para inicializar la UI con datos del modelo.

    view.show()
    # Hacemos visible la ventana principal en pantalla.

    sys.exit(app.exec_())
    # app.exec_() arranca el bucle de eventos de Qt (escucha clics, redraws, etc.).
    # sys.exit(...) asegura que, cuando salga del bucle, el proceso termine limpio
    # y devuelva el código de salida apropiado al sistema operativo.

if __name__ == "__main__":
    # Esta comprobación evita que main() se ejecute si importamos este archivo
    # desde otro módulo. Solo se ejecuta si lanzamos directamente "python main.py".
    main()
