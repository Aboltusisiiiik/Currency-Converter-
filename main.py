import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

# Константы
API_KEY = "ВАШ_КЛЮЧ_ЗДЕСЬ"  # Получите на https://exchangerate-api.com
BASE_URL = f"https://exchangerate-api.com{API_KEY}/latest/"

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.history_file = "history.json"
        
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Поля ввода
        ttk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency = ttk.Combobox(self.root, values=["USD", "EUR", "RUB", "GBP"])
        self.from_currency.set("USD")
        self.from_currency.grid(row=1, column=0, padx=10, pady=10)

        self.to_currency = ttk.Combobox(self.root, values=["USD", "EUR", "RUB", "GBP"])
        self.to_currency.set("RUB")
        self.to_currency.grid(row=1, column=1, padx=10, pady=10)

        # Кнопка
        self.convert_btn = ttk.Button(self.root, text="Конвертировать", command=self.convert)
        self.convert_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.tree = ttk.Treeview(self.root, columns=("Date", "From", "To", "Result"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("From", text="Из")
        self.tree.heading("To", text="В")
        self.tree.heading("Result", text="Результат")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def convert(self):
        amount = self.amount_entry.get()
        
        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")
            return

        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        try:
            response = requests.get(f"{BASE_URL}{from_curr}")
            data = response.json()
            rate = data['conversion_rates'][to_curr]
            result = round(amount * rate, 2)
            
            # Сохранение в историю
            self.save_to_history(from_curr, to_curr, amount, result)
            messagebox.showinfo("Результат", f"{amount} {from_curr} = {result} {to_curr}")
        except Exception as e:
            messagebox.showerror("Ошибка API", "Не удалось получить курс валют")

    def save_to_history(self, f, t, a, res):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "to": t,
            "result": res
        }
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
        self.update_table(entry)

    def load_history(self):
        if os.path.exists(self.history_file):
                    self.update_table(item)

    def update_table(self, item):
        self.tree.insert("", "end", values=(item['date'], item['from'], item['to'], item['result']))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
            with open(self.history_file, 'r') as file:
                history = json.load(file)
                for item in history:
        with open(self.history_file, 'w') as file:
            json.dump(history, file, indent=4)
        
                history = json.load(file)
        
        history.append(entry)
        
        # Чтение и запись JSON
        history = []

