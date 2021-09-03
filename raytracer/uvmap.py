from __future__ import  annotations

import math
from abc import ABC, abstractmethod

import geometry
from geometry.vector import Vector


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


class UVMapTriangle(UVMap):
    def __init__(self, triangle: geometry.Triangle):
        self.triangle = triangle

    def get_uv(self, xyz: Vector) -> Vector:
        t1 = self.triangle.t1
        t2 = self.triangle.t2
        t3 = self.triangle.t3


        tangent = t3 - t1
        normal = self.triangle.get_normal_at(xyz)
        bitangent = tangent @ normal

        width = tangent
        height = t2 - t1 - ((width * t2 - width * t1) / width ** 2) * width

        i = width
        j = height
        k = normal.normalize()

        local_xyz = xyz - t1

        # u, v, _ = local_xyz.in_terms_of_components(i, j, k)
        return local_xyz.in_terms_of_components(i, j, k)

        # print(u, v, _)
        # print(i.normalize(), j.normalize())



        # triangle_width = abs(width)
        # triangle_height = abs(height)
        #
        # print(triangle_width, triangle_height)

if __name__ == "__main__":
    t = geometry.Triangle(Vector(-5, 6, 5),
                          Vector(0, 0, 3),
                          Vector(5, 6, 3),
                          None)

    u = UVMapTrianle(t)
    print(u.get_uv(Vector(-0.42, 4.32, 3.8)))
    print(u.get_uv(Vector(-0.72, 2.16, 3.5)))
