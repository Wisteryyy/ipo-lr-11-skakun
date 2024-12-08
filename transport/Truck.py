from .Vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        if not isinstance(color, str) or not color.strip(): # проверка на всякий бред по типу пробела вместо строки
            raise ValueError("Цвет должен быть непустой строкой.")
        
        self.color = color  # цвет грузовика

    def __str__(self):
        first_str = super().__str__() # получаем изначальную строку
        return f"Грузовик, {first_str}, Цвет: {self.color}" # добавляем цвет в строку
