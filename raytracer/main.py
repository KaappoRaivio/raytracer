import math
from pathlib import Path

from geometry import Rectangle, Triangle, Sphere, Plane
from painter import Painter
from scene import Camera, Scene, Light
from texture import SolidColor, ImageTexture
from vector import Vector
from visual import Material

viewport_size = (2000, 2000)


CAMERA_POSITION = Vector(0, -5, 7)
camera = Camera(CAMERA_POSITION, (math.radians(0), math.radians(20)), viewplane_distance=2, viewplane_size=(2, 2), viewport_size=viewport_size)


triangle = Material(SolidColor(Vector(1, 0.01, 0.01)), specular_reflectivity=Vector(0.05, 0.05, 0.05))
blue = Material(SolidColor(Vector(0.5, 0.5, 1)))
white = Material(SolidColor(Vector(1, 1, 1)))

# yellow1 = SolidColor(Vector(0.8, 0.8, 0.05))
yellow1 = ImageTexture(Path("res/texture1.png"))
# yellow2 = SolidColor(Vector(1, 0.9, 0.05))
yellow2 = ImageTexture(Path("res/texture1.png"))
# yellow3 = SolidColor(Vector(1, 1, 0.05))
yellow3 = ImageTexture(Path("res/texture1.png"))

darkblue = SolidColor(Vector(0, 0, 1))


s = 0.25

s1 = Material(yellow1, specular_reflectivity=Vector(s * 1, s * 1, s * 1))
s2 = Material(yellow2, specular_reflectivity=Vector(s * 2, s * 2, s * 2))
s3 = Material(yellow3, specular_reflectivity=Vector(s * 4, s * 4, s * 4))

sky = Material(darkblue, interacts_with_light=True)

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
              Material(SolidColor(Vector(0.7, 0.2, 0.2))),
              t5=CAMERA_POSITION),
    Rectangle(Vector(5, 6, -1),
              Vector(5, 6, 3),
              Vector(0, 0, -1),
              Vector(0, 0, 3),
              Material(SolidColor(Vector(0.7, 0.2, 0.2))),
              t5=CAMERA_POSITION),
    #
    #
    Sphere(Vector(-2.5, 4, 4.5), 0.3, s1),
    Sphere(Vector(-1, 4, 4.3), 0.6, s2),
    Sphere(Vector(1, 4, 4), 1, s3),


    Sphere(CAMERA_POSITION + Vector(0,0, 0), 200, sky),
    # Sphere(Vector(-1, 1, 1), 0.1, Material(Vector(1, 1, 0.6))),

    Plane(Vector(0, 0, 1), -1, white),


    # Plane(-Vector(0, 0.5, -1), 100, sky)
]

lights = [
    # Light(Vector(0, 0, 2), Vector(500, 1000, 3000)),
    # Light(Vector(0.5, -3, 0.5), Vector(0.6, 1.5, 2)),

    Light(Vector(3, 4, 5), Vector(3, 1, 10)),
    Light(Vector(-3, 2, 5), Vector(10, 1, 3)),

    # Light(Vector(-5, -10, 25), Vector(1, 1, 1) * 10),
]
scene = Scene(objects, lights, camera, ambient_light_intensity=Vector(0.01, 0.01, 0.01))
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

with Painter(*viewport_size, int(max(1000, viewport_size[0]) / viewport_size[0])) as painter:
    while True:
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
        painter.wait(callback=handler)


