from __future__ import annotations

from typing import Any

from components.vector import Vector


class Point:
    """A point in 3D space."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __sub__(self, other: Point) -> Vector:
        from components.vector import Vector
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Point | Vector) -> Point:
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, other: float) -> Point:
        return Point(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> Point:
        return self.__mul__(other)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y, -self.z)
