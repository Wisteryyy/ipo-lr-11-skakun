# доработать валидацию, таблицы и их вывод, расположение кнопок, фреймы, закончить метод распределения грузов

import tkinter as tk
from tkinter import messagebox, ttk
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
        return []

def save_data_to_json(data):
    with open("dump.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

class TransportCompanyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная Компания Экспресс")
        self.root.geometry("820x595")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="white")

        self.company = TransportCompany("Транспортная Компания")
        self.clients_data = load_data_from_json()

        for client_dict in self.clients_data:
            try:
                client = Client(client_dict['name'], client_dict['cargo_weight'], client_dict['is_vip'])
                self.company.add_client(client)
            except ValueError as e:
                print(f"Ошибка при загрузке клиента: {e}")

        frame1 = tk.Frame(self.root, bg='gray15')
        frame1.place(relx=0.25, rely=0.26, relwidth=0.5, relheight=0.5)

        frame2 = tk.Frame(self.root, bg='gray15')
        frame2.place(relx=0.08, rely=0.04, relwidth=0.85, relheight=0.2)

        info_text1 = """
        Добро пожаловать на страничку транспортной
        компании Экспресс!"""
        main_label = tk.Label(root, text=info_text1, font=("Arial", 22), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        info_text2 = """
        Вы можете как просматривать списки уже 
        существующих клиентов, транспортных 
        средств, так и регистрировать их со всеми 
        параметрами. Также наша компания 
        предоставляет возможность распределять 
        груз по транспортным средствам. 

        Чтобы груз клиента распределялся в 
        первоочередном порядке, клиенту нужен 
        VIP-статус."""
        info_label = tk.Label(root, text=info_text2, font=("Arial", 12), fg="white", bg="gray15")
        info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        btn_open_clients = tk.Button(self.root, text="Действия с клиентами", width=35, height=3, bg="black", fg="white", command=self.open_new_clientsworkwindow)
        btn_open_clients.pack(pady=20)

        btn_open_vehicles = tk.Button(self.root, text="Действия с транспортными средствами", width=35, height=3, bg="black", fg="white", command=self.open_new_vehidesworkwindow)
        btn_open_vehicles.pack(pady=20)

        btn_open_cargo = tk.Button(self.root, text="Распределение груза", width=35, height=3, bg="black", fg="white", command=self.open_new_cargo_distribution)
        btn_open_cargo.pack(pady=20)

        btn_exit = tk.Button(self.root, text="Выйти из программы", width=20, height=5, bg="black", fg="white", command=self.root.quit)
        btn_exit.pack(pady=20)

        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        export_menu = tk.Menu(menubar, tearoff=0)
        export_menu.add_command(label="Экспорт результата", command=self.export_results)
        export_menu.add_separator()
        export_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Меню", menu=export_menu)
        self.root.config(menu=menubar)

    def diagramma_clients(self):
        self.client_tree = ttk.Treeview(self.root, columns=("Имя", "Вес груза", "VIP статус"), show='headings')
        self.client_tree.heading("Имя", text="Имя клиента")
        self.client_tree.heading("Вес груза", text="Вес груза")
        self.client_tree.heading("VIP статус", text="VIP статус")
        self.client_tree.pack(pady=10)

    def diagramma_vehicles(self):
        self.vehicle_tree = ttk.Treeview(self.root, columns=("Тип", "Грузоподъемность"), show='headings')
        self.vehicle_tree.heading("Тип", text="Тип")
        self.vehicle_tree.heading("Грузоподъемность", text="Грузоподъемность")
        self.vehicle_tree.pack(pady=10)

    def open_new_clientsworkwindow(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Действия с клиентами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        btn_add_client = tk.Button(new_window, text="Добавить клиента", width=30, height=2, bg="black", fg="white", command=self.add_client)
        btn_add_client.pack(pady=20)

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

        self.diagramma_clients()

    def add_client(self):
        self.client_window = tk.Toplevel(self.root)
        self.client_window.title("Добавить клиента")
        
        tk.Label(self.client_window, text="Имя клиента:").grid(row=0, column=0)
        self.client_name_entry = tk.Entry(self.client_window)
        self.client_name_entry.grid(row=0, column=1)

        tk.Label(self.client_window, text="Вес груза:").grid(row=1, column=0)
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.grid(row=1, column=1)

        tk.Label(self.client_window, text="VIP статус:").grid(row=2, column=0)
        self.client_vip_var = tk.BooleanVar()
        self.client_vip_check = tk.Checkbutton(self.client_window, variable=self.client_vip_var)
        self.client_vip_check.grid(row=2, column=1)

        tk.Button(self.client_window, text="Сохранить", command=self.save_client).grid(row=3, column=0, columnspan=2)

    def save_client(self):
        name = self.client_name_entry.get()
        weight = self.client_weight_entry.get()
        is_vip = self.client_vip_var.get()
        try:
            weight = float(weight)
            if weight < 0 or weight > 10000:
                raise ValueError("Вес груза должен быть положительным числом и не более 10000 кг.")
            client = Client(name, weight, is_vip)
            self.company.add_client(client)
            self.update_client_tree()
            save_data_to_json(self.company.clients)
            self.client_window.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def update_client_tree(self):
        for row in self.client_tree.get_children():
            self.client_tree.delete(row)
        for client in self.company.clients:
            self.client_tree.insert("", "end", values=(client.name, client.cargo_weight, client.is_vip))

    def open_new_vehidesworkwindow(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Действия с транспортными средствами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        btn_add_vehicle = tk.Button(new_window, text="Добавить транспорт", width=30, height=2, bg="black", fg="white", command=self.add_vehicle)
        btn_add_vehicle.pack(pady=20)

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

        self.diagramma_vehicles()

    def add_vehicle(self):
        self.vehicle_window = tk.Toplevel(self.root)
        self.vehicle_window.title("Добавить транспортное средство")
        
        tk.Label(self.vehicle_window, text="Тип транспорта:").grid(row=0, column=0)
        self.vehicle_type_var = tk.StringVar()
        self.vehicle_type_combobox = ttk.Combobox(self.vehicle_window, textvariable=self.vehicle_type_var)
        self.vehicle_type_combobox['values'] = ("Грузовик", "Поезд")
        self.vehicle_type_combobox.grid(row=0, column=1)

        tk.Label(self.vehicle_window, text="Грузоподъемность:").grid(row=1, column=0)
        self.vehicle_capacity_entry = tk.Entry(self.vehicle_window)
        self.vehicle_capacity_entry.grid(row=1, column=1)

        tk.Button(self.vehicle_window, text="Сохранить", command=self.save_vehicle).grid(row=2, column=0, columnspan=2)

    def save_vehicle(self):
        vehicle_type = self.vehicle_type_var.get()
        capacity = self.vehicle_capacity_entry.get()
        try:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError("Грузоподъемность должна быть положительным числом.")
            if vehicle_type == "Грузовик":
                vehicle = Truck(capacity)
            elif vehicle_type == "Поезд":
                vehicle = Train(capacity, 10) # пример с количеством вагонов
            self.company.add_vehicle(vehicle)
            self.update_vehicle_tree()
            save_data_to_json(self.company.vehicles)
            self.vehicle_window.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def update_vehicle_tree(self):
        for row in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(row)
        for vehicle in self.company.vehicles:
            self.vehicle_tree.insert("", "end", values=(type(vehicle).__name__, vehicle.capacity))

    def open_new_cargo_distribution(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Распределение груза")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

    def close_new_window(self, window):
        window.destroy()
        self.root.deiconify()

    def export_results(self):
        messagebox.showinfo("Экспорт результата", "Экспорт результатов выполнен.")

    def show_about(self):
        messagebox.showinfo("О программе", "Транспортная Компания Экспресс\nЛабораторная работа №12\nВариант 1\nВыполнила: София Скакун")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportCompanyApp(root)
    root.mainloop()