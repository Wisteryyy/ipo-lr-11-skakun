import uuid # импортируем модуль uuid для генерации уникальных идентификаторов

class Vehicle: # определяем класс Vehicle
    def __init__(self, capacity): # конструктор класса
        if not isinstance(capacity, (int, float)) or capacity < 0: # проверка, является ли capacity положительным числом
            raise ValueError("Грузоподьемность должна быть положительным числом.")

        self.vehicle_id = str(uuid.uuid4()) # генерируем уникальный идентификатор для транспортного средства
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []

    def load_cargo(self, client): # метод для загрузки груза
        if not hasattr(client, 'cargo_weight'): # проверка, имеет ли объект client атрибут cargo_weight
            raise ValueError("Объект client должен иметь cargo_weight.")

        cargo_weight = client.cargo_weight # достаем вес груза из объекта client
        if not isinstance(cargo_weight, (float, int)) or cargo_weight < 0: # проверка, является ли cargo_weight положительным числом
            raise ValueError("Вес груза должен быть положительным числом.")

        if self.current_load + cargo_weight > self.capacity: # проверка, не превышает ли текущая загрузка плюс вес груза грузоподъемность
            raise ValueError("Недостаточно грузоподъемности для загрузки данного груза.")
        
        self.current_load += cargo_weight # увеличиваем текущую загрузку на вес груза
        self.clients_list.append(client) # добавляем имя клиента в список клиентов

    def __str__(self): # магический метод для строкового представления объекта
        return f"Уникальный идентификатор: {self.vehicle_id}, Грузоподьемность: {self.capacity} тонн, Текущая загрузка: {self.current_load} тонн"
    
class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        if not isinstance(color, str) or not color: # проверка на всякий бред по типу пробела вместо строки
            raise ValueError("Цвет должен быть непустой строкой.")
        
        self.color = color # цвет грузовика

    def __str__(self):
        first_str = super().__str__() # получаем изначальную строку
        return f"{first_str}, Цвет: {self.color}" # добавляем цвет в строку