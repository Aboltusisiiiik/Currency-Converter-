import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter Pro")
        self.root.geometry("650x500")
        
        # Конфигурация
        self.api_key = "ВАШ_КЛЮЧ_ЗДЕСЬ"  # Замените на ваш ключ
        self.history_file = "history.json"
        
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Секция ввода
        input_group = ttk.LabelFrame(main_frame, text=" Параметры конвертации ", padding="10")
        input_group.pack(fill="x", pady=(0, 10))

        ttk.Label(input_group, text="Сумма:").grid(row=0, column=0, sticky="w", padx=5)
        self.amount_entry = ttk.Entry(input_group, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=10)

        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT"]
        
        self.from_curr_var = tk.StringVar(value="USD")
        self.from_curr = ttk.Combobox(input_group, textvariable=self.from_curr_var, values=self.currencies, width=8, state="readonly")
        self.from_curr.grid(row=0, column=2, padx=5)

        ttk.Label(input_group, text="➔").grid(row=0, column=3, padx=2)

        self.to_curr_var = tk.StringVar(value="RUB")
        self.to_curr = ttk.Combobox(input_group, textvariable=self.to_curr_var, values=self.currencies, width=8, state="readonly")
        self.to_curr.grid(row=0, column=4, padx=5)

        self.calc_btn = ttk.Button(input_group, text="Конвертировать", command=self.perform_conversion)
        self.calc_btn.grid(row=0, column=5, padx=10)

        # Секция истории
        history_group = ttk.LabelFrame(main_frame, text=" История операций ", padding="10")
        history_group.pack(fill="both", expand=True)

        cols = ("date", "from_val", "to_val", "rate")
        self.tree = ttk.Treeview(history_group, columns=cols, show="headings")
        self.tree.heading("date", text="Дата и время")
        self.tree.heading("from_val", text="Исходная")
        self.tree.heading("to_val", text="Результат")
        self.tree.heading("rate", text="Курс")
        
        self.tree.column("date", width=140)
        self.tree.pack(fill="both", expand=True)

    def perform_conversion(self):
        amount_raw = self.amount_entry.get().replace(',', '.')
        from_c = self.from_curr_var.get()
        to_c = self.to_curr_var.get()

        # 1. Полная валидация
        if not self.api_key or self.api_key == "ВАШ_КЛЮЧ_ЗДЕСЬ":
            messagebox.showwarning("Ошибка конфига", "Не указан API-ключ в коде!")
            return

        try:
            amount = float(amount_raw)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите положительное число!")
            return

        if from_c == to_c:
            messagebox.showinfo("Инфо", "Выбраны одинаковые валюты. Результат равен сумме.")
            return

        # 2. Формирование URL и запрос
        url = f"https://exchangerate-api.com{self.api_key}/pair/{from_c}/{to_c}/{amount}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Проверка статус-кода (200, 404 и т.д.)
            data = response.json()

            if data.get("result") == "success":
                result = round(data["conversion_result"], 2)
                rate = data["conversion_rate"]
                
                entry = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "from_val": f"{amount} {from_c}",
                    "to_val": f"{result} {to_c}",
                    "rate": f"1:{rate}"
                }
                
                self.update_ui_and_history(entry)
                messagebox.showinfo("Успех", f"{amount} {from_c} = {result} {to_c}")
            else:
                error_type = data.get("error-type", "Unknown Error")
                messagebox.showerror("Ошибка API", f"Сервер вернул ошибку: {error_type}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Сетевая ошибка", f"Не удалось связаться с сервером:\n{e}")

    def update_ui_and_history(self, entry):
        self.tree.insert("", 0, values=(entry["date"], entry["from_val"], entry["to_val"], entry["rate"]))
        self.save_to_history(entry)

    def save_to_history(self, entry):
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError: history = []
        
        history.append(entry)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    for item in history:
                        self.tree.insert("", "end", values=(item["date"], item["from_val"], item["to_val"], item["rate"]))
            except Exception as e:
                print(f"Ошибка загрузки истории: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
