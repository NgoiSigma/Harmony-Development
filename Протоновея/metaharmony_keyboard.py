import tkinter as tk

class MetaharmonyKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Метагармония - Виртуальная клавиатура")

        keys = [
            ['Аз', 'Бу', 'Ве', '🜂', '🜄', '⚛'],
            ['♈', '♉', '♊', '♋', '♌', '⛩'],
            ['369', '144', '432', '∞', 'Ψ', 'Ω'],
        ]

        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                btn = tk.Button(root, text=key, font=("Arial", 14), command=lambda k=key: self.insert_text(k))
                btn.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=10)

        self.text_area = tk.Entry(root, font=("Arial", 16), width=40)
        self.text_area.grid(row=len(keys), column=0, columnspan=len(keys[0]), pady=10)

    def insert_text(self, key):
        self.text_area.insert(tk.END, key + " ")

root = tk.Tk()
app = MetaharmonyKeyboard(root)
root.mainloop()
