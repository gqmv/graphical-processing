from src.components.camera import Camera
from src.components.color import Color
from src.components.image import Image
from src.components.light import Light
from src.components.material import Material
from src.components.objects_in_space import Object
from src.components.point import Point
from src.components.ray import Ray
from src.components.scene import Scene
from src.components.vector import Vector


def trace_ray(ray: Ray, scene: Scene) -> Color:
    """Trace a ray and return the color of the first object hit."""
    closest_obj = None
    closest_obj_distance = float("inf")
    for obj in scene.objects:
        intersection = obj.find_intersection(ray)
        if intersection is not None:
            if intersection[0] < closest_obj_distance:
                closest_obj = obj
                closest_obj_distance = intersection[0]

    if closest_obj is None:
        return scene.ambient_color

    return closest_obj.material.color


def render_scene(scene: Scene) -> Image:
    """Render a scene and return the image."""
    image = Image(scene.camera.vertical_resolution, scene.camera.horizontal_resolution)

    for y in range(scene.camera.vertical_resolution):
        for x in range(scene.camera.horizontal_resolution):
            ray = scene.camera.get_ray(x, y)
            color = trace_ray(ray, scene)

            image.set_pixel(x, y, color)

    return image
