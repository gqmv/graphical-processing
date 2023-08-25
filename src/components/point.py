from __future__ import annotations

from typing import Any

from src.components.transformations import Transformable
from src.components.vector import Vector


class Point(Transformable):
    """A point in 3D space."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __sub__(self, other: Point | Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    Matrix = list[list[float]]

    def _transform_3x3(self, matrix: Matrix) -> Point:
        """Transforms the vector by a 3x3 matrix"""
        return self.__class__(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
        )

    def _transform_4x4(self, matrix: Matrix) -> Point:
        """Transforms the vector by a 4x4 matrix"""
        return self.__class__(
            self.x * matrix[0][0]
            + self.y * matrix[0][1]
            + self.z * matrix[0][2]
            + matrix[0][3],
            self.x * matrix[1][0]
            + self.y * matrix[1][1]
            + self.z * matrix[1][2]
            + matrix[1][3],
            self.x * matrix[2][0]
            + self.y * matrix[2][1]
            + self.z * matrix[2][2]
            + matrix[2][3],
        )

    def _transform(self, matrix: Matrix) -> Point:
        super().transform(matrix)

        if len(matrix) == 3:
            return self._transform_3x3(matrix)

        return self._transform_4x4(matrix)

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
