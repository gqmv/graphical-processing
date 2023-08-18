from __future__ import annotations

import math
from typing import Any, Self, Type, TypeVar, Union

import src.components
from src.components.transformations import Transformable


U = TypeVar("U")


class Vector(Transformable):
    """A 3D vector"""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vector):
            return False

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(
        self, other: Union[Self, src.components.Point]
    ) -> Self | src.components.Point:
        if isinstance(other, src.components.Point):
            return other + self

        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self | "src.components.point.Point") -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float | Self) -> Self:
        if isinstance(other, Vector):
            return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def __truediv__(self, other: Union[Self, float]) -> Self:
        if isinstance(other, Vector):
            return self.__class__(
                self.x / (other.x or 1),
                self.y / (other.y or 1),
                self.z / (other.z or 1),
            )
        else:
            return self.__class__(
                self.x / (other or 1), self.y / (other or 1), self.z / (other or 1)
            )

    def __pow__(self, power: int) -> Self:
        return self.__class__(self.x**power, self.y**power, self.z**power)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm(self) -> float:
        """Returns the norm of the vector"""
        return abs(self)

    def normalized(self) -> Self:
        """Returns the normalized vector"""
        return self / abs(self)

    Matrix = list[list[float]]

    def _transform_3x3(self, matrix: Matrix) -> Self:
        """Transforms the vector by a 3x3 matrix"""
        return self.__class__(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
        )

    def _transform_4x4(self, matrix: Matrix) -> Self:
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

    def transform(self, matrix: Matrix) -> Self:
        super().transform(matrix)

        if len(matrix) == 3:
            return self._transform_3x3(matrix)

        return self._transform_4x4(matrix)

    def dot_product(self, other: Self) -> float:
        """Returns the dot product of two vectors"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other: Vector) -> Vector:
        """Returns the cross product of two vectors"""
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
