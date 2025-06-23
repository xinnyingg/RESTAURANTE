# view.py

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal

class MainView(QMainWindow):
    addClicked    = pyqtSignal(int)   # índice del plato a añadir
    removeClicked = pyqtSignal(int)   # índice del plato a eliminar
    placeOrder    = pyqtSignal()      # señal de “Realizar Pedido”

    def __init__(self):
        super().__init__()

        # 1) Comprueba carga del .ui
        uic.loadUi("restaurante.ui", self)

        # 2) Lista atributos para verificar objectName
        attrs = [a for a in dir(self) if a.startswith("btnAdd") or a.startswith("btnRemove") or a=="btnRealizar"]

        # 3) Conecta cada btnAdd1…btnAdd7
        for i in range(1, 8):
            btn_add = getattr(self, f"btnAdd{i}", None)
            if btn_add:
                btn_add.clicked.connect(lambda _, idx=i-1: self._on_add(idx))

        # 4) Conecta cada btnRemove1…btnRemove7
        for i in range(1, 8):
            btn_rem = getattr(self, f"btnRemove{i}", None)
            if btn_rem:
                btn_rem.clicked.connect(lambda _, idx=i-1: self._on_remove(idx))

        # 5) Conecta btnRealizar
        btn_real = getattr(self, "btnRealizar", None)
        if btn_real:
            btn_real.clicked.connect(self._on_place_order)

    # slots internos que emiten señales para el Presenter
    def _on_add(self, idx):
        self.addClicked.emit(idx)

    def _on_remove(self, idx):
        self.removeClicked.emit(idx)

    def _on_place_order(self):
        self.placeOrder.emit()

    # Métodos para que el Presenter actualice la UI
    def set_quantity(self, index: int, qty: int):
        getattr(self, f"lblNum{index+1}").setText(str(qty))

    def set_remove_enabled(self, index: int, enabled: bool):
        getattr(self, f"btnRemove{index+1}").setEnabled(enabled)

    def set_total(self, total: float):
        self.lblTotal.setText(f"{total:.2f} €")

