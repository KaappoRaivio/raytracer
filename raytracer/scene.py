import math

from vector import Vector


class Camera:
    def __init__(self, origin, pitch, yaw):
        self.origin = origin

        self.direction = Vector(0, 1, 0).rotate(yaw, pitch)

class Scene:
    def __init__(self, triangles):
        self.triangles = triangles


if __name__ == '__main__':
    c = Camera(Vector.ORIGIN, math.radians(0), math.radians(62))
    print(c.direction)

