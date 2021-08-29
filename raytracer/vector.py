import math
import functools

@functools.total_ordering
class Vector:
    def __init__(self, i, j, k, normalized=False):
        self.__i = i
        self.__j = j
        self.__k = k

        self.__normalized = normalized


    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j, self.k + other.k)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.i * other.i + self.j * other.j + self.k * other.k
        else:
            return Vector(self.i * other, self.j * other, self.k * other)

    def __rmul__(self, other):
        return self * other

    def __rmatmul__(self, other):
        return self @ other

    def __rsub__(self, other):
        return self - other


    def __matmul__(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def __sub__(self, other):
        return self + -1 * other

    def __neg__(self):
        return self * -1

    def length(self):
        return math.sqrt(self.i ** 2 + self.j ** 2 + self.k ** 2)

    def __truediv__(self, other):
        return Vector(self.i / other, self.j / other, self.k / other)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.i == other.i and self.j == other.j and self.k == other.k
        else:
            return False

    def __bool__(self):
        return True

    def __iter__(self):
        yield self.i
        yield self.j
        yield self.k

    def __gt__(self, other):
        return self.i > other.i and self.j > other.j and self.k > other.k

    def __pow__(self, power, modulo=None):
        if power == 2:
            return self * self
        else:
            raise Exception(f"Cannot raise Vector to power of {power}!")

    def __abs__(self):
        return self.length()

    def __str__(self):
        return f"[{self.i:.2f}i, {self.j:.2f}j, {self.k:.2f}k]"

    def __repr__(self):
        return f"Vector({self.i}, {self.j}, {self.k})"

    def __mod__(self, other):
        return Vector(self.i * other.i, self.j * other.j, self.k * other.k)

    def transform(self, other):
        return Vector(self.i * other.i, self.j * other.j, self.k * other.k)

    def rotate_z(self, yaw):
        return self.rotate(yaw, 0)

    def rotate_x(self, pitch):
        return self.rotate(0, pitch)

    def rotate(self, yaw, pitch):
        return Vector(self.x * math.cos(yaw) + (self.z * math.sin(pitch) + self.y * math.cos(pitch)) * math.sin(yaw),
                      -self.x * math.sin(yaw) + (self.z * math.sin(pitch) + self.y * math.cos(pitch)) * math.cos(yaw),
                      self.z * math.cos(pitch) - self.y * math.sin(pitch))

    def normalize(self):
        if self.__normalized:
            return self
        else:
            normalized = self / abs(self)
            normalized.__normalized = True
            return normalized

    @property
    def x(self):
        return self.__i

    @property
    def i(self):
        return self.__i


    @property
    def y(self):
        return self.__j

    @property
    def j(self):
        return self.__j


    @property
    def k(self):
        return self.__k

    @property
    def z(self):
        return self.__k


Vector.ORIGIN = Vector(0, 0, 0)
