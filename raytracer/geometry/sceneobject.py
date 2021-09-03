from abc import ABC, abstractmethod

from geometry.ray import Ray
from geometry.vector import Vector


class SceneObject(ABC):
    def __init__(self, material):
        self.material = material

    @abstractmethod
    def get_intersection(self, ray: Ray):
        pass

    @abstractmethod
    def get_normal_at(self, position: Vector):
        pass

    @abstractmethod
    def get_uv(self, xyz: Vector):
        pass
