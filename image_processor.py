# Assignment 03 - Group Assignment (DAN/EXT 23)
# Group members: Maximus Turner, Michael Mills-Wynne
# Project: Picture Puzzle (OOP, Tkinter, OpenCV)

import base64

import cv2
import numpy as np


class ImageProcessor:

    def __init__(self, max_size=420):
        self._max_size = max_size

    def load(self, path):
        # fromfile works with weird paths
        data = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("This file could not be read as an image.")
        return img

    def prepare(self, img, n):
        # resize to fit the screen
        h, w = img.shape[:2]
        scale = self._max_size / max(h, w)
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        if scale < 1:
            small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # pad if the picture is too thin
        if min(new_h, new_w) < n * 20:
            size = max(new_h, new_w)
            top = (size - new_h) // 2
            bottom = size - new_h - top
            left = (size - new_w) // 2
            right = size - new_w - left
            small = cv2.copyMakeBorder(small, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            new_h, new_w = small.shape[:2]

        # crop the middle so it divides by n
        side = min(new_h, new_w)
        side = side - (side % n)
        top = (new_h - side) // 2
        left = (new_w - side) // 2
        return small[top:top + side, left:left + side].copy()

    @staticmethod
    def split(img, n):
        # cut into tiles
        ts = img.shape[0] // n
        tiles = []
        for r in range(n):
            for c in range(n):
                piece = img[r * ts:(r + 1) * ts, c * ts:(c + 1) * ts]
                tiles.append(piece.copy())
        return tiles

    @staticmethod
    def assemble(tile_images, n):
        # join tiles back
        rows = []
        for r in range(n):
            s = r * n
            rows.append(np.hstack(tile_images[s:s + n]))
        return np.vstack(rows)

    @staticmethod
    def to_png_data(img):
        # tkinter can show png data
        ok, buf = cv2.imencode(".png", img)
        if not ok:
            raise ValueError("Could not encode the image.")
        return base64.b64encode(buf.tobytes())
