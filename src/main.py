from src.components.camera import Camera
from src.components.color import Color
from src.components.light import Light
from src.components.material import Material
from src.components.objects_in_space import *
from src.components.point import Point
from src.components.ray import Ray
from src.components.scene import Scene
from src.components.vector import Vector
from src.renderer import render_scene

from jsonpickle import encode, decode


def main():
    objects = []

    sphere_mat = Material(
        color=Color.from_rgb(0, 0, 255).normalized(),
        diffusion_coefficient=0.8,
        specular_coefficient=1,
        ambient_coefficient=0.1,
        reflection_coefficient=0.5,
        transmission_coefficient=0.5,
        rugosity_coefficient=0,
    )
    sphere = Sphere(
        center=Point(25, 0, 30),
        radius=20,
        material=sphere_mat,
    )

    sphere2_mat = Material(
        color=Color(0, 255, 0).normalized(),
        diffusion_coefficient=0.8,
        specular_coefficient=0.1,
        ambient_coefficient=0.1,
        reflection_coefficient=0.5,
        transmission_coefficient=0.5,
        rugosity_coefficient=0,
    )

    sphere2 = Sphere(
        center=Point(-25, 0, 30),
        radius=20,
        material=sphere2_mat,
    )

    plane_mat = Material(
        color=Color(255, 0, 0).normalized(),
        diffusion_coefficient=0.8,
        specular_coefficient=0.1,
        ambient_coefficient=0.1,
        reflection_coefficient=0.5,
        transmission_coefficient=0.5,
        rugosity_coefficient=0,
    )
    plane = Plane(
        point=Point(0, 0, 0),
        normal=Vector(0, 1, 0),
        material=plane_mat,
    )

    objects.append(sphere)
    objects.append(sphere2)
    objects.append(plane)

    camera = Camera(
        position=Point(0, 10, 0),
        look_at=Point(0, 0, 50),
        v_up=Vector(0, 1, 0),
        distance_from_screen=90,
        vertical_resolution=500,
        horizontal_resolution=500,
    )

    lights = [
        Light(Point(-100, 50, 10), Color(100, 100, 100)),
        Light(Point(100, 50, 10), Color(100, 100, 100)),
        Light(Point(0, 50, 80), Color(100, 100, 100)),
    ]

    scene = Scene(
        camera=camera,
        objects=objects,
        lights=lights,
        ambient_color=Color(1, 1, 1),
        background_color=Color(0, 0, 0),
    )

    img = render_scene(scene)
    img.write_ppm("output_should_barely_be.ppm")


if __name__ == "__main__":
    main()
