from src.components.vector import Vector
from src.ui.utils import get_triplet


def get_vector(text: str) -> Vector:
    """Gets a vector from user input"""
    while True:
        try:
            x, y, z = get_triplet(text)
            return Vector(float(x), float(y), float(z))
        except ValueError:
            print("Invalid vector. Please try again.")
