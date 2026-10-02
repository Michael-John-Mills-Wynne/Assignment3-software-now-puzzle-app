# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import tkinter as tk

from image_processor import ImageProcessor


class BoardView(tk.Canvas):
    show_grid = False

    def __init__(self, parent, size=420):
        super().__init__(parent, width=size, height=size, bg="#050505",
                         highlightthickness=2, highlightbackground="#3a3a3a")
        self.photo = None  # keep it or tk deletes the picture
        self.n = 0
        self.ts = 0  # tile size
        self.size = size

    def show_placeholder(self, text):
        self.delete("all")
        self.config(width=self.size, height=self.size)
        self.create_rectangle(24, 24, self.size - 24, self.size - 24, outline="#3a3a3a", width=2, dash=(6, 6))
        self.create_text(self.size // 2, self.size // 2, text=text, fill="#6a6a6a", font=("Segoe UI", 14, "bold"))

    def draw(self, img, board):
        self.delete("all")
        h, w = img.shape[:2]
        self.config(width=w, height=h)
        self.n = board.get_grid()
        self.ts = w // self.n
        self.photo = tk.PhotoImage(data=ImageProcessor.to_png_data(img))
        self.create_image(0, 0, image=self.photo, anchor="nw")
        # faint grid lines
        if self.show_grid == True:
            for i in range(1, self.n):
                line = i * self.ts
                self.create_line(line, 0, line, h, fill="#a3a3a3")
                self.create_line(0, line, w, line, fill="#a3a3a3")
        self.draw_extra(board)

    def draw_extra(self, board):
        # children do this
        pass

    def tile_box(self, pos):
        row = pos // self.n
        col = pos % self.n
        x0 = col * self.ts
        y0 = row * self.ts
        return x0, y0, x0 + self.ts, y0 + self.ts

    def position_at(self, x, y):
        if self.ts == 0:
            return None
        col = int(x // self.ts)
        row = int(y // self.ts)
        if row < 0 or col < 0 or row >= self.n or col >= self.n:
            return None
        return row * self.n + col

    def draw_hint_circle(self, pos):
        x0, y0, x1, y1 = self.tile_box(pos)
        m = self.ts * 0.10
        self.create_oval(x0 + m - 4, y0 + m - 4, x1 - m + 4, y1 - m + 4, outline="#bae6fd", width=2)
        self.create_oval(x0 + m, y0 + m, x1 - m, y1 - m, outline="#0ea5e9", width=5)


class OriginalView(BoardView):

    def draw_extra(self, board):
        # blue circle at the home place
        home = board.get_hint_home()
        if home is not None:
            self.draw_hint_circle(home)


class PuzzleView(BoardView):
    show_grid = True

    def __init__(self, parent, size=420):
        super().__init__(parent, size)
        # yellow border so player knows this one is clickable
        self.config(highlightbackground="#facc15")

    def draw_extra(self, board):
        # green ticks
        for pos in range(board.get_total()):
            if board.is_correct(pos) == True:
                x0, y0, x1, y1 = self.tile_box(pos)
                s = self.ts * 0.24
                pad = self.ts * 0.05
                left = x1 - pad - s
                top = y0 + pad
                self.create_oval(left, top, left + s, top + s, fill="#22c55e", outline="white", width=2)
                self.create_line(left + 0.25 * s, top + 0.52 * s, left + 0.43 * s, top + 0.70 * s,
                                 left + 0.76 * s, top + 0.30 * s, fill="white", width=3)

        # selected tile border
        sel = board.get_selected()
        if sel is not None:
            x0, y0, x1, y1 = self.tile_box(sel)
            self.create_rectangle(x0 + 2, y0 + 2, x1 - 2, y1 - 2, outline="#ff6a00", width=5)
            self.create_rectangle(x0 + 7, y0 + 7, x1 - 7, y1 - 7, outline="#ffffff", width=1)

        # hint circle
        hp = board.get_hint_pos()
        if hp is not None:
            self.draw_hint_circle(hp)
