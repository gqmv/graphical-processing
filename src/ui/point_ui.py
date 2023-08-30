from src.components.point import Point
from src.ui.utils import get_triplet


def get_point(text: str) -> Point:
    """Gets a point from user input"""
    while True:
        try:
            x, y, z = get_triplet(text)
            return Point(float(x), float(y), float(z))
        except ValueError:
            print("Invalid point. Please try again.")
