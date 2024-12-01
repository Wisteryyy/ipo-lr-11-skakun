from transport.Client import Client
from transport.Vehicle import Vehicle
from transport.Truck import Truck
from transport.Train import Train
from transport.TransportCompany import TransportCompany
import json


def load_data_from_json():
    try:
        with open("dump.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return [] # если файл отсутствует, возвращаем пустой список

def save_data_to_json(data):
    with open("dump.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


company = TransportCompany("Транспортная Компания")
clients_data = load_data_from_json()

for client_dict in clients_data:
    try:
        client = Client(client_dict['name'], client_dict['cargo_weight'], client_dict['is_vip'])
        company.add_client(client)
    except ValueError as e:
        print(f"Ошибка при загрузке клиента: {e}")

status = True

while status:
    print("--------------------------------")
    print("--------------Меню--------------")
    print("-----1. Клиенты компании--------")
    print("-----2. Транспортное средство---")
    print("-----3. Распределение грузов----")
    print("-----4. Выход-------------------")
    print("--------------------------------")

    b = input("Введите номер желаемой операции: ")
    try:
        a = int(b)
        if a < 1 or a > 4:
            print("Введите корректный номер.")
            continue
    except ValueError:
        print("Введите целочисленное число.")
        continue

    if a == 1:
        while True:
            print("---------------------------------------------------------")
            print("-------Какую именно операцию Вы бы хотели совершить?-----")
            print("--1. Создание клиента(ов)--------------------------------")
            print("--2. Просмотреть информацию о уже существующих клиентах--")
            print("--3. Назад к главному меню-------------------------------")
            print("---------------------------------------------------------")
            d = input("Введите номер желаемой операции: ")
            try:
                c = int(d)
                if c < 1 or c > 3:
                    print("Введите корректный номер.")
                    continue
            except ValueError:
                print("Введите целочисленное число.")
                continue

            if c == 1:
                while True:
                    f = input("Введите количество клиентов, которых Вы бы хотели создать: ")
                    try:
                        e = int(f)
                        if e < 1:
                            print("Введите корректное количество клиентов.")
                            continue
                        break
                    except ValueError:
                        print("Введите целочисленное число.")

                clients_data = []
                for i in range(e):
                    while True:
                        name = input(f"Введите имя клиента {i + 1}: ")
                        if name.strip() == "":
                            print("Имя клиента не может быть пустым. Повторите ввод.")
                            continue
                        else:
                            break

                    while True:
                        cargo_weight = input(f"Введите вес груза {i + 1} клиента: ")
                        try:
                            cargo_weight_float = float(cargo_weight)
                            if cargo_weight_float < 0:
                                print("Вес груза должен быть положительным числом.")
                                continue
                            break
                        except ValueError:
                            print("Введите корректный вес груза.")

                    while True:
                        is_vip = input(f"Есть ли у {i + 1} клиента VIP-статус? (True/False): ")
                        if is_vip.lower() in ['true', 'false']:
                            is_vip_bool = is_vip.lower() == 'true'
                            break
                        else:
                            print("Введите корректный VIP-статус (True/False).")

                    try:
                        client = Client(name, cargo_weight_float, is_vip_bool)
                        company.add_client(client)
                        clients_data.append(client.__dict__)  # сохраняем данные клиента в список
                        print(f"Клиент {name} добавлен.")
                    except ValueError as e:
                        print(f"Ошибка: {e}")

                save_data_to_json(clients_data)

            elif c == 2:
                if not company.clients:
                    print("В данный момент нет клиентов.")
                else:
                    print("Список клиентов:")
                    for client in clients_data:
                        print(f"Имя клиента: {client['name']}, Вес груза: {client['cargo_weight']}, VIP-статус: {client['is_vip']}")

            elif c == 3:
                break

    elif a == 2:
        while True:
            print("----------------------------------------------")
            print("--Выберите транспорт для указания параметров--")
            print("----------1. Грузовик-------------------------")
            print("----------2. Поезд----------------------------")
            print("----------3. Назад к главному меню------------")
            print("----------------------------------------------")
            f = input("Выберите номер желаемой операции: ")
            try:
                e = int(f)
                if e < 1 or e > 3:
                    print("Введите корректный номер.")
                    continue
            except ValueError:
                print("Введите целочисленное число.")
                continue

            if e == 1:
                while True:
                    print("---------------------------------------------------------")
                    print("-------Какую именно операцию Вы бы хотели совершить?-----")
                    print("-1. Зарегистрировать грузовик----------------------------")
                    print("-2. Просмотреть информацию о уже существующих грузовиках-")
                    print("-3. Назад к главному меню--------------------------------")
                    print("---------------------------------------------------------")
                    p = input("Выберите номер желаемой операции: ")
                    try:
                        n = int(p)
                        if n < 1 or n > 3:
                            print("Введите корректный номер.")
                            continue
                    except ValueError:
                        print("Введите целочисленное число.")
                        continue

                    if n == 1:
                        while True:
                            q = input("Введите количество грузовиков, которых Вы хотите создать: ")
                            try:
                                w = int(q)
                                if w < 1:
                                    print("Введите корректное количество грузовиков.")
                                    continue
                                break
                            except ValueError:
                                print("Введите целочисленное число.")

                        for i in range(w):
                            while True:
                                capacity = input(f"Введите грузоподъемность {i + 1} грузовика (в тоннах): ")
                                try:
                                    capacity_float = float(capacity)
                                    if capacity_float <= 0:
                                        print("Грузоподъемность должна быть положительным числом.")
                                        continue
                                    break
                                except ValueError:
                                    print("Введите корректное значение грузоподъемности (число).")

                            while True:
                                color = input(f"Введите цвет {i + 1} грузовика: ")
                                if color.strip() == "":
                                    print("Цвет не может быть пустой строкой.")
                                    continue
                                break

                            try:
                                truck = Truck(capacity_float, color)
                                company.add_vehicle(truck)
                                print(f"Грузовик {color} с грузоподъемностью {capacity_float} тонн добавлен.")
                            except ValueError as e:
                                print(f"Ошибка при добавлении грузовика: {e}")

                    elif n == 2:
                        print("Список грузовиков:")
                        if not company.vehicles:
                            print("В данный момент нет грузовиков.")
                        else:
                            for vehicle in company.list_vehicles():
                                print(vehicle)

                    elif n == 3:
                        break

            elif e == 2:
                while True:
                    print("---------------------------------------------------------")
                    print("-------Какую именно операцию Вы бы хотели совершить?-----")
                    print("-1. Зарегистрировать поезд-------------------------------")
                    print("-2. Просмотреть информацию о уже существующих поездах----")
                    print("-3. Назад к главному меню--------------------------------")
                    print("---------------------------------------------------------")
                    l = input("Выберите номер желаемой операции: ")
                    try:
                        u = int(l)
                        if u < 1 or u > 3:
                            print("Введите корректный номер.")
                            continue
                    except ValueError:
                        print("Введите целочисленное число.")
                        continue

                    if u == 1:
                        while True:
                            q = input("Введите количество поездов, которые Вы хотите создать: ")
                            try:
                                w = int(q)
                                if w < 1:
                                    print("Введите корректное количество поездов.")
                                    continue
                                break
                            except ValueError:
                                print("Введите целочисленное число.")

                        for i in range(w):
                            while True:
                                capacity = input(f"Введите грузоподъемность {i + 1} поезда (в тоннах): ")
                                try:
                                    capacity_float = float(capacity)
                                    if capacity_float <= 0:
                                        print("Грузоподъемность должна быть положительным числом.")
                                        continue
                                    break
                                except ValueError:
                                    print("Введите корректное значение грузоподъемности (число).")

                            while True:
                                number_of_cars = input(f"Введите количество вагонов {i + 1} поезда: ")
                                try:
                                    number_of_cars_int = int(number_of_cars)
                                    if number_of_cars_int <= 0:
                                        print("Количество вагонов должно быть положительным числом.")
                                        continue
                                    break
                                except ValueError:
                                    print("Введите корректное количество вагонов.")

                            try:
                                train = Train(capacity_float, number_of_cars_int)
                                company.add_vehicle(train)
                                print(f"Поезд с грузоподъемностью {capacity_float} тонн и количеством вагонов {number_of_cars_int} добавлен.")
                            except ValueError as e:
                                print(f"Ошибка при добавлении поезда: {e}")

                    elif u == 2:
                        print("Список поездов:")
                        if not company.vehicles:
                            print("В данный момент нет поездов.")
                        else:
                            for vehicle in company.list_vehicles():
                                print(vehicle)

                    elif u == 3:
                        break

    elif a == 3:
        print("----------Распределение грузов----------")

        if not company.clients:
            print("В данный момент нет клиентов для распределения грузов.")
            continue
        if not company.vehicles:
            print("В данный момент нет транспортных средств для распределения грузов.")
            continue

        company.optimize_cargo_distribution()

        print("Распределение грузов выполнено:")
        for vehicle in company.list_vehicles():
            print(vehicle)
            if vehicle.clients_list:
                print("Загруженные клиенты:")
                for client in vehicle.clients_list:
                    print(f" - Имя: {client.name}, Вес груза: {client.cargo_weight}, VIP-статус: {client.is_vip}")
            else:
                print(" - Не загружено ни одного клиента.")

    elif a == 4:
        status = False

print("Выход из программы.")
