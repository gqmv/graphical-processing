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


def find_nearest_intersection(
    scene: Scene, ray: Ray
) -> tuple[Point, Vector, Object] | tuple[None, None, None]:
    """Return the nearest intersection point, normal and object."""
    closest_obj = None
    closest_obj_distance = float("inf")
    closest_obj_normal = None

    for obj in scene.objects:
        intersection_ditance, normal_at_position = obj.find_intersection(ray)

        if (
            intersection_ditance is not None
            and intersection_ditance < closest_obj_distance
        ):
            closest_obj = obj
            closest_obj_distance = intersection_ditance
            closest_obj_normal = normal_at_position

    if closest_obj is None or closest_obj_normal is None:
        return None, None, None

    return (
        ray.origin + ray.direction * closest_obj_distance,
        closest_obj_normal,
        closest_obj,
    )


def color_at(
    object_hit: Object, hit_position: Point, normal_at_position: Vector, scene: Scene
) -> Color:
    """Return the color at the given hit position, according to Phong shading."""
    # Ambient
    color = object_hit.material.get_ambient_component(scene_color=scene.ambient_color)
    for light in scene.lights:
        light_ray = Ray(hit_position, light.position - hit_position)
        distance_hit, _, obj = find_nearest_intersection(scene, light_ray)
        
        if obj is not None and obj != object_hit:
            continue

        # Diffuse
        color += object_hit.material.get_diffuse_component(
            light=light,
            hit_position=hit_position,
            normal_at_position=normal_at_position,
        )

        # Specular
        # color += object_hit.material.get_specular_component(
        #     light=light,
        #     hit_position=hit_position,
        #     normal_at_position=normal_at_position,
        #     spectator_position=scene.camera.position,  # TODO: When reccursive ray-tracing is implemented, the spectator will change.
        # )

    return color


def trace_ray(ray: Ray, scene: Scene) -> Color:
    """Trace a ray and return the color of the first object hit."""
    closest_obj = None
    closest_obj_distance = float("inf")
    closest_obj_normal = None
    for obj in scene.objects:
        intersection_ditance, normal_at_position = obj.find_intersection(ray)

        if (
            intersection_ditance is not None
            and intersection_ditance < closest_obj_distance
        ):
            closest_obj = obj
            closest_obj_distance = intersection_ditance
            closest_obj_normal = normal_at_position

    if (
        closest_obj is None or closest_obj_normal is None
    ):  # checking closest_obj_normal is redundant, but it's here for clarity
        return scene.background_color

    return color_at(
        object_hit=closest_obj,
        hit_position=ray.origin + ray.direction * closest_obj_distance,
        normal_at_position=closest_obj_normal,
        scene=scene,
    )


def render_scene(scene: Scene) -> Image:
    """Render a scene and return the image."""
    image = Image(scene.camera.vertical_resolution, scene.camera.horizontal_resolution)

    for y in range(scene.camera.vertical_resolution):
        for x in range(scene.camera.horizontal_resolution):
            ray = scene.camera.get_ray(x, y)
            color = trace_ray(ray, scene)

            image.set_pixel(x, y, color)

    return image
