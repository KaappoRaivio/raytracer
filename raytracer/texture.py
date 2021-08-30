import os
import pathlib

from PIL import Image

from vector import Vector

from abc import ABC, abstractmethod


class Texture(ABC):
    @abstractmethod
    def get_color(self, uv: Vector):
        pass


class ImageTexture(Texture):
    def __init__(self, path: os.PathLike):
        self.image = Image.open(path)
        # print(self.image.format)
        # print(self.image.size)
        # print(self.image.mode)
        self.pixels = self.image.load()
        self.size = self.image.size
        # self.size = Vector(size[0], size[1], 0)
        print(self.pixels[0, 100])

    def get_color(self, uv: Vector):
        i = int(uv.u * self.size[0])
        j = int(uv.v * self.size[1])

        return Vector(*self.pixels[i, j]) / 256

class SolidColor(Texture):
    def __init__(self, color: Vector):
        self.color = color

    def get_color(self, uv: Vector):
        return self.color


if __name__ == "__main__":
    # print(PIL.__version__)
    t = ImageTexture(pathlib.Path("/home/kaappo/git/raytracer/raytracer/res/texture1.png"))
    print(t.get_color())

