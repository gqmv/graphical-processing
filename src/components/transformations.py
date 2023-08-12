from __future__ import annotations

import math
from abc import abstractmethod

import components


class Transformable:
    """An object that can suffer linear transformations."""

    def _check_matrix(self, matrix: list[list[float]]) -> bool:
        """Checks if the given matrix is a 3x3 or 4x4 matrix"""
        if len(matrix) == 3:
            for i in range(3):
                if len(matrix[i]) != 3:
                    return False
            return True
        elif len(matrix) == 4:
            for i in range(4):
                if len(matrix[i]) != 4:
                    return False
            return True
        else:
            return False

    @abstractmethod
    def transform(self, matrix: list[list[float]]) -> Transformable:
        """
        Returns the object transformed by the given matrix.
        Note: The matrix must be either a 3x3 or 4x4 matrix.
        """
        if not self._check_matrix(matrix):
            raise ValueError("The given matrix is not a 3x3 or 4x4 matrix.")

        return self

    def translate(self, vector: components.vector.Vector) -> Transformable:
        """Returns the object translated by the given vector."""
        return self.transform(
            [
                [1, 0, 0, vector.x],
                [0, 1, 0, vector.y],
                [0, 0, 1, vector.z],
                [0, 0, 0, 1],
            ]
        )

    def scale(self, vector: components.vector.Vector) -> Transformable:
        """Returns the object scaled by the given vector."""
        return self.transform(
            [
                [vector.x, 0, 0, 0],
                [0, vector.y, 0, 0],
                [0, 0, vector.z, 0],
                [0, 0, 0, 1],
            ]
        )

    def reflect(
        self, point: components.point.Point, normal: components.vector.Vector
    ) -> Transformable:
        """Returns the object reflected by the given point and normal vector."""
        return self.transform(
            [
                [
                    1 - 2 * normal.x * normal.x,
                    -2 * normal.x * normal.y,
                    -2 * normal.x * normal.z,
                    2 * normal.x * point.x,
                ],
                [
                    -2 * normal.y * normal.x,
                    1 - 2 * normal.y * normal.y,
                    -2 * normal.y * normal.z,
                    2 * normal.y * point.y,
                ],
                [
                    -2 * normal.z * normal.x,
                    -2 * normal.z * normal.y,
                    1 - 2 * normal.z * normal.z,
                    2 * normal.z * point.z,
                ],
                [0, 0, 0, 1],
            ]
        )

    def rotate(
        self,
        point: components.point.Point,
        vector: components.vector.Vector,
        angle_radians: float | None = None,
        angle_degrees: float | None = None,
    ) -> Transformable:
        """Returns the object rotated by the given point, vector, and angle. The angle must be specified in either radians or degrees."""
        if angle_radians is not None and angle_degrees is not None:
            raise ValueError(
                "Only one of angle_radians or angle_degrees can be specified."
            )

        if angle_degrees is not None:
            angle_radians = math.radians(angle_degrees)
        elif angle_radians is None:
            raise ValueError("Either angle_radians or angle_degrees must be specified.")

        axis = vector.normalized()
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)

        rotation_matrix = [
            [
                cos + axis.x * axis.x * (1 - cos),
                axis.x * axis.y * (1 - cos) - axis.z * sin,
                axis.x * axis.z * (1 - cos) + axis.y * sin,
                0,
            ],
            [
                axis.y * axis.x * (1 - cos) + axis.z * sin,
                cos + axis.y * axis.y * (1 - cos),
                axis.y * axis.z * (1 - cos) - axis.x * sin,
                0,
            ],
            [
                axis.z * axis.x * (1 - cos) - axis.y * sin,
                axis.z * axis.y * (1 - cos) + axis.x * sin,
                cos + axis.z * axis.z * (1 - cos),
                0,
            ],
            [0, 0, 0, 1],
        ]

        # TODO: Implement this method
        raise NotImplementedError("This method is not yet fully implemented.")
