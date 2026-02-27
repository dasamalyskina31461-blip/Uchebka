import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from typing import List, Dict, Any, Optional

# ----------------------------------------------------------------------
# Модуль 1: Разработка модулей ПО
# Вариант №3: Учёт заявок на ремонт автомобилей (расширенная версия)
# ----------------------------------------------------------------------

# ======================================================================
# 1. ЗАГРУЗКА И СОХРАНЕНИЕ ДАННЫХ
# ======================================================================

DATA_FILES = {
    'users': 'inputDataUsers.csv',
    'requests': 'inputDataRequests.csv',
    'comments': 'inputDataComments.csv'
}

def load_csv(filename: str, fieldnames: List[str], delimiter: str = ';') -> List[Dict[str, Any]]:
    """Загружает данные из CSV-файла с преобразованием типов."""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                # Преобразование полей, если они есть
                if 'userID' in row:
                    row['userID'] = int(row['userID']) if row['userID'] else None
                if 'requestID' in row:
                    row['requestID'] = int(row['requestID'])
                if 'masterID' in row:
                    row['masterID'] = int(row['masterID']) if row['masterID'] not in ('null', '') else None
                if 'clientID' in row:
                    row['clientID'] = int(row['clientID']) if row['clientID'] else None
                if 'commentID' in row:
                    row['commentID'] = int(row['commentID'])
                # Преобразование пустых строк и 'null' в None
                for k, v in row.items():
                    if v in ('null', ''):
                        row[k] = None
                data.append(row)
    except FileNotFoundError:
        # Если файл не найден, создаём тестовые данные
        if filename == DATA_FILES['users']:
            data = [
                {'userID': 1, 'fio': 'Белов А.Д.', 'phone': '89210563128', 'login': 'login1', 'password': 'pass1', 'type': 'Менеджер'},
                {'userID': 2, 'fio': 'Харитонова М.П.', 'phone': '89535078985', 'login': 'login2', 'password': 'pass2', 'type': 'Автомеханик'},
                {'userID': 7, 'fio': 'Ильина Т.Д.', 'phone': '89219567841', 'login': 'login12', 'password': 'pass12', 'type': 'Заказчик'},
            ]
        elif filename == DATA_FILES['requests']:
            data = [
                {'requestID': 1, 'startDate': '2023-06-06', 'carType': 'Легковая', 'carModel': 'Hyundai Avante',
                 'problemDescryption': 'Отказали тормоза.', 'requestStatus': 'В процессе ремонта',
                 'completionDate': None, 'repairParts': None, 'masterID': 2, 'clientID': 7},
                {'requestID': 2, 'startDate': '2023-05-05', 'carType': 'Легковая', 'carModel': 'Nissan 180SX',
                 'problemDescryption': 'Отказали тормоза.', 'requestStatus': 'В процессе ремонта',
                 'completionDate': None, 'repairParts': None, 'masterID': 3, 'clientID': 8},
            ]
        elif filename == DATA_FILES['comments']:
            data = [
                {'commentID': 1, 'message': 'Очень странно.', 'masterID': 2, 'requestID': 1},
                {'commentID': 2, 'message': 'Будем разбираться!', 'masterID': 3, 'requestID': 2},
            ]
    return data

def save_csv(filename: str, data: List[Dict[str, Any]], fieldnames: List[str], delimiter: str = ';'):
    """Сохраняет данные в CSV-файл."""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        # Преобразуем None в пустую строку для записи
        for row in data:
            out_row = {k: ('' if v is None else v) for k, v in row.items()}
            writer.writerow(out_row)

# ======================================================================
# 2. ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ
# ======================================================================

class AutoServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автосервис: Учёт заявок на ремонт")
        self.root.geometry("1000x650")
        
        # Данные (имитация БД)
        self.users = load_csv(DATA_FILES['users'], ['userID', 'fio', 'phone', 'login', 'password', 'type'])
        self.requests = load_csv(DATA_FILES['requests'], 
                                 ['requestID', 'startDate', 'carType', 'carModel', 'problemDescryption',
                                  'requestStatus', 'completionDate', 'repairParts', 'masterID', 'clientID'])
        self.comments = load_csv(DATA_FILES['comments'], ['commentID', 'message', 'masterID', 'requestID'])
        
        # Текущий пользователь
        self.current_user = None
        
        # Показываем окно авторизации
        self.show_login_window()
    
    # ------------------------------------------------------------------
    # Сохранение данных
    # ------------------------------------------------------------------
    def save_all_data(self):
        """Сохраняет все данные в CSV-файлы."""
        save_csv(DATA_FILES['users'], self.users, ['userID', 'fio', 'phone', 'login', 'password', 'type'])
        save_csv(DATA_FILES['requests'], self.requests, 
                 ['requestID', 'startDate', 'carType', 'carModel', 'problemDescryption',
                  'requestStatus', 'completionDate', 'repairParts', 'masterID', 'clientID'])
        save_csv(DATA_FILES['comments'], self.comments, ['commentID', 'message', 'masterID', 'requestID'])
    
    # ------------------------------------------------------------------
    # Авторизация
    # ------------------------------------------------------------------
    def show_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Авторизация")
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True)
        
        ttk.Label(main_frame, text="Вход в систему учёта заявок", 
                 font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(main_frame, text="Логин:").grid(row=1, column=0, sticky="w", pady=5)
        self.login_entry = ttk.Entry(main_frame, width=30)
        self.login_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Пароль:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(main_frame, text="Войти", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        
        for user in self.users:
            if user['login'] == login and user['password'] == password:
                self.current_user = user
                self.show_main_window()
                return
        
        messagebox.showerror("Ошибка входа", "Неверный логин или пароль.")
    
    # ------------------------------------------------------------------
    # Главное окно
    # ------------------------------------------------------------------
    def show_main_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Автосервис - Главная (пользователь: {self.current_user['fio']})")
        
        # Верхняя панель
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(fill=tk.X)
        ttk.Label(top_frame, text=f"Вы вошли как: {self.current_user['fio']} ({self.current_user['type']})").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Выйти", command=self.logout).pack(side=tk.RIGHT)
        
        # Панель инструментов
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.pack(fill=tk.X)
        
        # Кнопки доступны в зависимости от роли
        if self.current_user['type'] == 'Менеджер':
            ttk.Button(toolbar, text="➕ Новая заявка", command=self.add_request_window).pack(side=tk.LEFT, padx=2)
            ttk.Button(toolbar, text="✏️ Редактировать", command=self.edit_selected_request).pack(side=tk.LEFT, padx=2)
            ttk.Button(toolbar, text="🗑️ Удалить", command=self.delete_selected_request).pack(side=tk.LEFT, padx=2)
        elif self.current_user['type'] == 'Автомеханик':
            ttk.Button(toolbar, text="✏️ Сменить статус", command=self.edit_selected_request).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar, text="📊 Статистика", command=self.show_stats).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Обновить", command=self.refresh_requests_list).pack(side=tk.LEFT, padx=2)
        
        # Поиск и фильтр
        ttk.Label(toolbar, text="Поиск:").pack(side=tk.LEFT, padx=(20, 2))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda a, b, c: self.filter_requests())
        ttk.Entry(toolbar, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="Статус:").pack(side=tk.LEFT, padx=(10, 2))
        self.status_filter_var = tk.StringVar(value="Все")
        statuses = ["Все", "Новая заявка", "В процессе ремонта", "Готова к выдаче", "Выдана"]
        ttk.Combobox(toolbar, textvariable=self.status_filter_var, values=statuses, 
                     state="readonly", width=15).pack(side=tk.LEFT, padx=2)
        self.status_filter_var.trace('w', lambda a, b, c: self.filter_requests())
        
        # Таблица заявок
        columns = ('ID', 'Дата', 'Авто', 'Проблема', 'Статус', 'Мастер', 'Клиент')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        self.tree.heading('ID', text='№')
        self.tree.heading('Дата', text='Дата создания')
        self.tree.heading('Авто', text='Автомобиль')
        self.tree.heading('Проблема', text='Описание')
        self.tree.heading('Статус', text='Статус')
        self.tree.heading('Мастер', text='Ответственный')
        self.tree.heading('Клиент', text='Клиент')
        
        self.tree.column('ID', width=50)
        self.tree.column('Дата', width=100)
        self.tree.column('Авто', width=150)
        self.tree.column('Проблема', width=200)
        self.tree.column('Статус', width=120)
        self.tree.column('Мастер', width=120)
        self.tree.column('Клиент', width=150)
        
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self.tree.bind('<Double-1>', lambda e: self.show_request_details())
        
        self.refresh_requests_list()
        
        # Привязываем сохранение при закрытии окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def logout(self):
        self.current_user = None
        self.show_login_window()
    
    def on_closing(self):
        """При закрытии окна сохраняем данные."""
        self.save_all_data()
        self.root.destroy()
    
    # ------------------------------------------------------------------
    # Работа со списком заявок
    # ------------------------------------------------------------------
    def refresh_requests_list(self):
        """Обновление таблицы (без фильтрации)."""
        self.filter_requests()  # просто применяем текущие фильтры
    
    def filter_requests(self):
        """Фильтрация заявок по поиску и статусу."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        search_text = self.search_var.get().lower()
        status_filter = self.status_filter_var.get()
        
        for req in self.requests:
            # Если пользователь - заказчик, показываем только его заявки
            if self.current_user['type'] == 'Заказчик' and req['clientID'] != self.current_user['userID']:
                continue
            
            # Фильтр по статусу
            if status_filter != "Все" and req['requestStatus'] != status_filter:
                continue
            
            # Фильтр по поиску
            if search_text:
                if (search_text not in str(req['requestID']).lower() and
                    search_text not in req['carModel'].lower() and
                    search_text not in req['problemDescryption'].lower()):
                    continue
            
            master_name = self.get_user_name(req['masterID']) if req['masterID'] else 'Не назначен'
            client_name = self.get_user_name(req['clientID'])
            
            self.tree.insert('', tk.END, values=(
                req['requestID'],
                req['startDate'],
                f"{req['carType']} {req['carModel']}",
                req['problemDescryption'][:50] + ('...' if len(req['problemDescryption']) > 50 else ''),
                req['requestStatus'],
                master_name,
                client_name
            ), tags=(req['requestID'],))
    
    def get_user_name(self, user_id: int) -> str:
        for user in self.users:
            if user['userID'] == user_id:
                return user['fio']
        return "Неизвестно"
    
    def get_user_list(self, role_filter: Optional[str] = None) -> List[tuple]:
        """Возвращает список (ID, ФИО) пользователей, опционально по роли."""
        result = []
        for user in self.users:
            if role_filter is None or user['type'] == role_filter:
                result.append((user['userID'], user['fio']))
        return result
    
    # ------------------------------------------------------------------
    # Добавление заявки
    # ------------------------------------------------------------------
    def add_request_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Новая заявка на ремонт")
        add_win.geometry("500x500")
        add_win.transient(self.root)
        add_win.grab_set()
        
        frame = ttk.Frame(add_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Тип авто:").grid(row=0, column=0, sticky="w", pady=5)
        car_type_var = tk.StringVar(value="Легковая")
        ttk.Combobox(frame, textvariable=car_type_var, values=["Легковая", "Грузовая", "Мотоцикл"], 
                    state="readonly", width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Модель авто:*").grid(row=1, column=0, sticky="w", pady=5)
        model_entry = ttk.Entry(frame, width=32)
        model_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Описание проблемы:*").grid(row=2, column=0, sticky="w", pady=5)
        problem_text = tk.Text(frame, width=30, height=5)
        problem_text.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Клиент:").grid(row=3, column=0, sticky="w", pady=5)
        client_combo = ttk.Combobox(frame, width=30, state="readonly")
        clients = [(uid, name) for uid, name in self.get_user_list('Заказчик')]
        client_combo['values'] = [f"{uid} - {name}" for uid, name in clients]
        if clients:
            client_combo.current(0)
        client_combo.grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="* - обязательные поля", foreground="gray").grid(row=4, column=0, columnspan=2, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_request():
            car_model = model_entry.get().strip()
            problem = problem_text.get("1.0", tk.END).strip()
            if not car_model or not problem:
                messagebox.showwarning("Предупреждение", "Заполните все обязательные поля.")
                return
            
            # Получаем ID клиента из выбранного
            client_selection = client_combo.get()
            client_id = None
            if client_selection and '-' in client_selection:
                client_id = int(client_selection.split('-')[0].strip())
            else:
                client_id = 7  # по умолчанию
            
            new_id = max([r['requestID'] for r in self.requests], default=0) + 1
            new_request = {
                'requestID': new_id,
                'startDate': datetime.now().strftime('%Y-%m-%d'),
                'carType': car_type_var.get(),
                'carModel': car_model,
                'problemDescryption': problem,
                'requestStatus': 'Новая заявка',
                'completionDate': None,
                'repairParts': None,
                'masterID': None,
                'clientID': client_id
            }
            self.requests.append(new_request)
            self.refresh_requests_list()
            messagebox.showinfo("Успех", f"Заявка №{new_id} создана.")
            add_win.destroy()
        
        ttk.Button(btn_frame, text="Сохранить", command=save_request).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=add_win.destroy).pack(side=tk.LEFT, padx=5)
    
    # ------------------------------------------------------------------
    # Редактирование заявки
    # ------------------------------------------------------------------
    def edit_selected_request(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите заявку.")
            return
        
        item = self.tree.item(selected[0])
        request_id = int(item['values'][0])
        request = next((r for r in self.requests if r['requestID'] == request_id), None)
        if not request:
            return
        
        self.edit_request_window(request)
    
    def edit_request_window(self, request):
        """Окно редактирования заявки (доступно менеджеру и механику с ограничениями)."""
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Редактирование заявки №{request['requestID']}")
        edit_win.geometry("500x600")
        edit_win.transient(self.root)
        edit_win.grab_set()
        
        frame = ttk.Frame(edit_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        ttk.Label(frame, text="Тип авто:").grid(row=row, column=0, sticky="w", pady=5)
        car_type_var = tk.StringVar(value=request['carType'])
        car_type_combo = ttk.Combobox(frame, textvariable=car_type_var, 
                                      values=["Легковая", "Грузовая", "Мотоцикл"], 
                                      state="readonly" if self.current_user['type']=='Менеджер' else 'disabled')
        car_type_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Модель авто:").grid(row=row, column=0, sticky="w", pady=5)
        model_entry = ttk.Entry(frame, width=32)
        model_entry.insert(0, request['carModel'])
        model_entry.config(state='normal' if self.current_user['type']=='Менеджер' else 'disabled')
        model_entry.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Описание проблемы:").grid(row=row, column=0, sticky="w", pady=5)
        problem_text = tk.Text(frame, width=30, height=5)
        problem_text.insert(1.0, request['problemDescryption'])
        problem_text.config(state='normal' if self.current_user['type']=='Менеджер' else 'disabled')
        problem_text.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Статус:").grid(row=row, column=0, sticky="w", pady=5)
        status_var = tk.StringVar(value=request['requestStatus'])
        status_combo = ttk.Combobox(frame, textvariable=status_var,
                                    values=["Новая заявка", "В процессе ремонта", "Готова к выдаче", "Выдана"],
                                    state="readonly")
        status_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Мастер:").grid(row=row, column=0, sticky="w", pady=5)
        master_combo = ttk.Combobox(frame, width=30, state="readonly")
        masters = [(uid, name) for uid, name in self.get_user_list('Автомеханик')]
        master_combo['values'] = [f"{uid} - {name}" for uid, name in masters] + ["Не назначен"]
        # Установка текущего мастера
        if request['masterID']:
            master_combo.set(f"{request['masterID']} - {self.get_user_name(request['masterID'])}")
        else:
            master_combo.set("Не назначен")
        master_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Дата завершения:").grid(row=row, column=0, sticky="w", pady=5)
        completion_entry = ttk.Entry(frame, width=32)
        if request['completionDate']:
            completion_entry.insert(0, request['completionDate'])
        completion_entry.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Запчасти:").grid(row=row, column=0, sticky="w", pady=5)
        parts_entry = ttk.Entry(frame, width=32)
        if request['repairParts']:
            parts_entry.insert(0, request['repairParts'])
        parts_entry.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(frame, text="Клиент:").grid(row=row, column=0, sticky="w", pady=5)
        client_combo = ttk.Combobox(frame, width=30, state="readonly" if self.current_user['type']=='Менеджер' else 'disabled')
        clients = [(uid, name) for uid, name in self.get_user_list('Заказчик')]
        client_combo['values'] = [f"{uid} - {name}" for uid, name in clients]
        client_combo.set(f"{request['clientID']} - {self.get_user_name(request['clientID'])}")
        client_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_changes():
            # Обновляем поля
            if self.current_user['type'] == 'Менеджер':
                request['carType'] = car_type_var.get()
                request['carModel'] = model_entry.get().strip()
                request['problemDescryption'] = problem_text.get("1.0", tk.END).strip()
                # Клиент
                client_sel = client_combo.get()
                if client_sel and '-' in client_sel:
                    request['clientID'] = int(client_sel.split('-')[0].strip())
            # Статус могут менять и менеджер, и механик
            request['requestStatus'] = status_var.get()
            # Мастер
            master_sel = master_combo.get()
            if master_sel == "Не назначен":
                request['masterID'] = None
            elif master_sel and '-' in master_sel:
                request['masterID'] = int(master_sel.split('-')[0].strip())
            # Дата завершения
            comp_date = completion_entry.get().strip()
            request['completionDate'] = comp_date if comp_date else None
            # Запчасти
            parts = parts_entry.get().strip()
            request['repairParts'] = parts if parts else None
            
            self.refresh_requests_list()
            messagebox.showinfo("Успех", "Изменения сохранены.")
            edit_win.destroy()
        
        ttk.Button(btn_frame, text="Сохранить", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=edit_win.destroy).pack(side=tk.LEFT, padx=5)
    
    # ------------------------------------------------------------------
    # Удаление заявки (только менеджер)
    # ------------------------------------------------------------------
    def delete_selected_request(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        request_id = int(item['values'][0])
        
        if not messagebox.askyesno("Подтверждение", f"Удалить заявку №{request_id}?"):
            return
        
        # Удаляем заявку и связанные комментарии
        self.requests = [r for r in self.requests if r['requestID'] != request_id]
        self.comments = [c for c in self.comments if c['requestID'] != request_id]
        self.refresh_requests_list()
        messagebox.showinfo("Успех", "Заявка удалена.")
    
    # ------------------------------------------------------------------
    # Просмотр деталей и комментарии
    # ------------------------------------------------------------------
    def show_request_details(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        request_id = int(item['values'][0])
        request = next((r for r in self.requests if r['requestID'] == request_id), None)
        if not request:
            return
        
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Заявка №{request_id}")
        detail_win.geometry("600x550")
        detail_win.transient(self.root)
        
        main_frame = ttk.Frame(detail_win, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Информация о заявке
        info_frame = ttk.LabelFrame(main_frame, text="Информация о заявке", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=f"Номер: {request['requestID']}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Дата создания: {request['startDate']}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Автомобиль: {request['carType']} {request['carModel']}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Проблема: {request['problemDescryption']}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Статус: {request['requestStatus']}").pack(anchor="w")
        
        master_name = self.get_user_name(request['masterID']) if request['masterID'] else 'Не назначен'
        ttk.Label(info_frame, text=f"Мастер: {master_name}").pack(anchor="w")
        
        client_name = self.get_user_name(request['clientID'])
        ttk.Label(info_frame, text=f"Клиент: {client_name}").pack(anchor="w")
        
        if request['completionDate']:
            ttk.Label(info_frame, text=f"Дата завершения: {request['completionDate']}").pack(anchor="w")
        if request['repairParts']:
            ttk.Label(info_frame, text=f"Запчасти: {request['repairParts']}").pack(anchor="w")
        
        # Комментарии
        comments_frame = ttk.LabelFrame(main_frame, text="Комментарии", padding="10")
        comments_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        comments_text = tk.Text(comments_frame, height=8, state=tk.DISABLED)
        comments_text.pack(fill=tk.BOTH, expand=True)
        
        comments_text.config(state=tk.NORMAL)
        comments_text.delete(1.0, tk.END)
        request_comments = [c for c in self.comments if c['requestID'] == request_id]
        for c in request_comments:
            author = self.get_user_name(c['masterID'])
            comments_text.insert(tk.END, f"[{author}]: {c['message']}\n{'-'*40}\n")
        if not request_comments:
            comments_text.insert(tk.END, "Нет комментариев.")
        comments_text.config(state=tk.DISABLED)
        
        # Добавление комментария (для механика и менеджера)
        if self.current_user['type'] in ('Автомеханик', 'Менеджер'):
            add_frame = ttk.Frame(main_frame)
            add_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(add_frame, text="Новый комментарий:").pack(anchor="w")
            self.comment_entry = ttk.Entry(add_frame, width=50)
            self.comment_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            
            def add_comment():
                message = self.comment_entry.get().strip()
                if not message:
                    return
                
                new_id = max([c['commentID'] for c in self.comments], default=0) + 1
                new_comment = {
                    'commentID': new_id,
                    'message': message,
                    'masterID': self.current_user['userID'],
                    'requestID': request_id
                }
                self.comments.append(new_comment)
                
                comments_text.config(state=tk.NORMAL)
                comments_text.insert(tk.END, f"[{self.current_user['fio']}]: {message}\n{'-'*40}\n")
                comments_text.config(state=tk.DISABLED)
                self.comment_entry.delete(0, tk.END)
                messagebox.showinfo("Успех", "Комментарий добавлен.")
            
            ttk.Button(add_frame, text="Добавить", command=add_comment).pack(side=tk.RIGHT)
        
        # Кнопка закрытия
        ttk.Button(main_frame, text="Закрыть", command=detail_win.destroy).pack(pady=10)
    
    # ------------------------------------------------------------------
    # Статистика
    # ------------------------------------------------------------------
    def show_stats(self):
        total = len(self.requests)
        completed = 0
        total_days = 0
        problem_stats = {}
        
        for req in self.requests:
            if req['requestStatus'] == 'Готова к выдаче' and req['completionDate']:
                completed += 1
                try:
                    start = datetime.strptime(req['startDate'], '%Y-%m-%d')
                    end = datetime.strptime(req['completionDate'], '%Y-%m-%d')
                    total_days += (end - start).days
                except (ValueError, TypeError):
                    pass
            
            # Группировка по первому слову описания проблемы
            words = req['problemDescryption'].split()
            if words:
                key = words[0]
                problem_stats[key] = problem_stats.get(key, 0) + 1
        
        avg_time = total_days / completed if completed > 0 else 0
        
        stats_win = tk.Toplevel(self.root)
        stats_win.title("Статистика работы сервиса")
        stats_win.geometry("400x300")
        stats_win.transient(self.root)
        
        frame = ttk.Frame(stats_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Статистика заявок", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text=f"Всего заявок: {total}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Выполнено заявок: {completed}").pack(anchor="w", pady=2)
        ttk.Label(frame, text=f"Среднее время ремонта: {avg_time:.1f} дней").pack(anchor="w", pady=2)
        
        ttk.Label(frame, text="\nСтатистика по проблемам:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        sorted_problems = sorted(problem_stats.items(), key=lambda x: x[1], reverse=True)
        for prob, count in sorted_problems[:5]:
            ttk.Label(frame, text=f"  {prob}: {count}").pack(anchor="w")
        
        ttk.Button(frame, text="Закрыть", command=stats_win.destroy).pack(pady=20)


# ======================================================================
# 3. ЗАПУСК
# ======================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoServiceApp(root)
    root.mainloop()