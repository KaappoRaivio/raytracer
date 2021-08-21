import dataclasses

from vector import Vector

@dataclasses.dataclass
class Plane:
    normal: Vector
    intersect: float

    limit: float = 0.001

    def includes(self, vector):
        return abs(self.normal * vector + self.intersect) < self.limit

    def get_intersection_distance(self, ray):
        if self.normal * ray.direction == 0:
            raise Exception(f"Ray {ray} doesn't intersect plane {self}!")
        else:
            return -(self.normal * ray.constant + self.intersect) / (self.normal * ray.direction)


@dataclasses.dataclass
class Ray:
    constant: Vector
    direction: Vector

    def apply(self, λ):
        return self.constant + λ * self.direction


class Triangle:
    def __init__(self, t1, t2, t3):
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

        self.plane = Plane(normal, intersect)


    def contains(self, vector):
        return self.check_coarse(vector) and self.plane.includes(vector) and self.check_fine(vector)


    def get_intersection(self, ray):
        λ = self.plane.get_intersection_distance(ray)
        print(λ)
        intersection = ray.apply(λ)
        if not self.contains(intersection):
            return False
        else:
            return intersection

    def check_coarse(self, vector):
        # print(self.minimum < vector < self.maximum)
        return self.minimum < vector < self.maximum

    def check_fine(self, vector):
        # print(self.minimum < vector < self.maximum)
        v = self.t2 - self.t3
        a = v @ (vector - self.t3)
        b = v @ (self.t1 - self.t3)
        c = a * b

        if c < 0: return False

        v = self.t1 - self.t3
        a = v @ (vector - self.t3)
        b = v @ (self.t2 - self.t3)
        c = a * b

        if c < 0: return False

        v = self.t2 - self.t1
        a = v @ (vector - self.t1)
        b = v @ (self.t3 - self.t1)
        c = a * b

        if c < 0: return False

        return True








if __name__ == "__main__":
    t = Triangle(Vector(1, 0, 0),
                 Vector(0, 1, 0),
                 Vector(0, 0, 1))

    # print(t.plane.normal)
    # print(t.plane.intersect)

    origin = Vector(5, 6, 4)
    direction = Vector(-1.09, -1.21, -0.8)
    ray = Ray(origin, direction)
    print(t.get_intersection(ray))
