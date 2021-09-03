import itertools
import math
import time
from pathlib import Path

import numpy as np
from PIL import Image

from geometry.plane import Plane
from geometry.rectangle import Rectangle
from geometry.sphere import Sphere
from geometry.triangle import Triangle
from painter import Painter
from scene.scene import Camera, Scene, Light
from geometry.vector import Vector
from visual import Material, Color, ImageTexture, SolidTexture, Intensity

viewport_size = (500, 500)
# viewport_size = (100, 100)


CAMERA_POSITION = Vector(0, -5, 7)
camera = Camera(CAMERA_POSITION, (math.radians(6.5), math.radians(20)), viewplane_distance=50, viewplane_size=(2, 2), viewport_size=viewport_size)

triangletexture = ImageTexture(Path("res/texture1.png"), gamma=0.5)
# triangletexture = SolidColor(Vector(1, 0.01, 0.01))
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


s = 0.25

s1 = Material(yellow1, specular_reflectivity=Vector.ONE * s)
s2 = Material(yellow2, specular_reflectivity=Vector.ONE * s * 2)
s3 = Material(yellow3, specular_reflectivity=Vector.ONE * s * 4)

sky = Material(darkblue, interacts_with_light=True)
triangle = Material(triangletexture, specular_reflectivity=Vector.ONE * 0.1)

objects = [
    Triangle(Vector(-5, 6, 5),
             Vector(0, 0, 3),
             Vector(5, 6, 3),
             triangle,
             t4=CAMERA_POSITION),
    Rectangle(Vector(-2, 4, -1),
              Vector(-5, 6, 5),
              Vector(0, 0, -1),
              Vector(0, 0, 3),
              Material(SolidTexture(Intensity(1, 0.2, 0.2)), specular_reflectivity=Vector.ONE * 0),
              t5=CAMERA_POSITION),
    Rectangle(Vector(5, 6, -1),
              Vector(5, 6, 3),
              Vector(0, 0, -1),
              Vector(0, 0, 3),
              Material(SolidTexture(Intensity(1, 0.2, 0.2))),
              t5=CAMERA_POSITION),
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
    Light(Vector(-5, -10, 10), Intensity(1, 1, 1) * 400),
    Light(Vector(3, 4, 5), Intensity(2.5, 2.5, 5)),
    # Light(Vector(5, 0, 5), Intensity(1, 0.1, 0.1) * 100),
]

scene = Scene(objects, lights, camera, ambient_light_intensity=Intensity(0.01, 0.01, 0.01) * 10, gamma=2)
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
        return False

    return False


times = []

with Painter(*viewport_size, int(max(1000, viewport_size[0]) / viewport_size[0])) as painter:
    for i in itertools.count():
        start = time.time()
        pixels = scene.trace(3)
        print("traced", flush=True)
        # print(timeit.timeit(lambda: scene.trace(), number=100) / 100)
        # cProfile.run("scene.trace()")
        # scene.camera.viewplane_distance += 0.1
        # scene.camera.origin += Vector(0, -10, 0)
        # painter.set(1, 1, (255, 0, 0))

        painter.fill(pixels, viewport_size[0])
        painter.update()
        # input()
        
        # camera.viewplane_distance *= 0.99
        #
        # _24bit = list(map(painter.to_24_bit_rgb, pixels))
        # buffer = np.array(_24bit).astype(np.uint8)
        # buffer = buffer.reshape((*viewport_size, 3))
        #
        # image = Image.fromarray(buffer)
        # image.save(f"output/frame{i}.png")
        #
        # end = time.time()
        #
        # interval = end - start
        # times.append(interval)
        # print(f"Took {interval :.2f} seconds. Estimated {sum(times) / len(times) * (348 - i)} seconds remaining!")
        #
        # if camera.viewplane_distance < 1.5:
        #     break

        painter.wait(callback=handler)


