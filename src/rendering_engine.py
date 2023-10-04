from math import sqrt
from multiprocessing import Pool

from src.components.color import Color
from src.components.image import Image
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
    object_hit: Object,
    hit_position: Point,
    normal_at_position: Vector,
    scene: Scene,
    spectator_position: Point | None = None,
) -> Color:
    """Return the color at the given hit position, according to Phong shading."""
    spectator_position = (
        spectator_position if spectator_position else scene.camera.position
    )

    # Ambient
    color = object_hit.material.get_ambient_component(scene_color=scene.ambient_color)
    for light in scene.lights:
        light_ray = Ray(hit_position, light.position - hit_position)
        _, _, obj = find_nearest_intersection(scene, light_ray)

        if obj is not None and obj != object_hit:
            continue

        # Diffuse
        color += object_hit.material.get_diffuse_component(
            light=light,
            hit_position=hit_position,
            normal_at_position=normal_at_position,
        )

        # Specular
        color += object_hit.material.get_specular_component(
            light=light,
            hit_position=hit_position,
            normal_at_position=normal_at_position,
            spectator_position=spectator_position,  # TODO: When reccursive ray-tracing is implemented, the spectator will change.
        )

    return color * object_hit.material.color


def trace_ray(ray: Ray, scene: Scene, depth: int = 0) -> Color:
    """Trace a ray and return the color that should be displayed, according to Phong shading."""
    (
        intersection_point,
        intersection_normal,
        intersected_obj,
    ) = find_nearest_intersection(scene, ray)

    if (
        intersected_obj is None
        or intersection_normal is None
        or intersection_point is None
    ):  # Checking all three is surely redundant, but it's done for clarity and for Mypy to be happy.
        return scene.background_color

    color = Color(0, 0, 0)

    color += color_at(
        object_hit=intersected_obj,
        hit_position=intersection_point,
        normal_at_position=intersection_normal,
        scene=scene,
        spectator_position=ray.origin,
    )

    MAX_DEPTH = 5
    if depth < MAX_DEPTH:
        material = intersected_obj.material
        normal = intersection_normal
        omega = -ray.direction
        relative_transmission_coeff = material.transmission_coefficient

        # If the ray is inside the object, the normal should be flipped.
        if normal.dot_product(omega) < 0:
            normal = -normal

            # If the ray is inside the object, the transmission coefficient should be inverted.
            relative_transmission_coeff = (
                0
                if relative_transmission_coeff == 0
                else 1 / relative_transmission_coeff
            )

        # Reflection
        if material.reflection_coefficient > 0:
            reflected_ray_pos = intersection_point + (normal * 0.01)
            reflected_ray_dir = ray.direction.reflect_vec(normal)
            
            reflected_ray = Ray(reflected_ray_pos, reflected_ray_dir)

            color += (
                trace_ray(reflected_ray, scene, depth + 1)
                * material.reflection_coefficient
            )

        # Refraction / Transmission
        if material.transmission_coefficient > 0:
            delta = 1 - (1 / relative_transmission_coeff**2) * (
                1 - normal.dot_product(omega) ** 2
            )

            # If delta is positive, the ray is refracted.
            if delta >= 0:
                inverse_transmission_coeff = 1 / relative_transmission_coeff

                refracted_ray_dir = inverse_transmission_coeff * (
                    ray.direction - normal.dot_product(ray.direction) * normal
                ) - normal * sqrt(delta)
                reflected_ray_pos = intersection_point + (-normal * 0.01)
                refracted_ray = Ray(reflected_ray_pos, refracted_ray_dir)

                color += (
                    trace_ray(refracted_ray, scene, depth + 1)
                    * material.transmission_coefficient
                )
            # If delta is negative, the ray is reflected. (Total internal reflection)
            else:
                reflected_ray_dir = ray.direction.reflect_vec(normal)
                reflected_ray_pos = intersection_point + (normal * 0.01)
                reflected_ray = Ray(reflected_ray_pos, reflected_ray_dir)
                color += (
                    trace_ray(reflected_ray, scene, depth + 1)
                    * material.transmission_coefficient
                )

    return color


def _render_ray(x: int, y: int, scene: Scene):
    """Render a ray and return the color."""
    ray = scene.camera.get_ray(x, y)
    color = trace_ray(ray, scene)

    return color


def render_scene_single_thread(scene: Scene) -> Image:
    """Render a scene and return the image."""
    pixels = []
    for y in range(scene.camera.vertical_resolution):
        pixels.append(
            [
                _render_ray(x, y, scene)
                for x in range(scene.camera.horizontal_resolution)
            ]
        )

    image = Image(
        scene.camera.vertical_resolution, scene.camera.horizontal_resolution, pixels
    )
    return image


def render_scene_multi_threaded(scene: Scene) -> Image:
    """Render a scene and return the image."""
    pixels = []
    with Pool() as p:
        results = []
        for y in range(scene.camera.vertical_resolution):
            results.append(
                p.starmap_async(
                    _render_ray,
                    [(x, y, scene) for x in range(scene.camera.horizontal_resolution)],
                )
            )
        for result in results:
            pixels.append(result.get())

    image = Image(
        scene.camera.vertical_resolution, scene.camera.horizontal_resolution, pixels
    )

    return image


def render_scene(scene: Scene, multithread: bool = False) -> Image:
    """Render a scene and return the image."""
    if multithread:
        return render_scene_multi_threaded(scene)
    else:
        return render_scene_single_thread(scene)
