from components.camera import Camera
from components.color import Color
from components.light import Light
from components.material import Material
from components.objects_in_space import *
from components.point import Point
from components.ray import Ray
from components.scene import Scene
from components.vector import Vector
from renderer import render_scene


def main():
    objects = []
    camera = Camera(Point(0, 0, 0), Vector(10, 0, 10), Vector(0, 1, 0), 5, 500, 500)

    sphere_mat = Material(Color(1, 0, 0), 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
    sphere = Sphere(material=sphere_mat, center=Point(10, 0, 10), radius=1)

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
