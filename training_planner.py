"""
Training Planner - Основной модуль приложения для планирования тренировок
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Цветовая схема
        self.colors = {
            'bg': '#f0f0f0',
            'header': '#2c3e50',
            'button': '#3498db',
            'button_hover': '#2980b9',
            'success': '#27ae60',
            'error': '#e74c3c',
            'text': '#2c3e50',
            'table_bg': '#ffffff'
        }
        
        # Стилизация
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Данные
        self.training_data = []
        self.filename = "data.json"
        
        # Инициализация интерфейса
        self.setup_ui()
        self.load_data()
        
    def configure_styles(self):
        """Настройка стилей для виджетов"""
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), background=self.colors['bg'])
        self.style.configure('Custom.TButton', font=('Arial', 10), padding=8)
        self.style.configure('Treeview', rowheight=25, font=('Arial', 10))
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        header = ttk.Label(main_frame, text="📋 Training Planner", style='Header.TLabel')
        header.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавить новую тренировку", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # Поля ввода
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=25)
        self.date_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(input_frame, textvariable=self.type_var, width=22, state="readonly")
        self.type_combobox['values'] = ("Бег", "Плавание", "Велосипед", "Йога", "Силовая", "Кардио", "Растяжка", "Бокс")
        self.type_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(input_frame, text="Длительность (мин.):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar()
        self.duration_entry = ttk.Entry(input_frame, textvariable=self.duration_var, width=25)
        self.duration_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="✅ Добавить тренировку", 
                                    style='Custom.TButton', command=self.add_training)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        
        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="15")
        filter_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
self.date - self Ресурсы и информация.
www.self.date

ttk.Label(filter_frame, text="По типу:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filter_type_var = tk.StringVar()
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, 
                                             width=20, state="readonly")
        self.filter_type_combo['values'] = ("Все", "Бег", "Плавание", "Велосипед", "Йога", 
                                           "Силовая", "Кардио", "Растяжка", "Бокс")
        self.filter_type_combo.set("Все")
        self.filter_type_combo.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(filter_frame, text="По дате:").grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        self.filter_date_var = tk.StringVar()
        self.filter_date_entry = ttk.Entry(filter_frame, textvariable=self.filter_date_var, width=20)
        self.filter_date_entry.grid(row=0, column=3, sticky=tk.W)
        
        self.apply_filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", 
                                          command=self.apply_filters)
        self.apply_filter_btn.grid(row=0, column=4, padx=(20, 0))
        
        self.clear_filter_btn = ttk.Button(filter_frame, text="✖ Очистить фильтры", 
                                          command=self.clear_filters)
        self.clear_filter_btn.grid(row=0, column=5, padx=(10, 0))
        
        # Таблица тренировок
        table_frame = ttk.LabelFrame(main_frame, text="Список тренировок", padding="10")
        table_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Создание таблицы
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин.)")
        
        self.tree.column("date", width=150)
        self.tree.column("type", width=200)
        self.tree.column("duration", width=150)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления внизу
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky=tk.E)
        
        self.delete_button = ttk.Button(button_frame, text="🗑 Удалить выбранное", 
                                      command=self.delete_training)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(button_frame, text="💾 Сохранить данные", 
                                    command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(button_frame, text="📊 Статистика", 
                                      command=self.show_statistics)
        self.export_button.pack(side=tk.LEFT)
        
    def validate_input(self):
        """Валидация введенных данных"""
        # Проверка даты
        date_text = self.date_var.get().strip()
        try:
            date_obj = datetime.strptime(date_text, "%d.%m.%Y")
            if date_obj > datetime.now():
                messagebox.showwarning("Предупреждение", "Дата не может быть в будущем!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return False
        
        # Проверка типа тренировки
        if not self.type_var.get():
            messagebox.showerror("Ошибка", "Выберите тип тренировк

и!")
            return False
        
        # Проверка длительности
        try:
            duration = float(self.duration_var.get().strip())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом!")
            return False
        
        return True
    
    def add_training(self):
        """Добавление новой тренировки"""
        if not self.validate_input():
            return
        
        training = {
            "date": self.date_var.get().strip(),
            "type": self.type_var.get(),
            "duration": f"{float(self.duration_var.get().strip()):.0f} мин."
        }
        
        self.training_data.append(training)
        self.update_table()
        self.clear_inputs()
        self.save_data()
        
        messagebox.showinfo("Успех", "Тренировка успешно добавлена!")
    
    def clear_inputs(self):
        """Очистка полей ввода"""
        self.date_var.set("")
        self.type_var.set("")
        self.duration_var.set("")
    
    def delete_training(self):
        """Удаление выбранной тренировки"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите тренировку для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранные тренировки?"):
            # Получаем индексы выбранных элементов
            indices = []
            for item in selected:
                values = self.tree.item(item)['values']
                # Находим индекс в данных
                for i, data in enumerate(self.training_data):
                    if (data['date'] == values[0] and 
                        data['type'] == values[1] and 
                        data['duration'] == values[2]):
                        indices.append(i)
            
            # Удаляем с конца, чтобы не сбить индексы
            for index in sorted(indices, reverse=True):
                del self.training_data[index]
            
            self.update_table()
            self.save_data()
            messagebox.showinfo("Успех", "Тренировки удалены!")
    
    def apply_filters(self):
        """Применение фильтров"""
        filtered_data = self.training_data.copy()
        
        # Фильтр по типу
        filter_type = self.filter_type_var.get()
        if filter_type and filter_type != "Все":
            filtered_data = [t for t in filtered_data if t['type'] == filter_type]
        
        # Фильтр по дате
        filter_date = self.filter_date_var.get().strip()
        if filter_date:
            filtered_data = [t for t in filtered_data if t['date'] == filter_date]
        
        self.update_table(filtered_data)
    
    def clear_filters(self):
        """Очистка фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_var.set("")
        self.update_table()
    
    def update_table(self, data=None):
        """Обновление данных в таблице"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполнение данными
        if data is None:
            data = self.training_data
        
        for training in data:
            self.tree.insert("", tk.END, values=(
                training['date'],
                training['type'],
                training['duration']
            ))
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из JSON файл

а"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.training_data = json.load(f)
                self.update_table()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.training_data = []
    
    def show_statistics(self):
        """Показать статистику тренировок"""
        if not self.training_data:
            messagebox.showinfo("Статистика", "Нет данных для анализа")
            return
        
        # Подсчет статистики
        total_trainings = len(self.training_data)
        
        type_stats = {}
        total_duration = 0
        
        for t in self.training_data:
            training_type = t['type']
            duration_str = t['duration'].replace(' мин.', '')
            duration = float(duration_str)
            total_duration += duration
            
            if training_type in type_stats:
                type_stats[training_type]['count'] += 1
                type_stats[training_type]['duration'] += duration
            else:
                type_stats[training_type] = {'count': 1, 'duration': duration}
        
        # Создание окна статистики
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика тренировок")
        stats_window.geometry("500x400")
        
        stats_frame = ttk.Frame(stats_window, padding="20")
        stats_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(stats_frame, text="📊 Статистика тренировок", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 15))
        
        ttk.Label(stats_frame, text=f"Всего тренировок: {total_trainings}", 
                 font=('Arial', 11)).pack(pady=5)
        ttk.Label(stats_frame, text=f"Общая длительность: {total_duration:.0f} минут", 
                 font=('Arial', 11)).pack(pady=5)
        ttk.Label(stats_frame, text=f"Средняя длительность: {total_duration/total_trainings:.0f} минут", 
                 font=('Arial', 11)).pack(pady=5)
        
        # Таблица по типам
        ttk.Label(stats_frame, text="\nПо типам тренировок:", 
                 font=('Arial', 11, 'bold')).pack(pady=(15, 10))
        
        stats_tree = ttk.Treeview(stats_frame, columns=("type", "count", "duration"), 
                                  show="headings", height=8)
        stats_tree.heading("type", text="Тип")
        stats_tree.heading("count", text="Количество")
        stats_tree.heading("duration", text="Общее время (мин.)")
        
        stats_tree.column("type", width=150)
        stats_tree.column("count", width=100)
        stats_tree.column("duration", width=120)
        
        for training_type, stats in type_stats.items():
            stats_tree.insert("", tk.END, values=(
                training_type, 
                stats['count'], 
                f"{stats['duration']:.0f}"
            ))
        
        stats_tree.pack(pady=10)



