import math
import random
from abc import ABC, abstractmethod
from typing import List

DEBUG = False

import dataclasses
import multiprocessing

from geometry.intersection import Intersection
from geometry.ray import Ray
from geometry.sphere import Sphere
from geometry.vector import Vector
from visual import Material, ColorBlend, Color, SolidTexture, Intensity


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



class LightSource(ABC):
    @abstractmethod
    def get_representative_object(self):
        pass

    @abstractmethod
    def emits_light(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_intensity(self):
        pass


@dataclasses.dataclass
class PointLightSource(LightSource):
    position: Vector
    intensity: Intensity

    render_in_picture: bool = True
    emit_light: bool = True

    def get_representative_object(self):
        if self.render_in_picture:
            return Sphere(self.position, math.sqrt(abs(self.intensity)) / 20, Material(SolidTexture(self.intensity.normalize()), interacts_with_light=False))
        else:
            return None

    def emits_light(self):
        return self.emit_light

    def get_position(self):
        return self.position

    def get_intensity(self):
        return self.intensity


@dataclasses.dataclass
class ScatteredLightSource:
    position: Vector
    intensity: Intensity

    radius: float
    amount_of_light_points: int

    def __iter__(self):
        yield PointLightSource(self.position, self.intensity, render_in_picture=True, emit_light=False)
        for i in range(self.amount_of_light_points):
            length = random.random() * self.radius
            i, j, k = (random.random() - 0.5 for i in range(3))
            offset = Vector(i, j, k).normalize() * length
            print(offset)
            yield PointLightSource(self.position + offset, self.intensity / self.amount_of_light_points, render_in_picture=False)








class Scene:
    def __init__(self, objects, lights: List[LightSource],  camera, ambient_light_intensity: Intensity=Intensity(0, 0, 0), gamma=2.2):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.ambient_light_intensity = ambient_light_intensity
        self.gamma = gamma

    def do_raycast(self, ray, bounces_left=2) -> Color:
        intersections = self.get_intersections(ray)

        if intersections:
            closest = min(intersections, key=lambda intersection: intersection.distance)

            return self.calculate_color(closest, bounces_left)
        else:
            return Intensity(0, 0, 0)

    def get_intersections(self, ray):
        intersections = []
        for object in self.objects:
            if intersection := object.get_intersection(ray):
                intersections.append(intersection)
        for light in self.lights:
            object = light.get_representative_object()

            if object is not None and (intersection := object.get_intersection(ray)):
                intersections.append(intersection)
        return intersections

    def calculate_color(self, intersection: Intersection, bounces_left=1):
        material = intersection.vertex.material
        vertex_normal = intersection.vertex.get_normal_at(intersection.intersection).normalize()
        vector_to_camera = (self.camera.origin - intersection.intersection).normalize()


        specular_intensity = ColorBlend()
        diffuse_intensity = ColorBlend()
        texel = material.albedo.get_color(intersection.vertex.get_uv(intersection.intersection))

        if not material.interacts_with_light:
            return texel.apply_gamma(self.gamma)


        for light in self.lights:
            if not light.emits_light():
                continue

            occlusions = []

            vector_to_light = light.get_position() - intersection.intersection

            new_ray = Ray(intersection.intersection, vector_to_light.normalize())

            for object in self.objects:
                if occlusion := object.get_intersection(new_ray):
                    if occlusion.vertex.material.interacts_with_light and occlusion.distance < abs(vector_to_light):
                        occlusions.append(occlusion)


            if not occlusions:
                specular_direction_coefficient = abs(intersection.ray.direction.reflection(vertex_normal) * vector_to_light.normalize())
                diffuse_direction_coefficient = abs(vector_to_light.normalize() * vertex_normal)
                # diffuse_direction_coefficient = 1

                distance_coefficient = 1 / vector_to_light ** 2
                # pixel_color += abs(vertex_normal * vector_to_light.normalize()) * abs(vector_to_light) ** 2 * self.do_gamma_correction(light.intensity, 2.2)
                specular_intensity.add(light.get_intensity() * distance_coefficient * specular_direction_coefficient)
                diffuse_intensity.add(light.get_intensity() * distance_coefficient * diffuse_direction_coefficient)

        specular_reflectivity = material.specular_reflectivity
        diffuse_reflectivity = material.diffuse_reflectivity

        if bounces_left > 0 and specular_reflectivity != Vector(0, 0, 0):
            reflection_ray_direction = intersection.ray.direction.reflection(vertex_normal)
            reflection_ray_origin = intersection.intersection

            spexel = self.do_raycast(Ray(reflection_ray_origin, reflection_ray_direction), bounces_left - 1)
        else:
            spexel = Intensity(0, 0, 0)



        # dot = abs(vertex_normal * vector_to_camera)
        # specular_intensity.add(self.ambient_light_intensity * dot)
        # print("early return")


        luxel = specular_intensity.blend(1) * specular_reflectivity + diffuse_intensity.blend(1) * (Vector.ONE - specular_reflectivity)
        # luxel = specular_intensity.blend(1) * specular_reflectivity + diffuse_intensity.blend(1) * diffuse_reflectivity
        # result = texel * luxel + spexel * specular_reflectivity
        result = texel * luxel * (Vector.ONE - specular_reflectivity) + spexel * specular_reflectivity
        return result


    def do_inverse_gamma_correction(self, color, gamma):
        return Vector(color.i ** (1 / gamma), color.j ** (1 / gamma), color.k ** (1 / gamma))

    def do_gamma_correction(self, color, gamma):
        return Vector(color.i ** gamma, color.j ** gamma, color.k ** gamma)


    def trace(self, bounces):
        if not DEBUG:
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
                    # pass


                return self.do_raycast(Ray(self.camera.origin, direction), bounces)

            with multiprocessing.Pool(10) as pool:
                return pool.map(f, flattened, 128)
        else:
            print("generating viewplane, DEBUG")
            viewplane = self.camera.get_viewplane()

            print("starting tracing")

            a = 0.5
            flattened = [(pixel, x, y) for y, row in enumerate(viewplane) for x, pixel in enumerate(row)]


            def f(args):
                direction, x, row = args
                if not row % 10 and x == 0:
                    # pygame.event.get()
                    print(row)

                try:
                    return self.do_raycast(Ray(self.camera.origin, direction), bounces)
                except Exception as e:
                    print(args)
                    raise e

            return list(map(f, flattened))




