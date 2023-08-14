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

    def as_rgb(self) -> tuple[int, int, int]:
        """Returns the color as a tuple of ints"""
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)
        if x > 1 or y > 1 or z > 1:
            raise ValueError("Color values must be between 0 and 1")

    @classmethod
    def from_hex(cls, hex: str):
        """Takes a hex string and returns a color object"""
        if hex.startswith("#"):
            hex = hex[1:]

        x = int(hex[0:2], 16) / 255
        y = int(hex[2:4], 16) / 255
        z = int(hex[4:6], 16) / 255

        return cls(x, y, z)

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float):
        """Takes rgb values and returns a color object"""
        return cls(r / 255, g / 255, b / 255)
