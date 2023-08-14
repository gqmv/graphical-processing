import math
from abc import ABC, abstractmethod

from src.components.material import Material
from src.components.point import Point
from src.components.ray import Ray
from src.components.vector import Vector


class Object(ABC):
    """Abstract class for all objects in space."""

    def __init__(self, material: Material):
        self.material = material

    @abstractmethod
    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | None:
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

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | None:
        a_coeff = ray.direction.dot_product(ray.direction)
        b_coeff = 2 * ray.direction.dot_product(ray.origin - self.center)
        c_coeff = (ray.origin - self.center).dot_product(
            ray.origin - self.center
        ) - self.radius**2

        discriminant = b_coeff**2 - 4 * a_coeff * c_coeff

        if discriminant < 0:
            return None

        t1 = (-b_coeff + math.sqrt(discriminant)) / (2 * a_coeff)
        t2 = (-b_coeff - math.sqrt(discriminant)) / (2 * a_coeff)

        if t1 < 0 and t2 < 0:
            return None

        if t1 < 0:
            return t2, self.get_normal_at_point(ray.origin + t2 * ray.direction)

        if t2 < 0:
            return t1, self.get_normal_at_point(ray.origin + t1 * ray.direction)

        return min(t1, t2), self.get_normal_at_point(
            ray.origin + min(t1, t2) * ray.direction
        )


class Plane(Object):
    """Class for plane objects."""

    def __init__(self, material: Material, normal: Vector, point: Point):
        super().__init__(material)
        self.normal = normal.normalized()
        self.point = point


class Triangle(Object):
    """Class for triangle objects."""

    def __init__(
        self,
        material: Material,
        points: tuple[Point, Point, Point],
        normal: Vector,
        points_normal: tuple[Vector, Vector, Vector],
    ):
        super().__init__(material)
        self.points = points
        self.normal = normal.normalized()
        self.points_normal = points_normal


class TriangleMesh(Object):
    """Class for triangle mesh objects."""

    def __init__(self, material: Material, triangles: list[Triangle]):
        super().__init__(material)
        self.triangles = triangles
