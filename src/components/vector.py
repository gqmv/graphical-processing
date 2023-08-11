import math
from typing import Union, Any


class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vector):
            return False
        
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union["Vector", float]) -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: Union["Vector", float]) -> "Vector":
        return self.__mul__(other)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def __truediv__(self, other: Union["Vector", float]) -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector(self.x / other, self.y / other, self.z / other)

    def __pow__(self, power: int) -> "Vector":
        return Vector(self.x**power, self.y**power, self.z**power)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def norm(self) -> float:
        """Returns the norm of the vector"""
        return abs(self)

    def normalized(self) -> "Vector":
        """Returns the normalized vector"""
        return self / abs(self)


def dot_product(v1: Vector, v2: Vector) -> float:
    """Returns the dot product of two vectors"""
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def cross_product(v1: Vector, v2: Vector) -> Vector:
    """Returns the cross product of two vectors"""
    return Vector(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x
    )
