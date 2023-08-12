from src.components.point import Point
from src.components.vector import Vector


class Ray:
    """A light ray. Has an origin point and a vector that indicates it's direction."""

    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def __repr__(self) -> str:
        return f"Ray(Origin:{self.origin}, Direction:{self.direction})"
