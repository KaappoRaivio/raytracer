import dataclasses

from vector import Vector


class Color:
    @staticmethod
    def blend(base, color, gamma):
        return Vector(base.i ** gamma + (color.i ** gamma), base.j ** gamma + (color.j ** gamma), base.k ** gamma + (color.k ** gamma))


@dataclasses.dataclass
class Material:
    albedo: Vector
    interacts_with_light: bool = True


