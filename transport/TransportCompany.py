from Vehicle import Vehicle
from Client import Client
from Truck import Truck
from Train import Train

class TransportCompany:
    def __init__(self, name, vehicles, clients):
        if not name or not name.strip(): # проверяем, что имя не пустое или не состоит только из пробелов
            raise ValueError("Название компании не может быть пустой строкой.")
        
        self.name = name  
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle): # проверяем, что добавляемый объект является экземпляром класса Vehicle
            raise ValueError("Нельзя добавить не транспортное средство.")
        self.vehicles.append(vehicle) # добавляем транспорт в список

    def list_vehicles(self):
        return self.vehicles # возвращаем список транспортных средств

    def add_client(self, client):
        if not isinstance(client, Client): # проверяем, что добавляемый объект является экземпляром класса Client
            raise ValueError("Клиентов нет.")
        self.clients.append(client) # добавляем клиента в список

    def optimize_cargo_distribution(self):
        vip_clients = [client for client in self.clients if client.is_vip] # получаем список VIP-клиентов
        simple_clients = [client for client in self.clients if not client.is_vip] # получаем список обычных клиентов

        vip_clients.sort(key=lambda c: c.cargo_weight, reverse=True) # сортируем VIP-клиентов по весу груза в порядке убывания
        simple_clients.sort(key=lambda c: c.cargo_weight, reverse=True) # сортируем обычных клиентов по весу груза в порядке убывания

        for client in vip_clients: # проходим по каждому VIP-клиенту
            for vehicle in self.vehicles: # проходим по каждому транспортному средству
                if isinstance(vehicle, Truck) or isinstance(vehicle, Train): # проверяем, является ли транспортное средство грузовиком или поездом
                    try: # пробуем загрузить груз
                        vehicle.load_cargo(client) # загружаем груз в транспортное средство
                        break # если груз загружен, выходим из цикла
                    except ValueError: # если недостаточно места
                        continue # переходим к следующему транспортному средству

        for client in simple_clients: # тоже самое с обычными клиентами
            for vehicle in self.vehicles:
                if isinstance(vehicle, Truck) or isinstance(vehicle, Train):
                    try:
                        vehicle.load_cargo(client)
                        break
                    except ValueError:
                        continue

    def __str__(self):
        return f"Название компании: {self.name}"