from __future__ import  annotations

import math
from abc import ABC, abstractmethod

import geometry
from vector import Vector


class UVMap(ABC):
    @abstractmethod
    def get_uv(self, xyz: Vector) -> Vector:
        pass


class UVMapSphere(UVMap):
    def __init__(self, sphere: geometry.Sphere):
        self.sphere = sphere

    def get_uv(self, xyz: Vector) -> Vector:
        d = (self.sphere.center - xyz).normalize()

        u = 0.5 + math.atan2(d.x, d.y) / (2 * math.pi)
        v = 0.5 - math.asin(d.z) / math.pi

        return Vector(u, v, 0)


class UVMapTrianle(UVMap):
    def __init__(self, triangle: geometry.Triangle):
        self.triangle = triangle

    def get_uv(self, xyz: Vector) -> Vector:
        t1 = self.triangle.t1
        t2 = self.triangle.t2
        t3 = self.triangle.t3


        tangent = t3 - t1
        bitangent = tangent @ self.triangle.get_normal_at(xyz)

        width = tangent
        height = t2 - t1 - ((width * t2 - width * t1) / width ** 2) * width

        i = width.normalize()
        j = height.normalize()

        local_xyz = xyz - t1
        


        triangle_width = abs(width)
        triangle_height = abs(height)

        print(triangle_width, triangle_height)

if __name__ == "__main__":
    t = geometry.Triangle(Vector(-5, 6, 5),
                          Vector(0, 0, 3),
                          Vector(5, 6, 3),
                          None)

    u = UVMapTrianle(t)
    print(u.get_uv(Vector(0,0,0)))
