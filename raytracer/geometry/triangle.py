import uvmap
from geometry.intersection import Intersection
from geometry.plane import Plane
from geometry.sceneobject import SceneObject
from geometry.vector import Vector


class Triangle(SceneObject):
    def __init__(self, t1, t2, t3, material, t4=None):
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

        if t4 is not None:
            if normal * (t1 - t4) > 0:
                normal = -normal

        intersect = -normal * t1

        self.v1 = self.t2 - self.t3
        self.v2 = self.t1 - self.t3
        self.v3 = self.t2 - self.t1

        self.b1 = self.v1 @ self.v2
        self.b2 = self.v2 @ self.v1
        self.b3 = self.v3 @ (-self.v2)

        self.plane = Plane(normal, intersect, material)

        self.uv_map = uvmap.UVMapTriangle(self)

    def contains(self, vector):
        return self.plane.includes(vector) and self.check_fine(vector)

    def get_normal_at(self, position: Vector):
        return self.plane.get_normal_at(position)

    def get_intersection(self, ray):
        λ = self.plane.get_intersection_distance(ray)
        if not λ or λ < 0:
            return False
        # print(λ)
        intersection = ray.apply(λ)
        if not self.contains(intersection):
            return False
        else:
            return Intersection(λ, intersection, self, ray)

    def check_coarse(self, vector):
        return self.minimum < vector < self.maximum

    def check_fine(self, vector):
        a = self.v1 @ (vector - self.t3)
        c = a * self.b1

        if c < 0: return False

        a = self.v2 @ (vector - self.t3)
        c = a * self.b2

        if c < 0: return False

        a = self.v3 @ (vector - self.t1)
        c = a * self.b3

        if c < 0: return False

        return True

    def get_uv(self, xyz: Vector):
        return self.uv_map.get_uv(xyz)
