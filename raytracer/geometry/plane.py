from geometry.intersection import Intersection, LIMIT
from geometry.ray import Ray
from geometry.sceneobject import SceneObject
from geometry.vector import Vector


class Plane(SceneObject):

    def __init__(self, normal, intersect, material):
        super().__init__(material)
        pass

        self.normal = normal
        self.intersect = intersect

    def includes(self, vector):
        return abs(self.normal * vector + self.intersect) < LIMIT

    def get_intersection_distance(self, ray):
        if self.normal * ray.direction == 0 or self.includes(ray.constant):
            # raise Exception(f"{ray} doesn't intersect {self}!")
            return 0
        else:
            return -(self.normal * ray.constant + self.intersect) / (self.normal * ray.direction)

    def get_intersection(self, ray: Ray):
        d = self.get_intersection_distance(ray)
        if d <= 0:
            return False

        return Intersection(d, ray.apply(d), self, ray)

    def get_normal_at(self, position: Vector):
        return self.normal.normalize()

    def get_uv(self, xyz: Vector):
        return Vector(0.5, 0.5, 0)
