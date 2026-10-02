# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import random

from image_processor import ImageProcessor
from tile import Tile
from transforms import FlipTransform, RotateTransform, SwapTransform, make_random_changes


class PuzzleBoard:
    MAX_HINTS = 3
    SCRAMBLE_COUNTS = {3: 6, 4: 12, 5: 20}

    def __init__(self, tile_images, n):
        self._n = n
        self._tiles = []
        for i in range(len(tile_images)):
            self._tiles.append(Tile(i, tile_images[i]))
        self._moves = 0
        self._hints_used = 0
        self._hint_pos = None
        self._selected = None
        self.scramble()

    # getters
    def get_grid(self):
        return self._n

    def get_total(self):
        return self._n * self._n

    def get_moves(self):
        return self._moves

    def get_selected(self):
        return self._selected

    def get_hint_pos(self):
        return self._hint_pos

    def get_hint_home(self):
        # home of the hinted tile
        if self._hint_pos is None:
            return None
        return self._tiles[self._hint_pos].get_num()

    def get_hints_left(self):
        return self.MAX_HINTS - self._hints_used

    def get_tile(self, p):
        return self._tiles[p]

    def is_correct(self, p):
        return self._tiles[p].is_correct()

    def count_wrong(self):
        cnt = 0
        for t in self._tiles:
            if t.is_correct() == False:
                cnt = cnt + 1
        return cnt

    def is_solved(self):
        if self.count_wrong() == 0:
            return True
        else:
            return False

    def can_hint(self):
        if self.get_hints_left() > 0 and self.is_solved() == False:
            return True
        return False

    def get_image(self):
        imgs = []
        for t in self._tiles:
            imgs.append(t.get_image())
        return ImageProcessor.assemble(imgs, self._n)

    # used by the transformations
    def swap_tiles(self, p1, p2):
        temp = self._tiles[p1]
        self._tiles[p1] = self._tiles[p2]
        self._tiles[p2] = temp
        self._tiles[p1].set_pos(p1)
        self._tiles[p2].set_pos(p2)

    def _reset_tiles(self):
        # put every tile at home
        new_list = [None] * self.get_total()
        for t in self._tiles:
            new_list[t.get_num()] = t
        self._tiles = new_list
        for t in self._tiles:
            t.reset()

    def scramble(self):
        count = self.SCRAMBLE_COUNTS.get(self._n, self.get_total() * 2)
        while True:
            self._reset_tiles()
            changes = make_random_changes(self.get_total(), count)
            for c in changes:
                c.apply(self)
            # try again if everything cancelled out
            if self.count_wrong() > 0:
                break
        self._moves = 0
        self._hints_used = 0
        self._hint_pos = None
        self._selected = None

    def play(self, change):
        # one player move
        if self.is_solved() == True:
            return False
        change.apply(self)
        self._moves = self._moves + 1
        self._hint_pos = None
        return True

    def left_click(self, p):
        if self.is_solved() == True:
            return False
        # first click selects
        if self._selected is None:
            self._selected = p
            return False
        # same tile again deselects
        if self._selected == p:
            self._selected = None
            return False
        # second tile swaps
        first = self._selected
        self._selected = None
        return self.play(SwapTransform(first, p))

    def rotate_tile(self, p):
        return self.play(RotateTransform(p, 90))

    def flip_tile(self, p):
        return self.play(FlipTransform(p, True))

    def give_hint(self):
        if self.can_hint() == False:
            return None
        wrong = []
        for i in range(self.get_total()):
            if self._tiles[i].is_correct() == False:
                wrong.append(i)
        self._hint_pos = random.choice(wrong)
        self._hints_used = self._hints_used + 1
        return self._hint_pos

    def solve(self):
        # undo everything
        self._reset_tiles()
        self._moves = 0
        self._hint_pos = None
        self._selected = None
