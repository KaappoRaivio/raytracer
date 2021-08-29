import math
from abc import ABC, abstractmethod

from geometry import Sphere
from vector import Vector


class UVMap(ABC):
    @abstractmethod
    def get_uv(self, xyz: Vector) -> Vector:
        pass


class UVMapSphere(UVMap):
    def __init__(self, sphere: Sphere):
        self.sphere = sphere

    def get_uv(self, xyz: Vector) -> Vector:
        d = self.sphere.center - xyz

        u = 0.5 + math.atan2(d.x, d.y) / (2 * math.pi)
        v = 0.5 - math.asin(d.z) / math.pi

        return Vector(u, v, 0)

