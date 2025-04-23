import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from data import CrosswordModel
from crossword import generate_crossword
from file_manager import save_project, load_project
from image_export import export_to_image

class CrosswordApp:
    def __init__(self, root):
        self.root = root
        self.model = CrosswordModel()
        self.difficulty = tk.StringVar(value='Лёгкий')

        root.title("Составитель кроссвордов")

        self.word_entry = tk.Entry(root)
        self.clue_entry = tk.Entry(root)
        self.add_button = tk.Button(root, text="Добавить", command=self.add_word)
        self.generate_button = tk.Button(root, text="Сгенерировать", command=self.generate)
        self.save_button = tk.Button(root, text="Сохранить проект", command=self.save)
        self.load_button = tk.Button(root, text="Загрузить проект", command=self.load)
        self.export_button = tk.Button(root, text="Экспорт PNG", command=self.export)
        self.word_listbox = tk.Listbox(root, width=50)
        self.canvas = tk.Canvas(root, width=800, height=800)

        self.difficulty_menu = ttk.Combobox(root, values=['Лёгкий', 'Средний', 'Сложный'], textvariable=self.difficulty)
        self.difficulty_menu.current(0)

        self.word_entry.grid(row=0, column=0)
        self.clue_entry.grid(row=0, column=1)
        self.add_button.grid(row=0, column=2)
        self.difficulty_menu.grid(row=0, column=3)
        self.word_listbox.grid(row=1, column=0, columnspan=4, pady=5)
        self.generate_button.grid(row=2, column=0)
        self.save_button.grid(row=2, column=1)
        self.load_button.grid(row=2, column=2)
        self.export_button.grid(row=2, column=3)
        self.canvas.grid(row=3, column=0, columnspan=4, pady=10)

        self.word_entry.bind("<FocusOut>", self.auto_clue)

    def auto_clue(self, event=None):
        word = self.word_entry.get().strip().upper()
        try:
            with open("assets/dictionary.txt", encoding='utf-8') as f:
                for line in f:
                    w, c = line.strip().split(" — ")
                    if w == word:
                        self.clue_entry.delete(0, tk.END)
                        self.clue_entry.insert(0, c)
                        break
        except Exception:
            pass

    def add_word(self):
        word = self.word_entry.get()
        clue = self.clue_entry.get()
        if not word or not clue:
            messagebox.showerror("Ошибка", "Введите слово и подсказку.")
            return
        self.model.add_word(word, clue)
        self.word_listbox.insert(tk.END, f"{word.upper()} — {clue}")
        self.word_entry.delete(0, tk.END)
        self.clue_entry.delete(0, tk.END)

    def generate(self):
        generate_crossword(self.model, self.difficulty.get())
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        size = 30
        for i in range(self.model.size):
            for j in range(self.model.size):
                x, y = j * size, i * size
                self.canvas.create_rectangle(x, y, x+size, y+size, outline='black')
                ch = self.model.grid[i][j]
                if ch != ' ':
                    self.canvas.create_text(x+size/2, y+size/2, text=ch)

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".pkl")
        if path:
            save_project(self.model, path)

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Project Files", "*.pkl")])
        if path:
            self.model = load_project(path)
            self.word_listbox.delete(0, tk.END)
            for entry in self.model.word_list:
                self.word_listbox.insert(tk.END, f"{entry.word} — {entry.clue}")
            self.draw_grid()

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            export_to_image(self.model, path)
