from src.components.vector import *


class Color(Vector):
    """A color object that inherits from Vector"""

    @property
    def r(self):
        return self.x

    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z

    def __add__(self, other):
        return Color(
            min(self.r + other.r, 255),
            min(self.g + other.g, 255),
            min(self.b + other.b, 255),
        )

    def as_rgb(self) -> tuple[int, int, int]:
        """Returns the color as a tuple of ints"""
        return (int(self.r), int(self.g), int(self.b))

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __init__(self, r: float, g: float, b: float):
        super().__init__(min(r, 255), min(g, 255), min(b, 255))

    @classmethod
    def from_hex(cls, hex: str):
        """Takes a hex string and returns a color object"""
        if hex.startswith("#"):
            hex = hex[1:]

        x = int(hex[0:2], 16)
        y = int(hex[2:4], 16)
        z = int(hex[4:6], 16)

        return cls(x, y, z)

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float):
        """Takes rgb values and returns a color object"""
        return cls(r, g, b)
