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

    def __init__(self, material: Material, points: list[list[Point]], K1: int, K2: int): # é uma lista de listas de pontos que formam, cada uma, uma curva de bezier
        super().__init__(material)
        self.points = points

        # Primeiro passo: Criar a matriz intermediaria com as iterações do deCasteljau com K1
        new_matriz_k1 = []
        for lista_pontos in points:
            new_pontos = []
            for i in range(K1):
                new_ponto = self.deCasteljau(lista_pontos, i/(K1 - 1))
                new_pontos.append(new_ponto)
            new_matriz_k1.append(new_pontos)

        # Segunda matriz
        final_matriz_k2 = []
        for j in range(K1): # Posição das colunas
            coluna = [linha[j] for linha in new_matriz_k1]
            new_pontos = []
            for i in range(K2):
                new_ponto = self.deCasteljau(coluna, i/(K2 - 1))
                new_pontos.append(new_ponto)
            final_matriz_k2.append(new_pontos)
            # A matriz vai ficar transposta mas nao importa para a malha de trigulos

        lista_triangulos = []
        for i in range(K1-1):
            for j in range(K2-1):
                vector_11 = final_matriz_k2[i][j+1] - final_matriz_k2[i][j]
                vector_12 = final_matriz_k2[i+1][j] - final_matriz_k2[i][j]
                normal1 = vector_12.cross_product(vector_11).normalized()
                T1 = Triangle(self.material, (final_matriz_k2[i][j+1], final_matriz_k2[i][j], final_matriz_k2[i+1][j]), normal1)

                vector_21 = final_matriz_k2[i][j+1] - final_matriz_k2[i+1][j+1]
                vector_22 = final_matriz_k2[i+1][j] - final_matriz_k2[i+1][j+1]
                normal2 = vector_21.cross_product(vector_22).normalized()
                T2 = Triangle(self.material, (final_matriz_k2[i][j+1], final_matriz_k2[i+1][j+1], final_matriz_k2[i+1][j]), normal2)

                lista_triangulos.append(T1)

                lista_triangulos.append(T2)

        self.malha = TriangleMesh(material, lista_triangulos)
        print(len(lista_triangulos))

           
    def interpolate(self, pointA: Point, pointB: Point, t: float):
        mult1 = pointA.__mul__(t) 
        mult2 = pointB.__mul__(1-t)
        return mult1.__add__(mult2)
    
    def deCasteljau(self, points: list[Point], t):
        grade = len(points) - 1
        
        if grade == 1:
            return self.interpolate(points[0], points[1], t)
        
        newPoints = []
        for i in range(grade):
            pointA = points[i]
            pointB = points[i + 1]
            newPoint = self.interpolate(pointA, pointB, t)
            
            newPoints.append(newPoint)
        
        return self.deCasteljau(newPoints, t)

    def get_normal_at_point(self, point: Point) -> Vector:
        return self.malha.get_normal_at_point(point)

    def find_intersection(self, ray: Ray) -> tuple[float, Vector] | tuple[None, None]:
        return self.malha.find_intersection(ray)

    def _transform(self, matrix: list[list[float]]) -> Self:
        return self.malha._transform(matrix)