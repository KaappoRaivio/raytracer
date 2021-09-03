LIMIT = 0.001

import dataclasses

from geometry.ray import Ray
from geometry.sceneobject import SceneObject
from geometry.vector import Vector


@dataclasses.dataclass
class Intersection:
    distance: int
    intersection: Vector
    vertex: SceneObject
    ray: Ray

