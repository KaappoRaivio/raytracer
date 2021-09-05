import itertools
import math
import time
from pathlib import Path

import numpy as np
import pygame
from PIL import Image

from geometry.intersection import Intersection
from geometry.plane import Plane
from geometry.ray import Ray
from geometry.rectangle import Rectangle
from geometry.sphere import Sphere
from geometry.triangle import Triangle
from painter import Painter
from scene.scene import Camera, Scene, PointLightSource, ScatteredLightSource
from geometry.vector import Vector
from visual import Material, Color, ImageTexture, SolidTexture, Intensity

# viewport_size = (250, 250)
WINDOW_SIZE = 1000
VIEWPORT_SIZE = (1000, 1000)
# VIEWPORT_SIZE = (100, 100)


CAMERA_POSITION = Vector(0, -5, 7)
camera = Camera(CAMERA_POSITION, (math.radians(1.05), math.radians(23)), viewplane_distance=2, viewplane_size=(2, 2), viewport_size=VIEWPORT_SIZE)

# triangletexture = ImageTexture(Path("res/texture1.png"), gamma=0.5)
triangletexture = SolidTexture(Intensity(1, 1, 0.8))
# triangle = Material(triangletexture, interacts_with_light=True)
blue = Material(SolidTexture(Intensity(0.5, 0.5, 1)))
white = Material(SolidTexture(Intensity(1, 1, 1)))

# yellow1 = SolidColor(Vector(0.8, 0.8, 0.05))
yellow1 = ImageTexture(Path("res/texture1.png"))
# yellow2 = SolidColor(Vector(1, 0.9, 0.05))
yellow2 = ImageTexture(Path("res/texture1.png"))
# yellow3 = SolidColor(Vector(1, 1, 0.05))
yellow3 = ImageTexture(Path("res/texture1.png"))

darkblue = SolidTexture(Intensity(0, 0, 1))


s = 1

s1 = Material(yellow1, specular_reflectivity=Vector.ONE * s)
s2 = Material(yellow2, specular_reflectivity=Vector.ONE * s)
s3 = Material(yellow3, specular_reflectivity=Vector.ONE * s)

sky = Material(darkblue, interacts_with_light=True)
triangle = Material(triangletexture, specular_reflectivity=Vector.ONE * 0.1)

objects = [
    Triangle(Vector(-5, 6, 5),
             Vector(0, 0, 3),
             Vector(5, 6, 3),
             triangle,
             t4=CAMERA_POSITION),
    # Rectangle(Vector(-2, 4, -1),
    #           Vector(-5, 6, 5),
    #           Vector(0, 0, -1),
    #           Vector(0, 0, 3),
    #           Material(SolidTexture(Intensity(1, 0.2, 0.2)), specular_reflectivity=Vector.ONE * 0),
    #           t5=CAMERA_POSITION),
    # Rectangle(Vector(5, 6, -1),
    #           Vector(5, 6, 3),
    #           Vector(0, 0, -1),
    #           Vector(0, 0, 3),
    #           Material(SolidTexture(Intensity(1, 0.2, 0.2))),
    #           t5=CAMERA_POSITION),
    Sphere(Vector(-2.5, 4, 4.5), 0.3, s1),
    Sphere(Vector(-1, 4, 4.3), 0.6, s2),
    Sphere(Vector(1, 4, 4), 1, s3),

    Plane(Vector(0, 0, 1), -1, white),
]



# objects = [
#     Triangle(Vector(-5, 6, 5),
#              Vector(0, 0, 3),
#              Vector(5, 6, 3),
#              triangle,
#              t4=CAMERA_POSITION),
#         Rectangle(Vector(5, 6, -1),
#                   Vector(5, 6, 3),
#                   Vector(0, 0, -1),
#                   Vector(0, 0, 3),
#                   Material(SolidTexture(Intensity(1, 0.2, 0.2))),
#                   t5=CAMERA_POSITION),
#     Sphere(Vector(1, 4, 4), 1, s3),
#     Plane(Vector(0, 0, 1), -1, white),
#
# ]

#
# lights = [
#     Light(Vector(3, 4, 5), Intensity(2.5, 2.5, 5)),
#     Light(Vector(-3, 2, 4), Intensity(8, 8, 2)),
#     Light(Vector(-5, -10, 25), Intensity(1, 1, 1) * 800),
# ]

lights = [
    # Light(Vector(-5, -10, 10), Intensity(1, 1, 1) * 400),
    # Light(Vector(3, 4, 5), Intensity(2.5, 2.5, 10)),
    *ScatteredLightSource(Vector(4, 4.5, 4), Intensity(1, 1, 10) * 7, 2, 200),
    *ScatteredLightSource(Vector(-4, 4.5, 5.5), Intensity(10, 2.5, 10) * 3, 2, 200),
    # *ScatteredLightSource(Vector(-4, 4.5, 5.5), Intensity(10, 2.5, 10) * 3, 2, 10),
    *ScatteredLightSource(Vector(-0.12, 3.83, 3.8), Intensity(2, 2, 0.5) / 2, 0.2, 200)
    # Light(Vector(0, 20, 5), Intensity(2.5, 2, 1) * 100),
    # Light(Vector(5, 0, 5), Intensity(1, 0.1, 0.1) * 100),
]

scene = Scene(objects, lights, camera, ambient_light_intensity=Intensity(0.01, 0.01, 0.01) * 10, gamma=2)
# print("\n".join(map(lambda f: " ".join(map(str, f)), pixels)))

viewplane = camera.get_viewplane()
# print(viewplane)


def handler(event):
    # print(event.type)
    if event.type == 1026:
        x, y = pygame.mouse.get_pos()
        i, j = int(x / (WINDOW_SIZE / VIEWPORT_SIZE[0])), int(y / (WINDOW_SIZE / VIEWPORT_SIZE[1]))
        print(i, j)
        intersections = scene.get_intersections(Ray(camera.origin, viewplane[j][i]))
        closest: Intersection = min(intersections, key=lambda intersection: intersection.distance, default=None)
        if closest is not None:
            print(closest.intersection)





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
        return False

    return False


times = []



d1 = 600
d2 = 2
n = 0.99
iterations = math.ceil(math.log(d2 / d1) / math.log(n))
# camera.viewplane_distance = d1


with Painter(*VIEWPORT_SIZE, int(max(WINDOW_SIZE, VIEWPORT_SIZE[0]) / VIEWPORT_SIZE[0])) as painter:
    for i in itertools.count():
        start = time.time()
        pixels = scene.trace(3)
        print("traced", flush=True)
        # print(timeit.timeit(lambda: scene.trace(), number=100) / 100)
        # cProfile.run("scene.trace()")
        # scene.camera.viewplane_distance += 0.1
        # scene.camera.origin += Vector(0, -10, 0)
        # painter.set(1, 1, (255, 0, 0))

        painter.fill(pixels, VIEWPORT_SIZE[0])
        painter.update()
        # input()

        # camera.viewplane_distance *= n
        #
        _24bit = list(map(painter.to_24_bit_rgb, pixels))
        buffer = np.array(_24bit).astype(np.uint8)
        buffer = buffer.reshape((*VIEWPORT_SIZE, 3))

        image = Image.fromarray(buffer)
        image.save(f"output/batch1.png")
        #
        # end = time.time()
        #
        # interval = end - start
        # times.append(interval)
        # print(f"Took {interval :.2f} seconds. Estimated {sum(times) / len(times) * (iterations - i)} seconds remaining!")
        #
        # if camera.viewplane_distance < d2:
        #     break

        painter.wait(callback=handler)


