# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import tkinter as tk


class GameButton(tk.Button):

    def __init__(self, parent, text, command, color, hover, fg="black"):
        super().__init__(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground=hover, activeforeground=fg,
                         relief="flat", bd=0, padx=20, pady=9,
                         font=("Segoe UI", 11, "bold"), cursor="hand2")
        self.color = color
        self.hover = hover
        self.fg_color = fg
        self.enabled = True
        self.bind("<Enter>", self.mouse_in)
        self.bind("<Leave>", self.mouse_out)

    def mouse_in(self, event):
        if self.enabled == True:
            self.config(bg=self.hover)

    def mouse_out(self, event):
        if self.enabled == True:
            self.config(bg=self.color)

    def set_enabled(self, value):
        self.enabled = value
        if value == True:
            self.config(state="normal", bg=self.color, fg=self.fg_color, cursor="hand2")
        else:
            self.config(state="disabled", bg="#1f1f1f", disabledforeground="#5a5a5a", cursor="arrow")


class GridPicker(tk.Frame):

    def __init__(self, parent, bg):
        super().__init__(parent, bg=bg)
        self.size = 3
        self.buttons = {}
        # three buttons 3x3 4x4 5x5
        for n in (3, 4, 5):
            b = tk.Button(self, text=str(n) + " x " + str(n), relief="flat", bd=0,
                          padx=12, pady=7, font=("Segoe UI", 10, "bold"),
                          cursor="hand2", command=lambda n=n: self.choose(n))
            b.pack(side="left", padx=2)
            self.buttons[n] = b
        self.choose(3)

    def choose(self, n):
        self.size = n
        for k in self.buttons:
            if k == n:
                self.buttons[k].config(bg="#facc15", fg="black", activebackground="#fde047", activeforeground="black")
            else:
                self.buttons[k].config(bg="#222222", fg="#b0b0b0", activebackground="#333333", activeforeground="white")

    def get_size(self):
        return self.size


class StatBox(tk.Frame):

    def __init__(self, parent, caption, color, card_color):
        super().__init__(parent, bg=card_color, padx=18, pady=8)
        self.cap = tk.Label(self, text=caption, bg=card_color, fg="#8a8a8a", font=("Segoe UI", 9, "bold"))
        self.cap.pack()
        self.number = tk.Label(self, text="0", bg=card_color, fg=color, font=("Segoe UI", 22, "bold"))
        self.number.pack()

    def set_value(self, v):
        self.number.config(text=str(v))
