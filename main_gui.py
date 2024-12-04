import tkinter as tk
import json
from tkinter import messagebox, ttk
from transport.Client import Client
from transport.Truck import Truck
from transport.Train import Train
from transport.TransportCompany import TransportCompany

def load_data_from_json():
    try:
        with open("dump.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def load_data_from_json_vehicles():
    try:
        with open("dump_vehicles.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data_to_json(data):
    with open("dump.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_data_to_json_vehicles(vehicles_data):
    vehicles_data = []
    for vehicle in vehicles_data:
        if isinstance(vehicle, Truck):
            vehicles_data.append({
                'type': 'Грузовик',
                'capacity': vehicle.capacity,
                'color': vehicle.color
            })
        elif isinstance(vehicle, Train):
            vehicles_data.append({
                'type': 'Поезд',
                'capacity': vehicle.capacity,
                'number_of_cars': vehicle.number_of_cars
            })
    with open("dump_vehicles.json", "w", encoding="utf-8") as file:
        json.dump(vehicles_data, file, indent=4)

class TransportCompanyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная Компания Экспресс")
        self.root.geometry("820x595")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="white")

        self.company = TransportCompany("Транспортная Компания")
        self.clients_data = load_data_from_json()
        self.vehicles_data = load_data_from_json_vehicles()  # Загрузка данных о транспортных средствах

        if isinstance(self.clients_data, list):
            for client_dict in self.clients_data:
                try:
                    client = Client(client_dict['name'], client_dict['cargo_weight'], client_dict['is_vip'])
                    self.company.add_client(client)
                except ValueError as e:
                    print(f"Ошибка при загрузке клиента: {e}")

        if isinstance(self.vehicles_data, list):
            for vehicle_dict in self.vehicles_data:           
                try:
                    if vehicle_dict['type'] == 'Грузовик':
                        vehicle = Truck(vehicle_dict['capacity'], vehicle_dict['color'])
                    elif vehicle_dict['type'] == 'Поезд':
                        vehicle = Train(vehicle_dict['capacity'], vehicle_dict['number_of_cars'])
                    self.company.add_vehicle(vehicle)
                except ValueError as e:
                    print(f"Ошибка при загрузке транспортного средства: {e}")

        frame1 = tk.Frame(self.root, bg='gray15')
        frame1.place(relx=0.25, rely=0.26, relwidth=0.5, relheight=0.5)

        frame2 = tk.Frame(self.root, bg='gray15')
        frame2.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text1 = """
        Добро пожаловать на страничку транспортной
        компании Экспресс!"""
        main_label = tk.Label(root, text=info_text1, font=("Arial", 17, 'bold'), fg="white", bg="gray15")
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
        info_label.place(relx=0.487, rely=0.5, anchor=tk.CENTER)

        btn_open_clients = tk.Button(self.root, text="Действия с клиентами", width=35, height=5, bg="black", fg="white", command=self.open_new_clientsworkwindow)
        btn_open_clients.place(x=130, y=470)

        btn_open_vehicles = tk.Button(self.root, text="Действия с транспортными средствами", width=35, height=5, bg="black", fg="white", command=self.open_new_vehidesworkwindow)
        btn_open_vehicles.place(x=450, y=470)

        btn_open_cargo = tk.Button(self.root, text="Распределение груза", width=23, height=5, bg="black", fg="white", command=self.open_new_cargo_distribution)
        btn_open_cargo.pack(side=tk.LEFT, padx=10, pady=10)

        btn_exit = tk.Button(self.root, text="Выйти из программы", width=23, height=5, bg="black", fg="white", command=self.root.quit)
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=10)

        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        export_menu = tk.Menu(menubar, tearoff=0)
        export_menu.add_command(label="Экспорт результата", command=self.export_results)
        export_menu.add_separator()
        export_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Меню", menu=export_menu)
        self.root.config(menu=menubar)


    def open_new_clientsworkwindow(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Действия с клиентами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.client_table = ttk.Treeview(self.frame, columns=("Имя", "Вес", "VIP"), show='headings')
        self.client_table.heading("Имя", text="Имя клиента")
        self.client_table.heading("Вес", text="Вес груза")
        self.client_table.heading("VIP", text="VIP статус")
        self.client_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame3 = tk.Frame(new_window, bg='gray15')
        frame3.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)
        
        info_text3 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text3, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_client = tk.Button(new_window, text="Добавить клиента", width=35, height=3, bg="black", fg="white", command=self.add_client)
        btn_add_client.place(x=150, y=180)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_clients_to_table()

    def load_clients_to_table(self):
        for client in self.company.clients:
            self.client_table.insert("", "end", values=(client.name, client.cargo_weight, "Да" if client.is_vip else "Нет"))

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
        vip_status = self.client_vip_var.get()

        if name.strip() == "":
            tk.messagebox.showerror("Ошибка", "Имя клиента не может быть пустым. Повторите ввод.")
            return
        if not weight.isdigit() or not int(weight) or not float(weight):
            tk.messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом.")
            return

        self.client_table.insert("", "end", values=(name, weight, "Да" if vip_status else "Нет"))
        self.company.add_client(Client(name, float(weight), vip_status))
        self.save_data_to_json(self.company.clients)

        self.client_window.destroy()
        self.status.config(text="Клиент добавлен")

    def open_new_vehidesworkwindow(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Действия с транспортными средствами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.transport_table = ttk.Treeview(self.frame, columns=("ID", "Тип", "Грузоподъемность"), show='headings')
        self.transport_table.heading("ID", text="ID")
        self.transport_table.heading("Тип", text="Тип транспорта")
        self.transport_table.heading("Грузоподъемность", text="Грузоподъемность")
        self.transport_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame4 = tk.Frame(new_window, bg='gray15')
        frame4.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)
        
        info_text4 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text4, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_client = tk.Button(new_window, text="Добавить транспорт", width=35, height=3, bg="black", fg="white", command=self.add_vehicle)
        btn_add_client.place(x=150, y=180)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_transport_table()

    def load_transport_table(self):
        for vehicle in self.company.vehicles:
            if isinstance(vehicle, Truck):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Грузовик", vehicle.capacity))
            elif isinstance(vehicle, Train):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Поезд", vehicle.capacity))

    def add_vehicle(self):
        self.transport_window = tk.Toplevel(self.root)
        self.transport_window.title("Добавить транспорт")

        tk.Label(self.transport_window, text="Тип транспорта:").grid(row=0, column=0)
        self.transport_type = ttk.Combobox(self.transport_window, values=["Грузовик", "Поезд"])
        self.transport_type.grid(row=0, column=1)
        self.transport_type.bind("<<ComboboxSelected>>", self.on_transport_type_selected)

        tk.Label(self.transport_window, text="Грузоподъемность:").grid(row=1, column=0)
        self.capacity = tk.Entry(self.transport_window)
        self.capacity.grid(row=1, column=1)

        self.color_label = tk.Label(self.transport_window, text="Цвет:")
        self.color_label.grid(row=2, column=0)
        self.color_entry = tk.Entry(self.transport_window)
        self.color_entry.grid(row=2, column=1)

        self.cars_label = tk.Label(self.transport_window, text="Количество вагонов:")
        self.cars_label.grid(row=3, column=0)
        self.cars_entry = tk.Entry(self.transport_window)
        self.cars_entry.grid(row=3, column=1)

        tk.Button(self.transport_window, text="Сохранить", command=self.save_transport).grid(row=4, column=0)

    def on_transport_type_selected(self, event):
        transport_type = self.transport_type.get()
        if transport_type == "Поезд":
            self.color_label.grid_remove()
            self.color_entry.grid_remove()
            self.cars_label.grid()
            self.cars_entry.grid()
        elif transport_type == "Грузовик":
            self.cars_label.grid_remove()
            self.cars_entry.grid_remove()
            self.color_label.grid()
            self.color_entry.grid()

    def save_transport(self):
        transport_type = self.transport_type.get()
        capacity = self.capacity.get()
        color = self.color_entry.get()
        number_of_cars = self.cars_entry.get()

        try:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
            return

        if transport_type == "Грузовик":
            if color.strip() == "":
                messagebox.showerror("Ошибка", "Цвет не может быть пустым.")
                return
            self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, transport_type, capacity, color))
            self.company.add_vehicle(Truck(capacity, color))
        elif transport_type == "Поезд":
            try:
                number_of_cars = int(number_of_cars)
                if number_of_cars <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Количество вагонов должно быть положительным числом.")
                return
            
            self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, transport_type, capacity, number_of_cars))
            self.company.add_vehicle(Train(capacity, number_of_cars))
        
        self.save_data_to_json_vehicles(self.company.vehicles)
        
        self.transport_window.destroy()
        self.status.config(text="Транспорт добавлен")

    def open_new_cargo_distribution(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Распределение груза")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

        self.result_text = tk.Text(new_window, height=20, width=80)
        self.result_text.pack(pady=10)

        if not self.company.clients:
            self.result_text.insert(tk.END, "В данный момент нет клиентов для распределения грузов.\n")
        elif not self.company.vehicles:
            self.result_text.insert(tk.END, "В данный момент нет транспортных средств для распределения грузов.\n")
        else:
            self.company.optimize_cargo_distribution()
            
            self.result_text.insert(tk.END, "Распределение грузов выполнено:\n")
            for vehicle in self.company.vehicles:
                self.result_text.insert(tk.END, f"Транспортное средство: {vehicle}\n")
                if vehicle.clients_list:
                    self.result_text.insert(tk.END, "Загруженные клиенты:\n")
                    for client in vehicle.clients_list:
                        self.result_text.insert(tk.END, f" - Имя: {client.name}, Вес груза: {client.cargo_weight}, VIP-статус: {client.is_vip}\n")
                else:
                    self.result_text.insert(tk.END, " - Не загружено ни одного клиента.\n")

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
