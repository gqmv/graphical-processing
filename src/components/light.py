from components.color import *
from components.point import *


class Light:
    """A light source in the scene."""

    def __init__(self, position: Point, color: Color):
        self.position = position
        self.color = color

    def __repr__(self):
        return f"Light(Pos:{self.position.__repr__}, Color:{self.color.__repr__})"
