from typing import Callable, TypeVar

from src.components.objects_in_space import Object
from src.components.point import Point
from src.components.vector import Vector
from src.ui.utils import GeneralizedFuntionRegistry, get_triplet

T = TypeVar("T", bound=Object)


class TransformationFunctionRegistry(
    GeneralizedFuntionRegistry[Callable[[Object], Object]]
):
    pass


transformation_function_registry = TransformationFunctionRegistry()


@transformation_function_registry.register("rotate")
def rotate(obj: T) -> T:
    """Rotates an object from user input."""
    while True:
        try:
            point_x, point_y, point_z = get_triplet(
                "Enter the point to rotate around (x, y, z): "
            )
            vector_x, vector_y, vector_z = get_triplet(
                "Enter the vector to rotate around (x, y, z): "
            )
            angle = float(input("Enter the angle to rotate by (degrees): "))
            return obj.rotate(
                point=Point(point_x, point_y, point_z),
                vector=Vector(vector_x, vector_y, vector_z),
                angle_degrees=angle,
            )
        except ValueError:
            print("Invalid rotation. Please try again.")


@transformation_function_registry.register("translate")
def translate(obj: T) -> T:
    """Translates an object from user input."""
    while True:
        try:
            x, y, z = get_triplet("Enter the translation vector (x, y, z): ")
            return obj.translate(Vector(x, y, z))
        except ValueError:
            print("Invalid translation. Please try again.")


@transformation_function_registry.register("reflect")
def reflect(obj: T) -> T:
    """Reflects an object from user input."""
    while True:
        try:
            x_point, y_point, z_point = get_triplet(
                "Enter the point to reflect through (x, y, z): "
            )
            x_vector, y_vector, z_vector = get_triplet(
                "Enter the vector to reflect through (x, y, z): "
            )
            return obj.reflect(
                point=Point(x_point, y_point, z_point),
                normal=Vector(x_vector, y_vector, z_vector),
            )
        except ValueError:
            print("Invalid reflection. Please try again.")


@transformation_function_registry.register("scale")
def scale(obj: T) -> T:
    """Scales an object from user input."""
    while True:
        try:
            x, y, z = get_triplet("Enter the scaling vector (x, y, z): ")
            return obj.scale(Vector(x, y, z))
        except ValueError:
            print("Invalid scaling. Please try again.")


def get_transformation_function():
    """Gets a transformation function from user input."""
    while True:
        print("Available transformation functions:")
        for transformation_function in transformation_function_registry:
            print(f" - {transformation_function}")

        transformation_function = input(
            "Enter the name of the transformation function: "
        )
        try:
            return transformation_function_registry.get(transformation_function)
        except KeyError:
            print("Invalid transformation function. Please try again.")


def apply_transformation(obj: T) -> T:
    """Applies a transformation to an object from user input."""
    transformation_function = get_transformation_function()
    return transformation_function(obj)
