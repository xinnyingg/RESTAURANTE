# presenter.py
from PyQt5.QtWidgets import QMessageBox

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view  = view

        view.addClicked.connect(self.on_add)
        view.removeClicked.connect(self.on_remove)
        view.placeOrder.connect(self.on_place_order)

        self.refresh_all()

    def on_add(self, idx: int):
        self.model.dishes[idx].quantity += 1
        self.refresh_item(idx)

    def on_remove(self, idx: int):
        if self.model.dishes[idx].quantity > 0:
            self.model.dishes[idx].quantity -= 1
            self.refresh_item(idx)

    def refresh_item(self, idx: int):
        d = self.model.dishes[idx]
        self.view.set_quantity(idx, d.quantity)
        self.view.set_remove_enabled(idx, d.quantity > 0)
        self.view.set_total(self.model.total())

    def refresh_all(self):
        for i, d in enumerate(self.model.dishes):
            self.view.set_quantity(i, d.quantity)
            self.view.set_remove_enabled(i, False)
        self.view.set_total(self.model.total())

    def on_place_order(self):
        # Si no hay nada pedido, total == 0.0, avisamos
        if self.model.total() == 0:
            QMessageBox.warning(
                self.view,
                "Pedido",
                "No hay nada seleccionado."
            )
        else:
            QMessageBox.information(
                self.view,
                "Pedido",
                "Pedido realizado correctamente."
            )
