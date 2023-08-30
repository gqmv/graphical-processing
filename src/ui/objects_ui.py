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
from src.ui.point_ui import get_point
from src.ui.utils import GeneralizedFuntionRegistry, ask_continue
from src.ui.vector_ui import get_vector


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
            return Sphere(
                material=material,
                radius=radius,
                center=get_point("Enter the center of the sphere (x, y, z): "),
            )
        except ValueError:
            print("Invalid center. Please try again.")


@object_creation_function_registry.register("plane")
def create_plane(material: Material) -> Plane:
    """Creates a plane from user input."""
    while True:
        try:
            return Plane(
                material=material,
                point=get_point("Enter the point of the plane (x, y, z): "),
                normal=get_vector("Enter the normal of the plane (x, y, z): "),
            )
        except ValueError:
            print("Invalid normal or point. Please try again.")


def get_triangle_normal(point_1: Point, point_2: Point, point_3: Point) -> Vector:
    """Asks the user which normal to use for the triangle."""
    vector_1 = point_2 - point_1
    vector_2 = point_3 - point_1
    normal = vector_1.cross_product(vector_2).normalized()

    print("Calculated normals: (You can use a different one if you want)")
    print(f" - {normal}")
    print(f" - {-normal}")

    return get_vector("Enter the normal of the triangle: (x, y, z)").normalized()


# NOTE: Since the user should never be able to create a triangle that is not part of a mesh, this function is not registered.
def create_triangle(material: Material) -> Triangle:
    """Creates a triangle from user input."""
    while True:
        try:
            point_1 = get_point("Enter the first point of the triangle (x, y, z): ")
            point_2 = get_point("Enter the second point of the triangle (x, y, z): ")
            point_3 = get_point("Enter the third point of the triangle (x, y, z): ")
            normal = get_triangle_normal(point_1, point_2, point_3)

            return Triangle(
                material=material,
                points=(point_1, point_2, point_3),
                normal=normal,
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
        print("Available object types:")
        for object_type in object_creation_function_registry:
            print(f" - {object_type}")

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
