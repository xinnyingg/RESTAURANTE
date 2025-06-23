# model.py
class Dish:
    def __init__(self, name: str, price: float, image_path: str):
        self.name = name
        self.price = price
        self.image_path = image_path
        self.quantity = 0

class OrderModel:
    def __init__(self):
        # Rellena con las 7 rutas y datos de tus imágenes
        self.dishes = [
            Dish("Lasagna", 15.0, "images/lasagna.jpg"),
            Dish("Spaghetti Carbonara", 10.0, "images/carbonara.jpg"),
            Dish("Risotto alla Milanese", 10.0, "images/risotto.jpg"),
            Dish("Fettuccine Alfredo", 10.0, "images/alfredo.jpg"),
            Dish("Ravioli", 8.0, "images/ravioli.jpg"),
            Dish("Minestrone", 12.0, "images/minestrone.jpg"),
            Dish("Pizza Margherita", 10.0, "images/cheesecake.jpg"),
        ]

    def total(self) -> float:
        return sum(d.price * d.quantity for d in self.dishes)
