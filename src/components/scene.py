from dataclasses import dataclass

from src.components.camera import Camera
from src.components.color import Color
from src.components.light import Light
from src.components.objects_in_space import Object


@dataclass
class Scene:
    """A scene is a collection of objects, lights, and a camera."""

    camera: Camera
    objects: list[Object]
    lights: list[Light]
    ambient_color: Color
    background_color: Color
