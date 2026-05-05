import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library v1.0")
        self.root.geometry("800x500")
        
        self.db_file = "movies.json"
        self.all_movies = []
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # --- Секция ввода данных ---
        input_frame = ttk.LabelFrame(self.root, text=" Добавить новый фильм ", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5)
        self.genre_combobox = ttk.Combobox(input_frame, values=["Драма", "Комедия", "Боевик", "Ужасы", "Фантастика"], width=15)
        self.genre_combobox.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Год:").grid(row=1, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, sticky="w")

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5)
        self.rating_entry = ttk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, sticky="w")

        self.add_btn = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=1, column=4, padx=20)

        # --- Секция фильтрации ---
        filter_frame = ttk.LabelFrame(self.root, text=" Фильтрация ", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5)
        self.filter_genre = ttk.Combobox(filter_frame, values=["Все"] + ["Драма", "Комедия", "Боевик", "Ужасы", "Фантастика"], width=15)
        self.filter_genre.set("Все")
        self.filter_genre.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Год:").grid(row=0, column=2, padx=5)
        self.filter_year = ttk.Entry(filter_frame, width=10)
        self.filter_year.grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Применить", command=self.apply_filter).grid(row=0, column=4, padx=10)
        ttk.Button(filter_frame, text="Сброс", command=self.reset_filter).grid(row=0, column=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(self.root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def validate(self, title, genre, year, rating):
        if not title or not genre:
            messagebox.showerror("Ошибка", "Заполните название и жанр!")
            return False
        try:
            year_int = int(year)
            rating_float = float(rating)
            if not (0 <= rating_float <= 10):
                raise ValueError("Рейтинг вне диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Год — число, Рейтинг — от 0 до 10!")
            return False
        return True

    def add_movie(self):
        t, g, y, r = self.title_entry.get(), self.genre_combobox.get(), self.year_entry.get(), self.rating_entry.get()
        
        if self.validate(t, g, y, r):
            movie = {"title": t, "genre": g, "year": y, "rating": r}
            self.all_movies.append(movie)
            self.save_data()
            self.display_movies(self.all_movies)
            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)

    def apply_filter(self):
        genre = self.filter_genre.get()
        year = self.filter_year.get()
        
        filtered = self.all_movies
        if genre != "Все":
            filtered = [m for m in filtered if m["genre"] == genre]
        if year:
            filtered = [m for m in filtered if m["year"] == year]
        
        self.display_movies(filtered)

    def reset_filter(self):
        self.filter_genre.set("Все")
        self.filter_year.delete(0, tk.END)
        self.display_movies(self.all_movies)

    def display_movies(self, movies_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in movies_list:
            self.tree.insert("", "end", values=(m["title"], m["genre"], m["year"], m["rating"]))

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.all_movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                self.all_movies = json.load(f)
            self.display_movies(self.all_movies)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
