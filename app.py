# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from board import PuzzleBoard
from image_processor import ImageProcessor
from views import OriginalView, PuzzleView
from widgets import GameButton, GridPicker, StatBox

BG = "#0a0a0a"
CARD = "#161616"
YELLOW = "#facc15"
GREY = "#8a8a8a"


class PuzzleApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Picture Puzzle")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.proc = ImageProcessor(420)
        self.board = None
        self.orig_img = None

        # header with gradient
        self.header = tk.Canvas(self.root, height=84, highlightthickness=0, bd=0)
        self.header.pack(fill="x")
        self.header.bind("<Configure>", self.draw_header)

        # top bar
        bar = tk.Frame(self.root, bg=BG)
        bar.pack(fill="x", padx=24, pady=(16, 6))
        tk.Label(bar, text="GRID", bg=BG, fg=GREY, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        self.grid_picker = GridPicker(bar, BG)
        self.grid_picker.pack(side="left")
        self.load_btn = GameButton(bar, "Load Image", self.load_image, YELLOW, "#fde047")
        self.load_btn.pack(side="left", padx=18)
        self.solve_btn = GameButton(bar, "Solve", self.click_solve, "#e5e5e5", "#ffffff")
        self.solve_btn.pack(side="right")
        self.hint_btn = GameButton(bar, "Hint", self.click_hint, "#f59e0b", "#fbbf24")
        self.hint_btn.pack(side="right", padx=10)

        # the two pictures
        area = tk.Frame(self.root, bg=BG)
        area.pack(padx=24, pady=8)

        card1 = tk.Frame(area, bg=CARD, padx=16, pady=12)
        card1.pack(side="left", padx=10)
        tk.Label(card1, text="ORIGINAL", bg=CARD, fg=YELLOW, font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))
        self.original_view = OriginalView(card1)
        self.original_view.pack()

        card2 = tk.Frame(area, bg=CARD, padx=16, pady=12)
        card2.pack(side="left", padx=10)
        tk.Label(card2, text="YOUR PUZZLE", bg=CARD, fg=YELLOW, font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))
        self.puzzle_view = PuzzleView(card2)
        self.puzzle_view.pack()

        # mouse clicks on the puzzle
        self.puzzle_view.bind("<Button-1>", self.click_left)
        self.puzzle_view.bind("<Shift-Button-1>", self.click_shift)
        self.puzzle_view.bind("<Button-3>", self.click_right)
        if sys.platform == "darwin":
            self.puzzle_view.bind("<Button-2>", self.click_right)

        # bottom bar
        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill="x", padx=24, pady=(6, 16))
        self.moves_box = StatBox(bottom, "MOVES", "#ffffff", CARD)
        self.moves_box.pack(side="left", padx=(10, 12))
        self.wrong_box = StatBox(bottom, "INCORRECT TILES", "#fb923c", CARD)
        self.wrong_box.pack(side="left", padx=12)
        self.hints_box = StatBox(bottom, "HINTS LEFT", YELLOW, CARD)
        self.hints_box.pack(side="left", padx=12)

        right_box = tk.Frame(bottom, bg=BG)
        right_box.pack(side="right", padx=10)
        self.win_label = tk.Label(right_box, text="", bg=BG, fg=YELLOW, font=("Segoe UI", 20, "bold"))
        self.win_label.pack(anchor="e")
        self.info_label = tk.Label(right_box, text="", bg=BG, fg=GREY, font=("Segoe UI", 10), justify="right")
        self.info_label.pack(anchor="e")

        self.update_screen()

    def run(self):
        self.root.mainloop()

    def draw_header(self, event):
        self.header.delete("all")
        w = self.header.winfo_width()
        # yellow to amber gradient
        for x in range(w):
            t = x / max(1, w - 1)
            r = int(253 + (245 - 253) * t)
            g = int(224 + (158 - 224) * t)
            b = int(71 + (11 - 71) * t)
            color = "#%02x%02x%02x" % (r, g, b)
            self.header.create_line(x, 0, x, 84, fill=color)
        self.header.create_line(0, 82, w, 82, fill="#000000", width=4)
        self.header.create_text(w // 2, 31, text="PICTURE PUZZLE", fill="#111111", font=("Segoe UI", 26, "bold"))
        self.header.create_text(w // 2, 62, text="Fix the scrambled picture. Swap, rotate and flip the tiles!",
                                fill="#3a2a00", font=("Segoe UI", 10, "bold"))

    def load_image(self):
        path = filedialog.askopenfilename(title="Choose an image",
                                          filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")])
        if path == "":
            return
        n = self.grid_picker.get_size()
        try:
            img = self.proc.load(path)
            self.orig_img = self.proc.prepare(img, n)
            tiles = ImageProcessor.split(self.orig_img, n)
            self.board = PuzzleBoard(tiles, n)
        except Exception as e:
            messagebox.showerror("Error", "Could not load the image.\n" + str(e))
            return
        self.update_screen()

    def click_hint(self):
        if self.board is not None:
            self.board.give_hint()
            self.update_screen()

    def click_solve(self):
        if self.board is not None:
            self.board.solve()
            self.update_screen()

    def get_pos(self, event):
        # no game or game finished = no click
        if self.board is None or self.board.is_solved() == True:
            return None
        return self.puzzle_view.position_at(event.x, event.y)

    def click_left(self, event):
        pos = self.get_pos(event)
        if pos is not None:
            moved = self.board.left_click(pos)
            self.after_click(moved)

    def click_shift(self, event):
        pos = self.get_pos(event)
        if pos is not None:
            moved = self.board.flip_tile(pos)
            self.after_click(moved)

    def click_right(self, event):
        pos = self.get_pos(event)
        if pos is not None:
            moved = self.board.rotate_tile(pos)
            self.after_click(moved)

    def after_click(self, moved):
        self.update_screen()
        # show message when player finishes
        if moved == True and self.board.is_solved() == True:
            self.root.update_idletasks()
            messagebox.showinfo("Well done!", "You restored the picture in " + str(self.board.get_moves()) +
                                " moves.\nLoad another image to play again.")

    def update_screen(self):
        board = self.board
        # no image loaded yet
        if board is None:
            self.original_view.show_placeholder("Load an image to start")
            self.puzzle_view.show_placeholder("")
            self.moves_box.set_value(0)
            self.wrong_box.set_value(0)
            self.hints_box.set_value(3)
            self.win_label.config(text="")
            self.info_label.config(text="Pick a grid size, then press Load Image.")
            self.hint_btn.config(text="Hint")
            self.hint_btn.set_enabled(False)
            self.solve_btn.set_enabled(False)
            return

        self.original_view.draw(self.orig_img, board)
        self.puzzle_view.draw(board.get_image(), board)

        self.moves_box.set_value(board.get_moves())
        self.wrong_box.set_value(board.count_wrong())
        self.hints_box.set_value(board.get_hints_left())

        self.hint_btn.config(text="Hint (" + str(board.get_hints_left()) + ")")
        self.hint_btn.set_enabled(board.can_hint())
        self.solve_btn.set_enabled(board.is_solved() == False)

        if board.is_solved() == True:
            self.win_label.config(text="PUZZLE SOLVED!")
            self.info_label.config(text="Load another image to play again.")
        else:
            self.win_label.config(text="")
            self.info_label.config(text="Left click: select / swap\nRight click: rotate 90\nShift + left click: flip")
