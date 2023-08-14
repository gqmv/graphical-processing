from dataclasses import dataclass

from src.components.color import *
from src.components.point import *


@dataclass
class Light:
    """A light source in the scene."""

    position: Point
    color: Color
