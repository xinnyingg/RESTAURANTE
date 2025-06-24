# main.py

import sys
# Importamos el módulo sys para acceder a argumentos de la línea de comandos y controlar la salida de la aplicación.

from PyQt5.QtWidgets import QApplication
# QApplication es la clase que gestiona la aplicación Qt, inicializa el entorno gráfico y el bucle de eventos.

from model import OrderModel
# Importamos nuestra clase OrderModel, que contiene la lógica de datos (platos, cantidades, historial).

from view import MainView
# Importamos MainView, ventana principal generada con QtDesigner y para emitir señales cuando el usuario interactúa.

from presenter import Presenter
# Importamos Presenter, que conecta model y view, gestiona la lógica de negocio y responde a las señales de view.

def main():

    # 1) Creamos la aplicación Qt
    app = QApplication(sys.argv)

    # 2) Instanciamos el modelo de datos
    model = OrderModel()

    # 3) Instanciamos la vista (interfaz gráfica)
    view = MainView()

    # 4) Creamos el presenter y lo conectamos
    presenter = Presenter(model, view)

    # 5) Mostramos la ventana en pantalla
    view.show()

    # 6) Arrancamos el bucle de eventos Qt
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
