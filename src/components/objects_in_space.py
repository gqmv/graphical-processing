import math
from abc import ABC, abstractmethod
from typing import Self

from src.components.material import Material
from src.components.point import Point
from src.components.ray import Ray
from src.components.transformations import Transformable
from src.components.vector import Vector


class Object(ABC, Transformable):
    """Abstract class for all objects in space."""

    def __init__(self, material: Material):
        self.material = material

    @abstractmethod
    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        """Find the intersection of the object with a ray.

        Returns:
            Tuple of the distance to the intersection and the normal vector at the intersection.
        """
        pass

    @abstractmethod
    def get_normal_at_point(self, point: Point) -> Vector:
        """Get the normal vector at a point on the object."""
        pass


class Sphere(Object):
    """Class for sphere objects."""

    def __init__(self, material: Material, radius: float, center: Point):
        super().__init__(material)
        self.radius = radius
        self.center = center

    def __repr__(self) -> str:
        return f"Sphere(Center:{self.center}, Radius:{self.radius})"

    def get_normal_at_point(self, point: Point) -> Vector:
        return (point - self.center).normalized()

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        a_coeff = ray.direction.dot_product(ray.direction)
        b_coeff = 2 * ray.direction.dot_product(ray.origin - self.center)
        c_coeff = (ray.origin - self.center).dot_product(
            ray.origin - self.center
        ) - self.radius**2

        discriminant = b_coeff**2 - 4 * a_coeff * c_coeff

        EPSILON = 0.0001
        if discriminant >= 0:
            distance = (-b_coeff - math.sqrt(discriminant)) / (2 * a_coeff)
            if distance > EPSILON:
                return distance, self.get_normal_at_point(
                    ray.origin + distance * ray.direction
                )

            distance = (-b_coeff + math.sqrt(discriminant)) / (2 * a_coeff)
            if distance > EPSILON:
                return distance, self.get_normal_at_point(
                    ray.origin + distance * ray.direction
                )

        return None, None

    def _transform(self, matrix: list[list[float]]) -> Self:
        center = self.center.transform(matrix)
        return self.__class__(self.material, self.radius, center)


class Plane(Object):
    """Class for plane objects."""

    def __init__(self, material: Material, normal: Vector, point: Point):
        super().__init__(material)
        self.normal = normal.normalized()
        self.point = point

    def get_normal_at_point(self, point: Point) -> Vector:
        return self.normal

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        EPSILON = 0.0001
        if abs(ray.direction.dot_product(self.normal)) < EPSILON:
            return None, None

        distance = self.normal.dot_product(
            self.point - ray.origin
        ) / ray.direction.dot_product(self.normal)
        if distance > EPSILON:
            return distance, self.normal

        return None, None

    def _transform(self, matrix: list[list[float]]) -> Self:
        point = self.point.transform(matrix)
        normal = self.normal.transform(matrix)
        return self.__class__(self.material, normal, point)


class Triangle(Object):
    """Class for triangle objects."""

    def __init__(
        self,
        material: Material,
        points: tuple[Point, Point, Point],
        normal: Vector,
    ):
        super().__init__(material)
        self.points = points
        self.normal = normal.normalized()

    def get_normal_at_point(self, point: Point) -> Vector:
        return self.normal

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        edge1 = self.points[1] - self.points[0]
        edge2 = self.points[2] - self.points[0]

        h = ray.direction.cross_product(edge2)
        a = edge1.dot_product(h)

        EPSILON = 0.0001
        if a > -EPSILON and a < EPSILON:
            return None, None

        f = 1 / a
        s = ray.origin - self.points[0]
        u = f * s.dot_product(h)

        if u < 0 or u > 1:
            return None, None

        q = s.cross_product(edge1)
        v = f * ray.direction.dot_product(q)

        if v < 0 or u + v > 1:
            return None, None

        t = f * edge2.dot_product(q)
        if t > EPSILON:
            return t, self.normal

        return None, None

    def _transform(self, matrix: list[list[float]]) -> Self:
        points = tuple(point.transform(matrix) for point in self.points)
        normal = self.normal.transform(matrix)
        return self.__class__(self.material, points, normal)  # type: ignore


class TriangleMesh(Object):
    """Class for triangle mesh objects."""

    def __init__(self, material: Material, triangles: list[Triangle]):
        super().__init__(material)
        self.triangles = triangles

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        distance = float("inf")
        normal = None
        for triangle in self.triangles:
            triangle_distance, triangle_normal = triangle.find_intersection(ray)
            if triangle_distance is not None and triangle_distance < distance:
                distance = triangle_distance
                normal = triangle_normal

        if normal is None:
            return None, None

        return distance, normal

    def find_triangle_at_point(self, point: Point) -> Triangle | None:
        EPSILON = 0.0001
        for triangle in self.triangles:
            edge1 = triangle.points[1] - triangle.points[0]
            edge2 = triangle.points[2] - triangle.points[0]

            h = edge2.cross_product(triangle.normal)
            a = edge1.dot_product(h)

            if a > -EPSILON and a < EPSILON:
                continue

            f = 1 / a
            s = point - triangle.points[0]
            u = f * s.dot_product(h)

            if u < 0 or u > 1:
                continue

            q = s.cross_product(edge1)
            v = f * edge2.dot_product(q)

            if v < 0 or u + v > 1:
                continue

            return triangle

        return None

    def get_normal_at_point(self, point: Point) -> Vector:
        triangle = self.find_triangle_at_point(point)
        if triangle is None:
            raise Exception("No triangle found at point")

        return triangle.get_normal_at_point(point)

    def _transform(self, matrix: list[list[float]]) -> Self:
        triangles = [triangle.transform(matrix) for triangle in self.triangles]
        return self.__class__(self.material, triangles)


class BezierSurface(Object):
    """Class for bezier surface objects."""

    def __init__(self, material: Material, points: list[list[Point]]):
        super().__init__(material)
        self.points = points

    def get_normal_at_point(self, point: Point) -> Vector:
        pass

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        pass

    def _transform(self, matrix: list[list[float]]) -> Self:
        pass
