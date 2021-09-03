import math

import uvmap
from geometry.intersection import LIMIT, Intersection
from geometry.sceneobject import SceneObject
from geometry.vector import Vector


class Sphere(SceneObject):

    def __init__(self, center, radius, material):
        super().__init__(material)

        self.center = center
        self.radius = radius

        self.uv_map = uvmap.UVMapSphere(self)

    def includes(self, point: Vector):
        return abs((self.center - point) ** 2 - self.radius ** 2) < LIMIT

    def get_intersection_distance(self, ray):
        if self.includes(ray.constant):
            return None

        d = ray.direction.normalize()
        C = ray.constant
        r = self.radius
        P = self.center

        discriminant = (d * (C - P)) ** 2 - ((C - P) ** 2 - r ** 2)
        # print(discriminant)
        if discriminant < 0:
            return None
        # else:
        #     print(discriminant)

        base = -(d * (C - P))
        if discriminant == 0:
            return base,

        return base + math.sqrt(discriminant), base - math.sqrt(discriminant)

    def get_uv(self, xyz: Vector):
        # return Vector(0.5, 0.5, 0)
        return self.uv_map.get_uv(xyz)

    def get_intersection(self, ray):
        distances = self.get_intersection_distance(ray)
        if distances is None:
            return False

        λ = min(filter(lambda x: x > 0, distances), default=0)
        if λ == 0:
            return False

        intersection = ray.apply(λ)
        return Intersection(λ, intersection, self, ray)

    def get_normal_at(self, position: Vector):
        # print((position - self.center).normalize())
        return (position - self.center).normalize()

