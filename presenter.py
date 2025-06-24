# presenter.py

from PyQt5.QtWidgets import QMessageBox
# Importamos QMessageBox para mostrar ventanas de advertencia e información

class Presenter:
    def __init__(self, model, view):
        # Este es el "constructor" del Presenter.
        # model: instancia de OrderModel (guarda los datos y hace cálculos)
        # view:  instancia de MainView  (muestra la interfaz al usuario)
        self.model = model
        self.view  = view

        # — Conectamos las "señales" de view con métodos —
        # Cuando view emite addClicked(idx), se ejecuta self.on_add(idx)
        view.addClicked.connect(self.on_add)
        # Cuando view emite removeClicked(idx), se ejecuta self.on_remove(idx)
        view.removeClicked.connect(self.on_remove)
        # Cuando view emite placeOrder(), se ejecuta self.on_place_order()
        view.placeOrder.connect(self.on_place_order)
        # Cuando view emite deleteOrderRequested(idx), se ejecuta self.on_delete_order(idx)
        view.deleteOrderRequested.connect(self.on_delete_order)

        # Al iniciar, sincronizamos toda la vista con el estado inicial del modelo
        self.refresh_all()

    def on_add(self, idx):
        """Se llama cuando el usuario hace clic en 'Añadir' de un plato."""
        # Incrementamos la cantidad del plato idx en model
        self.model.dishes[idx].quantity += 1
        # Actualizamos la interfaz solo para ese plato
        self.refresh_item(idx)

    def on_remove(self, idx):
        """Se llama cuando el usuario hace clic en 'Eliminar' de un plato."""
        # Solo restamos si la cantidad era mayor que cero
        if self.model.dishes[idx].quantity > 0:
            self.model.dishes[idx].quantity -= 1
            self.refresh_item(idx)

    def refresh_item(self, idx):
        """
        Actualiza en view:
         - label que muestra la cantidad
         - el botón 'Eliminar' (habilitado o no)
         - label que muestra el precio total
        para el plato con índice idx.
        """
        d = self.model.dishes[idx]                 # plato actual
        self.view.set_quantity(idx, d.quantity)    # muestra nueva cantidad
        # habilita 'Eliminar' solo si quantity > 0
        self.view.set_remove_enabled(idx, d.quantity > 0)
        # actualiza el precio total en view
        self.view.set_total(self.model.total())

    def refresh_all(self):
        """
        Inicializa todos los platos en view:
         - pone cada cantidad a 0
         - deshabilita todos los botones 'Eliminar'
         - actualiza el precio total a 0.00 €
        Útil al iniciar y tras resetear el modelo.
        """
        for i, d in enumerate(self.model.dishes):
            self.view.set_quantity(i, d.quantity)
            self.view.set_remove_enabled(i, False)
        self.view.set_total(self.model.total())

    def on_place_order(self):
        """
        Se ejecuta al pulsar 'Realizar Pedido'.
        1) Si total == 0 → muestra warning y no avanza.
        2) Si total > 0 → guarda pedido, cambia a la pestaña Historial, muestra confirmación,
                          y añadir y mostrar en historial.
        3) Resetea el modelo y refresca view.
        """
        total = self.model.total()  # calculamos el total actual
        # 1) Si no hay nada seleccionado, notificamos al usuario
        if total == 0:
            QMessageBox.warning(
                self.view,
                "Pedido vacío",
                "No hay nada seleccionado."
            )
            return  # salimos sin guardar ni cambiar de pestaña

        # 2.1) Guardar el pedido en el model
        self.model.add_order()
        order_number = len(self.model.history)   # Número de pedido = tamaño actual del historial
        last = self.model.history[-1]            # Recuperamos el último pedido que acabamos de guardar

        # 2.2) Cambiamos a la pestaña de Historial
        self.view.goto_historial()

        # 2.3) Añadimos y mostrarlo en view (lista de historial)
        self.view.add_history_entry(
            order_number,
            last["items"],
            last["total"]
        )

        # 2.4) Mostramos un mensaje de éxito
        QMessageBox.information(
            self.view,
            "Pedido",
            "Pedido realizado correctamente"
        )

        # 3) Preparamos un nuevo pedido: reseteamos model y refrescamos view
        self.model.reset()
        self.refresh_all()

    def on_delete_order(self, idx: int):
        """
        Se ejecuta al pulsar 'Eliminar Pedido' en la pestaña Historial:
        1) Borra el pedido idx del model.
        2) Limpia la lista y la vuelve a rellenar desde el model.
        """
        # 1) Eliminar del modelo si idx está en rango
        if 0 <= idx < len(self.model.history):
            del self.model.history[idx]

        # 2) Actualizar la vista: limpiar y repoblar historial
        self.view.clear_history()
        for i, order in enumerate(self.model.history, start=1):
            self.view.add_history_entry(
                i,
                order["items"],
                order["total"]
            )