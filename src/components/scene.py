from dataclasses import dataclass

from components.camera import Camera
from components.color import Color
from components.light import Light
from components.objects_in_space import AbstractObject


@dataclass
class Scene:
    camera: Camera
    objects: list[AbstractObject]
    lights: list[Light]
    ambient_color: Color
