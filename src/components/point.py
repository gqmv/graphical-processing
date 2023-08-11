from .vector import Vector
from typing import Any


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other: "Point") -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, other: float) -> "Point":
        return Point(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> "Point":
        return self.__mul__(other)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y, -self.z)
