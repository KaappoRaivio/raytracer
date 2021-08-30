import dataclasses
import math
import multiprocessing

import pygame

from geometry import Ray, Triangle, Sphere, Rectangle, Intersection, Plane
from painter import Painter
from texture import SolidColor
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
    def __init__(self, objects, lights,  camera, ambient_light_intensity=Vector(0, 0, 0)):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.ambient_light_intensity = ambient_light_intensity

    def do_raycast(self, ray, bounces_left=2):
        intersections = []

        for object in self.objects:
            if intersection := object.get_intersection(ray):
                intersections.append(intersection)

        for light in self.lights:
            object = Sphere(light.position, 0.05, Material(SolidColor(light.intensity.normalize()), interacts_with_light=False))

            if intersection := object.get_intersection(ray):
                intersections.append(intersection)

        if intersections:
            # print(intersections)
            closest = min(intersections, key=lambda intersection: intersection.distance)

            if not isinstance(closest, Intersection):
                print("Problem!!")

            color = self.calculate_color(closest, bounces_left)


            # brightness = min(255 * abs(closest.vertex.plane.normal.normalize() * ray.direction.normalize()) / (closest.distance * 0.3) ** 2, 255)
            # return (brightness, brightness, brightness)
            return color
        else:
            return Vector(0, 0, 0)

    def calculate_color(self, intersection: Intersection, bounces_left=1):
        material = intersection.vertex.material
        vertex_normal = intersection.vertex.get_normal_at(intersection.intersection).normalize()
        vector_to_camera = (self.camera.origin - intersection.intersection).normalize()


        diffuse_color = Vector(0, 0, 0)
        albedo_texture_color = material.albedo.get_color(intersection.vertex.get_uv(intersection.intersection))

        if not material.interacts_with_light:
            return self.do_gamma_correction(albedo_texture_color, 2.2)

        for light in self.lights:
            occlusions = []

            vector_to_light = light.position - intersection.intersection

            new_ray = Ray(intersection.intersection, vector_to_light.normalize())

            for object in self.objects:
                if occlusion := object.get_intersection(new_ray):
                    if occlusion.vertex.material.interacts_with_light and occlusion.distance < abs(vector_to_light):
                        occlusions.append(occlusion)


            if not occlusions:
                # diffuse_color += max(vertex_normal * vector_to_light.normalize(), 0) \
                #                  / abs(vector_to_light) ** 2 * self.do_gamma_correction(light.intensity, 2.2)
                diffuse_color += abs(vertex_normal * vector_to_light.normalize()) \
                                 / abs(vector_to_light) ** 2 * self.do_gamma_correction(light.intensity, 2.2)

        specular_reflectivity = material.specular_reflectivity
        if bounces_left > 0 and specular_reflectivity != Vector(0, 0, 0):
            reflection_ray_direction = intersection.ray.direction.reflection(vertex_normal)
            reflection_ray_origin = intersection.intersection

            spexel = self.do_raycast(Ray(reflection_ray_origin, reflection_ray_direction), bounces_left - 1)
        else:
            spexel = Vector(0, 0, 0)

        # specular_reflectivity = material.specular_reflectivity
        # print(specular_reflectivity, Vector.ONE - specular_reflectivity)

        dot = max(vertex_normal * vector_to_camera, 0)

        luxel = diffuse_color % self.do_gamma_correction(albedo_texture_color, 2.2) \
                + self.ambient_light_intensity * dot

        result = luxel % (Vector.ONE - specular_reflectivity) \
                 + spexel % specular_reflectivity


        # print(result)

        return self.do_inverse_gamma_correction(result, 2.2)

    def do_inverse_gamma_correction(self, color, gamma):
        # print(Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma)))
        return Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma))

    def do_gamma_correction(self, color, gamma):
        # print(Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma)))
        return Vector(color.i ** gamma, color.j ** gamma, color.k ** gamma)


    def trace(self, bounces):
        global f
        print("generating viewplane")
        viewplane = self.camera.get_viewplane()

        print("starting tracing")

        a = 0
        flattened = [(pixel, x, y) for y, row in enumerate(viewplane) for x, pixel in enumerate(row)]


        def f(args):
            direction, x, row = args
            if not row % 10 and x == 0:
                # pygame.event.get()
                print(row)


            return self.do_raycast(Ray(self.camera.origin, direction), bounces)

        with multiprocessing.Pool(12) as pool:
            return pool.map(f, flattened, 128)
        # pixels = [[self.do_raycast(Ray(self.camera.origin, x)) for x in z] for z in viewplane]
        #     pixels = []
        #     for index, z in enumerate(viewplane):
        #         row = pool.map(f, z, 128)
        #         pixels.append(row)
        #
        #         if not index % 10:
        #             print(f"Row {index}!")



        # return pixels



