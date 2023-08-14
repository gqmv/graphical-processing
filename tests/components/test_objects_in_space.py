from src.components.objects_in_space import Sphere
from src.components.material import Material
from src.components.color import Color
from src.components.point import Point
from src.components.vector import Vector
from src.components.ray import Ray


class TestSphere:
    def test_get_normal_at_point(self):
        sphere_material = Material(
            color=Color.from_hex("#FFFFFF"),
            diffusion_coefficient=0.7,
            specular_coefficient=0.2,
            ambient_coefficient=0.1,
            reflection_coefficient=0.5,
            transmission_coefficient=0.5,
            rugosity_coefficient=0.1,
        )
        sphere = Sphere(
            material=sphere_material,
            radius=1,
            center=Point(0, 0, 0),
        )

        assert sphere.get_normal_at_point(Point(0, 1, 0)) == Vector(0, 1, 0)
        assert sphere.get_normal_at_point(Point(0, 0, 1)) == Vector(0, 0, 1)

    def test_find_intersection(self):
        sphere_material = Material(
            color=Color.from_hex("#FFFFFF"),
            diffusion_coefficient=0.7,
            specular_coefficient=0.2,
            ambient_coefficient=0.1,
            reflection_coefficient=0.5,
            transmission_coefficient=0.5,
            rugosity_coefficient=0.1,
        )
        sphere = Sphere(
            material=sphere_material,
            radius=1,
            center=Point(0, 0, 0),
        )

        ray = Ray(origin=Point(0, 0, 0), direction=Vector(0, 0, 1))

        assert sphere.find_intersection(ray) == (1, Vector(0, 0, 1))
