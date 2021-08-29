from __future__ import  annotations

import math
from abc import ABC, abstractmethod

import geometry
import vector


class UVMap(ABC):
    @abstractmethod
    def get_uv(self, xyz: vector.Vector) -> vector.Vector:
        pass


class UVMapSphere(UVMap):
    def __init__(self, sphere: geometry.Sphere):
        self.sphere = sphere

    def get_uv(self, xyz: vector.Vector) -> vector.Vector:
        d = (self.sphere.center - xyz).normalize()

        u = 0.5 + math.atan2(d.x, d.y) / (2 * math.pi)
        v = 0.5 - math.asin(d.z) / math.pi

        return vector.Vector(u, v, 0)

