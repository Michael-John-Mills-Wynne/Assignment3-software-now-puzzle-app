# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import cv2


class Tile:

    def __init__(self, num, img):
        self._num = num  # home position
        self._img = img
        self._pos = num  # current position
        self._turns = 0
        self._flipped = False
        self._saved = None

    def get_num(self):
        return self._num

    def get_pos(self):
        return self._pos

    def set_pos(self, p):
        self._pos = p

    def get_turns(self):
        return self._turns

    def is_flipped(self):
        return self._flipped

    def rotate(self, times=1):
        # turn clockwise
        self._turns = (self._turns + times) % 4
        self._saved = None

    def flip_horizontal(self):
        # mirror reverses the turns
        self._turns = (4 - self._turns) % 4
        if self._flipped == True:
            self._flipped = False
        else:
            self._flipped = True
        self._saved = None

    def flip_vertical(self):
        # turn 180 then mirror
        self.rotate(2)
        self.flip_horizontal()

    def reset(self):
        self._pos = self._num
        self._turns = 0
        self._flipped = False
        self._saved = None

    def is_correct(self):
        if self._pos == self._num and self._turns == 0 and self._flipped == False:
            return True
        else:
            return False

    def get_image(self):
        # build the picture only if needed
        if self._saved is None:
            im = self._img
            if self._flipped == True:
                im = cv2.flip(im, 1)
            for i in range(self._turns):
                im = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
            self._saved = im
        return self._saved
