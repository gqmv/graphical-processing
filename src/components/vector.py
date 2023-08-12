from __future__ import annotations

import math
from typing import Any, TypeVar, Union

import src.components
from src.components.transformations import Transformable


class Vector(Transformable):
    """A 3D vector"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vector):
            return False

        return self.x == other.x and self.y == other.y and self.z == other.z

    T = TypeVar("T", "Vector", "src.components.point.Point")

    def __add__(self, other: T) -> T:
        if not isinstance(other, Vector):
            return other + self
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[Vector, float]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: Union[Vector, float]) -> Vector:
        return self.__mul__(other)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y, -self.z)

    def __truediv__(self, other: Union[Vector, float]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector(self.x / other, self.y / other, self.z / other)

    def __pow__(self, power: int) -> Vector:
        return Vector(self.x**power, self.y**power, self.z**power)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm(self) -> float:
        """Returns the norm of the vector"""
        return abs(self)

    def normalized(self) -> Vector:
        """Returns the normalized vector"""
        return self / abs(self)

    Matrix = list[list[float]]

    def _transform_3x3(self, matrix: Matrix) -> Vector:
        """Transforms the vector by a 3x3 matrix"""
        return Vector(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
        )

    def _transform_4x4(self, matrix: Matrix) -> Vector:
        """Transforms the vector by a 4x4 matrix"""
        return Vector(
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

    def transform(self, matrix: Matrix) -> Vector:
        super().transform(matrix)

        if len(matrix) == 3:
            return self._transform_3x3(matrix)

        return self._transform_4x4(matrix)

    def dot_product(self, other: Vector) -> float:
        """Convenience method that returns dot_product(self, other)"""
        return dot_product(self, other)

    def cross_product(self, other: Vector) -> Vector:
        """Convenience method that returns cross_product(self, other)"""
        return cross_product(self, other)


def dot_product(v1: Vector, v2: Vector) -> float:
    """Returns the dot product of two vectors"""
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def cross_product(v1: Vector, v2: Vector) -> Vector:
    """Returns the cross product of two vectors"""
    return Vector(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x
    )
