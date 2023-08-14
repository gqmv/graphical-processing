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


def main():
    objects = []
    camera = Camera(Point(0, 0, 0), Point(200, 0, 0), Vector(0, 1, 0), 90, 500, 500)

    sphere_mat = Material(Color(1, 0, 0), 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    sphere = Sphere(material=sphere_mat, center=Point(500, 0, 2), radius=1)

    objects.append(sphere)

    scene = Scene(
        camera=camera,
        objects=objects,
        lights=[Light(Point(0, 0, 0), Color(1, 1, 1))],
        ambient_color=Color(0, 0, 0),
    )

    img = render_scene(scene)
    img.write_ppm("test.ppm")


if __name__ == "__main__":
    main()
