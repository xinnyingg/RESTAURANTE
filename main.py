# main.py

import sys
from PyQt5.QtWidgets import QApplication
from model import OrderModel
from view import MainView
from presenter import Presenter

def main():
    app   = QApplication(sys.argv)

    model = OrderModel()
    view  = MainView()
    presenter = Presenter(model, view)      # <-- imprescindible

    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
