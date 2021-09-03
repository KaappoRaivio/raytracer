from __future__ import annotations

import dataclasses
import math
import os
from abc import ABC, abstractmethod
from typing import List, Union

from PIL import Image
# from PIL.Image import Image

from geometry.vector import Vector


class ColorBlend:
    def __init__(self, initialColors: List[Color]=None):
        if initialColors is None:
            initialColors = []

        # print(initialColors)
        self.colors = initialColors
        # print("Moiasdasdas")

    def add(self, color: Union[Color, ColorBlend]):
        if isinstance(color, ColorBlend):
            print(color)
            self.colors.extend(color.colors)
        elif isinstance(color, Color):
            self.colors.append(color)
        else:
            raise Exception()


    def blend(self, gamma=1) -> Color:
        return sum(map(Color.apply_gamma, self.colors), Color(0, 0, 0)).apply_gamma(gamma)


class Color:
    def __init__(self, r: float, g: float, b: float, gamma=2.2):
        self.r = r
        self.g = g
        self.b = b
        # self.gamma = gamma
        self.gamma = gamma

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    def __add__(self, other):
        if not isinstance(other, Color):
            raise Exception(f"Can't add {other} to color!")

        if self.gamma == 1 and other.gamma == 1:
            return Color(self.r + other.r, self.g + other.g, self.b + other.b, gamma=1)

        blended = []

        new_gamma = math.sqrt(self.gamma * other.gamma)
        for channel1, channel2 in zip(self, other):
            blended.append((channel1 ** self.gamma + channel2 ** other.gamma))

        return Color(*blended, gamma=new_gamma)

    def __abs__(self):
        return self.luminance()

    def luminance(self):
        a = self.apply_gamma(1)
        gamma = 1
        return (0.299 * self.r ** gamma + 0.587 * self.g ** gamma + 0.114 * self.b ** gamma) ** (1 / gamma)

    def normalize(self):
        return self / abs(self)

    def __truediv__(self, other):
        return self * (1 / other)

    def __mul__(self, other):
        applied = self.apply_gamma(1)

        if isinstance(other, Vector):
            return Color(applied.r * other.i, applied.g * other.j, applied.b * other.k, gamma=1)
        elif isinstance(other, Color):
            other_applied = other.apply_gamma(1)
            return Color(applied.r * other_applied.r, applied.g * other_applied.g, applied.b * other_applied.b)
        else:
            return Color(applied.r * other, applied.g * other, applied.b * other, gamma=1)

    def apply_gamma(self, new_gamma=1.):
        # return self
        # new_gamma = 1
        if new_gamma == 1:
            if self.gamma == 1:
                return self
            else:
                return Color(self.r ** self.gamma, self.g ** self.gamma, self.b ** self.gamma, gamma=1)
        else:
            power = (self.gamma / new_gamma)
            return Color(self.r ** power, self.g ** power, self.b ** power, gamma=new_gamma)

    def inv_gamma(self, gamma):
        return Color(self.r ** (1 / gamma), self.g ** (1 / gamma), self.b ** (1 / gamma))

    def map(self, func):
        r = func(self.r)
        g = func(self.g)
        b = func(self.b)

        return Color(r, g, b, gamma=self.gamma)

    def __repr__(self):
        return f"Color({self.r:.2f}, {self.g:.2f}, {self.b:.2f}, gamma={self.gamma:.2f})"


class Intensity(Color):
    def __init__(self, r, g, b):
        super().__init__(r, g, b, 1)


class Texture(ABC):
    @abstractmethod
    def get_color(self, uv: Vector) -> Intensity:
        pass


class ImageTexture(Texture):
    def __init__(self, path: os.PathLike, gamma=0.5):
        self.image = Image.open(path)
        # print(self.image.format)
        # print(self.image.size)
        # print(self.image.mode)
        self.pixels = self.image.load()
        self.size = self.image.size
        # self.size = Vector(size[0], size[1], 0)
        print(self.pixels[0, 100])
        self.gamma = gamma

    def get_color(self, uv: Vector) -> Intensity:
        i = int(uv.u * self.size[0])
        j = int(uv.v * self.size[1])

        r, g, b, *_ = self.pixels[i, j]

        return Intensity(r / 256, g / 256, b / 256)

class SolidTexture(Texture):
    def __init__(self, color: Intensity):
        self.color = color

    def get_color(self, uv: Vector) -> Intensity:
        return self.color




@dataclasses.dataclass
class Material:
    albedo: Texture
    specular_reflectivity: Vector = Vector(0, 0, 0)
    diffuse_reflectivity: Vector = Vector(1, 1, 1)
    interacts_with_light: bool = True



if __name__ == '__main__':
    b = ColorBlend()
    b.add(Color(1, 1, 1))
    b.add(Color(1, 1, 1))
    b.add(Color(1, 1, 1))
    b.add(Color(1, 1, 1))

    # print(b.colors)
    # print(sum(b.colors, Color(0, 0, 0)))

    print(b.blend(2.2))
    # print(Color(0.25, 0.25, 0.25) + Color(0.25, 0.25, 0.25))
