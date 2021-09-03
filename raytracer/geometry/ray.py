import dataclasses

from geometry.vector import Vector


@dataclasses.dataclass
class Ray:
    constant: Vector
    direction: Vector

    def apply(self, λ):
        return self.constant + λ * self.direction
