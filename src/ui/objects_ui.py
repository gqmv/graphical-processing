from typing import Callable

from src.components.material import Material
from src.components.objects_in_space import (
    Object,
    Plane,
    Sphere,
    Triangle,
    TriangleMesh,
)
from src.components.point import Point
from src.components.vector import Vector
from src.ui.material_ui import get_material
from src.ui.utils import GeneralizedFuntionRegistry, ask_continue, get_triplet


class ObjectCreationFunctionRegistry(
    GeneralizedFuntionRegistry[Callable[[Material], Object]]
):
    pass


object_creation_function_registry = ObjectCreationFunctionRegistry()


@object_creation_function_registry.register("sphere")
def create_sphere(material: Material) -> Sphere:
    """Creates a sphere from user input."""
    while True:
        radius = float(input("Enter the radius of the sphere: "))
        try:
            x, y, z = get_triplet("Enter the center of the sphere (x, y, z): ")
            return Sphere(
                material=material,
                radius=radius,
                center=Point(float(x), float(y), float(z)),
            )
        except ValueError:
            print("Invalid center. Please try again.")


@object_creation_function_registry.register("plane")
def create_plane(material: Material) -> Plane:
    """Creates a plane from user input."""
    while True:
        try:
            normal_x, normal_y, normal_z = get_triplet(
                "Enter the normal of the plane (x, y, z): "
            )
            point_x, point_y, point_z = get_triplet(
                "Enter the point of the plane (x, y, z): "
            )
            return Plane(
                material=material,
                point=Point(float(point_x), float(point_y), float(point_z)),
                normal=Vector(float(normal_x), float(normal_y), float(normal_z)),
            )
        except ValueError:
            print("Invalid normal or point. Please try again.")


# NOTE: Since the user should never be able to create a triangle that is not part of a mesh, this function is not registered.
def create_triangle(material: Material) -> Triangle:
    """Creates a triangle from user input."""
    while True:
        try:
            normal_x, normal_y, normal_z = get_triplet(
                "Enter the normal of the triangle (x, y, z): "
            )
            v1_x, v1_y, v1_z = get_triplet("Enter the first point of the triangle: ")
            v2_x, v2_y, v2_z = get_triplet("Enter the second point of the triangle: ")
            v3_x, v3_y, v3_z = get_triplet("Enter the third point of the triangle: ")
            return Triangle(
                material=material,
                points=(
                    Point(float(v1_x), float(v1_y), float(v1_z)),
                    Point(float(v2_x), float(v2_y), float(v2_z)),
                    Point(float(v3_x), float(v3_y), float(v3_z)),
                ),
                normal=Vector(float(normal_x), float(normal_y), float(normal_z)),
            )
        except ValueError:
            print("Invalid normal or point. Please try again.")


@object_creation_function_registry.register("mesh")
def create_triangle_mesh(material: Material) -> TriangleMesh:
    """Creates a triangle mesh from user input."""
    triangles = []
    first_run = True
    while first_run or ask_continue("triangles"):
        first_run = False
        triangles.append(create_triangle(material))

    return TriangleMesh(material=material, triangles=triangles)


def get_object_creation_function() -> Callable[[Material], Object]:
    """Gets the object creator function."""
    while True:
        object_type = input("Enter the type of the object: ").lower()
        try:
            return object_creation_function_registry.get(object_type)
        except KeyError:
            print("Invalid object type. Please try again.")


def create_scene_objects(materials: dict[str, Material]) -> list[Object]:
    """Creates the objects of the scene."""
    first_run = True
    objects: list[Object] = []
    while first_run or ask_continue("objects"):
        first_run = False
        material = get_material(materials)
        object_creation_function = get_object_creation_function()
        objects.append(object_creation_function(material))

    return objects
