from __future__ import annotations

LIMIT: float = 0.001


import dataclasses
from abc import ABC, abstractmethod
import math

from vector import Vector
# from visual import Visual


class Object(ABC):
    def __init__(self, material):
        self.material = material

    @abstractmethod
    def get_intersection(self, ray: Ray):
        pass

    @abstractmethod
    def get_normal_at(self, position: Vector):
        pass


@dataclasses.dataclass
class Intersection:
    distance: int
    intersection: Vector
    vertex: Object



@dataclasses.dataclass
class Plane:
    normal: Vector
    intersect: float


    def includes(self, vector):
        return abs(self.normal * vector + self.intersect) < LIMIT

    def get_intersection_distance(self, ray):
        if self.normal * ray.direction == 0 or self.includes(ray.constant):
            # raise Exception(f"{ray} doesn't intersect {self}!")
            return 0
        else:
            return -(self.normal * ray.constant + self.intersect) / (self.normal * ray.direction)


@dataclasses.dataclass
class Ray:
    constant: Vector
    direction: Vector

    def apply(self, λ):
        return self.constant + λ * self.direction



class Triangle(Object):
    def __init__(self, t1, t2, t3, material):
        super().__init__(material)

        self.t1 = t1
        self.t2 = t2
        self.t3 = t3


        self.minimum = Vector(min(t1.x, t2.x, t3.x),
                              min(t1.y, t2.y, t3.y),
                              min(t1.z, t2.z, t3.z))

        self.maximum = Vector(max(t1.x, t2.x, t3.x),
                              max(t1.y, t2.y, t3.y),
                              max(t1.z, t2.z, t3.z))

        normal = (t1 - t2) @ (t1 - t3)
        intersect = -normal * t1

        self.v1 = self.t2 - self.t3
        self.v2 = self.t1 - self.t3
        self.v3 = self.t2 - self.t1

        self.b1 = self.v1 @ self.v2
        self.b2 = self.v2 @ self.v1
        self.b3 = self.v3 @ (-self.v2)

        self.plane = Plane(normal, intersect)

    def contains(self, vector):
        return self.plane.includes(vector) and self.check_fine(vector)
        # return self.check_coarse(vector) and self.plane.includes(vector) and self.check_fine(vector)

    def get_normal_at(self, position: Vector):
        return self.plane.normal.normalize()

    def get_intersection(self, ray):
        λ = self.plane.get_intersection_distance(ray)
        if not λ or λ < 0:
            return False
        # print(λ)
        intersection = ray.apply(λ)
        if not self.contains(intersection):
            return False
        else:
            return Intersection(λ, intersection, self)

    def check_coarse(self, vector):
        # print(self.minimum < vector < self.maximum)
        return self.minimum < vector < self.maximum

    def check_fine(self, vector):
        # print(self.minimum < vector < self.maximum)
        # v = self.t2 - self.t3
        a = self.v1 @ (vector - self.t3)
        # b = self.v1 @ (self.v2)
        c = a * self.b1

        if c < 0: return False

        # v = self.t1 - self.t3
        a = self.v2 @ (vector - self.t3)
        # b = self.v2 @ (self.v1)
        c = a * self.b2

        if c < 0: return False

        # v = self.t2 - self.t1
        a = self.v3 @ (vector - self.t1)
        # b = self.v3 @ (-self.v2)
        c = a * self.b3

        if c < 0: return False

        return True


class Rectangle(Object):

    def get_intersection(self, ray: Ray):
        c1 = self.triangle1.get_intersection(ray)
        if c1:
            return c1

        c2 = self.triangle2.get_intersection(ray)
        if c2:
            return c2

        return False


    def get_normal_at(self, position: Vector):
        # pass
        return self.triangle1.plane.normal

    def __init__(self, t1, t2, t3, t4, material):
        super().__init__(material)

        self.triangle1 = Triangle(t1, t2, t3, material)
        self.triangle2 = Triangle(t2, t3, t4, material)
        # self.t1 = t1
        # self.t2 = t2
        # self.t3 = t3
        # self.t4 = t4



class Sphere(Object):

    def __init__(self, center, radius, material):
        super().__init__(material)

        self.center = center
        self.radius = radius

    def includes(self, point: Vector):
        return ((self.center - point) ** 2 - self.radius ** 2) < LIMIT

    def get_intersection_distance(self, ray):
        if self.includes(ray.constant):
            return None

        d = ray.direction.normalize()
        C = ray.constant
        r = self.radius
        P = self.center

        discriminant = (d * (C - P)) ** 2 - ((C - P) ** 2 - r ** 2)
        if discriminant < 0:
            return None

        base = -(d * (C - P))
        if discriminant == 0:
            return base,

        return base + math.sqrt(discriminant), base - math.sqrt(discriminant)

    def get_intersection(self, ray):
        distances = self.get_intersection_distance(ray)
        if distances is None:
            return False

        λ = min(filter(lambda x: x > 0, distances), default=0)
        if λ == 0:
            return False

        intersection = ray.apply(λ)
        return Intersection(λ, intersection, self)

    def get_normal_at(self, position: Vector):
        return (position - self.center).normalize()






if __name__ == "__main__":
    # t = Triangle(Vector(1, 0, 0),
    #              Vector(0, 1, 0),
    #              Vector(0, 0, 1))
    s = Sphere(Vector(5, 4, 3), 2.5)

    # print(t.plane.normal)
    # print(t.plane.intersect)

    origin = Vector(1, 0, 7)
    direction = Vector(1, 1, -0.5)
    ray = Ray(origin, direction)
    # print(s.get_intersection(ray))
    print(s.get_intersection(ray))
