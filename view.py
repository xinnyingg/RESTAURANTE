# view.py

import os  # módulo para interactuar con el sistema de archivos
from PyQt5 import uic  # para compilar y cargar archivos .ui de Qt Designer
from PyQt5.QtWidgets import (  # importamos los widgets básicos de PyQt5
    QMainWindow,    # ventana principal con barra de menú, status bar, etc.
    QAction,        # acción del menú que el usuario puede clicar
    QPushButton,    # botón clicable
    QLabel,         # etiqueta de texto
    QListWidget,    # lista de elementos de texto
    QStackedWidget  # contenedor de “páginas” que se muestran una a la vez
)
from PyQt5.QtCore import pyqtSignal  # para definir señales personalizadas

# Compilamos el archivo restaurante.ui en dos clases Python:
# Ui_MainWindow: la clase que tiene setupUi()
# QtBaseClass: la clase base (QMainWindow) de la UI
Ui_MainWindow, QtBaseClass = uic.loadUiType("restaurante.ui")

class MainView(QtBaseClass, Ui_MainWindow):
    # Definimos señales que emitiremos cuando el usuario interactúe
    addClicked           = pyqtSignal(int)  # indice de plato a añadir
    removeClicked        = pyqtSignal(int)  # indice de plato a eliminar
    placeOrder           = pyqtSignal()     # señal para “Realizar Pedido”
    deleteOrderRequested = pyqtSignal(int)  # índice de pedido a borrar

    def __init__(self):
        super().__init__()       # inicializamos la superclase (QMainWindow)
        self.setupUi(self)       # cargamos la UI diseñada en Qt Designer

        # --- Configuración de la barra de menú ---
        self.menuBar().clear()   # Borrar cualquier menú preexistente
        for text, slot in [
            ("Realizar Pedido", self.goto_pedido),     # acción → mostrar página 0
            ("Historial",       self.goto_historial),  # acción → mostrar página 1
            ("Sobre nosotros",  self.goto_sobre)       # acción → mostrar página 2
        ]:
            act = QAction(text, self)         # creamos la acción con ese texto
            act.triggered.connect(slot)       # conectamos su señal clicked → slot
            self.menuBar().addAction(act)     # la añadimos a la barra de menú

        # --- Conexión de los botones “Añadir” y “Eliminar” para cada plato ---
        for i in range(1, 8):
            btn_add = getattr(self, f"btnAdd{i}")       # Obtiene self.btnAdd1, self.btnAdd2, …
            btn_rem = getattr(self, f"btnRemove{i}")    # Obtiene self.btnRemove1, …
            # al clicar btnAdd emitimos addClicked(i-1)
            btn_add.clicked.connect(lambda _, idx=i-1: self.addClicked.emit(idx))
            # al clicar btnRemove emitimos removeClicked(i-1)
            btn_rem.clicked.connect(lambda _, idx=i-1: self.removeClicked.emit(idx))

        # --- Conexión del botón “Realizar Pedido” ---
        # Intentamos desconectar cualquier slot anterior para evitar cierres automáticos
        try:
            self.btnRealizar.clicked.disconnect()
        except Exception:
            pass
        # Luego conectamos solo nuestra señal placeOrder
        self.btnRealizar.clicked.connect(lambda: self.placeOrder.emit())

        # --- Conexión del botón “Eliminar Pedido” en la pestaña Historial ---
        if hasattr(self, "btnDeleteOrder"):
            self.btnDeleteOrder.clicked.connect(self._emit_delete_order)

    def _emit_delete_order(self):
        """
        Método interno que lee la fila seleccionada en lstHistory
        y emite deleteOrderRequested con ese índice.
        """
        idx = self.lstHistory.currentRow()  # fila actualmente seleccionada
        if idx >= 0:                        # si hay una selección válida
            self.deleteOrderRequested.emit(idx)

    # — Métodos que el Presenter usará para actualizar la UI —
    def set_quantity(self, index: int, qty: int):
        # Actualiza el label lblNumX con la nueva cantidad
        lbl = getattr(self, f"lblNum{index+1}")
        lbl.setText(str(qty))

    def set_remove_enabled(self, index: int, enabled: bool):
        # Activa o desactiva el botón btnRemoveX según enabled
        btn = getattr(self, f"btnRemove{index+1}")
        btn.setEnabled(enabled)

    def set_total(self, total: float):
        # Muestra el precio total en lblTotal
        self.lblTotal.setText(f"{total:.2f} €")

    def clear_history(self):
        # Borra todos los elementos de la lista lstHistory
        self.lstHistory.clear()

    def add_history_entry(self, order_number: int, items: list, total: float):
        """Añade una línea al lstHistory con el texto:'Pedido N: Plato1 x2, Plato2 x1 — Total: XX.XX €'"""
        # 1) Construimos fragmentos 'Nombre xCantidad' para cada ítem
        parts = [f"{name} x{qty}" for name, qty in items]
        # 2) Formamos la línea completa
        entry = f"Pedido {order_number}: " + ", ".join(parts) + f" — Total: {total:.2f} €"
        # 3) Añadimos a la lista
        self.lstHistory.addItem(entry)

    # — Slots para cambiar de página en el QStackedWidget —

    def goto_pedido(self):
        # Muestra la página 0 (Realizar Pedido)
        self.stackedWidget.setCurrentIndex(0)

    def goto_historial(self):
        # Muestra la página 1 (Historial)
        self.stackedWidget.setCurrentIndex(1)

    def goto_sobre(self):
        # Muestra la página 2 (Sobre nosotros)
        self.stackedWidget.setCurrentIndex(2)
