from geometry.ray import Ray
from geometry.sceneobject import SceneObject
from geometry.triangle import Triangle
from geometry.vector import Vector



class Rectangle(SceneObject):

    def get_intersection(self, ray: Ray):
        c1 = self.triangle1.get_intersection(ray)
        if c1:
            c1.vertex = self
            return c1

        c2 = self.triangle2.get_intersection(ray)
        if c2:
            c2.vertex = self
            return c2

        return False


    def get_normal_at(self, position: Vector):
        return self.triangle1.get_normal_at(position)

    def __init__(self, t1, t2, t3, t4, material, t5=None):
        super().__init__(material)

        self.triangle1 = Triangle(t1, t2, t3, material, t5)
        self.triangle2 = Triangle(t2, t3, t4, material, t5)

    def get_uv(self, xyz: Vector):
        return Vector(0.5, 0.5, 0)
