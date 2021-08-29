import dataclasses
import math
import multiprocessing

from geometry import Ray, Triangle, Sphere, Rectangle, Intersection
from painter import Painter
from vector import Vector
from visual import Material


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
                ray_matrix_row.append(Vector(viewport_to_viewplane_x * x - self.viewplane_size[0] // 2,
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
    intensity: Vector





class Scene:
    def __init__(self, objects, lights,  camera):
        self.objects = objects
        self.lights = lights
        self.camera = camera

    def do_raycast(self, ray):
        intersections = []

        for object in self.objects:
            if intersection := object.get_intersection(ray):
                intersections.append(intersection)

        for light in self.lights:
            object = Sphere(light.position, 0.05, Material(light.intensity.normalize(), False))

            if intersection := object.get_intersection(ray):
                intersections.append(intersection)

        if intersections:
            closest = min(intersections, key=lambda intersection: intersection.distance)

            if not isinstance(closest, Intersection):
                print("Problem!!")

            color = self.calculate_color(closest)


            # brightness = min(255 * abs(closest.vertex.plane.normal.normalize() * ray.direction.normalize()) / (closest.distance * 0.3) ** 2, 255)
            # return (brightness, brightness, brightness)
            return color
        else:
            return (0, 0, 0)

    def calculate_color(self, intersection: Intersection):
        color = Vector(0, 0, 0)

        if not intersection.vertex.material.interacts_with_light:
            return self.do_gamma_correction(intersection.vertex.material.albedo, 2.2)

        for light in self.lights:
            occlusions = []

            vectorToLight = light.position - intersection.intersection
            # print(vectorToLight)

            new_ray = Ray(intersection.intersection, vectorToLight.normalize())

            for object in self.objects:
                if occlusion := object.get_intersection(new_ray):
                    # print(occlusion)
                    if occlusion.vertex.material.interacts_with_light:
                        occlusions.append(occlusion)

            if not occlusions:
                color += abs(intersection.vertex.get_normal_at(intersection.intersection) * vectorToLight.normalize()) \
                         / abs(vectorToLight) ** 2 * self.do_gamma_correction(light.intensity, 2.2)
        # print(color)
        # return color
        result = color % self.do_gamma_correction(intersection.vertex.material.albedo, 2.2)

        return self.do_inverse_gamma_correction(result, 2.2)

    def do_inverse_gamma_correction(self, color, gamma):
        # print(Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma)))
        return Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma))

    def do_gamma_correction(self, color, gamma):
        # print(Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma)))
        return Vector(color.i ** gamma, color.j ** gamma, color.k ** gamma)


    def trace(self):
        global f
        viewplane = self.camera.get_viewplane()

        def f(x):
            return self.do_raycast(Ray(self.camera.origin, x))

        with multiprocessing.Pool(8) as pool:
        # pixels = [[self.do_raycast(Ray(self.camera.origin, x)) for x in z] for z in viewplane]
            pixels = [pool.map(f, z, 128) for z in viewplane]

        return pixels



viewport_size = (80, 80)

if __name__ == '__main__':
    camera = Camera(Vector(0, -5, 0), (math.radians(0), math.radians(0)), viewplane_distance=2, viewplane_size=(2, 2), viewport_size=viewport_size)

    red = Material(Vector(1, 0, 0))
    blue = Material(Vector(0.5, 0.5, 1))
    white = Material(Vector(1, 1, 1))

    objects = [
        Triangle(Vector(-5, 6, 4),
                        Vector(0, 3, -5),
                        Vector(5, 6, 2),
                 red),
        Sphere(Vector(0, 1, 1), 0.4, white),
        Rectangle(Vector(-20, 20, -20),
                         Vector(-20, 20, 20),
                         Vector(20, 10, -20),
                         Vector(20, 10, 20),
                  white),
    ]

    lights = [
        # Light(Vector(0, 0, 2), Vector(500, 1000, 3000)),
        Light(Vector(0.5, -3, 0.5), Vector(1.5, 1.5, 2)),
        Light(Vector(-0.5, -3, 0.5), Vector(2, 1.5, 1.5)),
    ]
    scene = Scene(objects, lights, camera)
    # print("\n".join(map(lambda f: " ".join(map(str, f)), pixels)))

    def handler(event):
        # print(event.type)
        if event.type == 769:
            table = {
                79: (10, 0, 0, 0),
                80: (-10, 0, 0, 0),
                81: (0, 10, 0, 0),
                82: (0, -10, 0, 0),

                26: (0, 0, 0, 0.5),
                22: (0, 0, 0, -0.5),
                4: (0, 0, -0.5, 0),
                7: (0, 0, 0.5, 0)
            }

            print(event.__dict__["scancode"])
            print(camera)


            transform = table.get(event.__dict__["scancode"], (0, 0, 0, 0))
            print(transform)
            camera.rotation = (camera.rotation[0] + math.radians(transform[0]), camera.rotation[1] + math.radians(transform[1]))
            camera.origin += Vector(transform[2], transform[3], 0)
            return True

        return False

    with Painter(*viewport_size, int(800 / viewport_size[0])) as painter:
        while True:
            pixels = scene.trace()
            # print("traced", flush=True)
            # print(timeit.timeit(lambda: scene.trace(), number=100) / 100)
            # cProfile.run("scene.trace()")
            # scene.camera.viewplane_distance += 0.1
            # scene.camera.origin += Vector(0, -10, 0)
            # painter.set(1, 1, (255, 0, 0))
            painter.fill(pixels)
            painter.update()
            painter.wait(callback=handler)


