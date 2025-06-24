# model.py

"""
Esta clase representa cada plato del menú, con su nombre, precio unitario y la cantidad que el cliente ha pedido.
"""
class Dish:
    def __init__(self, name: str, price: float):
        # Guarda el nombre del plato
        self.name     = name
        # Guarda el precio unitario del plato
        self.price    = price
        # Inicializa la cantidad pedida de este plato a cero
        self.quantity = 0


# Definimos la clase que maneja todos los datos del pedido
"""
Esta clase maneja todos los datos de los pedidos:
 - lista de platos disponibles (Dish)
 - historial de pedidos realizados
 - cálculo de precios totales
"""
class OrderModel:
    def __init__(self):
        # Creamos una lista de objetos Dish con los platos disponibles
        self.dishes = [
            Dish("Lasagna", 15.0),
            Dish("Spaghetti Carbonara", 10.0),
            Dish("Risotto alla Milanese", 10.0),
            Dish("Fettuccine Alfredo", 10.0),
            Dish("Ravioli", 8.0),
            Dish("Minestrone", 12.0),
            Dish("Pizza Margherita", 10.0),
        ]
        # Inicialmente no hay ningún pedido en el historial, guardaremos como una lista de diccionarios
        self.history = []

    def total(self) -> float:
        """
        Calcula el precio total del pedido actual.
        Recorre cada plato (Dish) y suma price * quantity.
        """
        return sum(
            d.price * d.quantity  # coste de cada plato = precio × unidades pedidas
            for d in self.dishes  # para cada Dish en la lista
        )

    def add_order(self):
        """
        Guarda el pedido actual en el historial:
        1) Filtra solo los platos con quantity > 0.
        2) Construye una lista de tuplas (nombre, cantidad).
        3) Calcula el total con self.total().
        4) Añade un dict al self.history.
        """
        # Paso 1 y 2: creamos lista de (nombre, cantidad) solo si se pidió algo
        items = [
            (d.name, d.quantity)        # tupla con nombre y cantidad
            for d in self.dishes        # recorre todos los platos
            if d.quantity > 0           # y filtra los que tienen qty > 0
        ]
        # Paso 3: calculamos el total
        total = self.total()
        # Paso 4: guardamos en el historial un diccionario con items y total
        self.history.append({
            "items": items,  # lista de (nombre, qty)
            "total": total   # importe total del pedido
        })

    def reset(self):
        """
        Vuelve todas las cantidades a cero después de concretar un pedido,
        para preparar un nuevo pedido sin restos del anterior.
        """
        for d in self.dishes:  # recorre cada Dish
            d.quantity = 0      # y pone su cantidad a 0
