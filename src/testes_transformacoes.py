from src.components.camera import Camera
from src.components.color import Color
from src.components.light import Light
from src.components.material import Material
from src.components.objects_in_space import Sphere
from src.components.point import Point
from src.components.scene import Scene
from src.components.vector import Vector
from src.renderer import render_scene

from jsonpickle import encode, decode
import cProfile
import pstats


def main():
    objects = []

    obj1_mat = Material(
            color=Color(255, 0, 0).normalized(),
            diffusion_coefficient=1,
            specular_coefficient=1,
            ambient_coefficient=1,
            reflection_coefficient=0,
            transmission_coefficient=0,
            rugosity_coefficient=500,
        )

    obj1 = Sphere(
        center=Point(3, -1, 0),
        radius=1,
        material=obj1_mat,
    )

    # Testando translação - Funcionando
    #vetor_1 = Vector(10, 5, 1)
    #obj1.translate(vetor_1)

    # Testando scale - Funcionando
    #vetor_1 = Vector(1, 0, 0)
    #obj1.scale(vetor_1)

    # Testando reflect -Funcionado?
    #ponto = Point(1,1,1)
    #normal = Vector(0, 0, 1)
    #obj1.reflect(ponto, normal)

    # Testando rotate
    ponto = Point(1,1,1)
    vetor = Vector(1, 0,0)
    angle = 90
    obj1.rotate(ponto, vetor, angle)

    obj2_mat = Material(
        color=Color(0, 0, 255).normalized(),
        diffusion_coefficient=1,
        specular_coefficient=1,
        ambient_coefficient=1,
        reflection_coefficient=0,
        transmission_coefficient=0,
        rugosity_coefficient=500,
    )
    obj2 = Sphere(
            center=Point(4, 0, 2),
            radius=1,
            material=obj2_mat,
        )

    obj3_mat = Material(
        color=Color(0, 255, 0).normalized(),
            diffusion_coefficient=1,
        specular_coefficient=1,
        ambient_coefficient=1,
        reflection_coefficient=0,
        transmission_coefficient=0,
        rugosity_coefficient=100,
    )
    obj3 = Sphere(
            center=Point(4, 0, -2),
            radius=1,
            material=obj3_mat,
        )
    

    obj4_mat = Material(
        color=Color(255, 255, 0).normalized(),
        diffusion_coefficient=1,
        specular_coefficient=1,
        ambient_coefficient=1,
        reflection_coefficient=0,
        transmission_coefficient=0,
        rugosity_coefficient=1000,
    )
    obj4 = Sphere(
        center=Point(0, -5001, 0),
        radius=5000,
        material=obj4_mat,
    )

    objects.append(obj1)
    objects.append(obj2)
    objects.append(obj3)
    objects.append(obj4)
    camera = Camera(position=Point(0, 0, 0),
        look_at=Point(1, 0, 0),
        v_up=Vector(0, 1, 0),
        distance_from_screen=250,
        vertical_resolution=500,
        horizontal_resolution=500,
    )

    lights = [Light(Point(0, 1, 2), Color(255, 255, 255) * 0.6),
    ]

    scene = Scene(
        camera=camera,
        objects=objects,
        lights=lights,

        ambient_color=Color(255, 255, 255) * 0.2,
        background_color=Color(0, 0, 0),
    )

    img = render_scene(scene, multithread=True)
    img.write_ppm("teste_1.ppm")


if __name__ == "__main__":
    main()
