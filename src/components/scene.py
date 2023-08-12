from dataclasses import dataclass

from src.components.camera import Camera
from src.components.color import Color
from src.components.light import Light
from src.components.objects_in_space import AbstractObject


@dataclass
class Scene:
    camera: Camera
    objects: list[AbstractObject]
    lights: list[Light]
    ambient_color: Color
