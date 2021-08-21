from typing import Tuple

import dataclasses
import math

from painter import Painter
from triangle import Ray, Triangle
from vector import Vector

def floatrange(start, stop, step):
    i = start

    if stop > start:
        while i < stop:
            yield i
            i += step
    else:
        while i > stop:
            yield i
            i += step


class Camera:
    DIRECTION_REFERENCE = Vector(0, 1, 0)

    def __init__(self, origin, rotation, viewplane_distance=2, viewplane_size=(1.0, 1.0), viewport_size=(80, 80)):
        self.origin = origin


        self.viewplane_distance = viewplane_distance
        self.viewplane_size = viewplane_size
        self.viewport_size = viewport_size

        self.direction = Camera.DIRECTION_REFERENCE.rotate(*rotation)
        self.rotation = rotation


    def get_viewplane(self):
        # v = Vector(self.scale * x, self.viewplane_distance, self.scale * z)

        ray_matrix = []


        # scaled_x = self.viewplane_scale * self.viewplane_size[0]
        # scaled_z = self.viewplane_scale * self.viewplane_size[1]
        viewport_to_viewplane_x = self.viewplane_size[0] / self.viewport_size[0]
        viewport_to_viewplane_z = self.viewplane_size[1] / self.viewport_size[1]



        for z in range(self.viewport_size[1] - 1, -1, -1):
            ray_matrix_row = []
            for x in range(self.viewport_size[0]):
                ray_matrix_row.append(self.origin
                                      + Vector(viewport_to_viewplane_x * x - self.viewplane_size[0] // 2,
                                             self.viewplane_distance,
                                             viewport_to_viewplane_z * z - self.viewplane_size[1] // 2)
                                      .rotate(*self.rotation)
                                      .normalize())
                # print("moi")
            ray_matrix.append(ray_matrix_row)



        return ray_matrix

    def __str__(self) -> str:
        return f"Camera({self.origin}, {self.rotation})"


@dataclasses.dataclass
class Light:
    position: Vector
    intensity: Tuple[float, float, float]


class Scene:
    def __init__(self, triangles, camera):
        self.triangles = triangles
        self.camera = camera

    def do_raycast(self, ray):
        intersections = []

        for triangle in self.triangles:
            if (intersection := triangle.get_intersection(ray)):
                intersections.append(intersection)

        if intersections:
            closest = min(intersections, key=lambda intersection: intersection.distance)
            brightness = 255 * abs(closest.vertex.plane.normal.normalize() * ray.direction.normalize())
            return (brightness, brightness, brightness)
        else:
            return (0, 0, 0)

    def trace(self):
        viewplane = self.camera.get_viewplane()
        pixels = [[self.do_raycast(Ray(self.camera.origin, x - self.camera.origin)) for x in z] for z in viewplane]

        return pixels




if __name__ == '__main__':
    camera = Camera(Vector(0, 0, -0.2), (math.radians(0), math.radians(0)), viewplane_distance=2, viewplane_size=(2, 2), viewport_size=(80, 80))
    triangles = [
        Triangle(Vector(-1, 4, 1),
                 Vector(1, 4, 0),
                 Vector(0, 2, -1)),
        Triangle(Vector(-1, 4, 1),
                 Vector(1, 4, 0),
                 Vector(0, 2, 3)),
        Triangle(Vector(-1, 4, 1),
                 Vector(0, 2, -1),
                 Vector(-2, 1, 2)),
    ]
    scene = Scene(triangles, camera)
    # print("\n".join(map(lambda f: " ".join(map(str, f)), pixels)))

    def handler(event):
        # print(event.type)
        if event.type == 769:
            table = {
                79: (10, 0, 0, 0),
                80: (-10, 0, 0, 0),
                81: (0, 10, 0, 0),
                82: (0, -10, 0, 0),

                26: (0, 0, 0, 0.1),
                22: (0, 0, 0, -0.1),
                4: (0, 0, -0.1, 0),
                7: (0, 0, 0.1, 0)
            }

            print(event.__dict__["scancode"])
            print(camera)


            transform = table.get(event.__dict__["scancode"], (0, 0, 0, 0))
            print(transform)
            camera.rotation = (camera.rotation[0] + math.radians(transform[0]), camera.rotation[1] + math.radians(transform[1]))
            camera.origin += Vector(transform[2], transform[3], 0)
            return True

        return False

    with Painter(80, 80, 10) as painter:
        while True:
            pixels = scene.trace()
            # scene.camera.viewplane_distance += 0.1
            # scene.camera.origin += Vector(0, -10, 0)
            # painter.set(1, 1, (255, 0, 0))
            painter.fill(pixels)
            painter.update()
            painter.wait(callback=handler)


