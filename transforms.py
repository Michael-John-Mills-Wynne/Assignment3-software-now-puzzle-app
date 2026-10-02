# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import random


class Transformation:
    name = "transformation"

    def apply(self, board):
        # children write this
        pass

    def describe(self):
        return self.name


class SwapTransform(Transformation):
    name = "swap"

    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    def apply(self, board):
        board.swap_tiles(self._p1, self._p2)

    def describe(self):
        return "swap " + str(self._p1) + " and " + str(self._p2)


class RotateTransform(Transformation):
    name = "rotate"

    def __init__(self, p, angle=90):
        self._p = p
        self._angle = angle

    def apply(self, board):
        # angle 90 = 1 turn, 180 = 2 turns, 270 = 3 turns
        t = board.get_tile(self._p)
        t.rotate(self._angle // 90)

    def describe(self):
        return "rotate " + str(self._p) + " by " + str(self._angle)


class FlipTransform(Transformation):
    name = "flip"

    def __init__(self, p, horizontal=True):
        self._p = p
        self._horizontal = horizontal

    def apply(self, board):
        t = board.get_tile(self._p)
        if self._horizontal == True:
            t.flip_horizontal()
        else:
            t.flip_vertical()

    def describe(self):
        return "flip " + str(self._p)


def make_random_changes(total, count):
    lst = []
    # one of each type first
    a, b = random.sample(range(total), 2)
    lst.append(SwapTransform(a, b))
    lst.append(RotateTransform(random.randrange(total), random.choice([90, 180, 270])))
    lst.append(FlipTransform(random.randrange(total), random.choice([True, False])))
    # fill the rest randomly
    while len(lst) < count:
        r = random.randint(1, 3)
        if r == 1:
            a, b = random.sample(range(total), 2)
            lst.append(SwapTransform(a, b))
        elif r == 2:
            lst.append(RotateTransform(random.randrange(total), random.choice([90, 180, 270])))
        else:
            lst.append(FlipTransform(random.randrange(total), random.choice([True, False])))
    random.shuffle(lst)
    return lst
